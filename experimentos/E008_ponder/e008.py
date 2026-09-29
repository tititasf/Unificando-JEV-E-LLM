"""
E008 - PonderNet reimplementada reproduz o efeito publicado? (ver PREREG.md)

Motor S2 treinado em T1 (identico ao E001), congelado. Cabeca de parada
estilo PonderNet treinada em trajetorias da distribuicao de treino
(N=12, d<=4). Teste: N=12, d em 0..9 (5..9 fora da distribuicao).
Comparacoes: CONV (parada por ponto fixo, E004) e FIXO (T_max sempre).

Uso: python3 experimentos/E008_ponder/e008.py [--quick] [--procs=4]
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
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, RAIZ)
from lab import baselines as B  # noqa: E402
from lab import estat, sementes  # noqa: E402

mlu = B.mlu
QUICK = "--quick" in sys.argv
SEMENTES_TREINO = list(range(800, 802)) if QUICK else list(range(800, 810))
T_MAX = 16
N = 12
DS = list(range(0, 10))
N_EX = 5 if QUICK else 30
N_CASOS_TREINO = 60 if QUICK else 300
BASE = "smoke" if QUICK else sementes.base_teste(__file__)
SEM_TESTE = sementes.derivar(BASE, len(SEMENTES_TREINO))
EPS = 0.02


def conv(linha_z):
    """Parada por ponto fixo (braco CONV do E004): primeiro t com |z_t - z_{t-1}|_1 < EPS."""
    for t in range(1, len(linha_z)):
        if sum(abs(a - b) for a, b in zip(linha_z[t], linha_z[t - 1])) < EPS:
            return max(range(N), key=lambda i: linha_z[t][i]), t
    return None, len(linha_z) - 1


def uma(arg):
    i, seed = arg
    t0 = time.time()
    rng = random.Random(seed)
    s2 = mlu.S2Step(4, rng)
    with contextlib.redirect_stdout(io.StringIO()):
        s2.train(mlu.dataset(mlu.N_TRAIN, mlu.TRAIN_DEPTHS, 20000, rng), iters=200 if QUICK else 600, rng=rng)
    casos = []
    for _ in range(N_CASOS_TREINO):
        p, s, r = mlu.make_example(N, rng.randint(0, 4), rng)
        casos.append((p, s, lambda t, r=r: r))
    w = B.treinar_ponder(B.trajetorias(s2, casos, T_MAX), iters=60 if QUICK else 150, rng=rng)
    trng = random.Random(SEM_TESTE[i])
    r = {"seed": seed, "w": w, "por_d": {}}
    for d in DS:
        acc_p = passos_p = acc_c = passos_c = abst_c = acc_f = 0
        for _ in range(N_EX):
            p, s, root = mlu.make_example(N, d, trng)
            linha = B.trajetorias(s2, [(p, s, lambda t: root)], T_MAX)[0]
            pred, t = B.decidir_ponder(w, linha)
            acc_p += pred == root
            passos_p += t
            z0 = [0.0] * N
            z0[s] = 1.0
            S = s2.affinity(p)
            zs = [z0]
            for _ in range(T_MAX):
                zs.append(s2.step(zs[-1], S))
            pc, tc = conv(zs)
            abst_c += pc is None
            acc_c += pc == root
            passos_c += tc
            acc_f += max(range(N), key=lambda k: zs[-1][k]) == root
        r["por_d"][d] = dict(acc_ponder=acc_p / N_EX, passos_ponder=passos_p / N_EX, acc_conv=acc_c / N_EX,
                             passos_conv=passos_c / N_EX, abst_conv=abst_c / N_EX, acc_fixo=acc_f / N_EX)
    r["cpu_s"] = time.time() - t0
    print(f"semente {seed} ok ({r['cpu_s']:.0f}s)", flush=True)
    return r


def spearman(x, y):
    def rk(v):
        o = sorted(range(len(v)), key=lambda k: v[k])
        rr = [0.0] * len(v)
        k = 0
        while k < len(o):
            j = k
            while j + 1 < len(o) and v[o[j + 1]] == v[o[k]]:
                j += 1
            for q in range(k, j + 1):
                rr[o[q]] = (k + j) / 2
            k = j + 1
        return rr
    rx, ry = rk(x), rk(y)
    mx, my = estat.media(rx), estat.media(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else 0.0


def main():
    procs = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--procs=")), 4))
    with Pool(procs) as pool:
        res = pool.map(uma, list(enumerate(SEMENTES_TREINO)))
    n = len(res)
    g = lambda d, k: [r["por_d"][d][k] for r in res]  # noqa: E731
    L = [f"# E008 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{n} sementes x {N_EX} exemplos por d; N={N}; T_max={T_MAX}; base das sementes de teste = {BASE[:12]}", "",
         "| d | acc PonderNet | passos PonderNet | acc CONV | passos CONV | abst CONV | acc FIXO (T=16) |",
         "|---|---|---|---|---|---|---|"]
    for d in DS:
        L.append(f"| {d} | {estat.media(g(d, 'acc_ponder')):.3f} | {estat.media(g(d, 'passos_ponder')):.2f} | "
                 f"{estat.media(g(d, 'acc_conv')):.3f} | {estat.media(g(d, 'passos_conv')):.2f} | "
                 f"{estat.media(g(d, 'abst_conv')):.3f} | {estat.media(g(d, 'acc_fixo')):.3f} |")
    rhos = [spearman(DS, [r["por_d"][d]["passos_ponder"] for d in DS]) for r in res]
    acc_in = [estat.media([r["por_d"][d]["acc_ponder"] for d in range(0, 5)]) for r in res]
    acc_out = [estat.media([r["por_d"][d]["acc_ponder"] for d in range(5, 10)]) for r in res]
    passos_p = [estat.media([r["por_d"][d]["passos_ponder"] for d in DS]) for r in res]
    passos_c = [estat.media([r["por_d"][d]["passos_conv"] for d in DS]) for r in res]
    L += ["", "## Checagem das previsões", "",
          f"- P1 Spearman(d, passos PonderNet) por semente: mediana {sorted(rhos)[n // 2]:.2f}, min {min(rhos):.2f} (previsto mediana >= 0,8)",
          f"- P2 acc PonderNet d<=4: IQM {estat.iqm(acc_in):.3f}, min {min(acc_in):.3f} (previsto >= 0,95)",
          f"- P3 acc PonderNet d=5..9 (fora da distribuicao): IQM {estat.iqm(acc_out):.3f}, min {min(acc_out):.3f} (previsto >= 0,90)",
          f"- P4 passos medios PonderNet {estat.media(passos_p):.2f} vs CONV {estat.media(passos_c):.2f} "
          f"(previsto: PonderNet <= CONV + 1)",
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
