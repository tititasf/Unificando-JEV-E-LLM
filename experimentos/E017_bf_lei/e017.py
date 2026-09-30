"""
E017 - lei de temperatura para a relaxacao suave (H11): caminho minimo e BFS, treino n = 16 -> teste n = 160 (10x).

Mecanismo (piloto do ciclo 17): o soft-min fica abaixo do minimo; em cada aresta u-v barata o termo de volta
d_u + w ~ d_v + 2w compete com o pai verdadeiro e o motor deriva para baixo enquanto beta * a * w_min <~ 1.
O E016 compensava com um vies b > 0 que so vale num tamanho (dilema do vies).
Em BFS (w = 1) o que desce o soft-min sao os k pais empatados: ln(k)/beta (a lei ln N do E013).
Lei: beta = kappa * ln(g_max) / (a * w_min(G)), com g_max (grau maximo) e w_min medidos no proprio grafo
(sem rotulos) e b = 0; kappa e aprendido em n = 16. Idem beta_p = kappa_p * ln(g_max) / w_min.

Motor (de E016): d_v <- softmin_beta { d_u + a*w_uv + b : u vizinho de v }, d_s = 0, d inicial = D0;
ponteiro p(u|v) = softmax_u(-beta_p (d_u + w_uv)). Parada por ponto fixo (tol 1e-7, orcamento 4n).
Bracos (todos treinados com progressive loss, T ~ U{1..32}, 300 iteracoes, Adam, diferencas centrais):
  DT        beta e beta_p constantes aprendidos, b aprendido (= DT do E016; linha de base publicada, principio)
  LEI       beta = kappa/(a w_min), beta_p = kappa_p/w_min, b = 0 fixo           (metodo)
  LEI_B     lei, b aprendido                                                     (ablacao: b = 0 importa?)
  CONST_B0  beta e beta_p constantes aprendidos, b = 0 fixo                      (ablacao: a lei importa?)
  GULOSO    vizinho de menor peso (linha de base trivial)
Familias: BF (pesos U(0,1); metrica = acuracia de ponteiros CLRS, pai unico q.c.)
          BFS (pesos 1; metrica = pai valido: vizinho a distancia d-1; desvio declarado da convencao de fila do CLRS)
          Em BFS w_min = 1: LEI escala so com ln(g_max): so DT, LEI e GULOSO.
Uso: python3 e017.py [--quick] [--procs=4]
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
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E016_clrs"))
from lab import estat, sementes  # noqa: E402
from lab import tarefas_clrs as C  # noqa: E402
import e016 as M  # noqa: E402  (motor: rodar, ponteiros, guloso)

QUICK = "--quick" in sys.argv
SEMENTES = [1790, 1791] if QUICK else list(range(1700, 1710))
NS = {"BF": (16, 64, 160, 320), "BFS": (16, 64, 160)}
N_EX = {16: 3, 64: 2, 160: 1, 320: 1} if QUICK else {16: 10, 64: 10, 160: 5, 320: 3}
ITERS = 40 if QUICK else 300
BRACOS = {"BF": ("DT", "LEI", "LEI_B", "CONST_B0", "GULOSO"), "BFS": ("DT", "LEI", "GULOSO")}
SO_LEI = {320}  # n = 320 (20x) so para LEI (custo); diagnostico P5
LEI = ("LEI", "LEI_B")
B_FIXO = ("LEI", "CONST_B0")
SUF = "_smoke" if QUICK else ""


def efetivo(th, braco, adj):
    """Parametros efetivos do motor do E016 para este grafo: [log beta, a, b, D0, log beta_p]."""
    lk, a, b, D0, lkp = th
    if braco in B_FIXO:
        b = 0.0
    if braco in LEI:
        wmin = min(w for l in adj for _, w in l)
        lg = math.log(math.log(max(2, max(len(l) for l in adj))))
        return [lk + lg - math.log(max(abs(a), 1e-6) * wmin), a, b, D0, lkp + lg - math.log(wmin)]
    return [lk, a, b, D0, lkp]


def exemplo(fam, n, rng):
    if fam == "BF":
        return C.exemplo("bellman_ford", n, rng)
    adj = C.grafo_er(n, 0.5, rng)
    s = rng.randrange(n)
    d, _ = C.bellman_ford(adj, s)
    return adj, s, d  # BFS: guarda as distancias exatas; acerto = pai valido


def acerto(fam, adj, s, pi, alvo):
    if fam == "BF":
        return C.acuracia_ponteiros(pi, alvo)
    d = alvo
    ok = 0
    for v in range(len(adj)):
        if v == s or d[v] == float("inf"):
            ok += pi[v] == v
        else:
            ok += any(u == pi[v] for u, _ in adj[v]) and abs(d[pi[v]] - (d[v] - 1)) < 1e-9
    return ok / len(adj)


def perda(th, braco, lote, Ts, fam):
    L, k = 0.0, 0
    for (adj, s, alvo), T in zip(lote, Ts):
        te = efetivo(th, braco, adj)
        d, _ = M.rodar(te, adj, s, T=T)
        _, P = M.ponteiros(te, adj, s, d)
        for v, p in enumerate(P):
            if p is None:
                continue
            if fam == "BF":
                L -= math.log(p.get(alvo[v], 0.0) + 1e-9)
            else:  # BFS: massa nos pais validos
                L -= math.log(sum(q for u, q in p.items() if abs(alvo[u] - (alvo[v] - 1)) < 1e-9) + 1e-9)
            k += 1
    return L / k


def treinar(rng, braco, fam):
    th = [math.log(2.0) if braco not in LEI else math.log(0.5), 0.5, 0.0, 3.0,
          math.log(2.0) if braco not in LEI else math.log(0.5)]
    livres = [i for i in range(5) if not (i == 2 and braco in B_FIXO)]
    dados = [exemplo(fam, C.N_TREINO, rng) for _ in range(200)]
    m, v = [0.0] * 5, [0.0] * 5
    for it in range(1, ITERS + 1):
        lote = [dados[rng.randrange(len(dados))] for _ in range(8)]
        Ts = [rng.randint(1, 2 * C.N_TREINO) for _ in lote]
        for i in livres:
            tp, tm = list(th), list(th)
            tp[i] += 1e-3
            tm[i] -= 1e-3
            g = (perda(tp, braco, lote, Ts, fam) - perda(tm, braco, lote, Ts, fam)) / 2e-3
            m[i] = 0.9 * m[i] + 0.1 * g
            v[i] = 0.999 * v[i] + 0.001 * g ** 2
        for i in livres:
            th[i] -= 0.1 * (m[i] / (1 - 0.9 ** it)) / (math.sqrt(v[i] / (1 - 0.999 ** it)) + 1e-8)
    return th


def uma(arg):
    seed, sem_teste = arg
    t0 = time.time()
    r = {"seed": seed}
    for fam in ("BF", "BFS"):
        rng = random.Random(seed * 10 + (fam == "BFS"))
        th = {b: treinar(rng, b, fam) for b in BRACOS[fam] if b != "GULOSO"}
        for b in th:
            r[f"{fam}|theta_{b}"] = th[b]
        trng = random.Random(sem_teste * 10 + (fam == "BFS"))
        for n in NS[fam]:
            bracos = ("LEI",) if n in SO_LEI else BRACOS[fam]
            acc = {b: [] for b in bracos}
            passos = {b: [] for b in bracos if b != "GULOSO"}
            for _ in range(N_EX[n]):
                adj, s, alvo = exemplo(fam, n, trng)
                for b in bracos:
                    if b == "GULOSO":
                        pi = M.guloso(adj, s)
                    else:
                        te = efetivo(th[b], b, adj)
                        d, t = M.rodar(te, adj, s)
                        pi = M.ponteiros(te, adj, s, d)[0]
                        passos[b].append(t)
                    acc[b].append(acerto(fam, adj, s, pi, alvo))
            for b in bracos:
                r[f"{fam}|{n}|{b}|acc"] = sum(acc[b]) / len(acc[b])
            for b in passos:
                r[f"{fam}|{n}|{b}|passos"] = sum(passos[b]) / len(passos[b])
    r["cpu_s"] = time.time() - t0
    print(f"semente {seed} ok ({r['cpu_s']:.0f}s)", flush=True)
    return r


def main():
    procs = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--procs=")), 4)
    teste = [1795, 1796] if QUICK else sementes.derivar(sementes.base_teste(__file__), len(SEMENTES))
    with Pool(procs) as pool:
        res = pool.map(uma, list(zip(SEMENTES, teste)))
    json.dump(res, open(os.path.join(AQUI, f"resultados{SUF}.json"), "w"), indent=1, sort_keys=True)

    def col(c):
        return [x[c] for x in res]

    def iq(fam, n, b):
        return estat.iqm(col(f"{fam}|{n}|{b}|acc"))
    L = [f"# E017 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{len(SEMENTES)} sementes; grafos por n: {N_EX}; Erdos-Renyi p = 0,5; treino n = 16, {ITERS} iteracoes, progressive loss.", "",
         "| família | n | braço | acerto IQM [IC95%] | passos |", "|---|---|---|---|---|"]
    for fam in ("BF", "BFS"):
        for n in NS[fam]:
            for b in (("LEI",) if n in SO_LEI else BRACOS[fam]):
                a = col(f"{fam}|{n}|{b}|acc")
                lo, hi = estat.bootstrap_ic(a, estat.iqm)
                ps = f"{estat.iqm(col(f'{fam}|{n}|{b}|passos')):.1f}" if b != "GULOSO" else "-"
                L.append(f"| {fam} | {n} | {b} | {estat.iqm(a):.3f} [{lo:.3f},{hi:.3f}] | {ps} |")
    L.append("")
    for fam in ("BF", "BFS"):
        for b in BRACOS[fam]:
            if b != "GULOSO":
                L.append(f"- {fam} {b} (log kappa|log beta, a, b, D0, log beta_p): " +
                         "; ".join(" ".join(f"{v:.2f}" for v in x) for x in col(f"{fam}|theta_{b}")))
    L += ["", "## Checagem das previsões", ""]
    ok = {}
    for fam in ("BF", "BFS"):
        lei, dt = col(f"{fam}|160|LEI|acc"), col(f"{fam}|160|DT|acc")
        lo, _ = estat.bootstrap_ic(lei, estat.iqm)
        ok[f"P1{fam}"] = iq(fam, 160, "LEI") >= 0.95
        L.append(f"- P1 {fam} {'OK' if ok[f'P1{fam}'] else 'FALHOU'}: LEI em n=160 IQM >= 0,95: {iq(fam, 160, 'LEI'):.3f} (IC inf {lo:.3f})")
        pv = estat.teste_permutacao(lei, dt)
        pab = estat.prob_melhoria(lei, dt)
        ok[f"P2{fam}"] = iq(fam, 160, "LEI") > iq(fam, 160, "DT") and pv < 0.05
        L.append(f"- P2 {fam} {'OK' if ok[f'P2{fam}'] else 'FALHOU'}: LEI > DT em n=160 (permutacao p < 0,05): "
                 f"{iq(fam, 160, 'LEI'):.3f} vs {iq(fam, 160, 'DT'):.3f}; p = {pv:.4f}; P(LEI>DT) = {pab:.2f}")
    c = iq("BF", 160, "CONST_B0")
    L.append(f"- P3 {'OK' if c <= 0.90 else 'FALHOU'}: CONST_B0 em n=160 <= 0,90: {c:.3f}")
    lb = iq("BF", 160, "LEI_B")
    L.append(f"- P4 {'OK' if lb < iq('BF', 160, 'LEI') - 0.03 else 'FALHOU'}: LEI_B < LEI - 0,03 em n=160: {lb:.3f} vs {iq('BF', 160, 'LEI'):.3f}")
    L.append(f"- P5 {'OK' if iq('BF', 320, 'LEI') >= 0.95 else 'FALHOU'}: LEI em n=320 >= 0,95: {iq('BF', 320, 'LEI'):.3f}")
    L.append(f"- CPU total: {sum(col('cpu_s')):.0f}s")
    txt = "\n".join(L)
    open(os.path.join(AQUI, f"resultados{SUF}.md"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
