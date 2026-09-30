"""
Passo do S2 em O(N) para qualquer grafo de ponteiros (floresta T1 ou permutacao T2),
com temperatura beta nos logits e opcao de cristalizar (argmax).

A afinidade S[j][i] = V(feat(j,i)) so difere do termo generico G[raiz_j][raiz_i]
quando j e filho de i, j e o pai de i, ou j == i. Logo
  logit_i = sum_r Z_r G[r][raiz_i] + sum_{j em J_i} z_j (V(feat(j,i)) - G[raiz_j][raiz_i]),
com J_i = filhos(i) U {pai(i)} U {i} e Z_r a massa nos nos com raiz_j = r.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "E001_mlu"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "E006_lei_margem"))
import mlu  # noqa: E402
import passo_rapido as PR  # noqa: E402


def preparar(s2, parent):
    V = PR.tabela(s2)
    cache = {}

    def v(f):
        if f not in cache:
            cache[f] = V(f)
        return cache[f]
    N = len(parent)
    raiz = [1 if parent[j] == j else 0 for j in range(N)]
    G = [[v((0.0, 0.0, 0.0, float(rj), float(ri), 1.0)) for ri in (0, 1)] for rj in (0, 1)]
    filhos = [[] for _ in range(N)]
    for j in range(N):
        if parent[j] != j:
            filhos[parent[j]].append(j)
    delta = []
    for i in range(N):
        J = set(filhos[i])
        J.add(parent[i])
        J.add(i)
        delta.append([(j, v(mlu.S2Step.feat(parent, j, i)) - G[raiz[j]][raiz[i]]) for j in J])
    return dict(N=N, parent=parent, raiz=raiz, G=G, delta=delta)


def passo(z, P, beta=1.0, crist=False):
    N, raiz, G = P["N"], P["raiz"], P["G"]
    Z = [0.0, 0.0]
    for j in range(N):
        Z[raiz[j]] += z[j]
    base = [Z[0] * G[0][ri] + Z[1] * G[1][ri] for ri in (0, 1)]
    lg = [0.0] * N
    for i in range(N):
        s = base[raiz[i]]
        for j, d in P["delta"][i]:
            if z[j]:
                s += z[j] * d
        lg[i] = beta * s
    if crist:
        k = max(range(N), key=lambda i: lg[i])
        o = [0.0] * N
        o[k] = 1.0
        return o
    m = max(lg)
    e = [math.exp(x - m) for x in lg]
    t = sum(e)
    return [x / t for x in e]


def vazamento(P, j, beta=1.0):
    z = [0.0] * P["N"]
    z[j] = 1.0
    return 1.0 - passo(z, P, beta)[P["parent"][j]]
