# ESTADO — onde estamos

Atualizado no fim de cada ciclo. Última atualização: ciclo 3 (2026-09-29).

## Fase atual

**Fase 1 — Micro (T1–T2).** Portão para sair: um mecanismo com **N2 em ≥2 famílias de tarefas**.
Progresso: 1 resultado N2 (E003, comunicação simbólica), numa família só (T1).
Bloqueio descoberto: a tarefa T1 é um atrator (autocorrige erros) → precisamos da T2 sem atrator.

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

## Fila de hipóteses (topo = próximo)

| Pri | Id | Hipótese | Átomo/Σ | Tipo | Custo |
|---|---|---|---|---|---|
| 1 | **H-T2** | Criar a tarefa T2 "salto exato" (seguir exatamente k ponteiros numa permutação: sem atrator, qualquer erro é fatal) e re-testar A1, A5, A6 nela | infra + 2.1, 1.4, 5.1 | promover para N3 (2ª família) | médio |
| 2 | **H-3.2a** | Confiança relativa (entropia normalizada por log N, ou margem top1−top2) mantém E-AURC≈0 e zero abstenções indevidas de N=12 a N=128 | 3.2 | conserta A4 | baixo |
| 3 | H-Σ1b | Com ruído **interno** no estado do S2, cristalizar ajuda o pensamento? (em T2) | 1.4, Σ1 | nova | baixo |
| 4 | H-Σ3 | Chutar (S1) e verificar com invariante O(1) (S3) domina o roteador por confiança | 3.3, Σ3 | nova | baixo |
| 5 | H-5.4 | Código mínimo: bits por passo × robustez; códigos corretores aprendidos vs one-hot | 5.4 | nova | médio |
| 6 | H-Σ4 | Busca bidirecional (da meta e do início) com o mesmo passo: passos ≈ d/2 | 6.3, Σ4 | nova | médio |
| 7 | H-Σ2 | Destilar S2→S1 ao longo da "vida" reduz o custo médio mantendo acc | 1.2, Σ2 | nova | médio |
| 8 | H-Σ5 | Energia restante (S0) como entrada do S3 → melhor Pareto que limiar fixo | 0.1, 0.3, Σ5 | nova | médio |
| 9 | H-Σ6 | Agentes inventam o próprio código discreto (comunicação emergente) | 5.2, Σ6 | nova | alto |
| 10 | H-2.3 | Tarefa com várias hipóteses vivas: quando a superposição (contínuo) vence o cristal? | 2.3 | nova | médio |

## Átomos por status

Ver `docs/SISTEMAS.md`. Resumo: 🟩 6 · 🟨 1 · 🟥 2 · ⬜ 20 (29 átomos).
