"""
Tarefa T2 "salto exato" (sem atrator): uma permutacao aleatoria pi de N nos,
um no inicial s e um numero de saltos k. Resposta: pi^k(s).

Diferenca para T1 (achar a raiz): numa permutacao nao ha raiz nem
convergencia. Cada no tem exatamente um antecessor, entao caminhos nunca
se juntam: um salto errado nunca e corrigido. Todo erro e fatal.

O motor S2 e o mesmo passo latente do E001 (S2Step), iterado exatamente k
vezes pelo controlador. O treino supervisiona apenas o instante t = k.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "E001_mlu"))
import mlu  # noqa: E402


def exemplo(N, k, rng):
    pi = list(range(N))
    rng.shuffle(pi)
    s = rng.randrange(N)
    alvo = s
    for _ in range(k):
        alvo = pi[alvo]
    return pi, s, k, alvo


def dados(N, ks, n, rng):
    ks = list(ks)
    return [exemplo(N, rng.choice(ks), rng) for _ in range(n)]


def perda_e_gradiente(s2, lote):
    """BPTT com supervisao so em t = k (adaptado de S2Step.loss_and_grad)."""
    H, F = s2.H, s2.F
    th = s2.theta
    W1, b1 = th[: H * F], th[H * F: H * F + H]
    w2 = th[H * F + H: H * F + 2 * H]
    grad = [0.0] * len(th)
    w = 1.0 / len(lote)
    L = 0.0
    for pi, s, k, alvo in lote:
        N = len(pi)
        S = s2.affinity(pi)
        zs = [[0.0] * N]
        zs[0][s] = 1.0
        for _ in range(k):
            zs.append(s2.step(zs[-1], S))
        gS = [[0.0] * N for _ in range(N)]
        gz_prox = [0.0] * N
        for t in range(k, 0, -1):
            z = zs[t]
            gz = list(gz_prox)
            if t == k:
                L -= w * math.log(z[alvo] + 1e-12)
                gz[alvo] -= w / (z[alvo] + 1e-12)
            dot = sum(a * b for a, b in zip(z, gz))
            gl = [z[i] * (gz[i] - dot) for i in range(N)]
            zp = zs[t - 1]
            gz_prox = [0.0] * N
            for j in range(N):
                if zp[j] == 0.0:
                    continue
                Sj, gSj = S[j], gS[j]
                acc = 0.0
                for i in range(N):
                    gSj[i] += zp[j] * gl[i]
                    acc += gl[i] * Sj[i]
                gz_prox[j] = acc
        gV = {}
        for j in range(N):
            for i in range(N):
                f = s2.feat(pi, j, i)
                gV[f] = gV.get(f, 0.0) + gS[j][i]
        for f, gv in gV.items():
            grad[-1] += gv
            for q in range(H):
                a = b1[q] + sum(W1[q * F + r] * f[r] for r in range(F))
                ta = math.tanh(a)
                grad[H * F + H + q] += gv * ta
                ga = gv * w2[q] * (1 - ta * ta)
                grad[H * F + q] += ga
                for r in range(F):
                    grad[q * F + r] += ga * f[r]
    return L, grad


def treinar(s2, dados_treino, iters, rng, lote=32, lr=0.03):
    P = len(s2.theta)
    m = [0.0] * P
    v = [0.0] * P
    for it in range(1, iters + 1):
        b = [dados_treino[rng.randrange(len(dados_treino))] for _ in range(lote)]
        _, g = perda_e_gradiente(s2, b)
        for q in range(P):
            m[q] = 0.9 * m[q] + 0.1 * g[q]
            v[q] = 0.999 * v[q] + 0.001 * g[q] * g[q]
            s2.theta[q] -= lr * (m[q] / (1 - 0.9 ** it)) / (math.sqrt(v[q] / (1 - 0.999 ** it)) + 1e-8)


def pensar(s2, pi, s, k, modo):
    """modo: CONT (estado continuo), CRIST (argmax a cada passo), AFIA (z^4 normalizado)."""
    N = len(pi)
    S = s2.affinity(pi)
    z = [0.0] * N
    z[s] = 1.0
    for _ in range(k):
        z = s2.step(z, S)
        if modo == "CRIST":
            j = max(range(N), key=lambda i: z[i])
            z = [0.0] * N
            z[j] = 1.0
        elif modo == "AFIA":
            z4 = [x ** 4 for x in z]
            tot = sum(z4)
            z = [x / tot for x in z4]
    return max(range(N), key=lambda i: z[i])


def novo_s2(rng):
    return mlu.S2Step(4, rng)
