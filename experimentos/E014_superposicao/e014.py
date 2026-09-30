"""
E014 - varias hipoteses vivas no S2 (H10): produto contra mistura de softmaxes.

O mesmo passo treinado em T2 (permutacao, N = 12, k <= 4) e aplicado sem re-treino a
estados com varias hipoteses. Duas formas de compor o passo sobre um estado z:
  GLOBAL   z' = softmax_i( beta * sum_j z_j S[j][i] )      (o S2 atual: softmax da soma)
  MISTURA  z' = sum_j z_j softmax_i( beta * S[j][i] )      (soma de softmaxes: cadeia de Markov)
Com z one-hot as duas sao identicas; so diferem quando ha mais de uma hipotese.

Tarefas (grafos sem vies de grau de entrada):
  SUP  permutacao; o estado inicial e uma superposicao de F inicios com pesos 1..F (normalizados);
       resposta: o conjunto {pi^k(s_i)}.
  BFS  uniao de duas permutacoes (grau 2 de saida e de entrada); inicio unico;
       resposta: o conjunto de nos alcancaveis em exatamente k saltos.
Leitura: os |R| nos de maior massa sao exatamente R (recuperacao do conjunto) e a massa em R.
Bracos: GLOBAL1, GLOBAL_TEO (beta da lei, E013), GLOBAL3 (beta = 3, nitido), CRIST (argmax), MIST1, MIST_TEO,
        FEIXE_TEO (F execucoes independentes de uma hipotese, so em SUP; custo F vezes).
Uso: python3 e014.py [--quick] [--procs=4]
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
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E005_t2_salto"))
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E006_lei_margem"))
_argv = sys.argv
sys.argv = [sys.argv[0]]
import tarefa_t2 as T2  # noqa: E402
import passo_rapido as PR  # noqa: E402
sys.argv = _argv
from lab import estat, sementes  # noqa: E402

QUICK = "--quick" in sys.argv
SEMENTES = [1490, 1491] if QUICK else list(range(1400, 1410))
NS = (256, 1024) if QUICK else (256, 1024, 4096)
N_EX = 3 if QUICK else 10
N_TR = 12
CEL_SUP = [(F, k) for F in (4, 8) for k in (16, 64)]
CEL_BFS = [(0, 3), (0, 5)]
BRACOS = ("GLOBAL1", "GLOBAL_TEO", "GLOBAL3", "CRIST", "MIST1", "MIST_TEO", "FEIXE_TEO")
SUF = "_smoke" if QUICK else ""


def feat(succ, j, i):
    return (1.0 if i in succ[j] else 0.0, 1.0 if j in succ[i] else 0.0, 1.0 if i == j else 0.0, 0.0, 0.0, 1.0)


class Grafo:
    """Pares estruturados (j -> i, delta = V(feat) - V(generico)); o resto recebe o termo generico."""

    def __init__(self, succ, V):
        N = len(succ)
        self.N = N
        pred = [[] for _ in range(N)]
        for j in range(N):
            for i in succ[j]:
                pred[i].append(j)
        cache = {}

        def v(f):
            if f not in cache:
                cache[f] = V(f)
            return cache[f]
        g = v((0.0, 0.0, 0.0, 0.0, 0.0, 1.0))
        self.saida = []   # por j: [(i, delta)]
        for j in range(N):
            alvos = set(succ[j]) | set(pred[j]) | {j}
            self.saida.append([(i, v(feat(succ, j, i)) - g) for i in alvos])
        self.entrada = [[] for _ in range(N)]  # por i: [(j, delta)]
        for j in range(N):
            for i, d in self.saida[j]:
                self.entrada[i].append((j, d))
        self._mist = {}

    def global_(self, z, beta, crist=False):
        lg = [beta * sum(z[j] * d for j, d in self.entrada[i]) for i in range(self.N)]
        if crist:
            k = max(range(self.N), key=lambda i: lg[i])
            o = [0.0] * self.N
            o[k] = 1.0
            return o
        m = max(lg)
        e = [math.exp(x - m) for x in lg]
        t = sum(e)
        return [x / t for x in e]

    def linhas(self, beta):
        if beta not in self._mist:
            L = []
            for j in range(self.N):
                ex = [(i, math.exp(beta * d)) for i, d in self.saida[j]]
                Z = (self.N - len(ex)) + sum(x for _, x in ex)
                L.append((1.0 / Z, [(i, (x - 1.0) / Z) for i, x in ex]))
            self._mist[beta] = L
        return self._mist[beta]

    def mistura(self, z, beta):
        L = self.linhas(beta)
        out = [0.0] * self.N
        gen = 0.0
        for j in range(self.N):
            zj = z[j]
            if zj:
                g0, cs = L[j]
                gen += zj * g0
                for i, c in cs:
                    out[i] += zj * c
        return [x + gen for x in out]

    def vaz_mist(self, j, beta):
        """Vazamento de um passo da MISTURA a partir de j one-hot (massa fora de succ[j])."""
        g0, cs = self.linhas(beta)[j]
        return self.N, g0, cs


def treinar(seed):
    rng = random.Random(seed + 1000)
    s2 = T2.novo_s2(rng)
    T2.treinar(s2, T2.dados(N_TR, range(1, 5), 20000, rng), iters=600, rng=rng)
    return PR.tabela(s2)


def margem(V):
    """Margem efetiva sem rotulos (como no E013): inverte o vazamento medio de um passo em N = 30."""
    r = random.Random(1)
    eps, n = 0.0, 0
    for _ in range(5):
        pi = list(range(30))
        r.shuffle(pi)
        G = Grafo([[pi[i]] for i in range(30)], V)
        for j in r.sample(range(30), 6):
            z = [0.0] * 30
            z[j] = 1.0
            eps += 1.0 - G.global_(z, 1.0)[pi[j]]
            n += 1
    eps /= n
    return -math.log(eps / ((1 - eps) * 29))


def beta_teo(N, m):
    return 1.0 + math.log((N - 1) / (N_TR - 1)) / m


def gerar(tarefa, N, F, k, rng):
    if tarefa == "SUP":
        pi = list(range(N))
        rng.shuffle(pi)
        succ = [[pi[i]] for i in range(N)]
        ini = rng.sample(range(N), F)
        t = F * (F + 1) / 2
        z0 = {s: (q + 1) / t for q, s in enumerate(ini)}
        alvo = set()
        for s in ini:
            for _ in range(k):
                s = pi[s]
            alvo.add(s)
        return succ, z0, alvo
    p1, p2 = list(range(N)), list(range(N))
    rng.shuffle(p1)
    rng.shuffle(p2)
    succ = [sorted({p1[i], p2[i]}) for i in range(N)]
    s = rng.randrange(N)
    fr = {s}
    for _ in range(k):
        fr = {i for j in fr for i in succ[j]}
    return succ, {s: 1.0}, fr


def pensar(G, z0, k, braco, bt):
    def ini(d):
        z = [0.0] * G.N
        for s, w in d.items():
            z[s] = w
        return z
    if braco == "FEIXE_TEO":
        tot = [0.0] * G.N
        for s, w in z0.items():
            z = ini({s: 1.0})
            for _ in range(k):
                z = G.global_(z, bt)
            tot = [a + w * b for a, b in zip(tot, z)]
        return tot
    z = ini(z0)
    for _ in range(k):
        if braco == "GLOBAL1":
            z = G.global_(z, 1.0)
        elif braco == "GLOBAL_TEO":
            z = G.global_(z, bt)
        elif braco == "GLOBAL3":
            z = G.global_(z, 3.0)
        elif braco == "CRIST":
            z = G.global_(z, 1.0, crist=True)
        elif braco == "MIST1":
            z = G.mistura(z, 1.0)
        else:
            z = G.mistura(z, bt)
    return z


def uma(arg):
    seed, sem_teste = arg
    t0 = time.time()
    V = treinar(seed)
    m = margem(V)
    r = {"seed": seed, "m": m}
    rng = random.Random(sem_teste)
    for N in NS:
        bt = beta_teo(N, m)
        for tarefa, celulas in (("SUP", CEL_SUP), ("BFS", CEL_BFS)):
            for F, k in celulas:
                ch = f"{tarefa}|{N}|{F}|{k}"
                ac = {b: 0 for b in BRACOS}
                ms = {b: 0.0 for b in BRACOS}
                vv = {b: 0.0 for b in BRACOS}
                prev = 0.0
                for _ in range(N_EX):
                    succ, z0, alvo = gerar(tarefa, N, F, k, rng)
                    G = Grafo(succ, V)
                    # previsao da lei da mistura (so SUP): massa em R = (1 - eps1)^k, eps1 medido num passo
                    if tarefa == "SUP":
                        e1 = []
                        for s in z0:
                            _, g0, cs = G.vaz_mist(s, 1.0)
                            c = dict(cs)
                            e1.append(1.0 - (g0 + c.get(succ[s][0], 0.0)))
                        prev += (1.0 - sum(e1) / len(e1)) ** k
                    for b in BRACOS:
                        if b == "FEIXE_TEO" and tarefa == "BFS":
                            continue
                        z = pensar(G, z0, k, b, bt)
                        top = set(sorted(range(N), key=lambda i: -z[i])[:len(alvo)])
                        ac[b] += top == alvo
                        ms[b] += sum(z[i] for i in alvo)
                        vv[b] += len(top & alvo) / len(alvo)
                r[ch + "|beta_teo"] = bt
                r[ch + "|prev_mist1"] = prev / N_EX
                for b in BRACOS:
                    if b == "FEIXE_TEO" and tarefa == "BFS":
                        continue
                    r[f"{ch}|{b}|acc"] = ac[b] / N_EX
                    r[f"{ch}|{b}|massa"] = ms[b] / N_EX
                    r[f"{ch}|{b}|vivas"] = vv[b] / N_EX
    r["cpu_s"] = time.time() - t0
    print(f"semente {seed} ok ({r['cpu_s']:.0f}s)", flush=True)
    return r


def main():
    procs = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--procs=")), 4)
    teste = [1590, 1591] if QUICK else sementes.derivar(sementes.base_teste(__file__), len(SEMENTES))
    with Pool(procs) as pool:
        res = pool.map(uma, list(zip(SEMENTES, teste)))
    json.dump(res, open(os.path.join(AQUI, f"resultados{SUF}.json"), "w"), indent=1, sort_keys=True)

    def col(c):
        return [x[c] for x in res]
    cels = [("SUP", N, F, k) for N in NS for F, k in CEL_SUP] + [("BFS", N, F, k) for N in NS for F, k in CEL_BFS]
    L = [f"# E014 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{len(SEMENTES)} sementes x {N_EX} instancias por celula; passo treinado em T2 (N = {N_TR}), aplicado sem re-treino.",
         f"Margens efetivas: {min(col('m')):.2f}-{max(col('m')):.2f}", "",
         "| tarefa | N | F | k | braço | recuperação IQM [IC95%] | colapsos (< 0,5) | massa em R (IQM) | fração de R viva (IQM) |",
         "|---|---|---|---|---|---|---|---|---|"]
    for t, N, F, k in cels:
        ch = f"{t}|{N}|{F}|{k}"
        for b in BRACOS:
            if b == "FEIXE_TEO" and t == "BFS":
                continue
            a = col(f"{ch}|{b}|acc")
            lo, hi = estat.bootstrap_ic(a, estat.iqm)
            L.append(f"| {t} | {N} | {F or '-'} | {k} | {b} | {estat.iqm(a):.2f} [{lo:.2f},{hi:.2f}] | "
                     f"{sum(v < 0.5 for v in a)}/{len(a)} | {estat.iqm(col(f'{ch}|{b}|massa')):.3f} | {estat.iqm(col(f'{ch}|{b}|vivas')):.2f} |")
    L += ["", "## Checagem das previsões", ""]
    sup = [c for c in cels if c[0] == "SUP"]
    tudo = cels

    def ch(c):
        return f"{c[0]}|{c[1]}|{c[2]}|{c[3]}"
    ok1 = all(estat.iqm(col(f"{ch(c)}|{b}|acc")) <= 0.10 for c in sup for b in ("GLOBAL1", "GLOBAL_TEO"))
    L.append(f"- P1 {'OK' if ok1 else 'FALHOU'}: GLOBAL (beta 1 e TEORIA) em SUP, recuperação IQM <= 0,10 em todas as células: max " +
             f"{max(estat.iqm(col(f'{ch(c)}|{b}|acc')) for c in sup for b in ('GLOBAL1', 'GLOBAL_TEO')):.2f}")
    ok2 = all(estat.iqm(col(f"{ch(c)}|MIST_TEO|acc")) >= 0.95 and min(col(f"{ch(c)}|MIST_TEO|acc")) >= 0.5 for c in tudo)
    L.append(f"- P2 {'OK' if ok2 else 'FALHOU'}: MIST_TEO recuperação IQM >= 0,95 e 0 colapsos em todas as células (SUP e BFS): min IQM " +
             f"{min(estat.iqm(col(f'{ch(c)}|MIST_TEO|acc')) for c in tudo):.2f}, pior semente {min(min(col(f'{ch(c)}|MIST_TEO|acc')) for c in tudo):.2f}")
    ok3 = all(estat.iqm(col(f"{ch(c)}|CRIST|acc")) <= 0.05 for c in tudo)
    L.append(f"- P3 {'OK' if ok3 else 'FALHOU'}: CRIST recuperação IQM <= 0,05 em todas as células: max {max(estat.iqm(col(f'{ch(c)}|CRIST|acc')) for c in tudo):.2f}")
    dentro = tot = 0
    for c in sup:
        for x, y in zip(col(f"{ch(c)}|MIST1|massa"), col(f"{ch(c)}|prev_mist1")):
            tot += 1
            dentro += abs(x - y) <= 0.05
    L.append(f"- P4 {'OK' if dentro >= 0.9 * tot else 'FALHOU'}: MIST1 em SUP, massa em R dentro de ±0,05 de (1-eps1)^k: {dentro}/{tot}")
    bfs5 = [c for c in cels if c[0] == "BFS" and c[3] == 5]
    d5 = [estat.iqm(col(f"{ch(c)}|MIST_TEO|massa")) - estat.iqm(col(f"{ch(c)}|GLOBAL_TEO|massa")) for c in bfs5]
    L.append(f"- P5 {'OK' if all(d >= 0.5 for d in d5) else 'FALHOU'}: BFS k=5, massa em R MIST_TEO - GLOBAL_TEO >= 0,5 em todo N: " +
             ", ".join(f"{d:.2f}" for d in d5))
    ok6 = all(estat.iqm(col(f"{ch(c)}|FEIXE_TEO|acc")) >= 0.95 for c in sup)
    L.append(f"- P6 {'OK' if ok6 else 'FALHOU'}: FEIXE_TEO (F execuções) recuperação IQM >= 0,95 em SUP: min {min(estat.iqm(col(f'{ch(c)}|FEIXE_TEO|acc')) for c in sup):.2f}")
    v7 = [(estat.iqm(col(f"{ch(c)}|GLOBAL3|acc")), estat.iqm(col(f"{ch(c)}|GLOBAL3|massa")), estat.iqm(col(f"{ch(c)}|GLOBAL3|vivas")), c[2]) for c in sup]
    ok7 = all(a <= 0.10 and m >= 0.9 and v <= 1.0 / F + 0.1 for a, m, v, F in v7)
    L.append(f"- P7 {'OK' if ok7 else 'FALHOU'}: GLOBAL3 em SUP = vencedor leva tudo (recuperação <= 0,10, massa em R >= 0,9, fração viva <= 1/F + 0,1): " +
             "; ".join(f"acc {a:.2f} massa {m:.2f} viva {v:.2f}" for a, m, v, F in v7))
    L.append(f"- CPU total: {sum(col('cpu_s')):.0f}s")
    txt = "\n".join(L)
    open(os.path.join(AQUI, f"resultados{SUF}.md"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
