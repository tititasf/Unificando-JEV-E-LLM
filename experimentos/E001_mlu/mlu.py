"""
MLU - Motor Latente Unificado (micro-escala, Python puro, sem dependencias)

Pergunta testada:
  Unir "Sistema 1" (resposta em uma passada) + "Sistema 2" (pensar iterando
  num estado latente, sem gerar texto) + "Sistema 3" (metacognicao: decidir
  quando parar e quando admitir que nao sabe) da resultados melhores que cada
  um isolado?

Tarefa: "achar a raiz". Recebe um grafo de ponteiros (cada no aponta para o
pai; raizes apontam para si mesmas) e um no inicial. A resposta e a raiz.
A dificuldade e controlada pela profundidade d (numero de saltos necessarios).
  - d pequeno: da para "intuir" (Sistema 1)
  - d grande: precisa encadear passos (Sistema 2)

Modelos comparados:
  S1-MLP   : classificador de uma passada (estilo "modelo de decisao tipada")
  S2-fixo  : passo latente aprendido, iterado sempre T_MAX vezes
  S2+S3    : o mesmo passo, mas a metacognicao para quando o estado converge
             e se abstem se nao convergir (sabe que nao sabe)
  MLU      : roteador S1 -> se confiante responde; senao aciona S2+S3
"""
import math
import random
import sys
import time
import json

SEED = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--seed=")), 7))
N_TRAIN = 12         # nos no treino
EXTRA_ROOTS = 2      # raizes distratoras garantidas
TRAIN_DEPTHS = range(0, 5)   # treina so com profundidade 0..4
T_MAX = 12           # orcamento maximo de "pensamento" latente


# ----------------------------------------------------------------- dados
def make_example(N, depth, rng):
    """Floresta aleatoria com um caminho garantido de comprimento `depth`."""
    nodes = list(range(N))
    rng.shuffle(nodes)
    parent = [None] * N
    path = nodes[: depth + 1]          # path[0] = raiz
    parent[path[0]] = path[0]
    for i in range(1, depth + 1):
        parent[path[i]] = path[i - 1]
    placed = list(path)
    rest = nodes[depth + 1:]
    assert len(rest) >= EXTRA_ROOTS, "sem espaco para raizes distratoras"
    for n_, v in enumerate(rest):
        # sempre ha outras raizes: "a raiz e o no que aponta para si" nao basta
        if n_ < EXTRA_ROOTS or rng.random() < 0.1:
            parent[v] = v
        else:
            parent[v] = rng.choice(placed)   # distratores tambem ficam profundos
        placed.append(v)
    return parent, path[depth], path[0]


def dataset(N, depths, n, rng):
    depths = list(depths)
    return [(*make_example(N, rng.choice(depths), rng),) for _ in range(n)]


def true_depth(parent, s):
    d = 0
    while parent[s] != s:
        s = parent[s]
        d += 1
    return d


def softmax(xs):
    m = max(xs)
    e = [math.exp(x - m) for x in xs]
    z = sum(e)
    return [v / z for v in e]


