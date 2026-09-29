"""
lab/registro.py - a arvore de experimentos do laboratorio (inspirada no
"solution tree" do AIDE/Weco e no arquivo do Darwin Godel Machine).

Cada no = um experimento ou diagnostico. Fica em registro/arvore.jsonl
(uma linha JSON por no, somente acrescimo). A partir dela se gera o
LIVRO.md (livro de etapas) e as meta-metricas: as metricas de
auto-aperfeicoamento do proprio laboratorio.

Uso:
  python3 -m lab.registro livro        # regenera LIVRO.md
  python3 -m lab.registro metricas     # imprime as meta-metricas
  python3 -m lab.registro hash ARQ...  # sha256 para colar no PREREG (guarda do avaliador)
  python3 -m lab.registro verificar    # confere se avaliadores mudaram depois do pre-registro
"""
import hashlib
import json
import os
import sys

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ARQ = os.path.join(RAIZ, "registro", "arvore.jsonl")
LIVRO = os.path.join(RAIZ, "LIVRO.md")

OPERADORES = {
    "RASCUNHO": "hipotese nova a partir do zero",
    "MELHORAR": "uma mudanca atomica sobre o no pai",
    "DEPURAR": "consertar um experimento que falhou por bug ou premissa errada",
    "REPLICAR": "mesmo mecanismo em outra tarefa, escala ou semente",
    "ABLAR": "remover uma peca para achar a causa",
    "DIAGNOSTICAR": "pos-hoc: explicar um resultado (nao muda veredito)",
    "META": "mudanca no proprio processo do laboratorio (regua, laco, ferramentas)",
}
VEREDITOS = ("PROMOVER", "MATAR", "PIVOTAR", "REPLICADO", "INFORMATIVO", "PENDENTE")


def carregar():
    if not os.path.exists(ARQ):
        return []
    with open(ARQ) as fh:
        return [json.loads(l) for l in fh if l.strip()]


def adicionar(no):
    """Acrescenta um no (dict). Valida campos minimos."""
    for campo in ("id", "ciclo", "operador", "tema", "hipotese", "veredito"):
        if campo not in no:
            raise ValueError(f"no sem campo obrigatorio: {campo}")
    if no["operador"] not in OPERADORES:
        raise ValueError(f"operador invalido: {no['operador']}")
    if no["veredito"] not in VEREDITOS:
        raise ValueError(f"veredito invalido: {no['veredito']}")
    ids = {n["id"] for n in carregar()}
    if no["id"] in ids:
        raise ValueError(f"id repetido: {no['id']}")
    if no.get("pai") and no["pai"] not in ids:
        raise ValueError(f"pai inexistente: {no['pai']}")
    os.makedirs(os.path.dirname(ARQ), exist_ok=True)
    with open(ARQ, "a") as fh:
        fh.write(json.dumps(no, ensure_ascii=False) + "\n")


