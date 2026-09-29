# E002 — Pré-registro: cristalização do estado latente

**Escrito antes de rodar.** Não editar depois da primeira execução do teste.
Trilha A (Fusão S1+S2). Nível de partida: N0/N1 (E001: contínuo colapsou em
3 de 14 sementes em d≥50; cristalizado 0 de 14; Fisher p≈0,22 → não significativo).

## Hipótese

H1: colapsar o estado latente para um ponto discreto a cada passo (argmax,
"cristalização") **reduz a taxa de colapso** em extrapolação extrema,
comparado ao estado contínuo, sem re-treino.

H2 (mecanismo): o colapso do estado contínuo é causado por uma margem
aprendida pequena entre "pai" e "outros" no passo latente: a massa que vaza
por passo ≈ (N−1)·e^(−margem). Sementes com margem menor colapsam mais.

## Montagem

- Treino idêntico ao E001 (N=12, d≤4, 600 iterações de Adam, BPTT). Só S2, sem S1.
- Sementes de treino: 200…229 (**30 sementes**).
- Teste congelado: sementes 30000+s; d ∈ {64, 128}; N = d+5; 12 exemplos por d; T_MAX = d+8.
- Braços (todos com o mesmo modelo treinado):
  - **CONT**: estado contínuo (softmax).
  - **CRIST**: argmax a cada passo.
  - **AFIA** (ablação): z ← z⁴ normalizado a cada passo (afiar sem discretizar).
    Separa "discretização" de "só afiar".
- Colapso: acurácia < 0,5 numa semente.

## Previsões e critérios

| # | Previsão | Critério de morte |
|---|---|---|
| P1 | Colapso CONT em d=128 ≥ 15% | Se < 5%: o problema não existe nesta escala → hipótese morta (nada a corrigir). |
| P2 | Colapso CRIST em d=128 ≤ 1/30 | Se CRIST ≥ CONT → **H1 morta**. |
| P3 | Fisher CRIST vs CONT, p < 0,01 | Se 0,01 ≤ p: inconclusivo, fica em N1. |
| P4 | AFIA fica entre CONT e CRIST | Se AFIA = CRIST: o mecanismo é "afiar", não "discretizar" → renomear o achado. |
| P5 (H2) | Correlação de Spearman entre margem aprendida e acurácia CONT > 0,3 | Se ≤ 0: H2 morta; o colapso tem outra causa. |

## Ameaças conhecidas

- Tarefa única (T1). Mesmo se tudo passar, o máximo é **N2 nesta tarefa**.
- A cristalização elimina superposição. Em tarefas que precisam manter
  várias hipóteses vivas, ela deve **piorar**. Isso não é testado aqui → E003.
- Relação com a literatura: discretização/"snap" de estado é uma ideia
  antiga (autômatos extraídos de RNNs, VQ); Buitrago et al. 2025 atribuem
  a falha de extrapolação a estados não explorados no treino. Novidade
  esperada: baixa a média. O valor aqui é a medida causal limpa.
