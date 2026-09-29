"""
lab/bussola.py - a bussola do laboratorio: arvore de habilidades + goals.

Le registro/habilidades.json e registro/arvore.jsonl e calcula:
  - estado de cada habilidade (desbloqueada so com evidencia: nos da arvore
    de experimentos com nivel >= nivel_minimo)
  - fronteira: habilidades trancadas com todos os pre-requisitos desbloqueados
  - valor de desbloqueio: quantas habilidades e goals dependem dela
  - progresso de cada goal (fracao das habilidades necessarias ja desbloqueadas)
  - prioridade da fronteira = (1 + descendentes + 3 * goals alcancaveis) / custo

Uso:
  python3 -m lab.bussola            # gera BUSSOLA.md
  python3 -m lab.bussola fronteira  # imprime o ranking da fronteira
"""
import json
import os
import re
import sys

from lab import registro

RAIZ = registro.RAIZ
ARQ = os.path.join(RAIZ, "registro", "habilidades.json")
SAIDA = os.path.join(RAIZ, "BUSSOLA.md")


def carregar(caminho=None):
    with open(caminho or ARQ) as fh:
        d = json.load(fh)
    hab = {h["id"]: h for h in d["habilidades"]}
    for h in hab.values():
        for p in h["prereqs"]:
            if p not in hab:
                raise ValueError(f"{h['id']}: pre-requisito inexistente {p}")
    for g in d["goals"]:
        for r in g["requer"]:
            if r not in hab:
                raise ValueError(f"{g['id']}: habilidade inexistente {r}")
    _checar_ciclos(hab)
    return hab, d["goals"]


def _checar_ciclos(hab):
    estado = {}

    def visita(i, pilha):
        if estado.get(i) == 1:
            raise ValueError("ciclo de pre-requisitos: " + " -> ".join(pilha + [i]))
        if estado.get(i) == 2:
            return
        estado[i] = 1
        for p in hab[i]["prereqs"]:
            visita(p, pilha + [i])
        estado[i] = 2
    for i in hab:
        visita(i, [])


def _nivel(texto):
    m = re.search(r"N(\d)", texto or "")
    return int(m.group(1)) if m else 0


def desbloqueadas(hab, nos=None):
    nos = registro.carregar() if nos is None else nos
    por_id = {n["id"]: n for n in nos}
    ok = set()
    for h in hab.values():
        prova = h.get("desbloqueada_por") or []
        if prova and all(p in por_id and _nivel(por_id[p].get("nivel")) >= h["nivel_minimo"] for p in prova):
            ok.add(h["id"])
    return ok


def ancestrais(hab, i):
    vistos = set()
    pilha = list(hab[i]["prereqs"])
    while pilha:
        p = pilha.pop()
        if p not in vistos:
            vistos.add(p)
            pilha.extend(hab[p]["prereqs"])
    return vistos


def descendentes(hab, i):
    return {j for j in hab if i in ancestrais(hab, j)}


def analisar(hab, goals, ok):
    fronteira = [i for i in hab if i not in ok and all(p in ok for p in hab[i]["prereqs"])]
    rank = []
    for i in fronteira:
        desc = descendentes(hab, i)
        gs = [g["id"] for g in goals if any(r == i or i in ancestrais(hab, r) for r in g["requer"])]
        prio = (1 + len(desc) + 3 * len(gs)) / hab[i]["custo"]
        rank.append(dict(id=i, prio=prio, desc=len(desc), goals=gs))
    rank.sort(key=lambda r: -r["prio"])
    prog = {}
    for g in goals:
        necessarias = set(g["requer"])
        for r in g["requer"]:
            necessarias |= ancestrais(hab, r)
        feitas = necessarias & ok
        faltam = [i for i in necessarias if i not in ok]
        prog[g["id"]] = dict(feitas=len(feitas), total=len(necessarias), faltam=sorted(faltam))
    return fronteira, rank, prog


