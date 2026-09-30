"""
E016 - protocolo CLRS reimplementado (H23): Bellman-Ford, treino n = 16 -> teste n = 32, 64.

Motor aprendido (5 parametros): relaxacao suave
    d_v <- softmin_beta { d_u + a*w_uv + b : u vizinho de v },  d_s = 0,  d inicial = D0
e cabeca de ponteiros p(u | v) = softmax_u( -beta_p (d_u + w_uv) ). Parada por ponto fixo no teste.
Bracos:
  APREND   treino com T = 16 passos fixos (gradiente por diferencas centrais, Adam)
  DT       Deep Thinking: progressive loss (T sorteado em 1..2n no treino; lab/baselines, principio)
  SURR     substituto duro: Bellman-Ford exato com os pesos aprendidos a*w + b (diagnostico do vies)
  GULOSO   ponteiro para o vizinho de menor peso (linha de base trivial)
  EXATO    lab.tarefas_clrs.bellman_ford (verdade)
Metrica: acuracia de ponteiros por no (protocolo CLRS), IQM e IC95% sobre sementes.
Uso: python3 e016.py [--quick] [--procs=4]
"""
import json
import math
import os
import random
import sys
import time
from multiprocessing import Pool

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, RAIZ)
from lab import estat, sementes  # noqa: E402
from lab import tarefas_clrs as C  # noqa: E402

QUICK = "--quick" in sys.argv
SEMENTES = [1690, 1691] if QUICK else list(range(1600, 1605))
NS = (16, 64) if QUICK else (16, 32, 64)
N_EX = 4 if QUICK else 20
ITERS = 60 if QUICK else 300
BRACOS = ("APREND", "DT", "SURR", "GULOSO")
SUF = "_smoke" if QUICK else ""


def lse_min(vals, beta):
    m = min(vals)
    return m - math.log(sum(math.exp(-beta * (v - m)) for v in vals)) / beta


def rodar(th, adj, s, T=None, tol=1e-7):
    beta, a, b, D0 = math.exp(th[0]), th[1], th[2], th[3]
    n = len(adj)
    d = [D0] * n
    d[s] = 0.0
    t = 0
    while True:
        nd = [0.0 if v == s or not adj[v] else lse_min([d[u] + a * w + b for u, w in adj[v]], beta) for v in range(n)]
        t += 1
        dif = max(abs(x - y) for x, y in zip(nd, d))
        d = nd
        if (T is not None and t >= T) or (T is None and (dif < tol or t >= 4 * n)):
            return d, t


def ponteiros(th, adj, s, d):
    bp = math.exp(th[4])
    n = len(adj)
    pi = list(range(n))
    P = []
    for v in range(n):
        if v == s or not adj[v]:
            P.append(None)
            continue
        sc = [(-bp * (d[u] + w), u) for u, w in adj[v]]
        m = max(x for x, _ in sc)
        Z = sum(math.exp(x - m) for x, _ in sc)
        P.append({u: math.exp(x - m) / Z for x, u in sc})
        pi[v] = max(sc)[1]
    return pi, P


def perda(th, lote, Ts):
    L, k = 0.0, 0
    for (adj, s, pv), T in zip(lote, Ts):
        d, _ = rodar(th, adj, s, T=T)
        _, P = ponteiros(th, adj, s, d)
        for v, p in enumerate(P):
            if p is not None:
                L -= math.log(p.get(pv[v], 0.0) + 1e-9)
                k += 1
    return L / k


def treinar(rng, progressivo):
    th = [math.log(2.0), 0.5, 0.0, 3.0, math.log(2.0)]
    dados = [C.exemplo("bellman_ford", C.N_TREINO, rng) for _ in range(200)]
    m, v = [0.0] * 5, [0.0] * 5
    for it in range(1, ITERS + 1):
        lote = [dados[rng.randrange(len(dados))] for _ in range(8)]
        Ts = [rng.randint(1, 2 * C.N_TREINO) if progressivo else C.N_TREINO for _ in lote]
        g = []
        for i in range(5):
            tp, tm = list(th), list(th)
            tp[i] += 1e-3
            tm[i] -= 1e-3
            g.append((perda(tp, lote, Ts) - perda(tm, lote, Ts)) / 2e-3)
        for i in range(5):
            m[i] = 0.9 * m[i] + 0.1 * g[i]
            v[i] = 0.999 * v[i] + 0.001 * g[i] ** 2
            th[i] -= 0.1 * (m[i] / (1 - 0.9 ** it)) / (math.sqrt(v[i] / (1 - 0.999 ** it)) + 1e-8)
    return th


def surrogado(th, adj, s):
    """Bellman-Ford exato com pesos a*w + b; ponteiro = argmin_u d_u + w_uv (como a cabeca)."""
    a, b = th[1], th[2]
    adj2 = [[(u, a * w + b) for u, w in l] for l in adj]
    d, _ = C.bellman_ford(adj2, s)
    pi = list(range(len(adj)))
    for v in range(len(adj)):
        if v != s and adj[v]:
            pi[v] = min(adj[v], key=lambda uw: (d[uw[0]] + uw[1], uw[0]))[0]
    return pi


