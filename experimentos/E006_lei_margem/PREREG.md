# E006 — Pré-registro: a lei N* (quando o pensamento se dissolve)

**Escrito antes de rodar (nem o smoke rodou). Não editar depois da primeira execução completa.**
Trilha A. Átomos: 2.1, 2.3. Nível de partida: A11 em N1 (E005d, 4 sementes).
Nó pai: **E005d**. Operador: **REPLICAR** (testar a lei com previsão por semente). Degrau: consolida S2 D04/D05 (não sobe degrau).

## Hipótese
H1 (lei): para cada modelo S2 treinado em T1, o N em que o pensamento deixa de andar
um salto por passo é previsto por uma propriedade de **um único passo**: N* = o N
em que o vazamento de um passo, a partir de um estado concentrado, chega a 0,5.
Abaixo de N* o S2 acerta; acima, ele se dissolve e erra.
H2 (A9 é artefato): o "atalho difusivo" do E004 só acerta quando o caminho domina
o grafo (d = N−5). Com d pequeno em relação a N, acima de N* ele erra.

## Relação com a literatura
- **Veličković et al., *Softmax Is Not Enough (for Sharp Size Generalisation)*, ICML 2025:** provam que circuitos de softmax aprendidos **precisam se dispersar** quando o número de itens cresce além do treino; propõem temperatura adaptativa. **Nossa lei é uma instância disso** num passo iterado.
- O que difere: prever, **por semente e a partir de um passo**, o N em que a dinâmica iterada muda de regime, e medir se a dispersão ainda acerta por equilíbrio (atalho do atrator) ou erra.
- Novidade esperada: **baixa a média**.

## Montagem
- Treino idêntico ao E001 (T1, N=12, d≤4, 600 iterações). Sementes **600–629** (30).
- N* por semente: bisseção em log N até o vazamento médio de um passo (5 grafos, d=20, a partir do nó inicial) = 0,5. Usa só o modelo, sem olhar acurácia.
- Teste congelado (sementes 110000+s), N = N* × {1/4, 1/2, 1, 2, 4} (mínimo 30, máximo 16384; células acima do máximo são puladas e declaradas):
  - **A:** d = 20, T = d+8, 10 exemplos. Acurácia do argmax e máx z final.
  - **B:** d = N−5 (caminho domina, como no E004), só se 4N* ≤ 2048; 5 exemplos.
- Passo O(N) exato (`passo_rapido.py`), verificado contra o passo original (erro 3e−16).
- N_c = cruzamento de acc = 0,5 na grade A (interpolação geométrica).
- Linhas de base: não há braço concorrente; o teste é de **previsão quantitativa**. A "linha de base" é a hipótese nula de que N* não informa N_c (Spearman ≈ 0; N_c espalhado).

## Previsões (probabilidades calibradas pela lição 10: evitar extremos)
| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1 | acc A ≥ 0,95 em N*/4 em ≥ 90% das sementes | 0,60 | — |
| P2 | acc A ≤ 0,5 em 4N* em ≥ 90% das sementes | 0,55 | — |
| P3 | N_c ∈ [N*/2, 2N*] em ≥ 80% das sementes com cruzamento | 0,45 | N_c fora de [N*/4, 4N*] em > 50% → **lei morta** |
| P4 | Spearman(N*, N_c) > 0,7 | 0,50 | ≤ 0,3 → **lei morta** (N* não informa) |
| P5 (H2) | onde há B: acc B ≥ 0,7 e acc A ≤ 0,3 em 4N*, em ≥ 70% dessas sementes | 0,50 | — |
| Morte geral | P1 e P2 falham juntas (nenhuma transição em torno de N*) | — | **lei morta** |

## Guarda do avaliador
```
experimentos/E006_lei_margem/e006.py          : ddd1da34a5896d90
experimentos/E006_lei_margem/passo_rapido.py  : 3aa24574de9b4029
experimentos/E001_mlu/mlu.py                  : 601604873fae9691
```

## Ameaças conhecidas
- N* é definido com o mesmo gerador de grafos do teste: é uma propriedade do modelo **na distribuição de grafos**, não só dos pesos. Honesto, mas menos "puro" que uma fórmula fechada.
- Sementes com N* muito grande terão células puladas (N > 16384): a amostra pode ficar enviesada para margens pequenas. Declarar quantas.
- 10 exemplos por célula dão resolução de 0,1 na acurácia.
