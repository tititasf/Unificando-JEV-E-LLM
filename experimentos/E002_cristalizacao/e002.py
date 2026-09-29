"""
E002 - cristalizacao do estado latente (ver PREREG.md; nao mudar os parametros abaixo).

Uso: python3 experimentos/E002_cristalizacao/e002.py [--quick] [--procs=4]
  --quick: smoke test com 4 sementes e d pequeno (NAO vale como resultado)
"""
import json
import math
import os
import random
import sys
from multiprocessing import Pool

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..", "..")
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E001_mlu"))
sys.path.insert(0, RAIZ)

import mlu  # noqa: E402
from lab import estat  # noqa: E402

QUICK = "--quick" in sys.argv
SEMENTES = list(range(200, 204)) if QUICK else list(range(200, 230))
DS = [16, 32] if QUICK else [64, 128]
N_EX = 12


def rodar(s2, parent, s, T, modo):
    S = s2.affinity(parent)
    N = len(parent)
    z = [0.0] * N
    z[s] = 1.0
    for _ in range(T):
        z = s2.step(z, S)
        if modo == "CRIST":
            k = max(range(N), key=lambda i: z[i])
            z = [0.0] * N
            z[k] = 1.0
        elif modo == "AFIA":
            z4 = [v ** 4 for v in z]
            tot = sum(z4)
            z = [v / tot for v in z4]
    return max(range(N), key=lambda i: z[i])


def margem(s2):
    """Margem aprendida: afinidade(pai) - max afinidade(outro) para um no nao-raiz."""
    rng = random.Random(0)
    parent, s, _ = mlu.make_example(12, 3, rng)
    S = s2.affinity(parent)
    return S[s][parent[s]] - max(S[s][i] for i in range(12) if i != parent[s])


def uma(seed):
    rng = random.Random(seed)
    train = mlu.dataset(mlu.N_TRAIN, mlu.TRAIN_DEPTHS, 20000, rng)
    s2 = mlu.S2Step(4, rng)
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        s2.train(train, iters=600, rng=rng)
    r = {"seed": seed, "margem": margem(s2)}
    trng = random.Random(30000 + seed)
    for d in DS:
        N = d + 5
        exs = [mlu.make_example(N, d, trng) for _ in range(N_EX)]
        for modo in ("CONT", "CRIST", "AFIA"):
            r[f"{modo}_d{d}"] = sum(rodar(s2, p, s, d + 8, modo) == rt for p, s, rt in exs) / N_EX
    print(f"semente {seed}: " + " ".join(f"{k}={v:.2f}" for k, v in r.items() if k != "seed"), flush=True)
    return r


def spearman(x, y):
    def ranks(v):
        o = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(o):
            j = i
            while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
                j += 1
            for k in range(i, j + 1):
                r[o[k]] = (i + j) / 2
            i = j + 1
        return r
    rx, ry = ranks(x), ranks(y)
    mx, my = estat.media(rx), estat.media(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else 0.0


def main():
    procs = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--procs=")), 4))
    with Pool(procs) as pool:
        res = pool.map(uma, SEMENTES)
    n = len(res)
    L = [f"# E002 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{n} sementes, {N_EX} exemplos por (semente, d).", "",
         "| braco | d | IQM acc | IC95% | colapsos |", "|---|---|---|---|---|"]
    col = lambda k: [r[k] for r in res]  # noqa: E731
    for d in DS:
        for m in ("CONT", "AFIA", "CRIST"):
            v = col(f"{m}_d{d}")
            lo, hi = estat.bootstrap_ic(v, estat.iqm)
            nc = sum(x < 0.5 for x in v)
            L.append(f"| {m} | {d} | {estat.iqm(v):.3f} | [{lo:.3f}, {hi:.3f}] | {nc}/{n} ({nc / n:.0%}) |")
    dmax = DS[-1]
    cc = sum(x < 0.5 for x in col(f"CONT_d{dmax}"))
    ck = sum(x < 0.5 for x in col(f"CRIST_d{dmax}"))
    ca = sum(x < 0.5 for x in col(f"AFIA_d{dmax}"))
    rho = spearman(col("margem"), col(f"CONT_d{dmax}"))
    L += ["", f"## Checagem das previsões (d={dmax})", "",
          f"- P1 colapso CONT = {cc}/{n} = {cc / n:.0%} (previsto >= 15%; morte se < 5%)",
          f"- P2 colapso CRIST = {ck}/{n} (previsto <= 1)",
          f"- P3 Fisher CRIST vs CONT: p = {estat.fisher_exato(cc, n, ck, n):.4g} (previsto < 0.01)",
          f"- P4 colapso AFIA = {ca}/{n} (previsto entre CRIST e CONT)",
          f"- P5 Spearman(margem, acc CONT) = {rho:.3f} (previsto > 0.3)",
          f"- margens: min {min(col('margem')):.2f}, IQM {estat.iqm(col('margem')):.2f}, max {max(col('margem')):.2f}"]
    txt = "\n".join(L)
    print(txt)
    nome = "resultados_smoke" if QUICK else "resultados"
    with open(os.path.join(AQUI, nome + ".md"), "w") as fh:
        fh.write(txt + "\n")
    with open(os.path.join(AQUI, nome + ".json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
