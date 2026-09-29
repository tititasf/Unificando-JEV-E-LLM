"""
E007 - lei de nitidez fora da amostra (ver PREREG.md; parametros congelados).

Para cada semente nova: treina o S2 em T1 (identico ao E001), calcula a curva de
vazamento de um passo eps(N) e PREVE N_c = o N com eps(N) = EPS_C (congelado do
E006d). Mede o N_c real na grade N_prev x FATORES (d = 20). Num subconjunto,
mede tambem com d = 10 e d = 40 para decidir "por passo" x "acumulado".

Uso: python3 experimentos/E007_lei_eps/e007.py [--quick] [--procs=4]
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
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E006_lei_margem"))
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E001_mlu"))
sys.path.insert(0, RAIZ)
import mlu  # noqa: E402
import e006  # noqa: E402  (vazamento_medio e acuracia, congelados no E006)
from lab import estat, sementes  # noqa: E402

QUICK = "--quick" in sys.argv
EPS_C = 0.071                 # congelado: IQM de eps(N_c) no E006d
N_CONST = 137                 # linha de base nula: mediana de N_c no E006d
SEMENTES_TREINO = list(range(700, 702)) if QUICK else list(range(700, 730))
SUBCONJ_D = 2 if QUICK else 15          # sementes com o teste de d
FATORES = (0.5, 0.71, 1.0, 1.41, 2.0)
FATORES_D = (0.25, 0.35, 0.5, 0.71, 1.0, 1.41, 2.0)
N_EX = 8 if QUICK else 40
BASE = "smoke" if QUICK else sementes.base_teste(__file__)
SEM_TESTE = sementes.derivar(BASE, len(SEMENTES_TREINO))


def prever_nc(s2):
    """Bissecao em log N ate eps(N) = EPS_C (mesmos grafos de prova do E006)."""
    lo, hi = 24, 1 << 15          # grafos de prova tem d = 20: N minimo 23
    if e006.vazamento_medio(s2, lo, random.Random(1)) >= EPS_C:
        return lo
    if e006.vazamento_medio(s2, hi, random.Random(1)) < EPS_C:
        return hi
    while hi - lo > max(2, lo // 100):
        mid = int(math.sqrt(lo * hi))
        if e006.vazamento_medio(s2, mid, random.Random(1)) < EPS_C:
            lo = mid
        else:
            hi = mid
    return (lo + hi) // 2


def cruzamento(curva, idx):
    """Primeira queda de curva[.][idx] abaixo de 0,5 subindo N (interpolacao geometrica).
    Devolve (N_c, tipo): tipo = ok | abaixo (ja < 0,5 no menor N) | acima (nunca cai)."""
    if curva[0][idx] < 0.5:
        return curva[0][0], "abaixo"
    for c0, c1 in zip(curva, curva[1:]):
        if c0[idx] >= 0.5 > c1[idx]:
            t = (c0[idx] - 0.5) / (c0[idx] - c1[idx])
            return math.exp(math.log(c0[0]) + t * (math.log(c1[0]) - math.log(c0[0]))), "ok"
    return curva[-1][0], "acima"


def medir_nc(s2, nprev, d, fatores, rng):
    """Mede, na grade, a acuracia e a nitidez media (max z final).
    Devolve dict com N_c pelo REGIME (nitidez = 0,5; primario) e pela ACURACIA (secundario)."""
    curva = []
    for f in fatores:
        N = max(d + 8, int(round(nprev * f)))
        acc, mz = e006.acuracia(s2, N, d, N_EX, rng)
        curva.append((N, acc, mz))
    nc_r, tipo_r = cruzamento(curva, 2)
    nc_a, tipo_a = cruzamento(curva, 1)
    return dict(nc=nc_r, tipo=tipo_r, nc_acc=nc_a, tipo_acc=tipo_a, curva=curva)


def uma(arg):
    i, seed = arg
    t0 = time.time()
    rng = random.Random(seed)
    s2 = mlu.S2Step(4, rng)
    with contextlib.redirect_stdout(io.StringIO()):
        s2.train(mlu.dataset(mlu.N_TRAIN, mlu.TRAIN_DEPTHS, 20000, rng), iters=200 if QUICK else 600, rng=rng)
    nprev = prever_nc(s2)
    trng = random.Random(SEM_TESTE[i])
    r = {"seed": seed, "nprev": nprev}
    r["d20"] = medir_nc(s2, nprev, 20, FATORES, trng)
    if i < SUBCONJ_D:
        r["d10"] = medir_nc(s2, nprev, 10, FATORES_D, trng)
        r["d40"] = medir_nc(s2, nprev, 40, FATORES_D, trng)
    r["cpu_s"] = time.time() - t0
    print(f"semente {seed}: N_prev={nprev} N_c(d20)={r['d20']['nc']:.0f} [{r['d20']['tipo']}] ({r['cpu_s']:.0f}s)", flush=True)
    return r


def main():
    procs = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--procs=")), 4))
    with Pool(procs) as pool:
        res = pool.map(uma, list(enumerate(SEMENTES_TREINO)))
    n = len(res)
    err_lei = [abs(math.log(r["d20"]["nc"] / r["nprev"])) for r in res]
    err_const = [abs(math.log(r["d20"]["nc"] / N_CONST)) for r in res]
    err_acc = [abs(math.log(r["d20"]["nc_acc"] / r["nprev"])) for r in res]
    dentro = [r["d20"]["tipo"] == "ok" and e <= math.log(1.5) for r, e in zip(res, err_lei)]
    dentro_acc = [r["d20"]["tipo_acc"] == "ok" and e <= math.log(1.5) for r, e in zip(res, err_acc)]
    na_grade = sum(r["d20"]["tipo"] == "ok" for r in res)
    L = [f"# E007 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{n} sementes novas; {N_EX} exemplos por celula; eps_c congelado = {EPS_C}; base das sementes de teste = {BASE[:12]}", "",
         "N_c primario = cruzamento da nitidez media (max z final = 0,5); secundario = cruzamento da acuracia = 0,5.", "",
         "| semente | N previsto | N_c regime (d=20) | tipo | erro |ln| | N_c acuracia | curva d=20 (N: acc/maxz) |",
         "|---|---|---|---|---|---|---|"]
    for r, e in zip(res, err_lei):
        curva = ", ".join(f"{N}:{a:.2f}/{m:.2f}" for N, a, m in r["d20"]["curva"])
        L.append(f"| {r['seed']} | {r['nprev']} | {r['d20']['nc']:.0f} | {r['d20']['tipo']} | {e:.2f} | "
                 f"{r['d20']['nc_acc']:.0f} ({r['d20']['tipo_acc']}) | {curva} |")
    lo, hi = estat.bootstrap_ic(err_lei, estat.media)
    L += ["", "## Checagem das previsões", "",
          f"- P1 N_c (regime) dentro de 1,5x do previsto: {sum(dentro)}/{n} = {sum(dentro) / n:.2f} (previsto >= 0,80)",
          f"- P2 cruzamento (regime) dentro da grade: {na_grade}/{n} = {na_grade / n:.2f} (previsto >= 0,90)",
          f"- P3 erro medio |ln| lei = {estat.media(err_lei):.3f} [IC95% {lo:.3f}, {hi:.3f}] vs constante = {estat.media(err_const):.3f}; "
          f"P(lei melhor) = {estat.prob_melhoria([-x for x in err_lei], [-x for x in err_const]):.2f}, "
          f"p permutacao = {estat.teste_permutacao(err_lei, err_const):.4f}",
          f"- (secundario) N_c pela acuracia dentro de 1,5x: {sum(dentro_acc)}/{n} = {sum(dentro_acc) / n:.2f}"]
    razoes = [r["d40"]["nc"] / r["d10"]["nc"] for r in res
              if "d10" in r and r["d10"]["tipo"] == "ok" and r["d40"]["tipo"] == "ok"]
    if razoes:
        L.append(f"- P4/P5 razao R = N_c(d=40)/N_c(d=10) pelo regime: n={len(razoes)}, "
                 f"mediana {sorted(razoes)[len(razoes) // 2]:.2f}, IQM {estat.iqm(razoes):.2f}, "
                 f"valores {', '.join(f'{x:.2f}' for x in razoes)}")
    else:
        L.append("- P4/P5: nenhuma semente com cruzamento (regime) dentro da grade em d=10 e d=40")
    L.append(f"- CPU total: {sum(r['cpu_s'] for r in res):.0f}s")
    txt = "\n".join(L)
    print(txt)
    nome = "resultados_smoke" if QUICK else "resultados"
    with open(os.path.join(AQUI, nome + ".md"), "w") as fh:
        fh.write(txt + "\n")
    with open(os.path.join(AQUI, nome + ".json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
