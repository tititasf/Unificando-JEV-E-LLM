"""
E013 - temperatura derivada da lei de nitidez: nitidez em qualquer escala sem re-treino (H05).

Para cada semente treina um S2 de T1 (raiz) e um de T2 (k saltos), ambos em N = 12.
Mede a margem efetiva m sem rotulos (vazamento de um passo em N = 30) e testa em
N in {12, 256, 4096} com temperatura beta nos logits:
  B1      beta = 1 (sem mecanismo)
  TEORIA  beta(N) = 1 + ln((N-1)/(N_TR-1)) / m   (mantem o vazamento de N_TR; zero parametros livres)
  SSMAX   beta(N) = ln(N-1) / ln(N_TR-1)         (Scalable-Softmax, s fixado para beta(N_TR) = 1)
  CONST3  beta = 3 (atalho: afiar sempre)
  CRIST   argmax a cada passo (atalho: cristalizar)
Uso: python3 e013.py [--quick]
"""
import contextlib
import importlib.util
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
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E005_t2_salto"))
_argv = sys.argv
sys.argv = [sys.argv[0]]
import passo_geral as PG  # noqa: E402  (poe E001 e E006 no caminho)
import mlu  # noqa: E402
import tarefa_t2 as T2  # noqa: E402
sys.argv = _argv
from lab import estat, sementes  # noqa: E402

_sp = importlib.util.spec_from_file_location("diag_e007", os.path.join(RAIZ, "experimentos", "E007_lei_eps", "diagnostico.py"))
DG = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(DG)

QUICK = "--quick" in sys.argv
SEMENTES = [1394, 1395] if QUICK else list(range(1300, 1310))
NS = (12, 256) if QUICK else (12, 256, 4096)
N_EX = 3 if QUICK else 10
N_TR = 12
D_T1, K_T2 = 8, 16
BRACOS = ("B1", "TEORIA", "SSMAX", "CONST3", "CRIST")
SUF = "_smoke" if QUICK else ""


def beta(braco, N, m):
    if braco == "TEORIA":
        return 1.0 + math.log((N - 1) / (N_TR - 1)) / m
    if braco == "SSMAX":
        return math.log(N - 1) / math.log(N_TR - 1)
    if braco == "CONST3":
        return 3.0
    return 1.0


def gerar(tarefa, N, rng):
    if tarefa == "T1":
        p, s, r = mlu.make_example(N, D_T1, rng)
        return p, s, r, D_T1 + 8
    pi, s, k, alvo = T2.exemplo(N, K_T2, rng)
    return pi, s, alvo, k


def margem(s2, tarefa):
    """Margem efetiva sem rotulos: inverte eps = K e^-m / (1 + K e^-m) em N = 30."""
    r = random.Random(1)
    eps, n = 0.0, 0
    for _ in range(5):
        p = gerar(tarefa, 30, r)[0]
        P = PG.preparar(s2, p)
        for j in r.sample([j for j in range(30) if p[j] != j], 6):
            eps += PG.vazamento(P, j)
            n += 1
    eps /= n
    return -math.log(eps / ((1 - eps) * 29))


def treinar(tarefa, rng):
    if tarefa == "T1":
        s2 = mlu.S2Step(4, rng)
        with contextlib.redirect_stdout(io.StringIO()):
            s2.train(mlu.dataset(N_TR, mlu.TRAIN_DEPTHS, 20000, rng), iters=600, rng=rng)
        return s2
    s2 = T2.novo_s2(rng)
    T2.treinar(s2, T2.dados(N_TR, range(1, 5), 20000, rng), iters=600, rng=rng)
    return s2


def uma(arg):
    i, seed, sem_teste = arg
    t0 = time.time()
    r = {"seed": seed}
    for tarefa in ("T1", "T2"):
        s2 = treinar(tarefa, random.Random(seed if tarefa == "T1" else seed + 1000))
        m = margem(s2, tarefa)
        r[f"{tarefa}|m"] = m
        r[f"{tarefa}|eps_c"] = DG.eps_c_teoria(m)
        trng = random.Random(sem_teste + (0 if tarefa == "T1" else 1))
        for N in NS:
            exs = [gerar(tarefa, N, trng) for _ in range(N_EX)]
            Ps = [PG.preparar(s2, e[0]) for e in exs]
            for b in BRACOS:
                be = beta(b, N, m)
                ok, eps = 0, 0.0
                for (g, s, alvo, T), P in zip(exs, Ps):
                    z = [0.0] * N
                    z[s] = 1.0
                    for _ in range(T):
                        z = PG.passo(z, P, be, b == "CRIST")
                    ok += max(range(N), key=lambda q: z[q]) == alvo
                    eps += PG.vazamento(P, s, be)
                r[f"{tarefa}|{N}|{b}|acc"] = ok / N_EX
                r[f"{tarefa}|{N}|{b}|beta"] = be
                if b != "CRIST":
                    r[f"{tarefa}|{N}|{b}|eps"] = eps / N_EX
    r["cpu_s"] = time.time() - t0
    print(f"semente {seed} ok ({r['cpu_s']:.0f}s)", flush=True)
    return r


