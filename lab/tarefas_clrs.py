"""
lab/tarefas_clrs.py - tarefas algoritmicas no estilo CLRS-30 (Velickovic et al., 2022),
reimplementadas em Python puro com resolvedores exatos.

Protocolo seguido (o que importa para comparabilidade):
  - grafos Erdos-Renyi; treino com n = 16 nos, teste fora da distribuicao com n = 64
  - saida = ponteiros predecessores (pi); metrica = acuracia de ponteiros por no
    (fracao de nos com pi correto) e exato (todos corretos)
  - convencoes: pi[s] = s; nos inalcancaveis apontam para si mesmos
Diferencas declaradas: nao e o dataset oficial (jax/tfds indisponiveis aqui);
p = 0,5 fixo; sem "hints" (trajetorias intermediarias). Resultados aqui sao
"protocolo CLRS reimplementado", nao numeros comparaveis 1:1 com o artigo.
"""
import heapq
import random


def grafo_er(n, p, rng, pesos=False):
    """Nao direcionado. adj[u] = lista ordenada de (v, peso)."""
    adj = [[] for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                w = rng.random() if pesos else 1.0
                adj[u].append((v, w))
                adj[v].append((u, w))
    for u in range(n):
        adj[u].sort()
    return adj


def bfs(adj, s):
    """Predecessores de BFS; vizinhos visitados em ordem crescente de indice."""
    n = len(adj)
    pi = list(range(n))
    visto = [False] * n
    visto[s] = True
    fila = [s]
    k = 0
    while k < len(fila):
        u = fila[k]
        k += 1
        for v, _ in adj[u]:
            if not visto[v]:
                visto[v] = True
                pi[v] = u
                fila.append(v)
    return pi


def bellman_ford(adj, s):
    """Distancias e predecessores de caminho minimo; empate -> menor indice."""
    n = len(adj)
    inf = float("inf")
    d = [inf] * n
    d[s] = 0.0
    for _ in range(n - 1):
        mudou = False
        for u in range(n):
            if d[u] == inf:
                continue
            for v, w in adj[u]:
                if d[u] + w < d[v] - 1e-12:
                    d[v] = d[u] + w
                    mudou = True
        if not mudou:
            break
    pi = list(range(n))
    for v in range(n):
        if v == s or d[v] == inf:
            continue
        melhor = None
        for u, w in adj[v]:          # grafo nao direcionado: vizinhos de v
            if abs(d[u] + w - d[v]) < 1e-9 and (melhor is None or u < melhor):
                melhor = u
        pi[v] = melhor
    return d, pi


def dijkstra(adj, s):
    n = len(adj)
    d = [float("inf")] * n
    d[s] = 0.0
    h = [(0.0, s)]
    while h:
        du, u = heapq.heappop(h)
        if du > d[u]:
            continue
        for v, w in adj[u]:
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(h, (d[v], v))
    return d


def acuracia_ponteiros(pred, verdade):
    return sum(a == b for a, b in zip(pred, verdade)) / len(verdade)


def exemplo(algoritmo, n, rng, p=0.5):
    if algoritmo == "bfs":
        adj = grafo_er(n, p, rng)
        s = rng.randrange(n)
        return adj, s, bfs(adj, s)
    if algoritmo == "bellman_ford":
        adj = grafo_er(n, p, rng, pesos=True)
        s = rng.randrange(n)
        return adj, s, bellman_ford(adj, s)[1]
    raise ValueError(algoritmo)


N_TREINO, N_TESTE_OOD = 16, 64
