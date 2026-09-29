"""
E004 - diagnostico pos-hoc (nao muda o veredito).

Pergunta: em N grande o S2 contínuo anda salto a salto ou chega a raiz
"em paralelo", por difusao ate um equilibrio? Mede acuracia do argmax em
funcao do numero de passos t (contínuo vs cristalizado) e, para cada caso,
o primeiro t em que o argmax passa a ser a raiz certa e nao muda mais.
"""
import contextlib
import io
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

CASOS = [(12, 7), (32, 27), (64, 59), (128, 123)]
TS = [3, 6, 12, 24, 48]


def uma(seed):
    rng = random.Random(seed)
    train = mlu.dataset(mlu.N_TRAIN, mlu.TRAIN_DEPTHS, 20000, rng)
    s2 = mlu.S2Step(4, rng)
    with contextlib.redirect_stdout(io.StringIO()):
        s2.train(train, iters=600, rng=rng)
    trng = random.Random(70000 + seed)
    r = {}
    for N, d in CASOS:
        for _ in range(10):
            p, s, root = mlu.make_example(N, d, trng)
            S = s2.affinity(p)
            for modo in ("cont", "crist"):
                z = [0.0] * N
                z[s] = 1.0
                hist = []
                for _t in range(max(d + 8, max(TS))):
                    z = s2.step(z, S)
                    if modo == "crist":
                        k = max(range(N), key=lambda i: z[i])
                        z = [0.0] * N
                        z[k] = 1.0
                    hist.append(max(range(N), key=lambda i: z[i]))
                for t in TS:
                    key = (N, modo, t)
                    r[key] = r.get(key, 0) + (hist[t - 1] == root)
                # primeiro t a partir do qual o argmax e sempre a raiz certa
                t_ok = len(hist)
                for t in range(len(hist) - 1, -1, -1):
                    if hist[t] != root:
                        break
                    t_ok = t + 1
                r[(N, modo, "t_ok")] = r.get((N, modo, "t_ok"), []) + [t_ok]
    return r


def main():
    with Pool(4) as pool:
        res = pool.map(uma, range(410, 414))
    L = ["# E004 - diagnostico: sequencial ou paralelo? (4 sementes x 10 casos por N; d = N-5)", "",
         "Acuracia do argmax apos t passos, e passos ate o argmax fixar na raiz certa.", "",
         "| N | d | modo | " + " | ".join(f"t={t}" for t in TS) + " | passos ate fixar (IQM) | passos / d |",
         "|---|---|---|" + "---|" * len(TS) + "---|---|"]
    for N, d in CASOS:
        for modo in ("cont", "crist"):
            accs = [sum(r[(N, modo, t)] for r in res) / (10 * len(res)) for t in TS]
            tok = [x for r in res for x in r[(N, modo, "t_ok")]]
            L.append(f"| {N} | {d} | {modo} | " + " | ".join(f"{a:.2f}" for a in accs)
                     + f" | {estat.iqm(tok):.1f} | {estat.iqm(tok) / d:.2f} |")
    txt = "\n".join(L)
    print(txt)
    with open(os.path.join(AQUI, "diagnostico.md"), "w") as fh:
        fh.write(txt + "\n")


if __name__ == "__main__":
    main()