# ------------------------------------------------ Sistema 1: MLP 1 passada
class S1MLP:
    """Entrada: matriz de ponteiros achatada + one-hot do inicio. Tamanho fixo."""

    def __init__(self, N, H, rng):
        self.N, self.H = N, H
        D = N * N + N
        self.D = D
        sc1, sc2 = 1 / math.sqrt(D), 1 / math.sqrt(H)
        self.W1 = [[rng.gauss(0, sc1) for _ in range(D)] for _ in range(H)]
        self.b1 = [0.0] * H
        self.W2 = [[rng.gauss(0, sc2) for _ in range(H)] for _ in range(N)]
        self.b2 = [0.0] * N

    def encode(self, parent, s):
        # entrada esparsa: indices ativos
        N = self.N
        return [j * N + parent[j] for j in range(N)] + [N * N + s]

    def forward(self, idx):
        h = []
        for k in range(self.H):
            row = self.W1[k]
            a = self.b1[k] + sum(row[i] for i in idx)
            h.append(a if a > 0 else 0.0)
        logits = [self.b2[c] + sum(w * x for w, x in zip(self.W2[c], h)) for c in range(self.N)]
        return h, softmax(logits)

    def train(self, data, epochs, lr, rng):
        for ep in range(epochs):
            rng.shuffle(data)
            loss = 0.0
            for parent, s, root in data:
                idx = self.encode(parent, s)
                h, p = self.forward(idx)
                loss -= math.log(p[root] + 1e-12)
                g = list(p)
                g[root] -= 1.0
                gh = [0.0] * self.H
                for c in range(self.N):
                    gc = g[c]
                    if gc == 0.0:
                        continue
                    W2c = self.W2[c]
                    for k in range(self.H):
                        gh[k] += gc * W2c[k]
                        W2c[k] -= lr * gc * h[k]
                    self.b2[c] -= lr * gc
                for k in range(self.H):
                    if h[k] <= 0.0:
                        continue
                    gk = lr * gh[k]
                    row = self.W1[k]
                    for i in idx:
                        row[i] -= gk
                    self.b1[k] -= gk
            print(f"  [S1-MLP] epoca {ep + 1}: loss {loss / len(data):.3f}", flush=True)

    def predict(self, parent, s):
        _, p = self.forward(self.encode(parent, s))
        c = max(range(self.N), key=lambda i: p[i])
        return c, p[c]

    def flops(self):
        return self.H * (self.N + 1) + self.H * self.N  # entrada esparsa


