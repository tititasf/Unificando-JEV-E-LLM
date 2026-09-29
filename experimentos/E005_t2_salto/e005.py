"""
E005 - REPLICAR o motor S2 na tarefa T2 "salto exato" (sem atrator). Ver PREREG.md.

Uso: python3 experimentos/E005_t2_salto/e005.py [--quick] [--procs=4]
"""
import json
import os
import random
import sys
import time
from multiprocessing import Pool

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..", "..")
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
import tarefa_t2 as T2  # noqa: E402
from lab import estat  # noqa: E402

QUICK = "--quick" in sys.argv
SEMENTES = list(range(500, 502)) if QUICK else list(range(500, 510))
NS = [12, 32] if QUICK else [12, 32, 64, 128]
KS = [4, 16] if QUICK else [4, 8, 16, 32, 64]
N_EX = 4 if QUICK else 10
N_TREINO, K_TREINO = 12, range(1, 5)
MODOS = ("SEM_ITER", "CONT", "AFIA", "CRIST")


def uma(seed):
    t0 = time.time()
    rng = random.Random(seed)
    treino = T2.dados(N_TREINO, K_TREINO, 20000, rng)
    s2 = T2.novo_s2(rng)
    T2.treinar(s2, treino, iters=150 if QUICK else 600, rng=rng)
    trng = random.Random(80000 + seed)
    r = {"seed": seed}
    for N in NS:
        for k in KS:
            exs = [T2.exemplo(N, k, trng) for _ in range(N_EX)]
            for modo in MODOS:
                if modo == "SEM_ITER":   # linha de base: uma passada (1 salto) e responde
                    ok = sum(T2.pensar(s2, pi, s, 1, "CONT") == alvo for pi, s, _, alvo in exs)
                else:
                    ok = sum(T2.pensar(s2, pi, s, k, modo) == alvo for pi, s, _, alvo in exs)
                r[f"{modo}|{N}|{k}"] = ok / N_EX
    r["cpu_s"] = time.time() - t0
    print(f"semente {seed} ok ({r['cpu_s']:.0f}s)", flush=True)
    return r


def main():
    procs = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--procs=")), 4))
    with Pool(procs) as pool:
        res = pool.map(uma, SEMENTES)
    n = len(res)
    col = lambda k: [r[k] for r in res]  # noqa: E731
    L = [f"# E005 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{n} sementes x {N_EX} exemplos por celula. Celula: IQM da acuracia entre sementes [IC95%] (colapsos <0,5).", "",
         "| modo | N | " + " | ".join(f"k={k}" for k in KS) + " |", "|---|---|" + "---|" * len(KS)]
    for modo in MODOS:
        for N in NS:
            cel = []
            for k in KS:
                v = col(f"{modo}|{N}|{k}")
                lo, hi = estat.bootstrap_ic(v, estat.iqm)
                c = sum(x < 0.5 for x in v)
                cel.append(f"{estat.iqm(v):.2f} [{lo:.2f},{hi:.2f}] ({c})")
            L.append(f"| {modo} | {N} | " + " | ".join(cel) + " |")
    L += ["", "## Razao de extrapolacao (maior k com IQM >= 0,95, dividido por 4)", ""]
    for modo in ("CONT", "AFIA", "CRIST"):
        L.append(f"- {modo}: " + ", ".join(
            f"N={N}: {estat.razao_extrapolacao({k: estat.iqm(col(f'{modo}|{N}|{k}')) for k in KS}, 4):.0f}x" for N in NS))
    Nm, km = NS[-1], KS[-1]
    a, b = col(f"CRIST|{Nm}|{km}"), col(f"CONT|{Nm}|{km}")
    L += ["", f"CRIST vs CONT em N={Nm}, k={km}: P(A>B) = {estat.prob_melhoria(a, b):.2f}, "
          f"p permutacao = {estat.teste_permutacao(a, b):.4f}",
          f"CPU total: {sum(col('cpu_s')):.0f}s"]
    txt = "\n".join(L)
    print(txt)
    nome = "resultados_smoke" if QUICK else "resultados"
    with open(os.path.join(AQUI, nome + ".md"), "w") as fh:
        fh.write(txt + "\n")
    with open(os.path.join(AQUI, nome + ".json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
