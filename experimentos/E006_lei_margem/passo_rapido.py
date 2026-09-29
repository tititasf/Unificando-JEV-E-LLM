"""
Passo do S2 em O(N) para a tarefa T1 (floresta de ponteiros).

A afinidade S[j][i] = V(f(j,i)) depende so de 5 atributos binarios:
(i = pai de j, j = pai de i, i == j, j raiz, i raiz). Logo
  logit_i = sum_j z_j S[j][i]
          = sum_r Z_r * G[r][raiz_i]                      (termo generico)
          + sum_{j filho de i, j != i} z_j (V_pai - G[0][raiz_i])
          + [i nao raiz] z_{pai(i)} (V_filho - G[raiz_pai][0])
          + z_i (V_self - G[raiz_i][raiz_i])
onde Z_r = massa total nos nos com raiz_j = r.
"""
import math


def tabela(s2):
    """Valores V(f) para todos os padroes de atributos possiveis."""
    H, F = s2.H, s2.F
    th = s2.theta
    W1, b1 = th[: H * F], th[H * F: H * F + H]
    w2, b2 = th[H * F + H: H * F + 2 * H], th[-1]

    def V(f):
        v = b2
        for k in range(H):
            v += w2[k] * math.tanh(b1[k] + sum(W1[k * F + q] * f[q] for q in range(F)))
        return v
    return V


def preparar(s2, parent):
    V = tabela(s2)
    N = len(parent)
    raiz = [1 if parent[j] == j else 0 for j in range(N)]
    G = [[V((0.0, 0.0, 0.0, float(rj), float(ri), 1.0)) for ri in (0, 1)] for rj in (0, 1)]
    # j nao-raiz, i = pai(j): (1, 0, 0, 0, ri, 1)
    Vpai = [V((1.0, 0.0, 0.0, 0.0, float(ri), 1.0)) for ri in (0, 1)]
    # i nao-raiz, j = pai(i): (0, 1, 0, rj, 0, 1)
    Vfilho = [V((0.0, 1.0, 0.0, float(rj), 0.0, 1.0)) for rj in (0, 1)]
    # i == j: (r, r, 1, r, r, 1)
    Vself = [V((float(r), float(r), 1.0, float(r), float(r), 1.0)) for r in (0, 1)]
    filhos = [[] for _ in range(N)]
    for j in range(N):
        if parent[j] != j:
            filhos[parent[j]].append(j)
    return dict(N=N, parent=parent, raiz=raiz, G=G, Vpai=Vpai, Vfilho=Vfilho, Vself=Vself, filhos=filhos)


def passo(z, P):
    N, parent, raiz, G = P["N"], P["parent"], P["raiz"], P["G"]
    Z = [0.0, 0.0]
    for j in range(N):
        Z[raiz[j]] += z[j]
    logits = [0.0] * N
    for i in range(N):
        ri = raiz[i]
        v = Z[0] * G[0][ri] + Z[1] * G[1][ri]
        corr = P["Vpai"][ri] - G[0][ri]
        for j in P["filhos"][i]:
            v += z[j] * corr
        if not ri:
            p = parent[i]
            v += z[p] * (P["Vfilho"][raiz[p]] - G[raiz[p]][0])
        v += z[i] * (P["Vself"][ri] - G[ri][ri])
        logits[i] = v
    m = max(logits)
    e = [math.exp(x - m) for x in logits]
    t = sum(e)
    return [x / t for x in e]


def vazamento(P, j):
    """1 - massa no pai apos um passo a partir de um estado concentrado em j."""
    z = [0.0] * P["N"]
    z[j] = 1.0
    return 1.0 - passo(z, P)[P["parent"][j]]
