"""
E006 - lei N* (ver PREREG.md; parametros congelados).

Para cada semente: treina o S2 em T1 (identico ao E001), calcula N* = o N em
que o vazamento de um passo (a partir de um estado concentrado num no do
caminho) chega a 0,5, e testa N em N* x {1/4, 1/2, 1, 2, 4}.
  A: d = 20 fixo (o caminho e uma fracao pequena do grafo quando N e grande)
  B: d = N - 5 (o caminho domina o grafo, como no E004), so quando 4N* <= 2048

Uso: python3 experimentos/E006_lei_margem/e006.py [--quick] [--procs=4]
"""
import contextlib
import io
import json
import math
import os
import random
import sys
import time
from multiprocessing import Pool

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..", "..")
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E001_mlu"))
sys.path.insert(0, RAIZ)
import mlu  # noqa: E402
import passo_rapido as PR  # noqa: E402
from lab import estat  # noqa: E402

QUICK = "--quick" in sys.argv
SEMENTES = list(range(600, 603)) if QUICK else list(range(600, 630))
FATORES = (0.25, 0.5, 1.0, 2.0, 4.0)
D_A = 20
N_MIN, N_MAX, N_MAX_B = 30, 16384, 2048
N_EX = 3 if QUICK else 10


def vazamento_medio(s2, N, rng):
    tot = 0.0
    for _ in range(5):
        p, s, _ = mlu.make_example(N, D_A, rng)
        tot += PR.vazamento(PR.preparar(s2, p), s)
    return tot / 5


