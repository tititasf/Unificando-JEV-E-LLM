"""Testes do registro. Rodar: python3 -m unittest lab.test_registro"""
import os
import tempfile
import unittest

from lab import registro as R


class TestRegistro(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.arq_orig = R.ARQ
        R.ARQ = os.path.join(self.tmp, "arvore.jsonl")

    def tearDown(self):
        R.ARQ = self.arq_orig

    def no(self, i, pai=None, v="MATAR", ciclo=1, **kw):
        d = dict(id=i, pai=pai, ciclo=ciclo, operador="RASCUNHO", tema="S2", hipotese="h", veredito=v)
        d.update(kw)
        return d

    def test_valida_campos(self):
        with self.assertRaises(ValueError):
            R.adicionar({"id": "X"})
        with self.assertRaises(ValueError):
            R.adicionar(self.no("A", operador="INVENTADO"))
        R.adicionar(self.no("A"))
        with self.assertRaises(ValueError):
            R.adicionar(self.no("A"))           # id repetido
        with self.assertRaises(ValueError):
            R.adicionar(self.no("B", pai="Z"))  # pai inexistente

    def test_metricas(self):
        R.adicionar(self.no("A", previsoes=[{"id": "P1", "prob": 0.8, "acertou": True},
                                           {"id": "P2", "prob": 0.8, "acertou": False}],
                            degrau_atingido={"S2": 3}))
        R.adicionar(self.no("B", pai="A", v="PROMOVER", ciclo=3, degrau_atingido={"S2": 4}))
        m = R.metricas()
        self.assertEqual(m["taxa_morte"], 0.5)
        self.assertEqual(m["acerto_previsoes"], 0.5)
        self.assertAlmostEqual(m["brier_previsoes"], (0.04 + 0.64) / 2)
        self.assertEqual(m["degrau_por_tema"], {"S2": 4})
        self.assertEqual(m["ciclos_sem_subir"], {"S2": 0})


if __name__ == "__main__":
    unittest.main()