# ------------------------------------------------------------ guarda
def sha(caminho):
    h = hashlib.sha256()
    with open(os.path.join(RAIZ, caminho), "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()[:16]


def verificar():
    """Avaliadores registrados no PREREG nao podem mudar depois (licao do DGM:
    o agente apagou os proprios marcadores de deteccao para subir a nota)."""
    problemas = []
    for n in carregar():
        for caminho, h in (n.get("hashes") or {}).items():
            if not os.path.exists(os.path.join(RAIZ, caminho)):
                problemas.append(f"{n['id']}: {caminho} sumiu")
            elif sha(caminho) != h:
                problemas.append(f"{n['id']}: {caminho} mudou depois do pre-registro")
    return problemas


# ----------------------------------------------------- meta-metricas
def metricas(nos=None):
    nos = carregar() if nos is None else nos
    exps = [n for n in nos if n["operador"] not in ("DIAGNOSTICAR", "META")]
    decididos = [n for n in exps if n["veredito"] != "PENDENTE"]
    prev = [p for n in nos for p in n.get("previsoes", []) if p.get("acertou") is not None]
    com_prob = [p for p in prev if p.get("prob") is not None]
    brier = (sum((p["prob"] - (1.0 if p["acertou"] else 0.0)) ** 2 for p in com_prob) / len(com_prob)
             if com_prob else None)
    # degraus: maior degrau atingido por tema ao longo dos ciclos
    degraus = {}
    for n in sorted(nos, key=lambda x: x["ciclo"]):
        for tema, d in (n.get("degrau_atingido") or {}).items():
            degraus.setdefault(tema, []).append((n["ciclo"], d))
    ciclo_max = max((n["ciclo"] for n in nos), default=0)
    estagnacao = {}
    for tema, hist in degraus.items():
        ultimo_salto = hist[0][0]
        for (c0, d0), (c1, d1) in zip(hist, hist[1:]):
            if d1 > d0:
                ultimo_salto = c1
        estagnacao[tema] = ciclo_max - ultimo_salto
    por_op = {}
    for n in nos:
        por_op[n["operador"]] = por_op.get(n["operador"], 0) + 1
    novidade = {}
    for n in exps:
        k = n.get("novidade", "?")
        novidade[k] = novidade.get(k, 0) + 1
    cpu = [n["custo_cpu_s"] for n in nos if n.get("custo_cpu_s")]
    return {
        "ciclos": ciclo_max,
        "nos": len(nos),
        "nos_por_operador": por_op,
        "taxa_morte": (sum(n["veredito"] == "MATAR" for n in decididos) / len(decididos)) if decididos else None,
        "taxa_promocao": (sum(n["veredito"] in ("PROMOVER", "REPLICADO") for n in decididos) / len(decididos)) if decididos else None,
        "previsoes_avaliadas": len(prev),
        "acerto_previsoes": (sum(p["acertou"] for p in prev) / len(prev)) if prev else None,
        "brier_previsoes": brier,
        "degrau_por_tema": {t: h[-1][1] for t, h in degraus.items()},
        "ciclos_sem_subir": estagnacao,
        "novidade": novidade,
        "achados_corrigidos": sum(len(n.get("corrige", [])) for n in nos),
        "cpu_medio_s": (sum(cpu) / len(cpu)) if cpu else None,
        "problemas_guarda": verificar(),
    }


# --------------------------------------------------------------- livro
def _arvore_txt(nos):
    filhos = {}
    for n in nos:
        filhos.setdefault(n.get("pai"), []).append(n)
    linhas = []

    def rec(pai, prof):
        for n in filhos.get(pai, []):
            marca = {"PROMOVER": "▲", "MATAR": "✖", "PIVOTAR": "↻", "REPLICADO": "≡",
                     "INFORMATIVO": "·", "PENDENTE": "…"}[n["veredito"]]
            linhas.append(f"{'    ' * prof}{marca} {n['id']} [{n['operador']}, {n['tema']}] "
                          f"{n.get('titulo', '')} → {n['veredito']} {n.get('nivel', '')}")
            rec(n["id"], prof + 1)
    rec(None, 0)
    return "\n".join(linhas)


def gerar_livro():
    nos = carregar()
    m = metricas(nos)
    fmt = lambda x: "—" if x is None else (f"{x:.2f}" if isinstance(x, float) else str(x))  # noqa: E731
    L = ["# LIVRO DE ETAPAS", "",
         "*Gerado por `python3 -m lab.registro livro` a partir de `registro/arvore.jsonl`. Não editar à mão.*", "",
         "## Meta-métricas do laboratório (o laboratório medindo a si mesmo)", "",
         "| métrica | valor |", "|---|---|",
         f"| ciclos | {m['ciclos']} |",
         f"| nós na árvore | {m['nos']} ({', '.join(f'{k} {v}' for k, v in m['nos_por_operador'].items())}) |",
         f"| taxa de morte de hipóteses | {fmt(m['taxa_morte'])} |",
         f"| taxa de promoção/replicação | {fmt(m['taxa_promocao'])} |",
         f"| previsões avaliadas / acerto | {m['previsoes_avaliadas']} / {fmt(m['acerto_previsoes'])} |",
         f"| Brier das previsões (menor = pesquisador mais calibrado) | {fmt(m['brier_previsoes'])} |",
         f"| degrau atual por tema | {', '.join(f'{t} D{d:02d}' for t, d in m['degrau_por_tema'].items())} |",
         f"| ciclos sem subir degrau | {', '.join(f'{t} {v}' for t, v in m['ciclos_sem_subir'].items())} |",
         f"| novidade dos achados | {', '.join(f'{k} {v}' for k, v in m['novidade'].items())} |",
         f"| registros antigos corrigidos | {m['achados_corrigidos']} |",
         f"| CPU médio por nó (s) | {fmt(m['cpu_medio_s'])} |",
         f"| guarda do avaliador | {'OK' if not m['problemas_guarda'] else '; '.join(m['problemas_guarda'])} |",
         "", "## Árvore de experimentos", "",
         "▲ promover · ✖ matar · ↻ pivotar · ≡ replicado · · informativo · … pendente", "",
         "```", _arvore_txt(nos), "```", "", "## Etapas em ordem", ""]
    for n in nos:
        L.append(f"### {n['id']} — {n.get('titulo', '')} (ciclo {n['ciclo']}, {n.get('data', '')})")
        L.append(f"- **Operador:** {n['operador']} · **pai:** {n.get('pai') or '—'} · **tema:** {n['tema']}"
                 f" · **degrau-alvo:** {n.get('degrau_alvo', '—')}")
        L.append(f"- **Hipótese:** {n['hipotese']}")
        L.append(f"- **Veredito:** {n['veredito']} · **nível:** {n.get('nivel', '—')} · **novidade:** {n.get('novidade', '—')}")
        if n.get("metrica"):
            L.append(f"- **Métrica principal:** {n['metrica']['nome']} = {n['metrica']['valor']}")
        if n.get("previsoes"):
            L.append("- **Previsões:** " + "; ".join(
                f"{p['id']} {'✅' if p['acertou'] else ('🟥' if p['acertou'] is False else '—')}"
                + (f" (p={p['prob']})" if p.get('prob') is not None else "") for p in n["previsoes"]))
        for lic in n.get("licoes", []):
            L.append(f"- **Lição:** {lic}")
        if n.get("corrige"):
            L.append(f"- **Corrige:** {', '.join(n['corrige'])}")
        if n.get("semeou"):
            L.append(f"- **Semeou:** {', '.join(n['semeou'])}")
        refs = [f"[{k}]({v})" for k, v in (n.get("arquivos") or {}).items()]
        if refs:
            L.append(f"- **Arquivos:** {' · '.join(refs)}")
        L.append(f"- **Commits:** pré-registro `{n.get('commit_prereg', '—')}` · resultado `{n.get('commit_resultado', '—')}`")
        L.append("")
    with open(LIVRO, "w") as fh:
        fh.write("\n".join(L))
    return LIVRO


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "livro"
    if cmd == "livro":
        print("escrito:", gerar_livro())
    elif cmd == "metricas":
        print(json.dumps(metricas(), indent=1, ensure_ascii=False))
    elif cmd == "hash":
        print(json.dumps({a: sha(a) for a in argv[2:]}, indent=1))
    elif cmd == "verificar":
        p = verificar()
        print("OK" if not p else "\n".join(p))
        sys.exit(1 if p else 0)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv)