def achar_nstar(s2):
    """Bissecao em log N ate vazamento medio = 0,5 (sementes fixas)."""
    lo, hi = 25, 1 << 17
    if vazamento_medio(s2, lo, random.Random(1)) >= 0.5:
        return lo
    if vazamento_medio(s2, hi, random.Random(1)) < 0.5:
        return hi
    for _ in range(14):
        mid = int(math.sqrt(lo * hi))
        if vazamento_medio(s2, mid, random.Random(1)) < 0.5:
            lo = mid
        else:
            hi = mid
        if hi - lo <= max(2, lo // 50):
            break
    return (lo + hi) // 2


def acuracia(s2, N, d, n, rng):
    ok = 0
    mz = 0.0
    for _ in range(n):
        p, s, root = mlu.make_example(N, d, rng)
        P = PR.preparar(s2, p)
        z = [0.0] * N
        z[s] = 1.0
        for _ in range(d + 8):
            z = PR.passo(z, P)
        k = max(range(N), key=lambda i: z[i])
        ok += k == root
        mz += z[k]
    return ok / n, mz / n


def uma(seed):
    t0 = time.time()
    rng = random.Random(seed)
    s2 = mlu.S2Step(4, rng)
    with contextlib.redirect_stdout(io.StringIO()):
        s2.train(mlu.dataset(mlu.N_TRAIN, mlu.TRAIN_DEPTHS, 20000, rng), iters=200 if QUICK else 600, rng=rng)
    nstar = achar_nstar(s2)
    r = {"seed": seed, "nstar": nstar, "A": {}, "B": {}}
    trng = random.Random(110000 + seed)
    for f in FATORES:
        N = max(N_MIN, int(round(nstar * f)))
        if N > N_MAX:
            continue
        r["A"][str(f)] = dict(N=N, acc_maxz=acuracia(s2, N, D_A, N_EX, trng))
        if nstar * 4 <= N_MAX_B:
            r["B"][str(f)] = dict(N=N, acc_maxz=acuracia(s2, N, N - 5, max(3, N_EX // 2), trng))
    r["cpu_s"] = time.time() - t0
    print(f"semente {seed}: N*={nstar} ({r['cpu_s']:.0f}s)", flush=True)
    return r


def cruzamento(r):
    """N_c: interpolacao geometrica do cruzamento de acc=0,5 na grade A."""
    pts = sorted((v["N"], v["acc_maxz"][0]) for v in r["A"].values())
    for (n0, a0), (n1, a1) in zip(pts, pts[1:]):
        if a0 >= 0.5 > a1:
            t = (a0 - 0.5) / (a0 - a1)
            return math.exp(math.log(n0) + t * (math.log(n1) - math.log(n0)))
    return None


def spearman(x, y):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        for pos, i in enumerate(o):
            r[i] = pos
        return r
    rx, ry = rk(x), rk(y)
    mx, my = estat.media(rx), estat.media(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else 0.0


def main():
    procs = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--procs=")), 4))
    with Pool(procs) as pool:
        res = pool.map(uma, SEMENTES)
    n = len(res)
    L = [f"# E006 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{n} sementes. Grade A: d={D_A}, {N_EX} exemplos por celula. Grade B: d=N-5 (so se 4N* <= {N_MAX_B}).", "",
         "| semente | N* | acc A em N*x(1/4, 1/2, 1, 2, 4) | max z A | N_c | acc B em N*x(1/4 ... 4) |",
         "|---|---|---|---|---|---|"]
    for r in res:
        accA = " / ".join(f"{r['A'][str(f)]['acc_maxz'][0]:.1f}" if str(f) in r["A"] else "–" for f in FATORES)
        mzA = " / ".join(f"{r['A'][str(f)]['acc_maxz'][1]:.2f}" if str(f) in r["A"] else "–" for f in FATORES)
        accB = " / ".join(f"{r['B'][str(f)]['acc_maxz'][0]:.1f}" if str(f) in r["B"] else "–" for f in FATORES)
        nc = cruzamento(r)
        L.append(f"| {r['seed']} | {r['nstar']} | {accA} | {mzA} | {'–' if nc is None else f'{nc:.0f}'} | {accB} |")

    def frac(cond, pool_):
        pool_ = [x for x in pool_ if x is not None]
        return (sum(cond(x) for x in pool_) / len(pool_), len(pool_)) if pool_ else (float("nan"), 0)

    p1 = frac(lambda a: a >= 0.95, [r["A"].get("0.25", {}).get("acc_maxz", [None])[0] for r in res])
    p2 = frac(lambda a: a <= 0.5, [r["A"].get("4.0", {}).get("acc_maxz", [None])[0] for r in res])
    ncs = [(r["nstar"], cruzamento(r)) for r in res]
    p3 = frac(lambda t: t[0] / 2 <= t[1] <= 2 * t[0], [t if t[1] else None for t in ncs])
    com = [t for t in ncs if t[1]]
    rho = spearman([t[0] for t in com], [t[1] for t in com]) if len(com) > 2 else float("nan")
    comB = [r for r in res if "4.0" in r["B"]]
    p5 = frac(lambda r: r["B"]["4.0"]["acc_maxz"][0] >= 0.7 and r["A"]["4.0"]["acc_maxz"][0] <= 0.3, comB)
    fora = sum(1 for t in ncs if t[1] and not (t[0] / 4 <= t[1] <= 4 * t[0]))
    L += ["", "## Checagem das previsões", "",
          f"- P1 acc A >= 0,95 em N*/4: {p1[0]:.2f} das sementes (n={p1[1]}; previsto >= 0,90)",
          f"- P2 acc A <= 0,5 em 4N*: {p2[0]:.2f} (n={p2[1]}; previsto >= 0,90)",
          f"- P3 N_c em [N*/2, 2N*]: {p3[0]:.2f} (n={p3[1]}; previsto >= 0,80); N_c fora de [N*/4, 4N*]: {fora}",
          f"- P4 Spearman(N*, N_c) = {rho:.2f} (n={len(com)}; previsto > 0,7)",
          f"- P5 atalho do atrator em 4N* (B >= 0,7 e A <= 0,3): {p5[0]:.2f} (n={p5[1]}; previsto >= 0,70)",
          f"- N*: min {min(r['nstar'] for r in res)}, IQM {estat.iqm([r['nstar'] for r in res]):.0f}, max {max(r['nstar'] for r in res)}",
          f"- CPU total: {sum(r['cpu_s'] for r in res):.0f}s"]
    txt = "\n".join(L)
    print(txt)
    nome = "resultados_smoke" if QUICK else "resultados"
    with open(os.path.join(AQUI, nome + ".md"), "w") as fh:
        fh.write(txt + "\n")
    with open(os.path.join(AQUI, nome + ".json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
