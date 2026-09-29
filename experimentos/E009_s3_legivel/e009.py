"""
E009 - S3 em dois tempos: metacognicao legivel em qualquer escala (ver PREREG.md).

S3 proposto (DOIS_TEMPOS):
  1. antes de pensar: mede o vazamento do PRIMEIRO passo desta instancia,
     eps_inst = 1 - max(z_1). Se eps_inst > eps_c(m) (teoria de campo medio,
     com a margem m do modelo medida uma vez em N=30), o pensamento vai se
     dissolver: abstem-se ja.
  2. durante: para por ponto fixo (|z_t - z_{t-1}|_1 < 0,02). Sem convergir
     ate T: abstem-se.
Comparacoes: SEMPRE (sem S3), ABS (E001), CONV (so o tempo 2), SO_ANTES
(so o tempo 1, responde em T), PONDER (PonderNet, lab/baselines.py).

Condicoes (N previsto pelo modelo: N_hat = N com eps(N) = eps_c(m)):
  DENTRO     N <= N_hat/1,5, T = d+6        -> deve responder (e acertar)
  FORA_ORC   N <= N_hat/1,5, T = d-3        -> deve se abster
  FORA_REG   N >= 1,5 N_hat (ate 1024), T = d+6 -> deve se abster (pensamento dissolvido)

Uso: python3 experimentos/E009_s3_legivel/e009.py [--quick] [--procs=4]
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
for sub in ("E006_lei_margem", "E007_lei_eps", "E001_mlu"):
    sys.path.insert(0, os.path.join(RAIZ, "experimentos", sub))
sys.path.insert(0, RAIZ)
import mlu  # noqa: E402
import passo_rapido as PR  # noqa: E402
import diagnostico as TEO  # noqa: E402  (E007: eps_c_teoria, margem_efetiva, n_para_eps)
from lab import baselines as B  # noqa: E402
from lab import estat, sementes  # noqa: E402

QUICK = "--quick" in sys.argv
SEMENTES_TREINO = list(range(900, 902)) if QUICK else list(range(900, 910))
N_EX = 5 if QUICK else 20
EPS_PARADA = 0.02
BRACOS = ("SEMPRE", "ABS", "CONV", "SO_ANTES", "PONDER", "DOIS_TEMPOS")
BASE = "smoke" if QUICK else sementes.base_teste(__file__)
SEM_TESTE = sementes.derivar(BASE, len(SEMENTES_TREINO))


def trajetoria(P, s, T):
    N = P["N"]
    z = [0.0] * N
    z[s] = 1.0
    zs = [z]
    for _ in range(T):
        zs.append(PR.passo(zs[-1], P))
    return zs


def argmax(z):
    return max(range(len(z)), key=lambda i: z[i])


def decide(braco, zs, eps_c, w_ponder):
    """Devolve (resposta ou None, passos de pensamento gastos)."""
    T = len(zs) - 1
    if braco == "SEMPRE":
        return argmax(zs[T]), T
    antes_ok = (1 - max(zs[1])) <= eps_c if T >= 1 else True
    if braco == "SO_ANTES":
        return (argmax(zs[T]), T) if antes_ok else (None, 1)
    if braco == "PONDER":
        linha = [(B._phi(zs[t], zs[t - 1]), 0.0, argmax(zs[t]), None) for t in range(1, T + 1)]
        return B.decidir_ponder(w_ponder, linha) if linha else (argmax(zs[0]), 0)
    if braco == "DOIS_TEMPOS" and not antes_ok:
        return None, 1
    for t in range(1, T + 1):
        parado = sum(abs(a - b) for a, b in zip(zs[t], zs[t - 1])) < EPS_PARADA
        if braco == "ABS" and parado and max(zs[t]) >= 0.9:
            return argmax(zs[t]), t
        if braco in ("CONV", "DOIS_TEMPOS") and parado:
            return argmax(zs[t]), t
    return None, T


def celula(s2, N, cond, rng, eps_c, w):
    cont = {b: dict(n=0, resp=0, ok=0, passos=0) for b in BRACOS}
    for _ in range(N_EX):
        dmax = min(N - 5, 30)
        d = rng.randint(4, dmax) if cond == "FORA_ORC" else rng.randint(0, dmax)
        T = max(1, d - 3) if cond == "FORA_ORC" else d + 6
        p, s, root = mlu.make_example(N, d, rng)
        zs = trajetoria(PR.preparar(s2, p), s, T)
        for b in BRACOS:
            pred, passos = decide(b, zs, eps_c, w)
            c = cont[b]
            c["n"] += 1
            c["resp"] += pred is not None
            c["ok"] += pred == root
            c["passos"] += passos
    return cont


def uma(arg):
    i, seed = arg
    t0 = time.time()
    rng = random.Random(seed)
    s2 = mlu.S2Step(4, rng)
    with contextlib.redirect_stdout(io.StringIO()):
        s2.train(mlu.dataset(mlu.N_TRAIN, mlu.TRAIN_DEPTHS, 20000, rng), iters=200 if QUICK else 600, rng=rng)
    m = TEO.margem_efetiva(s2)
    eps_c = TEO.eps_c_teoria(m) or 0.0
    n_hat = TEO.n_para_eps(s2, eps_c) if eps_c else 24
    casos = []
    for _ in range(100 if QUICK else 300):
        p, s, r = mlu.make_example(12, rng.randint(0, 4), rng)
        casos.append((p, s, lambda t, r=r: r))
    w = B.treinar_ponder(B.trajetorias(s2, casos, 16), iters=60 if QUICK else 150, rng=rng)
    trng = random.Random(SEM_TESTE[i])
    ns_dentro = sorted({n for n in (12, 24, int(n_hat / 2), int(n_hat / 1.5)) if 12 <= n <= n_hat / 1.5})
    ns_fora = sorted({n for n in (int(math.ceil(1.5 * n_hat)), int(3 * n_hat), 1024) if 1.5 * n_hat <= n <= 1024})
    res = {"seed": seed, "m": m, "eps_c": eps_c, "n_hat": n_hat, "celulas": []}
    for N in ns_dentro:
        for cond in ("DENTRO", "FORA_ORC"):
            res["celulas"].append((N, cond, celula(s2, N, cond, trng, eps_c, w)))
    for N in ns_fora:
        res["celulas"].append((N, "FORA_REG", celula(s2, N, "FORA_REG", trng, eps_c, w)))
    res["cpu_s"] = time.time() - t0
    print(f"semente {seed}: m={m:.2f} eps_c={eps_c:.3f} N_hat={n_hat} ({res['cpu_s']:.0f}s)", flush=True)
    return res


def agregar(res, cond, braco, com_passos=False):
    n = resp = ok = passos = 0
    for r in res:
        for N, c, cont in r["celulas"]:
            if c == cond:
                n += cont[braco]["n"]
                resp += cont[braco]["resp"]
                ok += cont[braco]["ok"]
                passos += cont[braco]["passos"]
    return (n, resp, ok, passos) if com_passos else (n, resp, ok)


def main():
    procs = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--procs=")), 4))
    with Pool(procs) as pool:
        res = pool.map(uma, list(enumerate(SEMENTES_TREINO)))
    L = [f"# E009 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{len(res)} sementes; {N_EX} exemplos por celula; base das sementes de teste = {BASE[:12]}", "",
         "| semente | m | eps_c(m) | N_hat | N dentro | N fora do regime |", "|---|---|---|---|---|---|"]
    for r in res:
        dentro = sorted({N for N, c, _ in r["celulas"] if c == "DENTRO"})
        fora = sorted({N for N, c, _ in r["celulas"] if c == "FORA_REG"})
        L.append(f"| {r['seed']} | {r['m']:.2f} | {r['eps_c']:.3f} | {r['n_hat']} | {dentro} | {fora} |")
    L += ["", "| braço | cobertura DENTRO [IC95%] | acc seletiva DENTRO | abstenção FORA_ORC [IC95%] | abstenção FORA_REG | erros FORA_REG [IC95%] | passos médios FORA_REG |",
          "|---|---|---|---|---|---|---|"]
    tab = {}
    for b in BRACOS:
        n1, r1, o1 = agregar(res, "DENTRO", b)
        n2, r2, _ = agregar(res, "FORA_ORC", b)
        n3, r3, o3, p3 = agregar(res, "FORA_REG", b, True)
        err = r3 - o3
        tab[b] = dict(cob=r1 / n1, accsel=(o1 / r1 if r1 else float("nan")), abst_orc=(n2 - r2) / n2,
                      abst_reg=(n3 - r3) / n3, err_reg=err / n3, passos_reg=p3 / n3)
        i1, i2, i3 = estat.ic_proporcao(r1, n1), estat.ic_proporcao(n2 - r2, n2), estat.ic_proporcao(err, n3)
        t = tab[b]
        L.append(f"| {b} | {t['cob']:.3f} [{i1[0]:.3f},{i1[1]:.3f}] | {t['accsel']:.4f} | {t['abst_orc']:.3f} [{i2[0]:.3f},{i2[1]:.3f}] | "
                 f"{t['abst_reg']:.3f} | {t['err_reg']:.3f} [{i3[0]:.3f},{i3[1]:.3f}] ({err}/{n3}) | {t['passos_reg']:.1f} |")
    d = tab["DOIS_TEMPOS"]
    a_ = tab["ABS"]
    passa = lambda t: t["cob"] >= 0.99 and t["accsel"] >= 0.995 and t["abst_orc"] >= 0.99 and t["err_reg"] <= 0.01  # noqa: E731
    L += ["", "## Checagem das previsões", "",
          f"- P1 DOIS_TEMPOS cobertura DENTRO {d['cob']:.3f} (>= 0,99) e acc seletiva {d['accsel']:.4f} (>= 0,995)",
          f"- P2 DOIS_TEMPOS abstenção FORA_ORC {d['abst_orc']:.3f} (>= 0,99)",
          f"- P3 DOIS_TEMPOS erros FORA_REG {d['err_reg']:.3f} (<= 0,01)",
          f"- P4 CONV erros FORA_REG {tab['CONV']['err_reg']:.3f} (previsto >= 0,20)",
          f"- P5 PONDER erros FORA_REG {tab['PONDER']['err_reg']:.3f} (previsto >= 0,20)",
          f"- P6 SO_ANTES abstenção FORA_ORC {tab['SO_ANTES']['abst_orc']:.3f} (previsto < 0,50)",
          f"- P7 ABS também passa P1-P3: {passa(a_)} (cob {a_['cob']:.3f}, accsel {a_['accsel']:.4f}, abst_orc {a_['abst_orc']:.3f}, err_reg {a_['err_reg']:.3f})",
          f"- P8 passos FORA_REG DOIS_TEMPOS / ABS = {d['passos_reg'] / a_['passos_reg']:.3f} (previsto <= 0,10)",
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
