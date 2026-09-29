"""
E001 - reavaliacao com a regua do laboratorio (lab/estat.py).

Controles adicionados em relacao a primeira rodada:
  C1  S1-estruturado: o MESMO passo latente, mas so 1 passada. Separa
      "ganho da iteracao" de "ganho dos atributos de aresta".
  C2  Overthinking: pensar 200 passos (muito alem do necessario) destroi a resposta?
  C3  Qualidade da abstencao (E-AURC) do S1-MLP vs do estado latente.
  C4  10 sementes, IQM + IC95% bootstrap, prob. de melhoria, teste de permutacao.

Uso:  python3 experimentos/E001_mlu/reavaliar.py [--sementes=10] [--procs=4]
"""
import json
import os
import random
import sys
from multiprocessing import Pool

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", ".."))

import mlu  # noqa: E402
from lab import estat  # noqa: E402

N = mlu.N_TRAIN
DEPTHS = list(range(0, 10))
EXTRAP_D = [8, 16, 32, 64]           # saltos; treino viu no maximo 4


def uma_semente(seed):
    rng = random.Random(seed)
    train = mlu.dataset(N, mlu.TRAIN_DEPTHS, 20000, rng)
    s1 = mlu.S1MLP(N, 48, rng)
    s1.train(train, epochs=4, lr=0.02, rng=rng)
    s2 = mlu.S2Step(4, rng)
    s2.train(train, iters=600, rng=rng)

    trng = random.Random(10_000 + seed)
    teste = [(d, mlu.make_example(N, d, trng)) for d in DEPTHS for _ in range(200)]

    r = {}
    ok = {"s1_mlp": 0, "s1_estr": 0, "s2s3": 0, "mlu": 0, "overthink200": 0}
    fl = {"s2fixo": 0, "s2s3": 0}
    conf_mlp, ok_mlp, conf_lat, ok_lat = [], [], [], []
    for d, (p, s, root) in teste:
        c, cf = s1.predict(p, s)
        ok["s1_mlp"] += c == root
        conf_mlp.append(cf)
        ok_mlp.append(c == root)
        ok["s1_estr"] += s2.run_fixed(p, s, 1)[0] == root
        pred, t = s2.run_meta(p, s, mlu.T_MAX)
        ok["s2s3"] += pred == root
        fl["s2s3"] += t * N * N
        fl["s2fixo"] += mlu.T_MAX * N * N
        ok["mlu"] += (c if cf >= 0.9 else pred) == root
        z = s2.trajectory(p, s, 200)[-1]
        k = max(range(N), key=lambda i: z[i])
        ok["overthink200"] += k == root
        # confianca do latente com orcamento curto (T=4): forca casos incertos
        zc = s2.trajectory(p, s, 4)[-1]
        kc = max(range(N), key=lambda i: zc[i])
        conf_lat.append(zc[kc])
        ok_lat.append(kc == root)
    n = len(teste)
    for k_, v in ok.items():
        r["acc_" + k_] = v / n
    r["economia_s3"] = 1 - fl["s2s3"] / fl["s2fixo"]
    r["eaurc_s1_mlp"] = estat.e_aurc(conf_mlp, ok_mlp)
    r["eaurc_latente_T4"] = estat.e_aurc(conf_lat, ok_lat)
    r["ece_s1_mlp"] = estat.ece(conf_mlp, ok_mlp)

    xrng = random.Random(20_000 + seed)
    for d in EXTRAP_D:
        Nb = d + mlu.EXTRA_ROOTS + 3
        exs = [mlu.make_example(Nb, d, xrng) for _ in range(12)]
        r[f"cont_d{d}"] = sum(s2.run_meta(p, s, d + 8)[0] == rt for p, s, rt in exs) / 12
        r[f"crist_d{d}"] = sum(s2.run_meta(p, s, d + 8, crystallize=True)[0] == rt
                               for p, s, rt in exs) / 12
    print(f"semente {seed} ok", flush=True)
    return r


def main():
    ns = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--sementes=")), 10))
    procs = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--procs=")), 4))
    import contextlib
    import io
    with Pool(procs) as pool:
        # silencia os logs de treino de cada processo
        with contextlib.redirect_stdout(io.StringIO()):
            pass
        res = pool.map(uma_semente, range(100, 100 + ns))

    chaves = list(res[0])
    col = {k: [r[k] for r in res] for k in chaves}
    linhas = ["| metrica | IQM | IC95% | min | max | colapsos (<0.5) |", "|---|---|---|---|---|---|"]
    for k in chaves:
        lo, hi = estat.bootstrap_ic(col[k], estat.iqm)
        colapso = f"{estat.taxa_colapso(col[k]):.0%}" if k.startswith(("acc", "cont", "crist")) else "-"
        linhas.append(f"| {k} | {estat.iqm(col[k]):.3f} | [{lo:.3f}, {hi:.3f}] "
                      f"| {min(col[k]):.3f} | {max(col[k]):.3f} | {colapso} |")

    comp = []
    for a, b in (("acc_s2s3", "acc_mlu"), ("acc_s2s3", "acc_s1_estr"), ("acc_s2s3", "acc_s1_mlp"),
                 ("crist_d64", "cont_d64"), ("eaurc_s1_mlp", "eaurc_latente_T4")):
        comp.append(f"| {a} vs {b} | {estat.prob_melhoria(col[a], col[b]):.2f} "
                    f"| {estat.teste_permutacao(col[a], col[b]):.4f} "
                    f"| {estat.cohen_d(col[a], col[b]):.2f} |")

    out = "\n".join(linhas) + "\n\n| comparacao | P(A>B) | p (permutacao) | d de Cohen |\n|---|---|---|---|\n" + "\n".join(comp)
    print(out)
    with open(os.path.join(AQUI, "reavaliacao.md"), "w") as fh:
        fh.write(f"# E001 - reavaliacao ({ns} sementes)\n\n" + out + "\n")
    with open(os.path.join(AQUI, "reavaliacao.json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
