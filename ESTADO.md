# ESTADO — onde estamos

Atualizado no fim de cada ciclo. Última atualização: ciclo 6 (2026-09-29).

> Norte: [`GOALS.md`](GOALS.md) · o que atacar agora: [`BUSSOLA.md`](BUSSOLA.md) (fronteira: H04 → H06 → H13 → H21).

## Fase atual

**Fase 1 — Micro (T1–T2): portão formalmente atingido no ciclo 5** (passo latente iterado com N2 em T1 e T2). Ressalva: mecanismo **conhecido** (replicação).
Antes da Fase 2 (T3, algoritmos contra Deep Thinking): fechar a lei de nitidez (H04), validar as linhas de base publicadas (H22) e o protocolo CLRS reimplementado (H23).
Infra disponível: T2 sem atrator (`experimentos/E005_t2_salto/tarefa_t2.py`), passo O(N) (`experimentos/E006_lei_margem/passo_rapido.py`), linhas de base (`lab/baselines.py`), tarefas CLRS (`lab/tarefas_clrs.py`), sementes derivadas do commit (`lab/sementes.py`), controle de qualidade (`lab/checar.py`).
Calibração do pesquisador: ver `LIVRO.md` (Brier do último ciclo: 0,25).

## Placar de achados

| Id | Achado | Nível | Novidade | Fonte |
|---|---|---|---|---|
| A1 | Iterar um passo latente de 33 parâmetros extrapola 25× a profundidade do treino (T1) | N1 | replicação (Deep Thinking) | E001 |
| A2 | Parar por convergência economiza 54% do compute sem perder acerto | N1 | replicação (ACT/PonderNet) | E001 |
| A3 | Colar S1 (confiança) na frente do S2 piora: 0,976 vs 1,000 | N1 | pequena | E001 |
| A4 | **S3 com limiar absoluto de confiança não escala:** se abstém em 100% dos casos com N≥64, embora o S2 acerte | N2 (negativo, pré-registrado) | provável boa contribuição metodológica | E002 |
| A5 | Cristalizar o estado **não** estabiliza o pensamento em T1 (0/30 colapsos sem ela) | N2 (negativo) | — | E002 |
| A6 | **Mensagens simbólicas > analógicas** sob ruído, com conhecimento fragmentado entre 2 agentes, sem re-treino: +0,59 a +0,81, p<1e-45, ~200× menos dados por passo | N2 | baixa (comunicação digital) | E003 |
| A7 | Tarefas-atrator mascaram o acúmulo de erros | N1 (diagnóstico) | metodológica | E003 |
| A8 | Nenhum sinal de parada fixado em N=12 funciona em N≥64; "estabilidade do argmax" = critério publicado de ponto fixo, sem ganho | N2 (negativo) | — | E004 |
| A9 | **Transição de fase do S2:** até N=64 o pensamento anda 1 salto/passo; em N=128 resolve por difusão até o equilíbrio, 12× mais rápido e 90% correto | N1 (diagnóstico) | possivelmente nova; ver A11 | E004 |
| A10 | **S2 extrapola sem atrator:** T2, treino k≤4 e N=12 → 100% até k=64 e N=128 (e N=1024 no diagnóstico), sem cristalização | N2 (reproduzido limpo) | baixa (replicação) | E005 |
| A11 | ~~Lei N* = e^margem~~ → **limiar de dissolução ε_c ≈ 0,07:** o S2 se dissolve quando o vazamento de um passo passa de ~0,07 (N_c varia 3× entre sementes; ε(N_c) quase constante). O limiar pré-registrado de 0,5 errou por > 4× (E006, N2 negativo) | N1 (pós-hoc, 12 sementes) | baixa-média (instância de Veličković 2025) | E006, E006d |

## Fila de hipóteses (topo = próximo)

Alvos N+1 atuais (EVOLUTION_LOG): S2 → D06 (memória de trabalho) · S3 → D04 (H-S3-legível) · S5 → D05 (H-5.4).
Política: a bússola põe H04 no topo (gargalo de 4 goals); depois H06 e H22. S3 está parado desde o ciclo 1 → H-S3-legível logo após H04.

| Pri | Id | Hipótese | Nó pai · operador | Degrau-alvo | Custo |
|---|---|---|---|---|---|
| 1 | **H-lei-eps** (→ H04) | ε_c = 0,071 congelado prevê N_c de 30 sementes novas (±1,5×); d ∈ {10, 20, 40} decide entre "ε_c constante" e "ε_c·d constante" | E006d · REPLICAR | fecha a fronteira do D04 | baixo |
| 2 | **H-S3-legível** (→ H07, precisa H04) | Com S2 de ε baixo (T2) ou cristalizado, CONV/ESTAVEL cumprem a P2 do E004 em N=12…128 | E004 · MELHORAR | S3 D04 | baixo |
| 3 | **H-memória** (→ H06) | Estado = distribuição × registro de contagem; o passo aprende a contar | E005 · RASCUNHO | S2 D06 | médio |
| 3b | **H-baselines** (→ H22) | Deep Thinking (progressive loss) e PonderNet reimplementados reproduzem os efeitos publicados: progressive loss evita overthinking; PonderNet aprende passos que crescem com d | E001 · REPLICAR | infra | baixo |
| 4 | H-temperatura-adaptativa | Temperatura crescente com N (Veličković 2025) mantém ε < ε_c e evita a dissolução em T1 | E006 · MELHORAR | — | baixo |
| 5 | H-latente-livre | Latente vetorial livre: acúmulo de ruído e quantização (Σ1 de verdade) | E005 · RASCUNHO | S2 D09 | médio |
| 6 | H-5.4 | Código mínimo: bits por passo × robustez | E003 · MELHORAR | S5 D05 | médio |
| 7 | H-Σ3 | Chutar (S1) e verificar com invariante O(1) (S3) | E001 · RASCUNHO | S3 D09 | baixo |
| 8 | H-Σ4 | Busca bidirecional (da meta e do início) | — · RASCUNHO | S6 | médio |
| 9 | H-Σ5 | Energia restante (S0) como entrada do S3 | — · RASCUNHO | S0/S3 | médio |
| 10 | H-Σ6 | Agentes inventam o próprio código discreto | E003 · RASCUNHO | S5 D11 | alto |

Diversidade: nenhum nó ainda em **S0, S4 (além de E003), S6**. Pela regra 7 da política, um deles entra até o ciclo 8. **S3 está há 5 ciclos sem subir**: pela regra 2 (ramificar ao estagnar), o próximo ciclo depois de H-lei-eps é H-S3-legível.

## Átomos por status

Ver `docs/SISTEMAS.md`. Resumo: 🟩 6 · 🟨 1 · 🟥 2 · ⬜ 20 (29 átomos).
