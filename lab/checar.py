"""
lab/checar.py - controle de qualidade: o laboratorio esta coerente consigo mesmo?

Varias fontes guardam a mesma verdade (arvore, habilidades, ESTADO, DIARIO,
EVOLUTION_LOG, LIVRO, BUSSOLA). Este verificador acusa quando elas divergem.

  ERRO  -> nao commitar (exit 1)
  AVISO -> corrigir no proximo ciclo

Uso:
  python3 -m lab.checar            # todas as verificacoes
  python3 -m lab.checar --resumo   # verificacoes + fronteira e meta-metricas (gancho de inicio de sessao)
"""
import glob
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout

from lab import bussola, registro

RAIZ = registro.RAIZ


def _ler(rel):
    p = os.path.join(RAIZ, rel)
    return open(p).read() if os.path.exists(p) else ""


def _git(*args):
    r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def verificar():
    erros, avisos = [], []
    nos = registro.carregar()
    por_id = {n["id"]: n for n in nos}
    ciclo_max = max((n["ciclo"] for n in nos), default=0)

    # 1. guarda do avaliador
    erros += [f"guarda: {p}" for p in registro.verificar()]

    # 2. cada PREREG tem exatamente um commit, igual ao registrado no no
    for pasta in sorted(glob.glob(os.path.join(RAIZ, "experimentos", "E[0-9]*"))):
        eid = os.path.basename(pasta).split("_")[0]
        prereg = os.path.join(pasta, "PREREG.md")
        if not os.path.exists(prereg):
            continue
        commits = (_git("log", "--format=%h", "--", os.path.relpath(prereg, RAIZ)) or "").split()
        if len(commits) == 0:
            avisos.append(f"{eid}: PREREG.md ainda nao commitado (commite antes de rodar)")
        elif len(commits) > 1:
            erros.append(f"{eid}: PREREG.md tem {len(commits)} commits (pre-registro editado depois)")
        elif eid in por_id and por_id[eid].get("commit_prereg") and not commits[0].startswith(por_id[eid]["commit_prereg"][:7]):
            erros.append(f"{eid}: commit do PREREG ({commits[0]}) != registrado ({por_id[eid]['commit_prereg']})")

    # 3. experimentos decididos tem RELATORIO; ciclos >= 5 tem probabilidades
    for n in nos:
        if n["operador"] in ("META", "DIAGNOSTICAR") or n["veredito"] == "PENDENTE":
            continue
        pastas = glob.glob(os.path.join(RAIZ, "experimentos", n["id"] + "_*"))
        if not pastas or not os.path.exists(os.path.join(pastas[0], "RELATORIO.md")):
            erros.append(f"{n['id']}: decidido ({n['veredito']}) mas sem RELATORIO.md")
        if n["ciclo"] >= 5:
            sem = [p["id"] for p in n.get("previsoes", []) if p.get("prob") is None]
            if sem:
                avisos.append(f"{n['id']}: previsoes sem probabilidade: {', '.join(sem)}")

    # 4. habilidades apontam para evidencia existente e suficiente
    hab, goals = bussola.carregar()
    ok = bussola.desbloqueadas(hab, nos)
    for h in hab.values():
        for e in h.get("desbloqueada_por") or []:
            if e not in por_id:
                erros.append(f"{h['id']}: desbloqueada_por {e}, que nao existe na arvore")
        if h.get("desbloqueada_por") and h["id"] not in ok:
            avisos.append(f"{h['id']}: tem evidencia listada mas abaixo do nivel minimo N{h['nivel_minimo']}")
    dados = json.load(open(bussola.ARQ))
    radar = dados.get("ultimo_radar_ciclo", 0)
    if ciclo_max - radar >= 5:
        avisos.append(f"radar de lacunas atrasado: ultimo no ciclo {radar}, estamos no {ciclo_max} (GOALS.md regra 7)")

    # 5. arquivos gerados em dia
    for nome, gerar, alvo in (("LIVRO.md", registro.gerar_livro, "LIVRO"), ("BUSSOLA.md", bussola.gerar, "SAIDA")):
        mod = registro if alvo == "LIVRO" else bussola
        orig = getattr(mod, alvo)
        with tempfile.TemporaryDirectory() as tmp:
            setattr(mod, alvo, os.path.join(tmp, nome))
            try:
                with redirect_stdout(io.StringIO()):
                    gerar()
                novo = open(os.path.join(tmp, nome)).read()
            finally:
                setattr(mod, alvo, orig)
        if novo != _ler(nome):
            erros.append(f"{nome} desatualizado: rode python3 -m lab.{'registro livro' if alvo == 'LIVRO' else 'bussola'}")

    # 6. ESTADO, DIARIO e EVOLUTION_LOG acompanham o ciclo mais recente
    m = re.search(r"Última atualização: ciclo (\d+)", _ler("ESTADO.md"))
    if not m or int(m.group(1)) != ciclo_max:
        erros.append(f"ESTADO.md diz ciclo {m.group(1) if m else '?'}, a arvore esta no ciclo {ciclo_max}")
    if f"## Ciclo {ciclo_max} " not in _ler("DIARIO.md"):
        erros.append(f"DIARIO.md sem entrada do ciclo {ciclo_max}")
    exps_ciclo = [n for n in nos if n["ciclo"] == ciclo_max and n["operador"] not in ("META", "DIAGNOSTICAR")]
    if exps_ciclo and f"## Ciclo {ciclo_max} " not in _ler("EVOLUTION_LOG.md"):
        erros.append(f"EVOLUTION_LOG.md sem entrada do ciclo {ciclo_max} (passo ESCALAR)")

    # 6b. autocritica do norte (regra 19): uma entrada por ciclo a partir do 18, com decisao
    if ciclo_max >= 18:
        crit = _ler("CRITICA.md")
        bloco = crit.split(f"## Ciclo {ciclo_max} ")[1].split("\n## Ciclo ")[0] if f"## Ciclo {ciclo_max} " in crit else ""
        if not bloco:
            erros.append(f"CRITICA.md sem entrada do ciclo {ciclo_max} (regra 19: rode python3 -m lab.critica)")
        elif not re.search(r"Decis[aã]o:\s*(APROFUNDAR|VARIAR|ENDURECER|PIVOTAR)", bloco):
            erros.append(f"CRITICA.md ciclo {ciclo_max}: falta 'Decisao: APROFUNDAR|VARIAR|ENDURECER|PIVOTAR'")

    # 7. fila do ESTADO aponta para habilidades validas e ainda trancadas
    for hid in re.findall(r"\(→ (H\d+)", _ler("ESTADO.md")):
        if hid not in hab:
            erros.append(f"ESTADO.md: fila cita {hid}, que nao existe")
        elif hid in ok:
            avisos.append(f"ESTADO.md: fila ainda ataca {hid}, que ja esta desbloqueada")

    # 8. afirmacoes mortas nao podem reaparecer sem riscar
    for linha in _ler("registro/obsoletos.txt").splitlines():
        frase = linha.strip()
        if not frase or frase.startswith("#"):
            continue
        for arq in ("ESTADO.md", "LICOES.md", "GOALS.md", "docs/SISTEMAS.md", "PLANO.md"):
            for texto in _ler(arq).splitlines():
                if frase.lower() in texto.lower() and "~~" not in texto:
                    erros.append(f"{arq}: afirmacao obsoleta sem riscar: '{frase}'")
    # 9. peso: o GitHub recusa arquivos > 100 MB; acima de 20 MB, usar git-lfs
    for linha in (_git("ls-files", "-z") or "").split("\0"):
        if not linha:
            continue
        caminho = os.path.join(RAIZ, linha)
        if os.path.isfile(caminho):
            mb = os.path.getsize(caminho) / 2 ** 20
            if mb > 90:
                erros.append(f"{linha}: {mb:.0f} MB (limite do GitHub e 100 MB): mover para git-lfs")
            elif mb > 20:
                avisos.append(f"{linha}: {mb:.0f} MB: considerar git-lfs (git lfs track)")
    return erros, avisos


def main(argv):
    erros, avisos = verificar()
    for e in erros:
        print("ERRO  ", e)
    for a in avisos:
        print("AVISO ", a)
    print(f"checar: {len(erros)} erro(s), {len(avisos)} aviso(s)")
    if "--resumo" in argv:
        m = registro.metricas()
        print(f"\nciclo {m['ciclos']} | degraus {m['degrau_por_tema']} | Brier {m['brier_previsoes']} | "
              f"sem subir {m['ciclos_sem_subir']}")
        print("fronteira da bussola (atacar nesta ordem):")
        with redirect_stdout(sys.stdout):
            bussola.main(["", "fronteira"])
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main(sys.argv)