# -------------------------------------- Sistema 2: passo latente aprendido
class S2Step:
    """
    Estado latente z = distribuicao sobre os nos (nao e texto, nao e token).
    Um pequeno MLP le atributos de cada par (j -> i) do grafo e produz uma
    "afinidade" S[j][i]. Um passo de pensamento e:
          z'_i = softmax_i( sum_j z_j * S[j][i] )
    Os mesmos pesos sao reusados a cada passo (recorrencia com pesos
    compartilhados), entao o modelo serve para qualquer N e qualquer numero de
    passos. Nada sobre "seguir o pai" esta codificado: tem que ser aprendido.
    """
    F = 6   # atributos por par

    def __init__(self, H, rng):
        self.H = H
        self.theta = [rng.gauss(0, 0.5) for _ in range(self.n_params())]

    def n_params(self):
        return self.H * self.F + self.H + self.H + 1

    @staticmethod
    def feat(parent, j, i):
        return (1.0 if parent[j] == i else 0.0,   # i e o pai de j
                1.0 if parent[i] == j else 0.0,   # j e o pai de i
                1.0 if i == j else 0.0,           # mesmo no
                1.0 if parent[j] == j else 0.0,   # j e raiz
                1.0 if parent[i] == i else 0.0,   # i e raiz
                1.0)

    def affinity(self, parent, theta=None):
        th = self.theta if theta is None else theta
        H, F = self.H, self.F
        W1 = th[: H * F]
        b1 = th[H * F: H * F + H]
        w2 = th[H * F + H: H * F + 2 * H]
        b2 = th[-1]
        N = len(parent)
        # so existem poucos padroes distintos de atributos -> cache
        cache = {}
        S = []
        for j in range(N):
            row = []
            for i in range(N):
                f = self.feat(parent, j, i)
                v = cache.get(f)
                if v is None:
                    v = b2
                    for k in range(H):
                        a = b1[k] + sum(W1[k * F + q] * f[q] for q in range(F))
                        v += w2[k] * math.tanh(a)
                    cache[f] = v
                row.append(v)
            S.append(row)
        return S

    @staticmethod
    def step(z, S):
        N = len(z)
        logits = [sum(z[j] * S[j][i] for j in range(N) if z[j] > 1e-9) for i in range(N)]
        return softmax(logits)

    def trajectory(self, parent, s, T, theta=None):
        S = self.affinity(parent, theta)
        N = len(parent)
        z = [0.0] * N
        z[s] = 1.0
        out = []
        for _ in range(T):
            z = self.step(z, S)
            out.append(z)
        return out

    def loss_and_grad(self, batch, supervise=(5, 6, 7, 8)):
        """
        Backprop exato atraves do tempo (BPTT) no laco latente.
        Perda em varios instantes -> incentiva a resposta a virar ponto fixo,
        o que e o que permite ao Sistema 3 detectar "terminei de pensar".
        """
        H, F = self.H, self.F
        th = self.theta
        W1, b1 = th[: H * F], th[H * F: H * F + H]
        w2 = th[H * F + H: H * F + 2 * H]
        grad = [0.0] * len(th)
        Tm = max(supervise)
        w = 1.0 / (len(batch) * len(supervise))
        L = 0.0
        for parent, s, root in batch:
            N = len(parent)
            S = self.affinity(parent)
            zs = [[0.0] * N]
            zs[0][s] = 1.0
            for _ in range(Tm):
                zs.append(self.step(zs[-1], S))
            gS = [[0.0] * N for _ in range(N)]
            gz_next = [0.0] * N          # dL/dz^t vindo do passo t+1
            for t in range(Tm, 0, -1):
                z = zs[t]
                gz = list(gz_next)
                if t in supervise:
                    L -= w * math.log(z[root] + 1e-12)
                    gz[root] -= w / (z[root] + 1e-12)
                dot = sum(a * b for a, b in zip(z, gz))
                gl = [z[i] * (gz[i] - dot) for i in range(N)]
                zp = zs[t - 1]
                gz_next = [0.0] * N
                for j in range(N):
                    if zp[j] == 0.0:
                        continue
                    Sj, gSj = S[j], gS[j]
                    acc = 0.0
                    for i in range(N):
                        gSj[i] += zp[j] * gl[i]
                        acc += gl[i] * Sj[i]
                    gz_next[j] = acc
            # gS -> padroes de atributos -> pesos do MLP de arestas
            gV = {}
            for j in range(N):
                for i in range(N):
                    f = self.feat(parent, j, i)
                    gV[f] = gV.get(f, 0.0) + gS[j][i]
            for f, gv in gV.items():
                grad[-1] += gv
                for k in range(H):
                    a = b1[k] + sum(W1[k * F + q] * f[q] for q in range(F))
                    ta = math.tanh(a)
                    grad[H * F + H + k] += gv * ta
                    ga = gv * w2[k] * (1 - ta * ta)
                    grad[H * F + k] += ga
                    for q in range(F):
                        grad[k * F + q] += ga * f[q]
        return L, grad

    def train(self, data, iters, rng, batch=32, lr=0.03):
        P = len(self.theta)
        m = [0.0] * P
        v = [0.0] * P
        for it in range(1, iters + 1):
            b = [data[rng.randrange(len(data))] for _ in range(batch)]
            L, g = self.loss_and_grad(b)
            for q in range(P):
                m[q] = 0.9 * m[q] + 0.1 * g[q]
                v[q] = 0.999 * v[q] + 0.001 * g[q] * g[q]
                mh = m[q] / (1 - 0.9 ** it)
                vh = v[q] / (1 - 0.999 ** it)
                self.theta[q] -= lr * mh / (math.sqrt(vh) + 1e-8)
            if it % 50 == 0:
                print(f"  [S2] iter {it}: loss {L:.4f}", flush=True)

    # --- inferencia
    def run_fixed(self, parent, s, T):
        z = self.trajectory(parent, s, T)[-1]
        c = max(range(len(z)), key=lambda i: z[i])
        return c, T

    def run_meta(self, parent, s, T_max, conf=0.9, eps=0.02, crystallize=False):
        """
        Sistema 3 (metacognicao): observa o proprio estado latente.
          - para quando esta confiante E o estado parou de mudar (ponto fixo)
          - se estourar o orcamento sem convergir, se ABSTEM (retorna None)
        """
        S = self.affinity(parent)
        N = len(parent)
        z = [0.0] * N
        z[s] = 1.0
        for t in range(1, T_max + 1):
            z2 = self.step(z, S)
            if crystallize:
                # "cristalizacao": o S1 colapsa o pensamento continuo num estado
                # discreto a cada passo, impedindo que o erro se acumule
                k = max(range(N), key=lambda i: z2[i])
                z2 = [0.0] * N
                z2[k] = 1.0
                change = 0.0 if z[k] == 1.0 else 2.0
                z = z2
                if change == 0.0:
                    return k, t
                continue
            change = sum(abs(a - b) for a, b in zip(z, z2))
            z = z2
            if max(z) >= conf and change < eps:
                return max(range(N), key=lambda i: z[i]), t
        return None, T_max

    @staticmethod
    def flops_per_step(N):
        return N * N  # z esparso na pratica, limite superior


