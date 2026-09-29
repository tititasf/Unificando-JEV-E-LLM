# Plano: o Ciclo de Evolução

A meta é **descobrir e provar** uma forma de unir decisão rápida (S1),
raciocínio latente (S2) e metacognição (S3) — e depois orçamento (S0),
enxame (S4/S5) e simulação (S6) — que seja mensuravelmente melhor que o
que existe. "Provar" segue a régua de [`docs/VALIDACAO.md`](docs/VALIDACAO.md).

O plano não é uma lista fixa. É um **laço que se alimenta**: cada ciclo
termina produzindo as hipóteses do próximo.

## 1. O laço

```
        ┌──────────────────────────────────────────────────────────┐
        │ 0. LER    CLAUDE.md, ESTADO.md, fim do DIARIO.md         │
        │ 1. ESCOLHER  hipótese do topo da fila (seção 3)          │
        │ 2. CHECAR NOVIDADE  busca na literatura → registrar      │
        │ 3. PRÉ-REGISTRAR   hipótese, previsão, critério de morte │
        │ 4. CONSTRUIR  o mínimo que testa, reusando lab/          │
        │ 5. RODAR   smoke → validação → teste congelado (1 vez)   │
        │ 6. MEDIR   painel completo com lab/estat.py              │
        │ 7. ATACAR  revisor hostil: 3 objeções + resposta         │
        │ 8. DECIDIR  PROMOVER | MATAR | PIVOTAR                   │
        │ 9. SEMEAR  1–3 novas hipóteses na fila                   │
        │10. REGISTRAR ESTADO.md + DIARIO.md → commit → push       │
        └───────────────────────────┬──────────────────────────────┘
                                    └──► volta ao passo 0
```

Um ciclo deve caber em **uma sessão** (idealmente < 30 min de CPU). Se não
couber, a hipótese é grande demais: quebrá-la.

## 2. Trilhas de pesquisa (as "direções")

| Trilha | Sistema | Pergunta central | Primeiro marco |
|---|---|---|---|
| **A. Fusão** | S1+S2 | Qual a melhor forma de a "intuição" e o "raciocínio" compartilharem o mesmo substrato? | Cristalização (colapso discreto) com evidência N2. |
| **B. Metacognição** | S3 | Um sistema pode saber quanto pensar e quando não sabe, de forma aprendida e calibrada? | Parada aprendida ≥ regra fixa, com E-AURC ≈ 0 fora da distribuição. |
| **C. Orçamento** | S0 | Um agente com "energia" finita aprende a gastar pensamento onde vale? | Fronteira de Pareto acurácia × custo que domina orçamento fixo. |
| **D. Enxame** | S4/S5 | Agentes que trocam vetores latentes superam os que trocam símbolos? | Tarefa de visão parcial em que a comunicação latente vence com IC. |
| **E. Simulação** | S6 | Simular futuros latentes antes de agir melhora a decisão? | Planejamento por rollouts latentes numa tarefa com efeitos atrasados. |

Cada trilha sobe a escada de tarefas T1→T6 (VALIDACAO.md §4). A trilha A
é a espinha: B–E usam o motor que ela produzir.

## 3. Como escolher a próxima hipótese

Prioridade = **(ganho se der certo × chance de dar certo) ÷ custo**, com duas regras:

1. **Promover antes de explorar.** Se existe um achado em N1 que pode subir para N2, ele vem primeiro (~70% dos ciclos). Ideias novas ficam com ~30%.
2. **Matar rápido.** Hipóteses com critério de morte barato vêm antes das caras.

A fila viva fica no [`ESTADO.md`](ESTADO.md).

## 4. Portões (quando mudar de fase)

| Fase | Portão para sair |
|---|---|
| 1. Micro (T1–T2) | Um mecanismo com N2 em ≥2 famílias de tarefas. |
| 2. Algorítmica (T3) | O mecanismo bate a linha de base recorrente publicada (Deep Thinking) em CLRS-like, com IC. |
| 3. Quebra-cabeças (T4) | Comparação direta com TRM/HRM em labirinto/Sudoku pequenos, no mesmo orçamento de parâmetros. |
| 4. Abstração (T5–T6) | Resultado em subconjunto do ARC-AGI com protocolo oficial. Aqui provavelmente é preciso sair do Python puro (pedir ao usuário). |

## 5. O que já foi feito

Ver `DIARIO.md` (cronologia) e `ESTADO.md` (placar e fila). Em resumo:
E001 (replicação N1), E002 (hipótese morta, achado A4 sobre o S3), E003
(N2: mensagens simbólicas; Σ1 parcialmente refutada). Próximo: H-T2.

## 6. Como rodar

```bash
python3 -m unittest lab.test_estat                    # a régua funciona?
python3 experimentos/E001_mlu/mlu.py                  # E001 (~30 s)
python3 experimentos/E001_mlu/reavaliar.py            # E001 com 10 sementes (~1,5 min)
python3 experimentos/E002_cristalizacao/e002.py       # E002 (~10 min)
python3 experimentos/E003_cristal_comum/e003.py       # E003 (~3 min)
```

No Claude Code, `/ciclo` executa um ciclo completo do laço.
