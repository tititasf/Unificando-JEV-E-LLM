"""
E003 - Cristal Comum: comunicacao analogica vs simbolica entre dois agentes
com conhecimento fragmentado (ver PREREG.md).

Uso: python3 experimentos/E003_cristal_comum/e003.py [--quick] [--procs=4]
"""
import contextlib
import io
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
SEMENTES = list(range(300, 302)) if QUICK else list(range(300, 310))
DS = [8, 32]
SIGMAS = [0.0, 0.5, 1.0, 2.0, 4.0]
N_EX = 6 if QUICK else 20


def conversa(S, owner, s, T, sigma, modo, rng):
    """Dois agentes; owner[j] in {0,1} diz quem conhece a linha j de S."""
    N = len(S)
    z = [0.0] * N
    z[s] = 1.0
    for _ in range(T):
        recebido = [0.0] * N
        for ag in (0, 1):
            massa = sum(z[j] for j in range(N) if owner[j] == ag)
            m = [sum(z[j] * S[j][i] for j in range(N) if owner[j] == ag and z[j] > 1e-12)
                 for i in range(N)]
            if modo == "SIMB":
                if massa < 0.5:
                    m = [0.0] * N          # quem nao detem o pensamento fica calado
                else:
                    norma = math.sqrt(sum(v * v for v in m))
                    k = max(range(N), key=lambda i: m[i])
                    m = [0.0] * N
                    m[k] = norma
            for i in range(N):
                recebido[i] += m[i] + rng.gauss(0, sigma)
        if modo == "SIMB":
            k = max(range(N), key=lambda i: recebido[i])
            z = [0.0] * N
            z[k] = 1.0
        else:
            z = mlu.softmax(recebido)
    return max(range(N), key=lambda i: z[i])


def uma(seed):
    rng = random.Random(seed)
    train = mlu.dataset(mlu.N_TRAIN, mlu.TRAIN_DEPTHS, 20000, rng)
    s2 = mlu.S2Step(4, rng)
    with contextlib.redirect_stdout(io.StringIO()):
        s2.train(train, iters=200 if QUICK else 600, rng=rng)
    r = {"seed": seed}
    trng = random.Random(40000 + seed)
    for d in DS:
        N = d + 5
        exs = []
        for _ in range(N_EX):
            p, s, root = mlu.make_example(N, d, trng)
            owner = [trng.randrange(2) for _ in range(N)]
            exs.append((s2.affinity(p), owner, s, root))
        for sg in SIGMAS:
            for modo in ("CONT", "SIMB"):
                nrng = random.Random(hash((seed, d, sg, modo)) & 0xFFFFFFFF)
                ok = sum(conversa(S, ow, s, d + 8, sg, modo, nrng) == rt for S, ow, s, rt in exs)
                r[f"{modo}_d{d}_s{sg}"] = ok / N_EX
    print(f"semente {seed} ok", flush=True)
    return r


def main():
    procs = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--procs=")), 4))
    with Pool(procs) as pool:
        res = pool.map(uma, SEMENTES)
    n = len(res)
    col = lambda k: [r[k] for r in res]  # noqa: E731
    L = [f"# E003 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{n} sementes x {N_EX} exemplos. Celulas: acuracia media [IC95% Wilson sobre todos os exemplos].", "",
         "| d | sigma | CONT | SIMB | SIMB-CONT | Fisher p |", "|---|---|---|---|---|---|"]
    vant = {}
    for d in DS:
        for sg in SIGMAS:
            tot = n * N_EX
            a = round(sum(col(f"CONT_d{d}_s{sg}")) * N_EX)
            b = round(sum(col(f"SIMB_d{d}_s{sg}")) * N_EX)
            ca, cb = estat.ic_proporcao(a, tot), estat.ic_proporcao(b, tot)
            p = estat.fisher_exato(b, tot, a, tot)
            vant[(d, sg)] = (b - a) / tot
            L.append(f"| {d} | {sg} | {a / tot:.2f} [{ca[0]:.2f},{ca[1]:.2f}] "
                     f"| {b / tot:.2f} [{cb[0]:.2f},{cb[1]:.2f}] | {(b - a) / tot:+.2f} | {p:.2g} |")
    L += ["", "## Checagem", ""]
    L.append(f"- Q1 sigma=0: CONT d32={estat.media(col('CONT_d32_s0.0')):.2f}, SIMB d32={estat.media(col('SIMB_d32_s0.0')):.2f}")
    melhor = max(SIGMAS, key=lambda sg: vant[(32, sg)])
    L.append(f"- Q2 maior vantagem SIMB em d=32: {vant[(32, melhor)]:+.2f} em sigma={melhor}")
    L.append(f"- Q3 vantagem nesse sigma: d=8 {vant[(8, melhor)]:+.2f} vs d=32 {vant[(32, melhor)]:+.2f}")
    L.append(f"- Q4 sigma=4: CONT d32={estat.media(col('CONT_d32_s4.0')):.2f}, SIMB d32={estat.media(col('SIMB_d32_s4.0')):.2f}")
    txt = "\n".join(L)
    print(txt)
    nome = "resultados_smoke" if QUICK else "resultados"
    with open(os.path.join(AQUI, nome + ".md"), "w") as fh:
        fh.write(txt + "\n")
    with open(os.path.join(AQUI, nome + ".json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
