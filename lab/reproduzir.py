"""
lab/reproduzir.py - reproducao limpa de um experimento (decisao compilada: este
procedimento foi feito a mao 5 vezes antes de virar codigo).

Cria um worktree no commit do PREREG do experimento, roda o avaliador la
(o codigo exatamente como pre-registrado) e compara o resultados.json com o
da arvore de trabalho, ignorando campos de tempo.

Uso: python3 -m lab.reproduzir experimentos/E010_memoria [--script=e010.py] [--dados=respostas_jev.jsonl]

--dados: arquivos da pasta do experimento copiados para o worktree antes de rodar
(respostas brutas de sistemas externos nao deterministicos, como o JEV; o avaliador
reprocessa essas respostas em vez de chamar o sistema de novo).
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

from lab import registro

RAIZ = registro.RAIZ
IGNORAR = {"cpu_s"}


def _limpo(x):
    if isinstance(x, dict):
        return {k: _limpo(v) for k, v in x.items() if k not in IGNORAR}
    if isinstance(x, list):
        return [_limpo(v) for v in x]
    return x


def reproduzir(pasta, script=None, dados=()):
    pasta = os.path.normpath(pasta)
    rel = os.path.relpath(os.path.join(RAIZ, pasta), RAIZ) if not os.path.isabs(pasta) else os.path.relpath(pasta, RAIZ)
    commits = subprocess.run(["git", "log", "--format=%H", "--", os.path.join(rel, "PREREG.md")], cwd=RAIZ,
                             capture_output=True, text=True, check=True).stdout.split()
    if len(commits) != 1:
        raise RuntimeError(f"PREREG deve ter exatamente 1 commit; achei {len(commits)}")
    if script is None:
        cands = sorted(os.path.basename(p) for p in glob.glob(os.path.join(RAIZ, rel, "e[0-9]*.py")))
        if not cands:
            raise RuntimeError("nenhum avaliador eNNN.py na pasta")
        script = cands[0]
    local = os.path.join(RAIZ, rel, "resultados.json")
    if not os.path.exists(local):
        raise RuntimeError("rode o experimento antes: resultados.json nao existe")
    tmp = tempfile.mkdtemp(prefix="repro_")
    wt = os.path.join(tmp, "wt")
    subprocess.run(["git", "worktree", "add", "-q", wt, commits[0]], cwd=RAIZ, check=True)
    try:
        for d in dados:
            shutil.copy(os.path.join(RAIZ, rel, d), os.path.join(wt, rel, d))
        subprocess.run([sys.executable, os.path.join(rel, script)], cwd=wt, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        a = _limpo(json.load(open(os.path.join(wt, rel, "resultados.json"))))
        b = _limpo(json.load(open(local)))
        return a == b, commits[0][:7]
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", wt], cwd=RAIZ)
        shutil.rmtree(tmp, ignore_errors=True)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        sys.exit(2)
    script = next((a.split("=", 1)[1] for a in argv if a.startswith("--script=")), None)
    dados = [x for a in argv if a.startswith("--dados=") for x in a.split("=", 1)[1].split(",")]
    igual, c = reproduzir(argv[1], script, dados)
    print(f"reproducao a partir do commit do PREREG {c}: {'IDENTICA' if igual else 'DIFERENTE'}")
    sys.exit(0 if igual else 1)


if __name__ == "__main__":
    main(sys.argv)
