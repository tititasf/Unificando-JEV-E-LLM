"""
E006 - diagnostico pos-hoc (nao muda o veredito).

A grade pre-registrada (N*/4 ... 4N*) comecou alta demais: o estado ja estava
dissolvido. Aqui: grade baixa N em {24, 32, 48, 64, 96, 128, 192, 256}, d=20,
e o vazamento de um passo eps(N) em cada N. Pergunta: o N_c real corresponde a
um eps_c aproximadamente constante entre sementes? (lei corrigida)
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
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E001_mlu"))
sys.path.insert(0, RAIZ)
import mlu  # noqa: E402
import e006  # noqa: E402
from lab import estat  # noqa: E402

NS = [24, 32, 48, 64, 96, 128, 192, 256]


def uma(seed):
    rng = random.Random(seed)
    s2 = mlu.S2Step(4, rng)
    with contextlib.redirect_stdout(io.StringIO()):
        s2.train(mlu.dataset(12, range(5), 20000, rng), iters=600, rng=rng)
    trng = random.Random(120000 + seed)
    linha = []
    for N in NS:
        acc, mz = e006.acuracia(s2, N, 20, 10, trng)
        eps = e006.vazamento_medio(s2, N, random.Random(1))
        linha.append((N, acc, mz, eps))
    return seed, linha


def main():
    with Pool(4) as pool:
        res = pool.map(uma, range(600, 612))
    L = ["# E006 - diagnostico: grade baixa (12 sementes, d=20, 10 exemplos)", "",
         "Célula: acc (vazamento de 1 passo eps).", "",
         "| semente | " + " | ".join(f"N={n}" for n in NS) + " | N_c | eps(N_c) |",
         "|---|" + "---|" * len(NS) + "---|---|"]
    eps_c = []
    for seed, linha in res:
        nc, ec = None, None
        for (n0, a0, _, e0), (n1, a1, _, e1) in zip(linha, linha[1:]):
            if a0 >= 0.5 > a1:
                t = (a0 - 0.5) / (a0 - a1)
                nc = math.exp(math.log(n0) + t * (math.log(n1) - math.log(n0)))
                ec = e0 + t * (e1 - e0)
                break
        if ec is not None:
            eps_c.append(ec)
        L.append(f"| {seed} | " + " | ".join(f"{a:.1f} ({e:.3f})" for _, a, _, e in linha)
                 + f" | {'–' if nc is None else f'{nc:.0f}'} | {'–' if ec is None else f'{ec:.3f}'} |")
    if eps_c:
        L += ["", f"eps(N_c): n={len(eps_c)}, min {min(eps_c):.3f}, IQM {estat.iqm(eps_c):.3f}, max {max(eps_c):.3f}"]
    txt = "\n".join(L)
    print(txt)
    with open(os.path.join(AQUI, "diagnostico.md"), "w") as fh:
        fh.write(txt + "\n")


if __name__ == "__main__":
    main()
