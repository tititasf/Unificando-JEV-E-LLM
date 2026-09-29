# ESTADO — onde estamos

Atualizado no fim de cada ciclo. Última atualização: ciclo 8 (2026-09-29).

> Norte: [`GOALS.md`](GOALS.md) · o que atacar agora: [`BUSSOLA.md`](BUSSOLA.md) (fronteira: H07 → H06 → H05 → H13 → H21).

## Fase atual

**Fase 1 — Micro (T1–T2): portão formalmente atingido no ciclo 5** (passo latente iterado com N2 em T1 e T2). Ressalva: mecanismo **conhecido** (replicação).
Antes da Fase 2 (T3, algoritmos contra Deep Thinking): ~~fechar a lei de nitidez (H04)~~ ✅ ciclo 7; ~~validar as linhas de base publicadas (H22)~~ ✅ ciclo 8; protocolo CLRS reimplementado (H23, depende de H06).
Infra disponível: T2 sem atrator (`experimentos/E005_t2_salto/tarefa_t2.py`), passo O(N) (`experimentos/E006_lei_margem/passo_rapido.py`), linhas de base (`lab/baselines.py`), tarefas CLRS (`lab/tarefas_clrs.py`), sementes derivadas do commit (`lab/sementes.py`), controle de qualidade (`lab/checar.py`).
Calibração do pesquisador: ver `LIVRO.md` (Brier do último ciclo: 0,04).

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
| A11 | **Lei de nitidez (validada fora da amostra):** o vazamento de um passo prevê onde o S2 se dissolve (25/30 dentro de 1,5×; p=0,0002 contra a constante); o efeito é por passo (independe de d); transição de fase abrupta | **N2** (E007, reproduzido limpo) | baixa | E006, E006d, E007 |
| A13 | **PonderNet reimplementada reproduz o efeito publicado:** passos = d+6, 100% inclusive fora da distribuição; em N=12 a parada por ponto fixo é ~1,9× mais barata com o mesmo acerto (PonderNet não ajustada). Deep Thinking: sem overthinking no motor estruturado | N2 | nenhuma (replicação) | E008, M006 |
| A12 | **O S2 é uma memória associativa tipo Hopfield:** teoria de campo médio (bifurcação sela-nó, m·a(1−a)=1) prevê N_c por modelo com ~9% de erro, sem parâmetros ajustados | N1 (pós-hoc, 30 sementes) | baixa (condição de separação de Hopfield moderno) | E007d |

## Fila de hipóteses (topo = próximo)

Alvos N+1 atuais (EVOLUTION_LOG): S2 → D06 (memória de trabalho) · S3 → D04 (H-S3-legível) · S5 → D05 (H-5.4).
Política: a bússola põe H04 no topo (gargalo de 4 goals); depois H06 e H22. S3 está parado desde o ciclo 1 → H-S3-legível logo após H04.

| Pri | Id | Hipótese | Nó pai · operador | Degrau-alvo | Custo |
|---|---|---|---|---|---|
| 1 | **H-S3-legível** (→ H07) | S3 em dois tempos: antes de pensar, prevê o regime pela margem (lei de nitidez); durante, para por ponto fixo. Responde ≥99% quando dá e se abstém ≥99% quando não dá, de N=12 a N=1024; contra CONV puro e PonderNet | E004 · MELHORAR | S3 D04 | baixo |
| 3 | **H-memória** (→ H06) | Estado = distribuição × registro de contagem; o passo aprende a contar | E005 · RASCUNHO | S2 D06 | médio |
| 4 | **H-temperatura-logN** (→ H05) | β(N) = log(N−1)/log(N_treino−1) nos logits mantém a nitidez em qualquer N sem re-treino (previsto pela teoria de Hopfield) | E007d · MELHORAR | S2 | baixo |
| 5b | H-custo-ponder | PonderNet com β e λ_p ajustados alcança o custo do CONV? Em N grande, qual quebra primeiro? | E008 · MELHORAR | S3 D07 / G5 | baixo |
| 5 | H-campo-médio-T2 | A teoria de campo médio, com margem medida em N=30, prevê o N_c em T2 (permutações) | E007d · REPLICAR | — | baixo |
| 6 | H-5.4 (→ H13) | Código mínimo: bits por passo × robustez | E003 · MELHORAR | S5 D05 | médio |
| 7 | H-latente-livre | Latente vetorial livre (bloqueado pelo teto do Python: docs/STACK.md) | E005 · RASCUNHO | S2 D09 | alto |
| 8 | H-Σ3 | Chutar (S1) e verificar com invariante O(1) (S3) | E001 · RASCUNHO | S3 D09 | baixo |
| 9 | H-Σ4 | Busca bidirecional (da meta e do início) | — · RASCUNHO | S6 | médio |
| 10 | H-Σ5 | Energia restante (S0) como entrada do S3 | — · RASCUNHO | S0/S3 | médio |

Diversidade: nenhum nó ainda em **S0, S4 (além de E003), S6**. Pela regra 7 da política, um deles entra até o ciclo 10. **S3 está parado desde o ciclo 1**: H07 (prioridade 14) é o topo da bússola e o próximo ciclo.

## Átomos por status

Ver `docs/SISTEMAS.md`. Resumo: 🟩 6 · 🟨 1 · 🟥 2 · ⬜ 20 (29 átomos).
