"""
lab/sementes.py - sementes de teste que ninguem escolhe.

As sementes do teste congelado sao derivadas do hash do commit que contem o
PREREG.md do experimento. Como o PREREG so pode ter UM commit (verificado por
lab/checar.py), nao da para "rolar os dados de novo" ate o resultado sair
bonito: mudar as sementes exigiria reescrever o pre-registro, e isso aparece.

Uso num avaliador:
    from lab import sementes
    base = sementes.base_teste(__file__)           # le o commit do PREREG.md ao lado
    sementes_teste = sementes.derivar(base, 30)     # 30 inteiros deterministicos
"""
import hashlib
import os
import subprocess


def commit_do_prereg(pasta):
    """Hash completo do (unico) commit que contem PREREG.md nesta pasta."""
    arq = os.path.join(pasta, "PREREG.md")
    raiz = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=pasta,
                          capture_output=True, text=True, check=True).stdout.strip()
    rel = os.path.relpath(arq, raiz)
    out = subprocess.run(["git", "log", "--format=%H", "--", rel], cwd=raiz,
                         capture_output=True, text=True, check=True).stdout.split()
    if len(out) != 1:
        raise RuntimeError(f"{rel}: esperado exatamente 1 commit do PREREG, achei {len(out)} "
                           "(sem commit = pre-registre antes; mais de 1 = PREREG editado)")
    return out[0]


def base_teste(arquivo_avaliador):
    return commit_do_prereg(os.path.dirname(os.path.abspath(arquivo_avaliador)))


def derivar(base, n, rotulo="teste"):
    """n sementes inteiras (31 bits) derivadas de base + rotulo."""
    res = []
    for i in range(n):
        h = hashlib.sha256(f"{base}|{rotulo}|{i}".encode()).hexdigest()
        res.append(int(h[:8], 16) & 0x7FFFFFFF)
    return res