def main():
    procs = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--procs=")), 4)
    teste = [1494, 1495] if QUICK else sementes.derivar(sementes.base_teste(__file__), len(SEMENTES))
    with Pool(procs) as pool:
        res = pool.map(uma, [(i, s, teste[i]) for i, s in enumerate(SEMENTES)])
    json.dump(res, open(os.path.join(AQUI, f"resultados{SUF}.json"), "w"), indent=1, sort_keys=True)

    def col(ch):
        return [x[ch] for x in res]
    Nmax = NS[-1]
    L = [f"# E013 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{len(SEMENTES)} sementes x {N_EX} instancias por celula; treino N = {N_TR}; T1 d = {D_T1}, T2 k = {K_T2}", "",
         "| tarefa | N | braço | beta (IQM) | acerto IQM [IC95%] | colapsos (< 0,5) | vazamento eps IQM | eps / eps(12) IQM |",
         "|---|---|---|---|---|---|---|---|"]
    for t in ("T1", "T2"):
        for N in NS:
            for b in BRACOS:
                a = col(f"{t}|{N}|{b}|acc")
                lo, hi = estat.bootstrap_ic(a, estat.iqm)
                if b != "CRIST":
                    e = col(f"{t}|{N}|{b}|eps")
                    rz = [x / y for x, y in zip(e, col(f"{t}|12|B1|eps"))]
                    es, rs = f"{estat.iqm(e):.4f}", f"{estat.iqm(rz):.2f}"
                else:
                    es = rs = "-"
                L.append(f"| {t} | {N} | {b} | {estat.iqm(col(f'{t}|{N}|{b}|beta')):.2f} | {estat.iqm(a):.2f} [{lo:.2f},{hi:.2f}] | "
                         f"{sum(v < 0.5 for v in a)}/{len(a)} | {es} | {rs} |")
    L += ["", f"Margens efetivas: T1 {min(col('T1|m')):.2f}–{max(col('T1|m')):.2f}; T2 {min(col('T2|m')):.2f}–{max(col('T2|m')):.2f}",
          "", "## Checagem das previsões", ""]
    ok1 = all(estat.iqm(col(f"{t}|{Nmax}|B1|acc")) <= 0.30 for t in ("T1", "T2"))
    L.append(f"- P1 {'OK' if ok1 else 'FALHOU'}: B1 em N={Nmax} acerto IQM <= 0,30: " +
             ", ".join(f"{t} {estat.iqm(col(f'{t}|{Nmax}|B1|acc')):.2f}" for t in ("T1", "T2")))
    ok2 = all(estat.iqm(col(f"{t}|{Nmax}|TEORIA|acc")) >= 0.95 and min(col(f"{t}|{Nmax}|TEORIA|acc")) >= 0.5 for t in ("T1", "T2"))
    L.append(f"- P2 {'OK' if ok2 else 'FALHOU'}: TEORIA em N={Nmax} IQM >= 0,95 e 0 colapsos: " +
             ", ".join(f"{t} {estat.iqm(col(f'{t}|{Nmax}|TEORIA|acc')):.2f} (min {min(col(f'{t}|{Nmax}|TEORIA|acc')):.2f})" for t in ("T1", "T2")))
    cel, det = 0, []
    for t in ("T1", "T2"):
        for N in NS[1:]:
            rz = [x / y for x, y in zip(col(f"{t}|{N}|TEORIA|eps"), col(f"{t}|12|B1|eps"))]
            dentro = sum(0.5 <= v <= 2.0 for v in rz)
            cel += dentro >= 0.9 * len(rz)
            det.append(f"{t} N={N}: {dentro}/{len(rz)}")
    tot = 2 * (len(NS) - 1)
    L.append(f"- P3 {'OK' if cel == tot else 'FALHOU'}: TEORIA eps(N)/eps(12) em [0,5; 2] em >= 90% das sementes, todas as células: {'; '.join(det)}")
    ok4 = all(estat.iqm(col(f"{t}|{Nmax}|{b}|acc")) >= 0.95 for t in ("T1", "T2") for b in ("SSMAX", "CONST3", "CRIST"))
    L.append(f"- P4 {'OK' if ok4 else 'FALHOU'}: atalhos (SSMAX, CONST3, CRIST) em N={Nmax} IQM >= 0,95: " +
             ", ".join(f"{t}/{b} {estat.iqm(col(f'{t}|{Nmax}|{b}|acc')):.2f}" for t in ("T1", "T2") for b in ("SSMAX", "CONST3", "CRIST")))
    rz5 = {t: estat.iqm([x / y for x, y in zip(col(f"{t}|{Nmax}|SSMAX|eps"), col(f"{t}|12|B1|eps"))]) for t in ("T1", "T2")}
    L.append(f"- P5 {'OK' if all(v < 0.1 for v in rz5.values()) else 'FALHOU'}: SSMAX afia demais, eps({Nmax})/eps(12) IQM < 0,1: " +
             ", ".join(f"{t} {v:.3f}" for t, v in rz5.items()))
    ok6 = all(e < c for t in ("T1", "T2") for e, c in zip(col(f"{t}|{Nmax}|TEORIA|eps"), col(f"{t}|eps_c")))
    L.append(f"- P6 {'OK' if ok6 else 'FALHOU'}: TEORIA eps({Nmax}) < eps_c(m) em todas as sementes (T1 e T2)")
    L.append(f"- CPU total: {sum(col('cpu_s')):.0f}s")
    txt = "\n".join(L)
    open(os.path.join(AQUI, f"resultados{SUF}.md"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
