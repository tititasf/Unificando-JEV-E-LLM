"""
E003 - diagnostico pos-hoc (nao muda o veredito pre-registrado).

D1: N fixo (=37) para d=8 e d=32 -> separa o efeito de d do efeito de N.
D2: braços cruzados -> qual metade do "cristal" importa?
    CONT      mensagem analogica, estado contínuo
    CONT_EST  mensagem analogica, estado cristalizado no receptor
    SIMB_SUAVE mensagem simbolica, estado contínuo (softmax)
    SIMB      mensagem simbolica, estado cristalizado
"""
import contextlib
import io
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

MODOS = ("CONT", "CONT_EST", "SIMB_SUAVE", "SIMB")
N_FIXO = 37
SIGMAS = (1.0, 2.0, 4.0)


def conversa(S, owner, s, T, sigma, modo, rng):
    N = len(S)
    msg_simb = modo.startswith("SIMB")
    est_crist = modo in ("SIMB", "CONT_EST")
    z = [0.0] * N
    z[s] = 1.0
    for _ in range(T):
        rec = [0.0] * N
        for ag in (0, 1):
            massa = sum(z[j] for j in range(N) if owner[j] == ag)
            m = [sum(z[j] * S[j][i] for j in range(N) if owner[j] == ag and z[j] > 1e-12) for i in range(N)]
            if msg_simb:
                if massa < 0.5:
                    m = [0.0] * N
                else:
                    nm = math.sqrt(sum(v * v for v in m))
                    k = max(range(N), key=lambda i: m[i])
                    m = [0.0] * N
                    m[k] = nm
            for i in range(N):
                rec[i] += m[i] + rng.gauss(0, sigma)
        if est_crist:
            k = max(range(N), key=lambda i: rec[i])
            z = [0.0] * N
            z[k] = 1.0
        else:
            z = mlu.softmax(rec)
    return max(range(N), key=lambda i: z[i])


def uma(seed):
    rng = random.Random(seed)
    train = mlu.dataset(mlu.N_TRAIN, mlu.TRAIN_DEPTHS, 20000, rng)
    s2 = mlu.S2Step(4, rng)
    with contextlib.redirect_stdout(io.StringIO()):
        s2.train(train, iters=600, rng=rng)
    trng = random.Random(50000 + seed)
    r = {}
    for d in (8, 32):
        exs = []
        for _ in range(20):
            p, s, root = mlu.make_example(N_FIXO, d, trng)
            exs.append((s2.affinity(p), [trng.randrange(2) for _ in range(N_FIXO)], s, root))
        for sg in SIGMAS:
            for modo in MODOS:
                nrng = random.Random(hash((seed, d, sg, modo)) & 0xFFFFFFFF)
                r[(d, sg, modo)] = sum(conversa(S, o, s, d + 8, sg, modo, nrng) == rt for S, o, s, rt in exs)
    return r


def main():
    with Pool(4) as pool:
        res = pool.map(uma, range(310, 316))
    tot = 20 * len(res)
    L = ["# E003 - diagnostico pos-hoc (6 sementes x 20, N fixo = 37)", "",
         "| d | sigma | " + " | ".join(MODOS) + " |", "|---|---|" + "---|" * len(MODOS)]
    for d in (8, 32):
        for sg in SIGMAS:
            cel = []
            for m in MODOS:
                a = sum(r[(d, sg, m)] for r in res)
                lo, hi = estat.ic_proporcao(a, tot)
                cel.append(f"{a / tot:.2f} [{lo:.2f},{hi:.2f}]")
            L.append(f"| {d} | {sg} | " + " | ".join(cel) + " |")
    txt = "\n".join(L)
    print(txt)
    with open(os.path.join(AQUI, "diagnostico.md"), "w") as fh:
        fh.write(txt + "\n")


if __name__ == "__main__":
    main()
