"""
E011 - modelo de mundo com o mesmo passo (H16). Ver PREREG.md.

Bracos:
  MUNDO        passo relacional aprendido com distancia a parede a frente
  SEM_PAREDE   ablacao: sem a distancia a parede (nao tem como antecipar o rebote)
  PERSISTENCIA linha de base mais simples: preve que nada muda
  SEM_REBOTE   linha de base "fisica ingenua": x' = x + v sem paredes (saturando no limite)

Uso: python3 experimentos/E011_mundo/e011.py [--quick] [--procs=4]
"""
import json
import os
import random
import sys
import time
from multiprocessing import Pool

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)
import mundo as W  # noqa: E402
from lab import baselines as B  # noqa: E402
from lab import estat, sementes  # noqa: E402

QUICK = "--quick" in sys.argv
SEMENTES_TREINO = list(range(1100, 1102)) if QUICK else list(range(1100, 1110))
L_TREINO, T_TREINO = 8, 8
ITERS = 100 if QUICK else 400
LS = (8, 32) if QUICK else (8, 32, 64)
T_TESTE = 16
N_EX = 5 if QUICK else 25
BASE = "smoke" if QUICK else sementes.base_teste(__file__)
SEM_TESTE = sementes.derivar(BASE, len(SEMENTES_TREINO))


def treinar(motor, rng):
    P = len(motor.theta)
    est = ([0.0] * P, [0.0] * P)
    g = W.Caixa(L_TREINO)
    for it in range(1, ITERS + 1):
        lote = []
        for _ in range(16):
            x0, a0 = rng.randrange(L_TREINO), rng.randrange(4)
            z0 = [0.0] * len(g)
            z0[g.idx(x0, a0)] = 1.0
            ver = W.verdade(L_TREINO, x0, a0, T_TREINO)
            lote.append((g, z0, T_TREINO, {t + 1: ver[t] for t in range(T_TREINO)}))
        _, gr = B.bptt(motor, lote)
        B._adam(motor, gr, est, it, 0.03)


def ingenuo(L, x0, a0, T, rebote):
    x, a = x0, a0
    out = []
    for _ in range(T):
        if rebote == "PERSISTENCIA":
            pass
        else:
            x = min(L - 1, max(0, x + W.VELS[a]))
        out.append(W.Caixa.idx(x, a))
    return out


def uma(arg):
    i, seed = arg
    t0 = time.time()
    rng = random.Random(seed)
    m = W.MotorMundo(8, rng)
    treinar(m, rng)
    s = W.MotorSemParede(8, random.Random(seed + 1))
    treinar(s, random.Random(seed + 2))
    trng = random.Random(SEM_TESTE[i])
    r = {"seed": seed}
    for L in LS:
        err = {b: 0 for b in ("MUNDO", "SEM_PAREDE", "PERSISTENCIA", "SEM_REBOTE")}
        traj_ok = {b: 0 for b in err}
        for _ in range(N_EX):
            x0, a0 = trng.randrange(L), trng.randrange(4)
            ver = W.verdade(L, x0, a0, T_TESTE)
            prev = {"MUNDO": W.rollout(m, L, x0, a0, T_TESTE), "SEM_PAREDE": W.rollout(s, L, x0, a0, T_TESTE),
                    "PERSISTENCIA": ingenuo(L, x0, a0, T_TESTE, "PERSISTENCIA"),
                    "SEM_REBOTE": ingenuo(L, x0, a0, T_TESTE, "SEM_REBOTE")}
            for b, p in prev.items():
                e = sum(1 for u, w in zip(p, ver) if u != w)
                err[b] += e
                traj_ok[b] += e == 0
        for b in err:
            r[f"{b}|{L}|erro_passo"] = err[b] / (N_EX * T_TESTE)
            r[f"{b}|{L}|traj_ok"] = traj_ok[b] / N_EX
    r["cpu_s"] = time.time() - t0
    print(f"semente {seed} ok ({r['cpu_s']:.0f}s)", flush=True)
    return r


def main():
    procs = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--procs=")), 4))
    with Pool(procs) as pool:
        res = pool.map(uma, list(enumerate(SEMENTES_TREINO)))
    n = len(res)
    col = lambda k: [r[k] for r in res]  # noqa: E731
    L_ = [f"# E011 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
          f"{n} sementes x {N_EX} trajetorias de {T_TESTE} passos; treino L={L_TREINO}; base das sementes de teste = {BASE[:12]}", "",
          "| braço | L | erro por passo, IQM [IC95%] | trajetórias 100% certas, IQM | colapsos (traj < 0,5) |", "|---|---|---|---|---|"]
    for b in ("MUNDO", "SEM_PAREDE", "PERSISTENCIA", "SEM_REBOTE"):
        for L in LS:
            e = col(f"{b}|{L}|erro_passo")
            t = col(f"{b}|{L}|traj_ok")
            lo, hi = estat.bootstrap_ic(e, estat.iqm)
            L_.append(f"| {b} | {L} | {estat.iqm(e):.4f} [{lo:.4f},{hi:.4f}] | {estat.iqm(t):.2f} | {sum(x < 0.5 for x in t)}/{n} |")
    Lm = LS[-1]
    a, b_ = col(f"MUNDO|{Lm}|erro_passo"), col(f"SEM_PAREDE|{Lm}|erro_passo")
    L_ += ["", "## Checagem das previsões", "",
           "- P1 MUNDO erro por passo < 0,01 em todo L: "
           + str(all(estat.iqm(col(f"MUNDO|{L}|erro_passo")) < 0.01 for L in LS))
           + " (" + ", ".join(f"L={L}: {estat.iqm(col(f'MUNDO|{L}|erro_passo')):.4f}" for L in LS) + ")",
           f"- P2 MUNDO trajetórias 100% certas em L={Lm}: IQM {estat.iqm(col(f'MUNDO|{Lm}|traj_ok')):.2f} (previsto >= 0,95)",
           f"- P3 SEM_PAREDE erro por passo em L={Lm}: IQM {estat.iqm(b_):.4f} (previsto > 0,05); "
           f"P(MUNDO melhor) = {estat.prob_melhoria([-x for x in a], [-x for x in b_]):.2f}, p = {estat.teste_permutacao(a, b_):.4f}",
           f"- P4 SEM_REBOTE erro por passo em L=8: IQM {estat.iqm(col('SEM_REBOTE|8|erro_passo')):.4f} (previsto > 0,30)",
           f"- CPU total: {sum(col('cpu_s')):.0f}s"]
    txt = "\n".join(L_)
    print(txt)
    nome = "resultados_smoke" if QUICK else "resultados"
    with open(os.path.join(AQUI, nome + ".md"), "w") as fh:
        fh.write(txt + "\n")
    with open(os.path.join(AQUI, nome + ".json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