# ------------------------------------------------------------- avaliacao
def evaluate(name, fn, tests):
    """fn(parent, s) -> (pred_or_None, custo_em_flops)"""
    rows = {}
    for d, exs in tests.items():
        ok = ans = 0
        cost = 0.0
        for parent, s, root in exs:
            pred, fl = fn(parent, s)
            cost += fl
            if pred is not None:
                ans += 1
                ok += pred == root
        n = len(exs)
        rows[d] = dict(acc=ok / n, cobertura=ans / n,
                       acc_quando_responde=(ok / ans if ans else float("nan")),
                       flops=cost / n)
    return name, rows


def print_table(title, results, depths):
    print(f"\n=== {title} ===")
    hdr = "modelo".ljust(12) + "".join(f"d={d}".rjust(8) for d in depths) + "   flops med."
    print(hdr)
    for name, rows in results:
        if rows is None:
            print(name.ljust(12) + "  (nao aplicavel: tamanho de entrada fixo)")
            continue
        line = name.ljust(12)
        for d in depths:
            r = rows[d]
            cell = f"{100 * r['acc']:.0f}%"
            if r["cobertura"] < 0.999:
                cell += "*"
            line += cell.rjust(8)
        fl = sum(rows[d]["flops"] for d in depths) / len(depths)
        print(line + f"   {fl:9.0f}")
    print("  (* = abstencoes: o modelo disse 'nao sei' em parte dos casos)")


