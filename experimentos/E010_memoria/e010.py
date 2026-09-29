"""
E010 - memoria de trabalho latente (S2 D06): o proprio estado conta os saltos.
Ver PREREG.md.

Bracos:
  MEMORIA      motor de pares (no, contador) aprendido; controlador roda T_RUN passos fixos
  SEM_MARCAS   ablacao: mesmo motor sem os atributos "a == 0", "b == 0"
  SEM_MEMORIA  so o ponteiro (S2 do E005, treinado em T2), roda T_RUN passos (nao sabe parar)
  CONTROLADOR  S2 do E005 com o controlador contando exatamente k passos (limite superior; "trapaca")

Uso: python3 experimentos/E010_memoria/e010.py [--quick] [--procs=4]
"""
import json
import math
import os
import random
import sys
import time
from multiprocessing import Pool

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E005_t2_salto"))
sys.path.insert(0, RAIZ)
import memoria as M  # noqa: E402
import tarefa_t2 as T2  # noqa: E402
from lab import baselines as B  # noqa: E402
from lab import estat, sementes  # noqa: E402

QUICK = "--quick" in sys.argv
SEMENTES_TREINO = list(range(1000, 1002)) if QUICK else list(range(1000, 1010))
N_TREINO, K_TREINO, T_TREINO = 8, 4, 8
ITERS = 120 if QUICK else 400
NS = (8, 32) if QUICK else (8, 32, 64)
KS = (4, 16) if QUICK else (4, 16, 64)
K_TESTE = 64
T_RUN = K_TESTE + 8            # o controlador roda sempre isto; nao conhece k
N_EX = 3 if QUICK else 15
BASE = "smoke" if QUICK else sementes.base_teste(__file__)
SEM_TESTE = sementes.derivar(BASE, len(SEMENTES_TREINO))


class SemMarcas(M.MotorMem):
    def feat(self, g, u, v):
        f = list(super().feat(g, u, v))
        f[7] = f[8] = 0.0
        return tuple(f)

    def tabela(self):
        V = super().tabela()
        # sem marcas: o valor nao pode depender de a0/b0
        return {k: V[(k[0], k[1], 0, 0)] for k in V}


def treinar(motor, rng):
    P = len(motor.theta)
    est = ([0.0] * P, [0.0] * P)
    for it in range(1, ITERS + 1):
        lote = []
        for _ in range(16):
            pi = list(range(N_TREINO))
            rng.shuffle(pi)
            k = rng.randint(1, K_TREINO)
            s = rng.randrange(N_TREINO)
            alvo = s
            for _ in range(k):
                alvo = pi[alvo]
            g = M.Pares(pi, K_TREINO)
            # supervisiona de t = k ate T: tem de chegar E ficar parado em (alvo, 0)
            alvos = {t: g.idx(alvo, 0) for t in range(k, T_TREINO + 1)}
            lote.append((g, M.estado_inicial(g, s, k), T_TREINO, alvos))
        _, gr = B.bptt(motor, lote)
        B._adam(motor, gr, est, it, 0.03)


def rodar_mem(motor, V, pi, s, k):
    g = M.Pares(pi, K_TESTE)
    z = M.estado_inicial(g, s, k)
    for _ in range(T_RUN):
        z = M.passo_rapido(z, g, V)
    return M.resposta(z, g)[0]


