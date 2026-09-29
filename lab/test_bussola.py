"""Testes da bussola. Rodar: python3 -m unittest lab.test_bussola"""
import json
import os
import tempfile
import unittest

from lab import bussola as B


def arq(habs, goals):
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump({"habilidades": habs, "goals": goals}, f)
    f.close()
    return f.name


def h(i, pre=(), prova=(), nivel=2, custo=1):
    return dict(id=i, nome=i, sistema="S2", escada="-", criterio="c", nivel_minimo=nivel,
                prereqs=list(pre), desbloqueada_por=list(prova), custo=custo)


class TestBussola(unittest.TestCase):
    def test_ciclo_detectado(self):
        with self.assertRaises(ValueError):
            B.carregar(arq([h("A", ["B"]), h("B", ["A"])], []))

    def test_estado_fronteira_e_progresso(self):
        habs = [h("A", prova=["E1"]), h("B", ["A"]), h("C", ["B"], custo=2), h("D", ["A"], prova=["E2"])]
        hab, goals = B.carregar(arq(habs, [dict(id="G", requer=["C"])]))
        nos = [{"id": "E1", "nivel": "N2"}, {"id": "E2", "nivel": "N1"}]  # E2 fraco demais para D
        ok = B.desbloqueadas(hab, nos)
        self.assertEqual(ok, {"A"})
        fronteira, rank, prog = B.analisar(hab, goals, ok)
        self.assertEqual(set(fronteira), {"B", "D"})
        self.assertEqual(rank[0]["id"], "B")          # B abre C e o goal G
        self.assertEqual(prog["G"]["feitas"], 1)
        self.assertEqual(prog["G"]["total"], 3)       # A, B, C

    def test_arquivo_real_valido(self):
        hab, goals = B.carregar()
        self.assertTrue(len(hab) >= 10 and len(goals) >= 3)


if __name__ == "__main__":
    unittest.main()
