"""Testes das linhas de base. Rodar: python3 -m unittest lab.test_baselines"""
import random
import unittest

from lab import baselines as B


def exemplo_raiz(rng, N=8, d=3):
    p, s, r = B.mlu.make_example(N, d, rng)
    return p, s, r


class TestBaselines(unittest.TestCase):
    def test_bptt_gradiente_numerico_com_z0_difuso(self):
        rng = random.Random(1)
        s2 = B.mlu.S2Step(4, rng)
        exs = []
        for _ in range(3):
            p, s, r = exemplo_raiz(rng)
            z0 = [rng.random() for _ in range(len(p))]
            t = sum(z0)
            exs.append((p, [x / t for x in z0], 4, {2: r, 4: r}))
        _, g = B.bptt(s2, exs)
        for q in (0, 7, 30):
            e = 1e-5
            s2.theta[q] += e
            lp, _ = B.bptt(s2, exs)
            s2.theta[q] -= 2 * e
            lm, _ = B.bptt(s2, exs)
            s2.theta[q] += e
            self.assertAlmostEqual(g[q], (lp - lm) / (2 * e), places=5)

    def test_progressivo_reduz_perda(self):
        rng = random.Random(2)
        s2 = B.mlu.S2Step(4, rng)
        dados = [(p, s, r) for p, s, r in (exemplo_raiz(rng, 10, rng.randint(0, 3)) for _ in range(200))]
        alvo = lambda info, t: info  # noqa: E731  (T1: a raiz e a resposta em qualquer t >= d)
        antes, _ = B.bptt(s2, [(p, [1.0 if i == s else 0.0 for i in range(len(p))], 6, {6: r}) for p, s, r in dados[:40]])
        B.treinar_progressivo(s2, dados, alvo, M=6, iters=40, rng=rng)
        depois, _ = B.bptt(s2, [(p, [1.0 if i == s else 0.0 for i in range(len(p))], 6, {6: r}) for p, s, r in dados[:40]])
        self.assertLess(depois, antes)

    def test_ponder_aprende_a_esperar(self):
        rng = random.Random(3)
        s2 = B.mlu.S2Step(4, rng)
        B.treinar_progressivo(s2, [exemplo_raiz(rng, 10, rng.randint(0, 4)) for _ in range(300)],
                              lambda info, t: info, M=8, iters=60, rng=rng)
        casos = []
        for _ in range(30):
            p, s, r = exemplo_raiz(rng, 10, rng.randint(0, 4))
            casos.append((p, s, lambda t, r=r: r))
        trajs = B.trajetorias(s2, casos, 10)
        w0 = [0.0, 0.0, 0.0, 0.0]
        w = B.treinar_ponder(trajs, iters=60, rng=rng)
        self.assertLess(B.perda_ponder(w, trajs), B.perda_ponder(w0, trajs))


if __name__ == "__main__":
    unittest.main()
