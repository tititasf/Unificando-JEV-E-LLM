"""
Motor com memoria de trabalho (S2 D06) para a tarefa T2 com k NA ENTRADA.

Estado: distribuicao sobre pares (no j, contador a), a em 0..K.
Um unico passo aprendido: z'(i,b) = softmax_{(i,b)} sum_{(j,a)} z(j,a) V(f((j,a) -> (i,b)))
com atributos binarios do par:
  ponteiro: i = pi(j) | i = j | j = pi(i) | generico      (one-hot, 4)
  contador: b = a-1   | b = a | generico                  (one-hot, 3)
  marcas:   a == 0, b == 0                                 (2)
  + vies                                                   (1)
V = MLP(tanh) desses 10 atributos. NADA diz "pare quando o contador zerar":
o passo precisa aprender (a > 0: avance e decremente; a = 0: fique parado).
O controlador roda um numero FIXO de passos (nao conhece k).

Treino: BPTT denso (lab/baselines.bptt) em N e K pequenos, sobre um "grafo"
de pares. Teste: passo estruturado O(N*K) exato (verificado contra o denso).
"""
import math
import os
import sys

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E001_mlu"))
import mlu  # noqa: E402

CLASSES_P = ("pai", "self", "filho", "gen")
CLASSES_C = ("dec", "igual", "gen")


class Pares:
    """'Grafo' do espaco de pares: indice = j * (K + 1) + a."""

    def __init__(self, pi, K):
        self.pi, self.K = pi, K
        self.N = len(pi)
        self.inv = [0] * self.N
        for j, p in enumerate(pi):
            self.inv[p] = j

    def __len__(self):
        return self.N * (self.K + 1)

    def idx(self, j, a):
        return j * (self.K + 1) + a


def classe_p(pi, j, i):
    if pi[j] == i and i != j:
        return 0
    if i == j:
        return 1
    if pi[i] == j:
        return 2
    return 3


def classe_c(a, b):
    if b == a - 1:
        return 0
    if b == a:
        return 1
    return 2


def atributos(cp, cc, a0, b0):
    f = [0.0] * 10
    f[cp] = 1.0
    f[4 + cc] = 1.0
    f[7] = float(a0)
    f[8] = float(b0)
    f[9] = 1.0
    return tuple(f)


class MotorMem(mlu.S2Step):
    F = 10

    def feat(self, g, u, v):
        K1 = g.K + 1
        j, a = divmod(u, K1)
        i, b = divmod(v, K1)
        return atributos(classe_p(g.pi, j, i), classe_c(a, b), a == 0, b == 0)

    def tabela(self):
        """V para todas as combinacoes (cp, cc, a0, b0)."""
        H, F = self.H, self.F
        th = self.theta
        W1, b1 = th[: H * F], th[H * F: H * F + H]
        w2, b2 = th[H * F + H: H * F + 2 * H], th[-1]
        V = {}
        for cp in range(4):
            for cc in range(3):
                for a0 in (0, 1):
                    for b0 in (0, 1):
                        f = atributos(cp, cc, a0, b0)
                        v = b2
                        for k in range(H):
                            v += w2[k] * math.tanh(b1[k] + sum(W1[k * F + q] * f[q] for q in range(F)))
                        V[(cp, cc, a0, b0)] = v
        return V


def estado_inicial(g, s, k):
    z = [0.0] * len(g)
    z[g.idx(s, k)] = 1.0
    return z


def _soma_classe(W, W0, Wtot, b, K1, Vf):
    """sum_a W[a] * Vf(classe_c(a, b), a == 0) em O(1), com W0 = W[0] e Wtot = sum(W).
    Classes do contador: a = b+1 -> dec; a = b -> igual; demais -> gen."""
    tot = W0 * Vf(2, 1) + (Wtot - W0) * Vf(2, 0)          # tudo como 'gen'
    for a, cc in ((b + 1, 0), (b, 1)):                    # corrige os dois especiais
        if 0 <= a < K1 and W[a] != 0.0:
            a0 = int(a == 0)
            tot += W[a] * (Vf(cc, a0) - Vf(2, a0))
    return tot


def passo_rapido(z, g, V):
    """Passo exato em O(N*K) usando a estrutura das classes."""
    N, K1 = g.N, g.K + 1
    Zc = [0.0] * K1
    linhas = []
    for j in range(N):
        lj = z[j * K1: (j + 1) * K1]
        linhas.append((lj, lj[0], sum(lj)))
        for a in range(K1):
            Zc[a] += lj[a]
    Z0, Ztot = Zc[0], sum(Zc)
    logits = [0.0] * (N * K1)
    for i in range(N):
        esp = []
        for j in (g.inv[i], i, g.pi[i]):
            if j not in [e for e, _ in esp]:
                esp.append((j, classe_p(g.pi, j, i)))
        for b in range(K1):
            b0 = int(b == 0)
            tot = _soma_classe(Zc, Z0, Ztot, b, K1, lambda cc, a0: V[(3, cc, a0, b0)])
            for j, cp in esp:
                if cp == 3:
                    continue
                lj, w0, wt = linhas[j]
                if wt == 0.0:
                    continue
                tot += _soma_classe(lj, w0, wt, b, K1, lambda cc, a0: V[(cp, cc, a0, b0)] - V[(3, cc, a0, b0)])
            logits[i * K1 + b] = tot
    mx = max(logits)
    e = [math.exp(x - mx) for x in logits]
    t = sum(e)
    return [x / t for x in e]


def resposta(z, g):
    """No mais provavel (marginal sobre o contador) e massa no contador 0."""
    K1 = g.K + 1
    marg = [sum(z[j * K1: (j + 1) * K1]) for j in range(g.N)]
    return max(range(g.N), key=lambda j: marg[j]), sum(z[j * K1] for j in range(g.N))
