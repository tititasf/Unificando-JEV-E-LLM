"""
E007 - diagnostico pos-hoc (nao muda o veredito): teoria de campo medio.

Modelo: massa a no no atual; o passo da vantagem m*a ao pai contra K = N-1
concorrentes: a' = 1/(1 + K e^{-m a}). O estado nitido e um ponto fixo que some
numa bifurcacao sela-no (condicao m a (1-a) = 1; so existe se m >= 4).
No limiar, o vazamento de um passo a partir de a = 1 e
    eps_c(m) = K_c e^{-m} / (1 + K_c e^{-m}),  K_c = ((1-a*)/a*) e^{m a*},
    a* = (1 + sqrt(1 - 4/m)) / 2.
Aqui: para cada semente do E007, mede a margem efetiva m (a partir do vazamento
em N pequeno), preve eps_c(m) pela teoria e N_c = N com eps(N) = eps_c(m);
compara o erro com o da lei de limiar fixo (0,071).
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
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E006_lei_margem"))
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E001_mlu"))
sys.path.insert(0, RAIZ)
import mlu  # noqa: E402
import e006  # noqa: E402
from lab import estat  # noqa: E402


def eps_c_teoria(m):
    if m < 4:
        return None
    a = (1 + math.sqrt(1 - 4 / m)) / 2
    K = ((1 - a) / a) * math.exp(m * a)
    return K * math.exp(-m) / (1 + K * math.exp(-m))


def margem_efetiva(s2):
    """Inverte eps(N) = K e^{-m}/(1+K e^{-m}) medido em N = 30 (K = N - 1)."""
    eps = e006.vazamento_medio(s2, 30, random.Random(1))
    return -math.log(eps / ((1 - eps) * 29))


def n_para_eps(s2, alvo):
    lo, hi = 24, 1 << 15
    if e006.vazamento_medio(s2, lo, random.Random(1)) >= alvo:
        return lo
    while hi - lo > max(2, lo // 100):
        mid = int(math.sqrt(lo * hi))
        if e006.vazamento_medio(s2, mid, random.Random(1)) < alvo:
            lo = mid
        else:
            hi = mid
    return (lo + hi) // 2


def uma(seed):
    rng = random.Random(seed)
    s2 = mlu.S2Step(4, rng)
    with contextlib.redirect_stdout(io.StringIO()):
        s2.train(mlu.dataset(mlu.N_TRAIN, mlu.TRAIN_DEPTHS, 20000, rng), iters=600, rng=rng)
    m = margem_efetiva(s2)
    ec = eps_c_teoria(m)
    return seed, m, ec, (n_para_eps(s2, ec) if ec else None)


def main():
    res_e007 = {r["seed"]: r for r in json.load(open(os.path.join(AQUI, "resultados.json")))}
    with Pool(4) as pool:
        res = pool.map(uma, sorted(res_e007))
    L = ["# E007 - diagnostico: teoria de campo medio (30 sementes do E007)", "",
         "| semente | margem efetiva m | eps_c teoria | N_c previsto (teoria) | N_c previsto (limiar 0,071) | N_c medido |",
         "|---|---|---|---|---|---|"]
    e_teo, e_fix = [], []
    for seed, m, ec, nt in res:
        r = res_e007[seed]
        nc, nf = r["d20"]["nc"], r["nprev"]
        L.append(f"| {seed} | {m:.2f} | {ec if ec is None else round(ec, 4)} | {nt} | {nf} | {nc:.0f} |")
        if nt:
            e_teo.append(abs(math.log(nc / nt)))
            e_fix.append(abs(math.log(nc / nf)))
    L += ["", f"- erro medio |ln| teoria = {estat.media(e_teo):.3f} vs limiar fixo = {estat.media(e_fix):.3f} (n={len(e_teo)})",
          f"- P(teoria melhor) = {estat.prob_melhoria([-x for x in e_teo], [-x for x in e_fix]):.2f}, "
          f"p permutacao = {estat.teste_permutacao(e_teo, e_fix):.4f}",
          f"- dentro de 1,5x: teoria {sum(e <= math.log(1.5) for e in e_teo)}/{len(e_teo)}, "
          f"limiar fixo {sum(e <= math.log(1.5) for e in e_fix)}/{len(e_fix)}",
          f"- margens efetivas: min {min(r[1] for r in res):.2f}, max {max(r[1] for r in res):.2f}"]
    txt = "\n".join(L)
    print(txt)
    with open(os.path.join(AQUI, "diagnostico.md"), "w") as fh:
        fh.write(txt + "\n")


if __name__ == "__main__":
    main()
