"""
E015 - codigo minimo corretor (H13): quantas dimensoes por mensagem um codigo precisa
para ter a robustez do one-hot sob ruido gaussiano?

Um emissor manda um de N simbolos por L canais com ruido N(0, sigma^2) por canal;
o receptor decodifica pelo codigo mais proximo (maxima verossimilhanca).
Dois canais fisicos:
  E (energia)   ||c|| = 1 por codigo (o canal do E003: a mensagem simbolica tem a norma da analogica)
  P (amplitude) |c_d| <= 1 por canal (cada canal satura; o one-hot e o mesmo nos dois canais)
Bracos: ONEHOT (L = N), SIMPLEX (L = N-1, referencia teorica), BIORT (+-e_i, L = N/2), BIN (binario, L = log2 N),
        APREND_L (codigo aprendido por SGD atraves do canal com ruido), ALEAT_L (sorteado, ablacao do aprendizado).
Uso: python3 e015.py [--quick] [--procs=4]
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
sys.path.insert(0, RAIZ)
from lab import estat, sementes  # noqa: E402

QUICK = "--quick" in sys.argv
SEMENTES = [1590, 1591] if QUICK else list(range(1500, 1510))
NS = (16,) if QUICK else (16, 32)
SIGMAS = (0.3, 0.4)
SIG_TREINO = 0.4
N_TESTE = 2000 if QUICK else 10000
ITERS = 1000 if QUICK else 4000
SUF = "_smoke" if QUICK else ""


def dims(N):
    lg = int(round(math.log2(N)))
    return {"E": sorted({lg, N // 4, N // 2, N - 1}), "P": sorted({lg, N // 4, N // 2})}


def normal(v):
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v]


def projetar(v, canal):
    return normal(v) if canal == "E" else [max(-1.0, min(1.0, x)) for x in v]


def onehot(N):
    return [[1.0 if i == j else 0.0 for j in range(N)] for i in range(N)]


def simplex(N):
    """Vertices do simplex regular (e_i - media), normalizados: vivem num subespaco de N-1 dimensoes."""
    return [normal([(1.0 if i == j else 0.0) - 1.0 / N for j in range(N)]) for i in range(N)]


def biort(N):
    C = []
    for i in range(N // 2):
        e = [0.0] * (N // 2)
        e[i] = 1.0
        C += [e, [-x for x in e]]
    return C


def binario(N, canal):
    L = int(round(math.log2(N)))
    a = 1.0 / math.sqrt(L) if canal == "E" else 1.0
    return [[a if (i >> b) & 1 else -a for b in range(L)] for i in range(N)]


def aleat(N, L, canal, rng):
    if canal == "E":
        return [normal([rng.gauss(0, 1) for _ in range(L)]) for _ in range(N)]
    return [[rng.uniform(-1, 1) for _ in range(L)] for _ in range(N)]


def treinar(N, L, canal, rng, iters=ITERS, lote=32, lr=0.05, sig=SIG_TREINO):
    """SGD na entropia cruzada do decodificador ML (logit_i = -||r - c_i||^2 / (2 sig^2))."""
    C = aleat(N, L, canal, rng)
    b = 1.0 / sig ** 2
    for _ in range(iters):
        G = [[0.0] * L for _ in range(N)]
        for _ in range(lote):
            s = rng.randrange(N)
            r = [c + rng.gauss(0, sig) for c in C[s]]
            lg = [-0.5 * b * sum((x - y) ** 2 for x, y in zip(r, c)) for c in C]
            m = max(lg)
            e = [math.exp(x - m) for x in lg]
            t = sum(e)
            for i in range(N):
                g = e[i] / t - (1.0 if i == s else 0.0)
                if abs(g) < 1e-9:
                    continue
                Ci, Gi, Gs = C[i], G[i], G[s]
                for d in range(L):
                    u = g * b * (r[d] - Ci[d])
                    Gi[d] += u          # dPerda/dc_i = g * dl_i/dc_i = g * b (r - c_i)
                    Gs[d] -= u          # via r = c_s + ruido: dl_i/dr = -b (r - c_i)
        C = [projetar([c - lr * g / lote for c, g in zip(C[i], G[i])], canal) for i in range(N)]
    return C


def erro(C, sig, rng, n=N_TESTE):
    N = len(C)
    nn = [sum(x * x for x in c) for c in C]
    err = 0
    for _ in range(n):
        s = rng.randrange(N)
        r = [c + rng.gauss(0, sig) for c in C[s]]
        # argmin ||r - c||^2 = argmax (2 r.c - ||c||^2)
        k = max(range(N), key=lambda i: 2 * sum(a * b for a, b in zip(C[i], r)) - nn[i])
        err += k != s
    return err / n


def uma(arg):
    seed, sem_teste = arg
    t0 = time.time()
    rng = random.Random(seed)
    trng = random.Random(sem_teste)
    r = {"seed": seed}
    for N in NS:
        cods = {"ONEHOT": onehot(N), "SIMPLEX": simplex(N), "BIORT": biort(N), "BIN_E": binario(N, "E"), "BIN_P": binario(N, "P")}
        for canal, Ls in dims(N).items():
            for L in Ls:
                cods[f"APREND_{canal}_{L}"] = treinar(N, L, canal, rng)
                cods[f"ALEAT_{canal}_{L}"] = aleat(N, L, canal, rng)
        for nome, C in cods.items():
            for sig in SIGMAS:
                r[f"{N}|{nome}|{sig}"] = erro(C, sig, trng)
    r["cpu_s"] = time.time() - t0
    print(f"semente {seed} ok ({r['cpu_s']:.0f}s)", flush=True)
    return r


def main():
    procs = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--procs=")), 4)
    teste = [1690, 1691] if QUICK else sementes.derivar(sementes.base_teste(__file__), len(SEMENTES))
    with Pool(procs) as pool:
        res = pool.map(uma, list(zip(SEMENTES, teste)))
    json.dump(res, open(os.path.join(AQUI, f"resultados{SUF}.json"), "w"), indent=1, sort_keys=True)

    def col(c):
        return [x[c] for x in res]

    def iq(c):
        return estat.iqm(col(c))
    L = [f"# E015 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{len(SEMENTES)} sementes; {N_TESTE} simbolos de teste por (semente, codigo, sigma); treino com sigma = {SIG_TREINO}, {ITERS} iteracoes.", "",
         "| N | código | canal | L (dimensões) | erro σ=0,3 IQM [IC95%] | erro σ=0,4 IQM | razão vs ONEHOT σ=0,3 | razão σ=0,4 |",
         "|---|---|---|---|---|---|---|---|"]
    for N in NS:
        lin = [("ONEHOT", "E/P", N), ("SIMPLEX", "E", N - 1), ("BIORT", "E", N // 2), ("BIN_E", "E", int(round(math.log2(N)))), ("BIN_P", "P", int(round(math.log2(N))))]
        for canal, Ls in dims(N).items():
            for Ld in Ls:
                lin += [(f"APREND_{canal}_{Ld}", canal, Ld), (f"ALEAT_{canal}_{Ld}", canal, Ld)]
        for nome, canal, Ld in lin:
            a = col(f"{N}|{nome}|0.3")
            lo, hi = estat.bootstrap_ic(a, estat.iqm)
            L.append(f"| {N} | {nome} | {canal} | {Ld} | {estat.iqm(a):.4f} [{lo:.4f},{hi:.4f}] | {iq(f'{N}|{nome}|0.4'):.4f} | "
                     f"{estat.iqm(a) / iq(f'{N}|ONEHOT|0.3'):.2f} | {iq(f'{N}|{nome}|0.4') / iq(f'{N}|ONEHOT|0.4'):.2f} |")

    def razao(N, nome, s):
        return iq(f"{N}|{nome}|{s}") / iq(f"{N}|ONEHOT|{s}")
    L += ["", "## Checagem das previsões", ""]
    v1 = [razao(N, f"APREND_E_{N - 1}", s) for N in NS for s in SIGMAS]
    L.append(f"- P1 {'OK' if all(v < 1.0 for v in v1) else 'FALHOU'}: canal E, APREND com L = N-1 tem erro < ONEHOT (razão IQM < 1) em todo N e σ: " + ", ".join(f"{v:.2f}" for v in v1))
    v2a = [razao(N, f"APREND_E_{N // 2}", s) for N in NS for s in SIGMAS]
    v2b = [razao(N, f"APREND_E_{N // 4}", s) for N in NS for s in SIGMAS]
    ok2 = all(0.9 <= v <= 1.15 for v in v2a) and all(v > 1.2 for v in v2b)
    L.append(f"- P2 {'OK' if ok2 else 'FALHOU'}: canal E, limite de Rankin: L = N/2 empata (razão em [0,9; 1,15]): " + ", ".join(f"{v:.2f}" for v in v2a) +
             "; L = N/4 perde (razão > 1,2): " + ", ".join(f"{v:.2f}" for v in v2b))
    v3 = [razao(N, f"APREND_P_{N // 4}", s) for N in NS for s in SIGMAS]
    L.append(f"- P3 {'OK' if all(v <= 0.5 for v in v3) else 'FALHOU'}: canal P, APREND com L = N/4 tem erro <= 0,5 x ONEHOT: " + ", ".join(f"{v:.3f}" for v in v3))
    tot = ok = 0
    for N in NS:
        for canal, Ls in dims(N).items():
            for Ld in Ls:
                for s in SIGMAS:
                    ganhou = sum(a < b for a, b in zip(col(f"{N}|APREND_{canal}_{Ld}|{s}"), col(f"{N}|ALEAT_{canal}_{Ld}|{s}")))
                    tot += 1
                    ok += ganhou >= 0.9 * len(SEMENTES)
    L.append(f"- P4 {'OK' if ok == tot else 'FALHOU'}: APREND < ALEAT em >= 90% das sementes, todas as células: {ok}/{tot}")
    v5 = [(iq(f"{N}|APREND_E_{int(round(math.log2(N)))}|{s}"), iq(f"{N}|BIN_E|{s}")) for N in NS for s in SIGMAS]
    L.append(f"- P5 {'OK' if all(a < b for a, b in v5) else 'FALHOU'}: canal E, APREND com L = log2 N < BIN: " + ", ".join(f"{a:.3f} vs {b:.3f}" for a, b in v5))
    L.append(f"- CPU total: {sum(col('cpu_s')):.0f}s")
    txt = "\n".join(L)
    open(os.path.join(AQUI, f"resultados{SUF}.md"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
