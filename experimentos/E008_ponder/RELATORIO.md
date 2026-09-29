# E008 — Relatório: PonderNet reimplementada como linha de base

**Veredito: REPLICADO.** Habilidade **H22 desbloqueada** (N2: pré-registrado, 10 sementes, sementes de teste derivadas do commit `487586f`, reproduzido de checkout limpo, guarda OK). **Novidade: nenhuma** (replicação, era o objetivo).

## Previsões
| # | Previsto | Prob. | Obtido | Status |
|---|---|---|---|---|
| P1 | Spearman(d, passos) mediana ≥ 0,8 | 0,85 | **1,00** (mínimo 1,00) | ✅ |
| P2 | acc d ≤ 4, IQM ≥ 0,95 | 0,85 | 1,000 | ✅ |
| P3 | acc d = 5..9 (fora da distribuição) ≥ 0,90 | 0,75 | 1,000 | ✅ |
| P4 | passos PonderNet ≤ CONV + 1 | 0,20 | 10,49 contra 5,63 | 🟥 (esperado pelo piloto) |

**Brier: 0,04.**

## O que foi mostrado
1. **A reimplementação faz o que o artigo diz:** passos = d + 6 (crescem exatamente com a dificuldade), 100% de acerto, inclusive fora da distribuição de treino. Temos uma linha de base publicada confiável para S3 e S0.
2. **O custo da PonderNet:** ela gasta ~5 passos a mais que a parada por ponto fixo (CONV), que também acerta 100% sem abstenções em N=12. O prior geométrico (λ_p = 0,2) e o limiar de 0,5 na probabilidade acumulada fazem a cabeça esperar. Em N=12 o nosso S3 por regra é **~1,9× mais barato** com o mesmo acerto. Isso vira hipótese para G5 (pensar com o custo certo), não conclusão: a PonderNet não foi ajustada (β, λ_p) e o teste é só em N=12.
3. **Deep Thinking:** implementado e testado, mas sem *overthinking* no motor estruturado (M006). O efeito será reavaliado com latente livre (H09).

## Revisor hostil
1. *"Tarefa fácil demais para a PonderNet."* Sim, declarado: o objetivo era validar a reimplementação, não testá-la em escala.
2. *"A comparação de custo é injusta: a PonderNet não foi ajustada."* Correto. Por isso o item 2 é hipótese (H-custo-ponder), não achado.
3. *"Spearman = 1 é bom demais."* Os passos saem exatamente d + 6 porque os sinais de entrada da cabeça (entropia, máx z, mudança) viram um degrau limpo no instante em que o motor chega à raiz; a cabeça aprende "espere ~5 passos depois de estabilizar". Coerente com o motor legível em N=12.

## Hipóteses semeadas
- **H-custo-ponder (G5):** com β e λ_p ajustados na validação, a PonderNet alcança o custo do CONV? E em N grande (regime difusivo), qual das duas quebra primeiro?
