# Plano: o Ciclo de Evolução

A meta é **descobrir e provar** uma forma de unir decisão rápida (S1),
raciocínio latente (S2) e metacognição (S3) — e depois orçamento (S0),
enxame (S4/S5) e simulação (S6) — que seja mensuravelmente melhor que o
que existe. "Provar" segue a régua de [`docs/VALIDACAO.md`](docs/VALIDACAO.md).

O plano não é uma lista fixa. É um **laço que se alimenta**: cada ciclo
termina produzindo as hipóteses do próximo.

## 1. O laço

```
        ┌───────────────────────────────────────────────────────────────┐
        │ 0. LER     CLAUDE.md, ESTADO.md, LICOES.md, fim do DIARIO,    │
        │            EVOLUTION_LOG do tema, LIVRO.md (meta-métricas)    │
        │ 1. ESCOLHER  política de busca (§3) → nó pai + operador       │
        │            + alvo = degrau N+1; rejeitar duplicata na árvore  │
        │ 2. CHECAR NOVIDADE  busca na literatura → registrar           │
        │ 3. PRÉ-REGISTRAR  hipótese, previsões COM PROBABILIDADE,      │
        │            critério de morte, hashes do avaliador → commit    │
        │ 4. CONSTRUIR  só o degrau N+1, uma mudança atômica            │
        │ 5. RODAR   smoke → completo (teste congelado, 1 vez)          │
        │ 6. MEDIR   painel com lab/estat.py                            │
        │ 7. ATACAR  revisor hostil + guarda (verificar) + reprodução   │
        │            limpa se for promover a N2+                         │
        │ 8. DECIDIR  PROMOVER | MATAR | PIVOTAR                        │
        │ 9. ESCALAR  EVOLUTION_LOG: diagnóstico, 30 degraus, transição │
        │10. SEMEAR  1–3 hipóteses na fila, cada uma com nó pai         │
        │11. REGISTRAR  nó na árvore → LIVRO.md → LICOES.md →           │
        │            ESTADO + DIARIO → commit → push                    │
        └────────────────────────────────┬──────────────────────────────┘
                                         └──► volta ao passo 0
```

Um ciclo deve caber em **uma sessão** (idealmente < 30 min de CPU). Se não
couber, a hipótese é grande demais: quebrá-la. A inspiração de cada peça do
laço (AIDE, AIDE², DGM, ShinkaEvolve, AI Scientist) está em
[`docs/RSI.md`](docs/RSI.md).

### Operadores (todo nó da árvore tem exatamente um)

| Operador | Quando usar |
|---|---|
| RASCUNHO | hipótese nova, sem pai direto no mesmo mecanismo |
| MELHORAR | **uma** mudança atômica sobre um nó (o efeito tem de ser atribuível) |
| DEPURAR | o nó pai falhou por bug ou premissa errada, não pela hipótese |
| REPLICAR | mesmo mecanismo em outra tarefa, escala ou família (sobe N1→N2→N3) |
| ABLAR | remover uma peça para achar a causa |
| DIAGNOSTICAR | pós-hoc; explica, nunca muda veredito |
| META | muda o próprio processo; avaliado pelas meta-métricas dos ciclos seguintes |

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

## 3. Política de busca (como escolher o próximo nó)

Inspirada no AIDE² ("seguir a linha promissora enquanto melhora; ao estagnar,
ramificar a partir do melhor") e no arquivo do DGM:

1. **Seguir a linha.** Se o último ciclo de um tema subiu degrau ou promoveu nível, o próximo ciclo continua no mesmo tema, no degrau N+1.
2. **Ramificar ao estagnar.** Se um tema está há **≥2 ciclos sem subir** (`ciclos_sem_subir` no LIVRO), troque de tema: parta do nó de maior nível de outro tema, ou de um *stepping stone* morto cuja lição abre caminho.
3. **Promover antes de explorar** (~70/30): um achado N1 que pode virar N2 vem antes de ideia nova.
4. **Matar rápido:** entre candidatos equivalentes, o de critério de morte mais barato primeiro.
5. **Infra desbloqueia:** se uma lição diz que a tarefa atual cega os testes (ex.: atrator), construir a tarefa nova vem antes.
6. **Rejeitar duplicatas:** se a hipótese já está na árvore, só entra como REPLICAR/MELHORAR citando o nó.
7. **Diversidade:** a cada 5 ciclos, pelo menos um em sistema ainda sem nenhum nó (S0, S4, S6…).

Prioridade dentro dessas regras = (ganho se der certo × probabilidade) ÷ custo.
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
