"""
E005 - diagnostico pos-hoc (nao muda o veredito).

D1: margem aprendida (afinidade do ponteiro - maior afinidade dos outros) em T2 vs T1.
D2: nitidez do estado continuo (max z) ao longo de 64 passos em N=128.
D3: onde o continuo quebra? N em {256, 512, 1024} com k=32. Previsao pela formula
    de vazamento: quebra quando (N-1)*exp(-margem) ~ 1.
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
import tarefa_t2 as T2  # noqa: E402


def margem_perm(s2):
    pi = list(range(12))
    random.Random(0).shuffle(pi)
    S = s2.affinity(pi)
    j = 0
    return S[j][pi[j]] - max(S[j][i] for i in range(12) if i != pi[j])


def uma(seed):
    rng = random.Random(seed)
    s2 = T2.novo_s2(rng)
    T2.treinar(s2, T2.dados(12, range(1, 5), 20000, rng), 600, rng)
    # modelo T1 com a mesma semente, para comparar margens
    rng1 = random.Random(seed)
    s1 = mlu.S2Step(4, rng1)
    with contextlib.redirect_stdout(io.StringIO()):
        s1.train(mlu.dataset(12, range(5), 20000, rng1), iters=600, rng=rng1)
    p, s, _ = mlu.make_example(12, 3, random.Random(0))
    S1 = s1.affinity(p)
    m_t1 = S1[s][p[s]] - max(S1[s][i] for i in range(12) if i != p[s])
    r = {"seed": seed, "margem_T2": margem_perm(s2), "margem_T1": m_t1}
    trng = random.Random(90000 + seed)
    pi, s, k, alvo = T2.exemplo(128, 64, trng)
    S = s2.affinity(pi)
    z = [0.0] * 128
    z[s] = 1.0
    mx = []
    for _ in range(64):
        z = s2.step(z, S)
        mx.append(max(z))
    r["maxz_t1"], r["maxz_t64"] = mx[0], mx[-1]
    for N in (256, 512, 1024):
        exs = [T2.exemplo(N, 32, trng) for _ in range(4)]
        r[f"cont_N{N}"] = sum(T2.pensar(s2, a, b, 32, "CONT") == c for a, b, _, c in exs) / 4
        r[f"crist_N{N}"] = sum(T2.pensar(s2, a, b, 32, "CRIST") == c for a, b, _, c in exs) / 4
    return r


def main():
    with Pool(4) as pool:
        res = pool.map(uma, range(510, 514))
    L = ["# E005 - diagnostico (4 sementes)", "",
         "| semente | margem T2 | margem T1 | vazamento previsto N=128 | max z t=1 | max z t=64 | N*=e^margem | cont N=256/512/1024 | crist N=256/512/1024 |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        m = r["margem_T2"]
        L.append(f"| {r['seed']} | {m:.2f} | {r['margem_T1']:.2f} | {127 * math.exp(-m):.3f} | {r['maxz_t1']:.3f} | {r['maxz_t64']:.3f} "
                 f"| {math.exp(m):.0f} | {r['cont_N256']:.2f}/{r['cont_N512']:.2f}/{r['cont_N1024']:.2f} "
                 f"| {r['crist_N256']:.2f}/{r['crist_N512']:.2f}/{r['crist_N1024']:.2f} |")
    txt = "\n".join(L)
    print(txt)
    with open(os.path.join(AQUI, "diagnostico.md"), "w") as fh:
        fh.write(txt + "\n")


if __name__ == "__main__":
    main()