def uma(arg):
    i, seed = arg
    t0 = time.time()
    rng = random.Random(seed)
    mem = M.MotorMem(6, rng)
    treinar(mem, rng)
    abl = SemMarcas(6, random.Random(seed + 1))
    treinar(abl, random.Random(seed + 2))
    s2 = T2.novo_s2(random.Random(seed + 3))
    T2.treinar(s2, T2.dados(12, range(1, 5), 20000, random.Random(seed + 4)), iters=150 if QUICK else 600,
               rng=random.Random(seed + 5))
    Vm, Va = mem.tabela(), abl.tabela()
    trng = random.Random(SEM_TESTE[i])
    r = {"seed": seed}
    for N in NS:
        for k in KS:
            ok = {b: 0 for b in ("MEMORIA", "SEM_MARCAS", "SEM_MEMORIA", "CONTROLADOR")}
            for _ in range(N_EX):
                pi, s, _, alvo = T2.exemplo(N, k, trng)
                ok["MEMORIA"] += rodar_mem(mem, Vm, pi, s, k) == alvo
                ok["SEM_MARCAS"] += rodar_mem(abl, Va, pi, s, k) == alvo
                ok["SEM_MEMORIA"] += T2.pensar(s2, pi, s, T_RUN, "CONT") == alvo
                ok["CONTROLADOR"] += T2.pensar(s2, pi, s, k, "CONT") == alvo
            for b, v in ok.items():
                r[f"{b}|{N}|{k}"] = v / N_EX
    r["cpu_s"] = time.time() - t0
    print(f"semente {seed} ok ({r['cpu_s']:.0f}s)", flush=True)
    return r


def main():
    procs = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--procs=")), 4))
    with Pool(procs) as pool:
        res = pool.map(uma, list(enumerate(SEMENTES_TREINO)))
    n = len(res)
    col = lambda key: [r[key] for r in res]  # noqa: E731
    L = [f"# E010 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{n} sementes x {N_EX} exemplos; treino N={N_TREINO}, k<={K_TREINO}; teste com contador de tamanho {K_TESTE} "
         f"e {T_RUN} passos fixos; base das sementes de teste = {BASE[:12]}", "",
         "Célula: IQM da acurácia entre sementes [IC95%] (colapsos < 0,5).", "",
         "| braço | N | " + " | ".join(f"k={k}" for k in KS) + " |", "|---|---|" + "---|" * len(KS)]
    for b in ("MEMORIA", "SEM_MARCAS", "SEM_MEMORIA", "CONTROLADOR"):
        for N in NS:
            cel = []
            for k in KS:
                v = col(f"{b}|{N}|{k}")
                lo, hi = estat.bootstrap_ic(v, estat.iqm)
                cel.append(f"{estat.iqm(v):.2f} [{lo:.2f},{hi:.2f}] ({sum(x < 0.5 for x in v)})")
            L.append(f"| {b} | {N} | " + " | ".join(cel) + " |")
    Nm, km = NS[-1], KS[-1]
    a, b_ = col(f"MEMORIA|{Nm}|{km}"), col(f"SEM_MARCAS|{Nm}|{km}")
    c = col(f"SEM_MEMORIA|{Nm}|{km}")
    L += ["", "## Checagem das previsões", "",
          f"- P1 MEMORIA IQM >= 0,95 em todas as células: {all(estat.iqm(col(f'MEMORIA|{N}|{k}')) >= 0.95 for N in NS for k in KS)}",
          f"- P2 MEMORIA em (N={Nm}, k={km}): IQM {estat.iqm(a):.2f}, colapsos {sum(x < 0.5 for x in a)}/{n}",
          f"- P3 SEM_MARCAS em (N={Nm}, k={km}): IQM {estat.iqm(b_):.2f}; MEMORIA vs SEM_MARCAS: P(A>B) = {estat.prob_melhoria(a, b_):.2f}, "
          f"p = {estat.teste_permutacao(a, b_):.4f}",
          f"- P4 SEM_MEMORIA em (N={Nm}, k={km}): IQM {estat.iqm(c):.2f}",
          f"- P5 CONTROLADOR (limite superior) em (N={Nm}, k={km}): IQM {estat.iqm(col(f'CONTROLADOR|{Nm}|{km}')):.2f}",
          f"- CPU total: {sum(col('cpu_s')):.0f}s"]
    txt = "\n".join(L)
    print(txt)
    nome = "resultados_smoke" if QUICK else "resultados"
    with open(os.path.join(AQUI, nome + ".md"), "w") as fh:
        fh.write(txt + "\n")
    with open(os.path.join(AQUI, nome + ".json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
