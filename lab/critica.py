"""
lab/critica.py - autocritica do norte (o S3 do proprio laboratorio). Regra 19 do CLAUDE.md.

Roda no inicio de todo ciclo, antes de ESCOLHER. Mede, a partir da arvore de experimentos,
os sinais de autoengano e de rumo, e imprime as perguntas que o pesquisador responde em
CRITICA.md (uma entrada por ciclo, com uma decisao: APROFUNDAR | VARIAR | ENDURECER | PIVOTAR).

Uso: python3 -m lab.critica
"""
import json
import os
from collections import Counter

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DECISOES = ("APROFUNDAR", "VARIAR", "ENDURECER", "PIVOTAR")

PERGUNTAS = [
    "1. Novo para o mundo? O ultimo ciclo produziu algo que um especialista da area acharia novo (nao so novo para nos)?",
    "2. Trabalho mais proximo: qual e, e em que numero mensuravel ja o superamos (ou por que ainda nao)?",
    "3. Escolha honesta: a pergunta atual foi escolhida porque importa ou porque cabe no orcamento?",
    "4. Profundidade x variedade: o foco ainda tem hipotese viva com chance > 20% de resultado novo? "
    "Se 3 ciclos seguidos sem avanco mensuravel no foco -> VARIAR ou PIVOTAR.",
    "5. Autoengano: atalho trivial, metrica fraca, previsao feita depois do piloto, benchmark saturado?",
    "6. Revisor externo hostil: o que ele mataria primeiro? Da para testar isso ja neste ciclo?",
    "7. Norte: o goal/foco atual ainda e o melhor uso do tempo, dada a literatura (docs/LITERATURA_*.md)?",
    "8. Meta (RSI da propria critica): a decisao da critica anterior foi seguida e deu resultado? "
    "Se a critica errou, que pergunta ou alerta faltou? Edite lab/critica.py para inclui-la.",
]


def carregar():
    with open(os.path.join(RAIZ, "registro", "arvore.jsonl")) as fh:
        return [json.loads(linha) for linha in fh if linha.strip()]


def classe_novidade(txt):
    t = (txt or "").lower()
    if t.startswith(("alta", "media", "média", "possivelmente nova")):
        return "candidata"
    if t.startswith(("nenhuma", "replica")):
        return "nenhuma"
    return "baixa"


def brier(nos):
    ps = [(p["prob"], 1.0 if p["acertou"] else 0.0) for n in nos for p in n.get("previsoes", [])
          if isinstance(p.get("prob"), (int, float)) and isinstance(p.get("acertou"), bool)]
    return (sum((a - b) ** 2 for a, b in ps) / len(ps), len(ps)) if ps else (None, 0)


def painel():
    nos = carregar()
    exps = [n for n in nos if n["id"].startswith("E")]
    ciclo = max(n["ciclo"] for n in nos)
    nov = Counter(classe_novidade(n.get("novidade")) for n in exps)
    cand = [n for n in exps if classe_novidade(n.get("novidade")) == "candidata"]
    ult_cand = max((n["ciclo"] for n in cand), default=0)
    externos = [n for n in exps if n.get("externo")]
    temas = [n.get("tema") for n in sorted(exps, key=lambda n: n["ciclo"])]
    seq = 1
    for a, b in zip(reversed(temas), list(reversed(temas))[1:]):
        if a != b:
            break
        seq += 1
    b_all, n_all = brier(exps)
    b_rec, n_rec = brier([n for n in exps if n["ciclo"] > ciclo - 5])
    niveis = Counter(n.get("nivel") for n in exps)
    L = [f"# Autocritica do norte - ciclo {ciclo + 1} (antes de escolher)", "",
         f"- experimentos: {len(exps)} | niveis: {dict(niveis)}",
         f"- novidade: nenhuma {nov['nenhuma']} · baixa {nov['baixa']} · candidata a nova {nov['candidata']}"
         f" (ultima candidata: ciclo {ult_cand}; {ciclo - ult_cand} ciclos atras)",
         f"- comparados com numero publicado em benchmark externo (campo 'externo'): {len(externos)}/{len(exps)}",
         f"- tema do ultimo experimento: {temas[-1] if temas else '-'} ({seq} experimento(s) seguidos no mesmo tema)",
         f"- Brier geral {b_all:.3f} ({n_all} previsoes) · ultimos 5 ciclos {b_rec:.3f} ({n_rec})"
         if b_all is not None else "- Brier: sem dados",
         "  (atencao: previsoes feitas depois de pilotos inflam a calibracao; conte so as feitas antes de ver dados)", ""]
    alertas = []
    if nov["candidata"] == 0 or ciclo - ult_cand >= 5:
        alertas.append("ALERTA: 5+ ciclos sem nada candidato a novo -> o norte esta produzindo replicacoes.")
    if len(externos) == 0:
        alertas.append("ALERTA: nenhum resultado comparado com numero publicado externo.")
    if b_rec is not None and b_rec < 0.08:
        alertas.append("ALERTA: calibracao boa demais -> as perguntas podem estar faceis ou pos-piloto.")
    L += alertas + ([""] if alertas else [])
    L += ["Responda em CRITICA.md (## Ciclo N), de 5 a 15 linhas, e termine com 'Decisao: " + " | ".join(DECISOES) + "':", ""]
    L += PERGUNTAS
    return "\n".join(L)


if __name__ == "__main__":
    print(painel())
