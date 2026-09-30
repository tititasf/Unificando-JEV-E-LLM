# E017 — Relatório: lei de temperatura da relaxação suave (caminho mínimo e BFS, n = 16 → 320)

**Veredito: PROMOVER.** P1-BF, P1-BFS e P2-BF passam, e em BFS LEI ≥ DT − 0,01 (1,000 = 1,000). O critério pré-registrado está cumprido e **a H11 está desbloqueada (N2)**. A ressalva: em BFS os dois braços saturam, então "bater o DT" só discrimina no caminho mínimo.

Nível: **N2**:
- pré-registrado;
- 10 sementes;
- sementes de teste derivadas do commit `73c69f1`;
- reprodução IDÊNTICA;
- guarda OK.

**Novidade: baixa.** Wittig et al. (ICML 2026) provam a generalização de tamanho do Bellman-Ford com regularização e treino curado. Aqui a temperatura vem de uma lei derivada do mecanismo de falha medido.

## Previsões
| # | Previsto | Prob. | Obtido | Status |
|---|---|---|---|---|
| P1-BF | LEI n=160 ≥ 0,95 | 0,80 | **0,993** [0,984; 0,998] | ✅ |
| P1-BFS | LEI n=160 ≥ 0,95 | 0,85 | 1,000 | ✅ |
| P2-BF | LEI > DT n=160, p < 0,05 | 0,85 | 0,993 contra **0,615**; p = 0,0002; P(LEI>DT) = 1,00 | ✅ |
| P2-BFS | LEI > DT n=160, p < 0,05 | 0,10 | 1,000 = 1,000 | 🟥 (previsto) |
| P3 | CONST_B0 n=160 ≤ 0,90 | 0,75 | 0,584 (esgota 640 passos) | ✅ |
| P4 | LEI_B < LEI − 0,03 | 0,65 | 0,443 | ✅ |
| P5 | LEI n=320 (20×) ≥ 0,95 | 0,70 | **0,991** [0,983; 0,997] | ✅ |

**Brier: 0,05.**

## Painel BF (acurácia de ponteiros, IQM)
| n | DT | LEI | LEI_B | CONST_B0 | GULOSO |
|---|---|---|---|---|---|
| 16 | 0,955 | 0,994 | 0,882 | 0,966 | 0,552 |
| 64 | 0,802 | 0,993 | 0,649 | 0,696 | 0,511 |
| 160 | 0,615 | **0,993** | 0,443 | 0,584 | 0,501 |
| 320 | — | **0,991** | — | — | — |

Passos até o ponto fixo:
- LEI: 5,8 → 8,4 → 10,2 → 12,3, que acompanha a profundidade em saltos da árvore;
- DT: 15,6 → 60 → 446 (deriva);
- CONST_B0: esgota o orçamento de passos.

Parâmetros aprendidos:
- LEI: κ = e^0,8 a e^1,5 (2,3 a 4,4); a ≈ 1,00 ± 0,05; b = 0.
- CONST_B0: aprende β ≈ e^4,6 ≈ 100, suficiente em n = 16 e insuficiente depois.

## O que foi mostrado
1. **O erro fora da distribuição do E016 tem causa identificada e corrigida.**
   - A causa é a descida do soft-min, com duas fontes: o termo de volta nas arestas baratas (a escala é 1/w_min) e os pais empatados (a escala é ln g, a lei do E013).
   - Com β = κ·ln(g_max)/(a·w_min), b = 0 e κ aprendido em n = 16, o motor mantém 0,99 até 20× o tamanho do treino.
2. **As duas peças são necessárias.**
   - Sem a lei (CONST_B0), o motor cai para 0,58 e não converge.
   - Com a lei mas b livre (LEI_B), o treino volta a usar b como compensador e o motor cai para 0,44. **O viés aditivo é o que quebra a extrapolação**, mesmo com a temperatura certa.
3. **A perda progressiva (DT) não basta.** Ela ajuda, mas não corrige a escala da temperatura (0,62 em 10×).
4. **Em BFS com p = 0,5 a tarefa satura.** Com pesos iguais, b não distorce a ordem, e o DT também acerta 1,000.

## Revisor hostil
1. *"Com β enorme o motor é o Bellman-Ford duro. A lei só diz 'afie muito'."* Em parte, sim.
   - Em n = 160 o β efetivo é da ordem de 10⁴ a 10⁵; o motor é praticamente o algoritmo exato, e os passos seguem a profundidade da árvore.
   - O que o experimento mostra é que **o treino sozinho não chega lá**: DT e CONST_B0 aprendem β ≈ 40–100, suficiente em n = 16.
   - A lei dá o **quanto** afiar, e o κ aprendido em n = 16 vale em 20×. É o mesmo atalho do E013, declarado.
2. *"A lei usa w_min do grafo de teste."* É uma grandeza de entrada, sem rótulo, lida em O(E), como a margem do E013.
3. *"Cinco parâmetros e alinhamento dado."* Sim. A H11 pede extrapolação de 10× contra o DT com IC, e não um motor genérico. O G1 (motor genérico e prova automática) continua aberto.

## Correções
- No E016 (hipótese semeada H-bf-lei), a lei proposta era β ∝ ln(grau). **Está incompleta:** o fator dominante no caminho mínimo é 1/w_min (a deriva nos 2-ciclos). ln(grau) sozinho não basta; ele é o fator que resolve o BFS.

## Hipóteses semeadas
- **H-bf-prova (→ G1, S2 D18–D19):** extrair o programa do motor LEI (a ≈ 1, b = 0, β → ∞ ⇒ relaxação min) e verificar automaticamente que ele é o Bellman-Ford. É o primeiro passo do G1 com um motor aprendido.
- **H-lei-unificada:** a mesma receita (medir a descida da normalização no próprio dado e escalar β por ela) em BFS esparso, em árvore geradora mínima e no S2 de T1/T2. Uma lei para as três famílias?
- **H-busca-cert (→ H24):** amortização verificada numa família de busca, em que resolver ≫ verificar (M009).