def main():
    quick = "--quick" in sys.argv
    rng = random.Random(SEED)
    t0 = time.time()

    n_mlp = 6000 if quick else 20000
    train = dataset(N_TRAIN, TRAIN_DEPTHS, n_mlp, rng)

    print("Treinando S1-MLP (classificador de uma passada)...")
    s1 = S1MLP(N_TRAIN, 48, rng)
    s1.train(train, epochs=2 if quick else 4, lr=0.02, rng=rng)

    print("Treinando S2 (passo latente recorrente, pesos compartilhados)...")
    s2 = S2Step(4, rng)
    print(f"  parametros S2: {s2.n_params()}  |  parametros S1-MLP: "
          f"{s1.H * s1.D + s1.H + s1.N * s1.H + s1.N}")
    s2.train(train, iters=200 if quick else 600, rng=rng)

    # --- testes
    n_test = 150 if quick else 400
    trng = random.Random(SEED + 1)
    in_dist = {d: [make_example(N_TRAIN, d, trng) for _ in range(n_test)] for d in range(0, 10)}
    N_BIG = 16
    big = {d: [make_example(N_BIG, d, trng) for _ in range(n_test // 2)] for d in (0, 2, 4, 8, 11, 13)}

    tau = 0.9

    def f_s1(p, s):
        return s1.predict(p, s)[0], s1.flops()

    def f_s2fixed(p, s):
        return s2.run_fixed(p, s, T_MAX)[0], T_MAX * S2Step.flops_per_step(len(p))

    def f_s2meta(p, s):
        pred, t = s2.run_meta(p, s, T_MAX)
        return pred, t * S2Step.flops_per_step(len(p))

    def f_mlu(p, s):
        c, conf = s1.predict(p, s)
        if conf >= tau:
            return c, s1.flops()
        pred, t = s2.run_meta(p, s, T_MAX)
        return pred, s1.flops() + t * S2Step.flops_per_step(len(p))

    # "atalhos" usados pelo roteador
    route = {}
    for d, exs in in_dist.items():
        route[d] = sum(s1.predict(p, s)[1] >= tau for p, s, _ in exs) / len(exs)

    res_in = [evaluate("S1-MLP", f_s1, in_dist),
              evaluate("S2-fixo", f_s2fixed, in_dist),
              evaluate("S2+S3", f_s2meta, in_dist),
              evaluate("MLU", f_mlu, in_dist)]
    res_big = [("S1-MLP", None),
               evaluate("S2-fixo", f_s2fixed, big),
               evaluate("S2+S3", f_s2meta, big)]

    print_table(f"N={N_TRAIN} nos (treino so viu d=0..4)", res_in, list(in_dist))
    print("\nFracao em que o roteador do MLU confiou no S1 (atalho intuitivo):")
    print("  " + "  ".join(f"d={d}: {100 * r:.0f}%" for d, r in route.items()))
    print_table(f"N={N_BIG} nos (tamanho nunca visto, T_MAX={T_MAX})", res_big, list(big))

    # confianca de o S3 saber quando nao sabe
    ans = wrong = abst = 0
    for exs in big.values():
        for p, s, root in exs:
            pred, _ = s2.run_meta(p, s, T_MAX)
            if pred is None:
                abst += 1
            else:
                ans += 1
                wrong += pred != root
    print(f"\nS3 em N=16: respondeu {ans}, errou {wrong} das respondidas, se absteve {abst}.")

    print("\nPassos latentes medios do S2+S3 por profundidade (N=12):")
    steps = {}
    for d, exs in in_dist.items():
        steps[d] = sum(s2.run_meta(p, s, T_MAX)[1] for p, s, _ in exs) / len(exs)
    print("  " + "  ".join(f"d={d}: {v:.1f}" for d, v in steps.items()))

    print("\nPensar mais tempo: mesmo modelo de 33 parametros, orcamento maior:")
    longer = {}
    print("  (continuo = estado latente difuso | cristalizado = colapso discreto a cada passo)")
    for N, d, T in ((16, 13, 24), (32, 25, 40), (64, 50, 64), (128, 100, 128)):
        exs = [make_example(N, d, trng) for _ in range(30)]
        ok = sum(s2.run_meta(p, s, T)[0] == r for p, s, r in exs)
        okc = sum(s2.run_meta(p, s, T, crystallize=True)[0] == r for p, s, r in exs)
        longer[f"N={N},d={d},T={T}"] = dict(continuo=ok / len(exs), cristalizado=okc / len(exs))
        print(f"  N={N:3d} d={d:3d} T_MAX={T:3d}: continuo {100 * ok / len(exs):3.0f}%"
              f" | cristalizado {100 * okc / len(exs):3.0f}%", flush=True)
    print(f"Tempo total: {time.time() - t0:.0f}s")

    out = dict(in_dist={n: r for n, r in res_in},
               big={n: r for n, r in res_big if r is not None},
               roteamento_s1=route, passos_s2s3=steps, pensar_mais=longer, s3_big=dict(respondeu=ans, errou=wrong, absteve=abst),
               theta_s2=s2.theta)
    with open(f"experimento/resultados_seed{SEED}.json", "w") as fh:
        json.dump(out, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
