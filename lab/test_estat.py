"""Testes da regua. Rodar: python3 -m unittest lab.test_estat"""
import unittest

from lab import estat


class TestEstat(unittest.TestCase):
    def test_iqm_ignora_extremos(self):
        self.assertAlmostEqual(estat.iqm([0, 10, 10, 10, 10, 10, 10, 100]), 10)

    def test_wilson_limites(self):
        lo, hi = estat.ic_proporcao(100, 100)
        self.assertAlmostEqual(hi, 1.0)
        self.assertGreater(lo, 0.95)
        lo, hi = estat.ic_proporcao(0, 10)
        self.assertAlmostEqual(lo, 0.0)
        self.assertGreater(hi, 0.2)  # 0/10 nao prova taxa zero

    def test_prob_melhoria(self):
        self.assertEqual(estat.prob_melhoria([2, 3], [0, 1]), 1.0)
        self.assertEqual(estat.prob_melhoria([1, 1], [1, 1]), 0.5)

    def test_permutacao(self):
        self.assertLess(estat.teste_permutacao([10] * 8, [0] * 8), 0.01)
        self.assertGreater(estat.teste_permutacao([1, 2, 3, 4], [2, 1, 4, 3]), 0.5)

    def test_aurc_oraculo_zero(self):
        corretos = [True, True, False, True, False]
        conf_perfeita = [0.9, 0.8, 0.1, 0.7, 0.2]
        self.assertAlmostEqual(estat.e_aurc(conf_perfeita, corretos), 0.0)
        conf_invertida = [0.1, 0.2, 0.9, 0.3, 0.8]
        self.assertGreater(estat.e_aurc(conf_invertida, corretos), 0.3)

    def test_ece_calibrado(self):
        conf = [0.8] * 10
        ok = [True] * 8 + [False] * 2
        self.assertAlmostEqual(estat.ece(conf, ok), 0.0)

    def test_pareto(self):
        pts = [("a", 1, 0.5), ("b", 2, 0.9), ("c", 3, 0.8), ("d", 1, 0.4)]
        self.assertEqual([p[0] for p in estat.fronteira_pareto(pts)], ["a", "b"])

    def test_extrapolacao(self):
        self.assertEqual(estat.razao_extrapolacao({4: 1.0, 8: 0.99, 16: 0.5}, 4), 2.0)

    def test_fisher(self):
        # tabela classica do cha da senhora: 3/4 vs 1/4 -> p ~ 0.486
        self.assertAlmostEqual(estat.fisher_exato(3, 4, 1, 4), 0.4857, places=3)
        self.assertLess(estat.fisher_exato(10, 30, 0, 30), 0.01)

    def test_colapso(self):
        self.assertEqual(estat.taxa_colapso([1, 1, 0, 0.2]), 0.5)

    def test_tamanho_amostra(self):
        n = estat.n_para_diferenca(0.5, 0.95, alfa=0.01, poder=0.8)
        self.assertTrue(10 <= n <= 30)                       # diferenca grande: poucos
        self.assertGreater(estat.n_para_diferenca(0.90, 0.95), 500)  # pequena: muitos
        self.assertLessEqual(estat.n_para_largura(0.5, 0.1), 100)
        self.assertGreater(estat.n_para_largura(0.5, 0.1), 50)


if __name__ == "__main__":
    unittest.main()
