import sys
sys.path.insert(0, "/home/user/Unificando-JEV-E-LLM")
from lab import registro as R

R.adicionar({
    "id": "M010", "titulo": "Pilotos G1: rede generica sem dicas, sonda e extracao (SP/WP)", "ciclo": 18,
    "data": "2026-09-30", "operador": "DIAGNOSTICAR", "pai": "E017", "tema": "S2",
    "hipotese": "Um MPNN generico sem dicas extrapola em SP/WP e sua regra pode ser extraida automaticamente?",
    "veredito": "INFORMATIVO", "nivel": "N0",
    "licoes": ["MPNN generico (agregacao max, lr 5e-4, corte 1,0) extrapola: SP 0,94->0,82, WP 0,98->0,95 (n=16->64); soma explode.",
               "A sintese direta sem rede acha o programa: o braco que o revisor pediria virou parte do E018.",
               "WP: aresta mais pesada = pai valido (arvore geradora maxima); ponteiro trivial."],
    "custo_cpu_s": 3000,
    "arquivos": {"relatorio": "experimentos/E018_extracao/pilotos/LEIAME.md"},
})
R.adicionar({
    "id": "E018", "titulo": "Extrair da rede generica ou sintetizar direto? (SP min-plus, WP max-min)", "ciclo": 18,
    "data": "2026-09-30", "operador": "RASCUNHO", "pai": "E017", "tema": "S2", "atomos": ["2.1"],
    "degrau_alvo": "S2:D18",
    "hipotese": "H-rede-superflua: na mesma linguagem de regras, a sintese direta (sem rede) recupera a relaxacao do semianel em >=80% das sementes, e a extracao da rede generica sem dicas recupera menos.",
    "veredito": "INFORMATIVO", "nivel": "N1",
    "novidade": "baixa (a rota da rede funciona no SP, mas a sintese direta faz o mesmo sem rede)",
    "externo": False,
    "metrica": {"nome": "programas reconhecidos como relaxacao exata (regra+ponteiro+inicio)",
                "valor": "SP: mecanistica 5/5, comportamental 5/5, sintese 5/5; WP: 0/5, 0/5, 5/5; sintese 10/10 vs 5/10 (Fisher p=0,033); programa 1,000 em n=256; rede 0,799 (SP) e 0,892 (WP) em n=64"},
    "previsoes": [
        {"id": "P1-SP", "texto": "sintese >=4/5", "prob": 0.9, "acertou": True, "pos_piloto": True},
        {"id": "P1-WP", "texto": "sintese >=4/5", "prob": 0.9, "acertou": True, "pos_piloto": True},
        {"id": "P2-SP", "texto": "comportamental >=4/5", "prob": 0.55, "acertou": True, "pos_piloto": True},
        {"id": "P2-WP", "texto": "comportamental >=4/5", "prob": 0.2, "acertou": False, "pos_piloto": True},
        {"id": "P3-SP", "texto": "mecanistica >=4/5", "prob": 0.45, "acertou": True, "pos_piloto": True},
        {"id": "P3-WP", "texto": "mecanistica >=4/5", "prob": 0.15, "acertou": False, "pos_piloto": True},
        {"id": "P4", "texto": "reconhecidos 1,000 em n=256", "prob": 0.95, "acertou": True, "pos_piloto": True},
        {"id": "P5-SP", "texto": "rede <0,99 em n=64", "prob": 0.97, "acertou": True, "pos_piloto": True},
        {"id": "P5-WP", "texto": "rede <0,99 em n=64", "prob": 0.9, "acertou": True, "pos_piloto": True},
        {"id": "P6", "texto": "sintese > comportamental", "prob": 0.75, "acertou": True, "pos_piloto": True},
    ],
    "licoes": ["Rede generica sem dicas guarda a relaxacao exata do BF nas transicoes (SP 5/5, prova por reducao para todo n), mas a sintese direta sem rede faz o mesmo: a rede e superflua nestas familias.",
               "Rede boa em ponteiro pode ser infiel nos valores (WP): a extracao herda os erros; acuracia de ponteiro nao mede fidelidade."],
    "semeou": ["H-G1-busca", "H-mec-pura", "H-G1-externo"],
    "custo_cpu_s": 6997,
    "hashes": {"experimentos/E018_extracao/e018.py": "f6bb6bab1251c388", "lab/tarefas_clrs.py": "fd2b3258eb55e4f4",
               "lab/sementes.py": "4a5e4da1269f9b77", "lab/estat.py": "40af21b3e5c3d582"},
    "commit_prereg": "8b5da77",
    "arquivos": {"prereg": "experimentos/E018_extracao/PREREG.md", "relatorio": "experimentos/E018_extracao/RELATORIO.md"},
})
print("ok")