def guloso(adj, s):
    pi = list(range(len(adj)))
    for v in range(len(adj)):
        if v != s and adj[v]:
            pi[v] = min(adj[v], key=lambda uw: (uw[1], uw[0]))[0]
    return pi


def uma(arg):
    seed, sem_teste = arg
    t0 = time.time()
    rng = random.Random(seed)
    th = {"APREND": treinar(rng, False), "DT": treinar(rng, True)}
    r = {"seed": seed, "theta_APREND": th["APREND"], "theta_DT": th["DT"]}
    trng = random.Random(sem_teste)
    for n in NS:
        acc = {b: [] for b in BRACOS}
        passos = {b: [] for b in ("APREND", "DT")}
        for _ in range(N_EX):
            adj, s, pv = C.exemplo("bellman_ford", n, trng)
            for b in ("APREND", "DT"):
                d, t = rodar(th[b], adj, s)
                acc[b].append(C.acuracia_ponteiros(ponteiros(th[b], adj, s, d)[0], pv))
                passos[b].append(t)
            acc["SURR"].append(C.acuracia_ponteiros(surrogado(th["APREND"], adj, s), pv))
            acc["GULOSO"].append(C.acuracia_ponteiros(guloso(adj, s), pv))
        for b in BRACOS:
            r[f"{n}|{b}|acc"] = sum(acc[b]) / N_EX
        for b in passos:
            r[f"{n}|{b}|passos"] = sum(passos[b]) / N_EX
    r["cpu_s"] = time.time() - t0
    print(f"semente {seed} ok ({r['cpu_s']:.0f}s)", flush=True)
    return r


def main():
    procs = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--procs=")), 4)
    teste = [1790, 1791] if QUICK else sementes.derivar(sementes.base_teste(__file__), len(SEMENTES))
    with Pool(procs) as pool:
        res = pool.map(uma, list(zip(SEMENTES, teste)))
    json.dump(res, open(os.path.join(AQUI, f"resultados{SUF}.json"), "w"), indent=1, sort_keys=True)

    def col(c):
        return [x[c] for x in res]
    L = [f"# E016 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{len(SEMENTES)} sementes x {N_EX} grafos por n (Erdos-Renyi p = 0,5, pesos U(0,1)); treino n = 16, {ITERS} iteracoes.", "",
         "| n | braço | acurácia de ponteiros IQM [IC95%] | passos até o ponto fixo |", "|---|---|---|---|"]
    for n in NS:
        L.append(f"| {n} | EXATO | 1.000 | - |")
        for b in BRACOS:
            a = col(f"{n}|{b}|acc")
            lo, hi = estat.bootstrap_ic(a, estat.iqm)
            ps = f"{estat.iqm(col(f'{n}|{b}|passos')):.1f}" if b in ("APREND", "DT") else "-"
            L.append(f"| {n} | {b} | {estat.iqm(a):.3f} [{lo:.3f},{hi:.3f}] | {ps} |")
    L += ["", "Parâmetros aprendidos (beta, a, b, D0, beta_p) por semente (APREND): " +
          "; ".join(" ".join(f"{v:.2f}" for v in x) for x in col("theta_APREND")), "", "## Checagem das previsões", ""]
    nm = NS[-1]

    def iq(n, b):
        return estat.iqm(col(f"{n}|{b}|acc"))
    L.append(f"- P1 {'OK' if iq(16, 'APREND') >= 0.95 else 'FALHOU'}: APREND em n=16 >= 0,95: {iq(16, 'APREND'):.3f}")
    L.append(f"- P2 {'OK' if iq(nm, 'APREND') <= iq(16, 'APREND') - 0.05 else 'FALHOU'}: APREND em n={nm} <= n=16 - 0,05: {iq(nm, 'APREND'):.3f} vs {iq(16, 'APREND'):.3f}")
    L.append(f"- P3 {'OK' if iq(nm, 'DT') <= iq(nm, 'APREND') + 0.03 else 'FALHOU'}: DT em n={nm} não supera APREND por mais de 0,03: {iq(nm, 'DT'):.3f} vs {iq(nm, 'APREND'):.3f}")
    dent = sum(abs(x - y) <= 0.03 for x, y in zip(col(f"{nm}|APREND|acc"), col(f"{nm}|SURR|acc")))
    L.append(f"- P4 {'OK' if dent >= 0.8 * len(SEMENTES) else 'FALHOU'}: SURR prevê APREND em n={nm} (±0,03) em >= 80% das sementes: {dent}/{len(SEMENTES)}")
    L.append(f"- P5 {'OK' if iq(16, 'GULOSO') < iq(16, 'APREND') else 'FALHOU'}: GULOSO < APREND em n=16: {iq(16, 'GULOSO'):.3f} vs {iq(16, 'APREND'):.3f}")
    L.append(f"- CPU total: {sum(col('cpu_s')):.0f}s")
    txt = "\n".join(L)
    open(os.path.join(AQUI, f"resultados{SUF}.md"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
