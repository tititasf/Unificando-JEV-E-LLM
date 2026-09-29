# E008 — Pré-registro: a PonderNet reimplementada reproduz o efeito publicado?

**Escrito antes de rodar o teste. Não editar depois da primeira execução completa.**
Trilha B (infra de linhas de base). Átomos: 3.1. Nível de partida: implementação com gradiente verificado (testes unitários).
Habilidade-alvo: **H22** (prioridade 19; critério revisado antes deste PREREG, ver nó M006). Nó pai: **E001**. Operador: **REPLICAR** (reproduzir o efeito publicado da PonderNet).

## Hipótese
A cabeça de parada estilo PonderNet (`lab/baselines.py`), treinada só com d ≤ 4 sobre um
motor S2 congelado, aprende a pensar **mais em problemas mais difíceis** (o efeito central
de Banino et al., 2021), mantendo o acerto, inclusive fora da distribuição (d = 5 a 9).

## Relação com a literatura
PonderNet (Banino et al., 2021): parada aprendida com prior geométrico e KL; relata
passos crescendo com a complexidade e extrapolação. Aqui é uma **reimplementação mínima**
(cabeça de 4 parâmetros sobre motor congelado). Objetivo: ter uma linha de base
publicada confiável para os experimentos de S3/S0. Novidade: nenhuma (replicação).

## Piloto (declarado)
Com o modelo completo, sementes fora da faixa (880, 881), 20 exemplos por d:
passos = **d + 6** exatamente, acurácia 1,0 em d = 0…9 nas duas sementes. As
probabilidades abaixo usam o piloto. O piloto sugere que a PonderNet gasta ~5
passos a mais que a parada por ponto fixo (prior geométrico λ_p = 0,2).

## Montagem
- Motor: treino idêntico ao E001 (T1, N=12, d≤4, 600 iterações). Sementes de treino **800–809** (10).
- Cabeça: 300 trajetórias de treino (d ∈ 0..4), T_max = 16, β = 0,01, λ_p = 0,2, 150 iterações (gradiente por diferenças centrais). Inferência: para no primeiro t com probabilidade acumulada ≥ 0,5.
- Teste: sementes derivadas do commit deste PREREG; N=12; d ∈ 0..9; **30 exemplos por d**.
- Braços: **PonderNet** (linha de base publicada), **CONV** (parada por ponto fixo, E004; o nosso S3 por regra), **FIXO** (T_max = 16 sempre; o mais simples).

## Sementes e poder
- 30 por d × 10 sementes = 300 por d. Spearman sobre 10 valores de d por semente.
- Custo estimado: ~5 min de CPU.

## Previsões
| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1 | Spearman(d, passos PonderNet), mediana entre sementes ≥ 0,8 | 0,85 | mediana < 0,5 → **H22 fica trancada** (a reimplementação não reproduz o efeito) |
| P2 | acc PonderNet em d ≤ 4, IQM ≥ 0,95 | 0,85 | < 0,8 → H22 fica trancada |
| P3 | acc PonderNet em d = 5..9 (fora da distribuição), IQM ≥ 0,90 | 0,75 | — |
| P4 | passos médios PonderNet ≤ passos CONV + 1 | 0,20 | — (o piloto sugere ~+4 a +5) |

**H22 desbloqueada** (N1) se P1 e P2 passam.

## Guarda do avaliador
```
experimentos/E008_ponder/e008.py   : 55f65339739d3260
lab/baselines.py                   : b93abd354fc2b361
experimentos/E001_mlu/mlu.py       : 601604873fae9691
lab/sementes.py                    : 4a5e4da1269f9b77
```

## Ameaças conhecidas
- O motor congelado já converge de forma legível em N=12 (E004): a PonderNet tem uma tarefa fácil. Isso não testa a PonderNet em escala; testa se a reimplementação faz o que o artigo diz.
- O teto T_max = 16 limita d ≤ 9 se os passos forem d + 6 (d = 10 já bateria no teto).
