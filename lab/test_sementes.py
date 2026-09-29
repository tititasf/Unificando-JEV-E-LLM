"""Testes das sementes derivadas. Rodar: python3 -m unittest lab.test_sementes"""
import os
import unittest

from lab import sementes


class TestSementes(unittest.TestCase):
    def test_deterministico_e_distinto(self):
        a = sementes.derivar("abc", 5)
        self.assertEqual(a, sementes.derivar("abc", 5))
        self.assertNotEqual(a, sementes.derivar("abd", 5))
        self.assertEqual(len(set(a)), 5)

    def test_commit_do_prereg_real(self):
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        c = sementes.commit_do_prereg(os.path.join(raiz, "experimentos", "E005_t2_salto"))
        self.assertTrue(c.startswith("f4dfd67"))


if __name__ == "__main__":
    unittest.main()
