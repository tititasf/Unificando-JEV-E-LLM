"""
lab/baselines.py - linhas de base publicadas, em versao minima fiel aos principios.

1) Deep Thinking com recall + progressive loss (Bansal et al., NeurIPS 2022)
   - recall: a entrada e reinjetada a cada passo. No nosso motor isso ja e
     inerente: a afinidade S e recalculada da entrada e usada em todo passo.
   - progressive loss: sorteia n ~ U{0..M-1} passos SEM gradiente (estado
     desligado do grafo) e depois k ~ U{1..M-n} passos COM gradiente; a perda
     final mistura (1-alfa) * perda em M passos + alfa * perda progressiva.
     Objetivo: aprender um passo que pode ser repetido indefinidamente, sem
     depender do numero da iteracao (evita overthinking).

2) Parada estilo PonderNet (Banino et al., 2021)
   - lambda_t = sigmoid(w . phi(z_t)), com phi = (entropia normalizada,
     max z, mudanca L1, 1). p_t = lambda_t * prod_{j<t}(1 - lambda_j).
   - perda = sum_t p_t * CE_t + beta * KL(p || Geometrica(lambda_p)).
   - Versao minima: treina so a cabeca de parada (4 parametros) sobre um motor
     congelado, com gradiente por diferencas centrais (poucos parametros).
   - Inferencia deterministica: para no primeiro t com prob. acumulada >= 0,5.

Honestidade: sao reimplementacoes dos principios no nosso motor de 33
parametros, nao reproducoes dos modelos originais. Servem como "a linha de
base publicada mais proxima" exigida pela regra 4, com essa ressalva escrita.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "experimentos", "E001_mlu"))
import mlu  # noqa: E402


# ------------------------------------------------------ BPTT generico
def bptt(s2, exemplos):
    """exemplos: lista de (grafo, z0, T, alvos) com alvos = {t: indice_alvo}.
    Perda = media sobre (exemplo, t supervisionado) de -log z_t[alvo].
    Devolve (perda, gradiente em relacao a s2.theta)."""
    H, F = s2.H, s2.F
    th = s2.theta
    W1, b1 = th[: H * F], th[H * F: H * F + H]
    w2 = th[H * F + H: H * F + 2 * H]
    grad = [0.0] * len(th)
    nsup = sum(len(a) for _, _, _, a in exemplos)
    w = 1.0 / max(1, nsup)
    L = 0.0
    for grafo, z0, T, alvos in exemplos:
        N = len(grafo)
        S = s2.affinity(grafo)
        zs = [list(z0)]
        for _ in range(T):
            zs.append(s2.step(zs[-1], S))
        gS = [[0.0] * N for _ in range(N)]
        gprox = [0.0] * N
        for t in range(T, 0, -1):
            z = zs[t]
            gz = list(gprox)
            if t in alvos:
                a = alvos[t]
                L -= w * math.log(z[a] + 1e-12)
                gz[a] -= w / (z[a] + 1e-12)
            dot = sum(x * y for x, y in zip(z, gz))
            gl = [z[i] * (gz[i] - dot) for i in range(N)]
            zp = zs[t - 1]
            gprox = [0.0] * N
            for j in range(N):
                if zp[j] == 0.0:
                    continue
                Sj, gSj = S[j], gS[j]
                acc = 0.0
                for i in range(N):
                    gSj[i] += zp[j] * gl[i]
                    acc += gl[i] * Sj[i]
                gprox[j] = acc
        gV = {}
        for j in range(N):
            for i in range(N):
                f = s2.feat(grafo, j, i)
                gV[f] = gV.get(f, 0.0) + gS[j][i]
        for f, gv in gV.items():
            grad[-1] += gv
            for q in range(H):
                a_ = b1[q] + sum(W1[q * F + r] * f[r] for r in range(F))
                ta = math.tanh(a_)
                grad[H * F + H + q] += gv * ta
                ga = gv * w2[q] * (1 - ta * ta)
                grad[H * F + q] += ga
                for r in range(F):
                    grad[q * F + r] += ga * f[r]
    return L, grad


def _adam(s2, g, estado, it, lr):
    m, v = estado
    for q in range(len(s2.theta)):
        m[q] = 0.9 * m[q] + 0.1 * g[q]
        v[q] = 0.999 * v[q] + 0.001 * g[q] * g[q]
        s2.theta[q] -= lr * (m[q] / (1 - 0.9 ** it)) / (math.sqrt(v[q] / (1 - 0.999 ** it)) + 1e-8)


def rodar(s2, grafo, z0, n):
    S = s2.affinity(grafo)
    z = list(z0)
    for _ in range(n):
        z = s2.step(z, S)
    return z


# ------------------------------------- Deep Thinking: progressive loss
def treinar_progressivo(s2, dados, alvo_em, M, iters, rng, alfa=0.5, lote=32, lr=0.03):
    """dados: lista de (grafo, s, info); alvo_em(info, t) -> indice correto apos t passos
    (None se a tarefa nao define resposta nesse t). M = iteracoes maximas de treino."""
    P = len(s2.theta)
    est = ([0.0] * P, [0.0] * P)
    for it in range(1, iters + 1):
        b = [dados[rng.randrange(len(dados))] for _ in range(lote)]
        ex_max, ex_prog = [], []
        for grafo, s, info in b:
            N = len(grafo)
            z0 = [0.0] * N
            z0[s] = 1.0
            a = alvo_em(info, M)
            if a is not None:
                ex_max.append((grafo, z0, M, {M: a}))
            n = rng.randrange(M)
            k = rng.randint(1, M - n)
            a = alvo_em(info, n + k)
            if a is not None:
                zn = rodar(s2, grafo, z0, n)          # sem gradiente: estado desligado
                ex_prog.append((grafo, zn, k, {k: a}))
        g = [0.0] * P
        for exs, peso in ((ex_max, 1 - alfa), (ex_prog, alfa)):
            if exs and peso > 0:
                _, gi = bptt(s2, exs)
                for q in range(P):
                    g[q] += peso * gi[q]
        _adam(s2, g, est, it, lr)


# ------------------------------------------------ PonderNet (parada)
def _phi(z, zp):
    N = len(z)
    ent = -sum(p * math.log(p) for p in z if p > 1e-15) / math.log(N)
    return (ent, max(z), sum(abs(a - b) for a, b in zip(z, zp)), 1.0)


def _sig(x):
    return 1 / (1 + math.exp(-max(-50.0, min(50.0, x))))


def trajetorias(s2, casos, T_max):
    """Pre-calcula (phi_t, CE_t) por caso; casos = (grafo, s, alvo_em_t)."""
    out = []
    for grafo, s, alvo in casos:
        N = len(grafo)
        S = s2.affinity(grafo)
        z = [0.0] * N
        z[s] = 1.0
        linha = []
        for t in range(1, T_max + 1):
            z2 = s2.step(z, S)
            a = alvo(t)
            ce = -math.log(z2[a] + 1e-12) if a is not None else 0.0
            linha.append((_phi(z2, z), ce, max(range(N), key=lambda i: z2[i]), a))
            z = z2
        out.append(linha)
    return out


def perda_ponder(w, trajs, beta=0.01, lam_p=0.2):
    L = 0.0
    for linha in trajs:
        resta = 1.0
        ps = []
        for t, (phi, ce, _, _) in enumerate(linha):
            lam = 1.0 if t == len(linha) - 1 else _sig(sum(a * b for a, b in zip(w, phi)))
            p = resta * lam
            ps.append(p)
            L += p * ce
            resta *= (1 - lam)
        for t, p in enumerate(ps):
            g = lam_p * (1 - lam_p) ** t
            if p > 1e-12:
                L += beta * p * math.log(p / g)
    return L / len(trajs)


def treinar_ponder(trajs, iters=150, lr=0.1, rng=None, beta=0.01, lam_p=0.2):
    rng = rng or random.Random(0)
    w = [rng.gauss(0, 0.1) for _ in range(4)]
    for _ in range(iters):
        g = []
        for q in range(4):
            e = 1e-4
            w[q] += e
            lp = perda_ponder(w, trajs, beta, lam_p)
            w[q] -= 2 * e
            lm = perda_ponder(w, trajs, beta, lam_p)
            w[q] += e
            g.append((lp - lm) / (2 * e))
        for q in range(4):
            w[q] -= lr * g[q]
    return w


def decidir_ponder(w, linha):
    """Para no primeiro t com probabilidade acumulada de parada >= 0,5.
    Devolve (resposta, passos)."""
    resta = 1.0
    acum = 0.0
    for t, (phi, _, pred, _) in enumerate(linha):
        lam = 1.0 if t == len(linha) - 1 else _sig(sum(a * b for a, b in zip(w, phi)))
        acum += resta * lam
        resta *= (1 - lam)
        if acum >= 0.5:
            return pred, t + 1
    return linha[-1][2], len(linha)
