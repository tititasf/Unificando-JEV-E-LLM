"""
E004 - metacognicao invariante a escala (ver PREREG.md; parametros congelados).

Uso: python3 experimentos/E004_s3_escala/e004.py [--quick] [--procs=4]
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
RAIZ = os.path.join(AQUI, "..", "..")
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E001_mlu"))
sys.path.insert(0, RAIZ)
import mlu  # noqa: E402
from lab import estat  # noqa: E402

QUICK = "--quick" in sys.argv
SEMENTES = list(range(400, 402)) if QUICK else list(range(400, 410))
NS = [12, 32] if QUICK else [12, 32, 64, 128]
N_EX = 4 if QUICK else 10
EPS = 0.02
BRACOS = ("SEMPRE", "ABS", "CONV", "ENT", "UNIF", "ESTAVEL", "ESTAVEL_PURO")


def argmax(z):
    return max(range(len(z)), key=lambda i: z[i])


def entropia_norm(z):
    return -sum(p * math.log(p) for p in z if p > 1e-15) / math.log(len(z))


def decide(traj, braco):
    """traj = [z_0, z_1, ..., z_T]. Devolve (resposta ou None, passos)."""
    T = len(traj) - 1
    if braco == "SEMPRE":
        return argmax(traj[T]), T
    N = len(traj[0])
    for t in range(1, T + 1):
        z, zp = traj[t], traj[t - 1]
        parado = sum(abs(a - b) for a, b in zip(z, zp)) < EPS
        k = argmax(z)
        est3 = t >= 3 and argmax(traj[t - 1]) == k and argmax(traj[t - 2]) == k
        if braco == "ABS":
            ok = max(z) >= 0.9 and parado
        elif braco == "CONV":
            ok = parado
        elif braco == "ENT":
            ok = entropia_norm(z) <= 0.5 and parado
        elif braco == "UNIF":
            ok = N * max(z) >= 2 and parado
        elif braco == "ESTAVEL":
            ok = est3 and parado
        elif braco == "ESTAVEL_PURO":
            ok = est3
        if ok:
            return k, t
    return None, T


def uma(seed):
    rng = random.Random(seed)
    train = mlu.dataset(mlu.N_TRAIN, mlu.TRAIN_DEPTHS, 20000, rng)
    s2 = mlu.S2Step(4, rng)
    with contextlib.redirect_stdout(io.StringIO()):
        s2.train(train, iters=200 if QUICK else 600, rng=rng)
    trng = random.Random(60000 + seed)
    # contagem[(N, braco)] = dict(dentro_ok, dentro_resp, fora_abst, resp, resp_ok, n_dentro, n_fora)
    cont = {}
    for N in NS:
        for b in BRACOS:
            cont[(N, b)] = dict(dentro_ok=0, dentro_resp=0, fora_abst=0, resp=0, resp_ok=0, n_dentro=0, n_fora=0)
        for d in (N // 2 - 2, N - 5):
            for cond in ("DENTRO", "FORA"):
                T = d + 6 if cond == "DENTRO" else max(1, d - 3)
                for _ in range(N_EX):
                    p, s, root = mlu.make_example(N, d, trng)
                    z0 = [0.0] * N
                    z0[s] = 1.0
                    traj = [z0] + s2.trajectory(p, s, T)
                    for b in BRACOS:
                        c = cont[(N, b)]
                        pred, _ = decide(traj, b)
                        if cond == "DENTRO":
                            c["n_dentro"] += 1
                            c["dentro_resp"] += pred is not None
                            c["dentro_ok"] += pred == root
                        else:
                            c["n_fora"] += 1
                            c["fora_abst"] += pred is None
                        if pred is not None:
                            c["resp"] += 1
                            c["resp_ok"] += pred == root
    out = {}
    for (N, b), c in cont.items():
        out[f"{b}|{N}"] = dict(
            cobertura=c["dentro_resp"] / c["n_dentro"],
            abstencao_fora=c["fora_abst"] / c["n_fora"],
            acc_seletiva=(c["resp_ok"] / c["resp"]) if c["resp"] else float("nan"),
            erros=c["resp"] - c["resp_ok"],
            placar=(c["dentro_ok"] + c["fora_abst"]) / (c["n_dentro"] + c["n_fora"]),
        )
    print(f"semente {seed} ok", flush=True)
    return out


def main():
    procs = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--procs=")), 4))
    with Pool(procs) as pool:
        res = pool.map(uma, SEMENTES)
    n = len(res)
    L = [f"# E004 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{n} sementes; por semente e N: {2 * N_EX} casos DENTRO e {2 * N_EX} FORA.", "",
         "| braco | N | cobertura DENTRO | abstencao FORA | acc seletiva | erros (total) | placar IQM [IC95%] |",
         "|---|---|---|---|---|---|---|"]
    for b in BRACOS:
        for N in NS:
            k = f"{b}|{N}"
            cob = estat.media([r[k]["cobertura"] for r in res])
            ab = estat.media([r[k]["abstencao_fora"] for r in res])
            accs = [r[k]["acc_seletiva"] for r in res if r[k]["acc_seletiva"] == r[k]["acc_seletiva"]]
            acc = estat.media(accs) if accs else float("nan")
            err = sum(r[k]["erros"] for r in res)
            pl = [r[k]["placar"] for r in res]
            lo, hi = estat.bootstrap_ic(pl, estat.iqm)
            L.append(f"| {b} | {N} | {cob:.3f} | {ab:.3f} | {acc:.4f} | {err} | {estat.iqm(pl):.3f} [{lo:.3f}, {hi:.3f}] |")
    Nm = NS[-1]
    a = [r[f"ESTAVEL|{Nm}"]["placar"] for r in res]
    b_ = [r[f"ABS|{Nm}"]["placar"] for r in res]
    L += ["", f"ESTAVEL vs ABS em N={Nm}: P(A>B) = {estat.prob_melhoria(a, b_):.2f}, "
          f"p permutacao = {estat.teste_permutacao(a, b_):.4f}"]
    txt = "\n".join(L)
    print(txt)
    nome = "resultados_smoke" if QUICK else "resultados"
    with open(os.path.join(AQUI, nome + ".md"), "w") as fh:
        fh.write(txt + "\n")
    with open(os.path.join(AQUI, nome + ".json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
