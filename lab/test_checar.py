"""Teste do controle de qualidade. Rodar: python3 -m unittest lab.test_checar"""
import unittest

from lab import checar


class TestChecar(unittest.TestCase):
    def test_roda_e_devolve_listas(self):
        erros, avisos = checar.verificar()
        self.assertIsInstance(erros, list)
        self.assertIsInstance(avisos, list)


if __name__ == "__main__":
    unittest.main()
