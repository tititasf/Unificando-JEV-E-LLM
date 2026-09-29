"""Testes dos resolvedores CLRS. Rodar: python3 -m unittest lab.test_tarefas_clrs"""
import random
import unittest

from lab import tarefas_clrs as C


class TestCLRS(unittest.TestCase):
    def test_bfs_arvore_de_caminhos_minimos(self):
        rng = random.Random(0)
        for _ in range(50):
            n = rng.randint(2, 20)
            adj = C.grafo_er(n, rng.choice([0.1, 0.3, 0.6]), rng)
            s = rng.randrange(n)
            pi = C.bfs(adj, s)
            dist = C.dijkstra(adj, s)          # pesos 1 = numero de saltos
            for v in range(n):
                if v == s or dist[v] == float("inf"):
                    self.assertEqual(pi[v], v)
                else:
                    self.assertEqual(dist[pi[v]] + 1, dist[v])
                    vizinhos = [u for u, _ in adj[v]]
                    self.assertIn(pi[v], vizinhos)

    def test_bellman_ford_igual_dijkstra(self):
        rng = random.Random(1)
        for _ in range(50):
            n = rng.randint(2, 20)
            adj = C.grafo_er(n, 0.4, rng, pesos=True)
            s = rng.randrange(n)
            d, pi = C.bellman_ford(adj, s)
            dj = C.dijkstra(adj, s)
            for v in range(n):
                self.assertAlmostEqual(d[v], dj[v]) if dj[v] != float("inf") else self.assertEqual(d[v], dj[v])
                if v != s and dj[v] != float("inf"):
                    w = dict(adj[v])[pi[v]]
                    self.assertAlmostEqual(d[pi[v]] + w, d[v])

    def test_metrica(self):
        self.assertEqual(C.acuracia_ponteiros([0, 1, 1], [0, 1, 2]), 2 / 3)


if __name__ == "__main__":
    unittest.main()