def gerar():
    hab, goals = carregar()
    ok = desbloqueadas(hab)
    _, rank, prog = analisar(hab, goals, ok)
    icone = lambda i: "🟩" if i in ok else ("🟨" if all(p in ok for p in hab[i]["prereqs"]) else "⬜")  # noqa: E731
    L = ["# BÚSSOLA — árvore de habilidades e goals", "",
         "*Gerado por `python3 -m lab.bussola` a partir de `registro/habilidades.json` e da árvore de experimentos. Não editar à mão.*",
         "Narrativa e critérios dos goals: [`GOALS.md`](GOALS.md).", "",
         "🟩 desbloqueada (com evidência) · 🟨 na fronteira (pode ser atacada agora) · ⬜ trancada", "",
         "## Goals (estrelas-guia)", "",
         "| goal | progresso | faltam | nível exigido |", "|---|---|---|---|"]
    for g in goals:
        p = prog[g["id"]]
        barra = "█" * p["feitas"] + "░" * (p["total"] - p["feitas"])
        L.append(f"| **{g['id']}** {g['nome']} | {barra} {p['feitas']}/{p['total']} | {', '.join(p['faltam'])} | N{g['nivel_exigido']} |")
    L += ["", "## Fronteira: o que atacar agora (maior prioridade primeiro)", "",
          "Prioridade = (1 + habilidades que dependem desta + 3 × goals que ela abre) ÷ custo.", "",
          "| # | habilidade | prioridade | abre | goals | hipóteses na fila |", "|---|---|---|---|---|---|"]
    for n, r in enumerate(rank, 1):
        h = hab[r["id"]]
        L.append(f"| {n} | {icone(r['id'])} **{r['id']}** {h['nome']} ({h['sistema']}) | {r['prio']:.1f} | {r['desc']} | "
                 f"{', '.join(r['goals']) or '—'} | {', '.join(h.get('hipoteses', [])) or '—'} |")
    L += ["", "## Árvore (pré-requisitos → habilidade)", ""]
    for i, h in hab.items():
        pre = " + ".join(hab[p]["id"] for p in h["prereqs"]) or "raiz"
        prova = f" — por {', '.join(h['desbloqueada_por'])}" if i in ok else ""
        L.append(f"- {icone(i)} **{i}** {h['nome']} · {h['sistema']} · {h['escada']} · requer: {pre}{prova}  ")
        L.append(f"  critério: {h['criterio']} (≥ N{h['nivel_minimo']})")
    L += ["", "## Mapa de dependências", "", "```"]
    filhos = {i: [j for j in hab if i in hab[j]["prereqs"]] for i in hab}
    impressos = set()

    def rec(i, prof):
        marca = "✔" if i in ok else ("◐" if all(p in ok for p in hab[i]["prereqs"]) else "·")
        rep = " (↑ já mostrado)" if i in impressos else ""
        L.append(f"{'  ' * prof}{marca} {i} {hab[i]['nome']}{rep}")
        if i in impressos:
            return
        impressos.add(i)
        for f in filhos[i]:
            rec(f, prof + 1)
    for i in hab:
        if not hab[i]["prereqs"]:
            rec(i, 0)
    for g in goals:
        L.append(f"★ {g['id']} {g['nome']} ⇐ {', '.join(g['requer'])}")
    L.append("```")
    with open(SAIDA, "w") as fh:
        fh.write("\n".join(L) + "\n")
    return SAIDA, rank


def main(argv):
    if len(argv) > 1 and argv[1] == "fronteira":
        hab, goals = carregar()
        ok = desbloqueadas(hab)
        for r in analisar(hab, goals, ok)[1]:
            print(f"{r['id']:4s} prio {r['prio']:5.1f}  abre {r['desc']:2d}  goals {','.join(r['goals']) or '-'}  {hab[r['id']]['nome']}")
    else:
        print("escrito:", gerar()[0])


if __name__ == "__main__":
    main(sys.argv)
