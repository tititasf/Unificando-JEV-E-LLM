# ESTADO — onde estamos

Atualizado no fim de cada ciclo. Última atualização: ciclo 4 (2026-09-29).

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
| A8 | Nenhum sinal de parada fixado em N=12 funciona em N≥64; "estabilidade do argmax" = critério publicado de ponto fixo, sem ganho | N2 (negativo) | — | E004 |
| A9 | **Transição de fase do S2:** até N=64 o pensamento anda 1 salto/passo; em N=128 resolve por difusão até o equilíbrio, 12× mais rápido e 90% correto | N1 (diagnóstico) | possivelmente nova; pode ser artefato do atrator | E004 |

## Fila de hipóteses (topo = próximo)

Alvos N+1 atuais (EVOLUTION_LOG): S2 → D05 (H-T2) · S3 → D04 novo (H-S3-legível) · S5 → D05 (H-5.4).

| Pri | Id | Hipótese | Átomo/Σ | Degrau-alvo | Custo |
|---|---|---|---|---|---|
| 1 | **H-T2** | Tarefa T2 "salto exato" (permutação, k saltos dados, sem atrator, erro fatal); re-testar A1, A6, A9 nela | 2.1, 1.4, 5.1 | S2 D05 | médio |
| 2 | **H-S3-legível** | Com S2 cristalizado, CONV/ESTAVEL cumprem os critérios da P2 do E004 em N=12…128 | 3.1, 3.2 | S3 D04 | baixo |
| 3 | **H-regime** | O regime difusivo (A9) é capacidade ou artefato? Prever o limiar de N pela margem aprendida; testar com d ≪ N | 2.1, 2.3 | S2 (D07) | baixo |
| 4 | H-5.4 | Código mínimo: bits por passo × robustez; one-hot × binário × código com distância | 5.4 | S5 D05 | médio |
| 5 | H-híbrido | S3 detecta o regime e alterna leitura de convergência / cristalização | 3.x, Σ1 | S3 D06 | médio |
| 6 | H-Σ1b | Ruído interno no estado: cristalizar ajuda o pensamento? (em T2) | 1.4, Σ1 | S2 D14 | baixo |
| 7 | H-Σ3 | Chutar (S1) e verificar com invariante O(1) (S3) domina o roteador por confiança | 3.3, Σ3 | S3 D09 | baixo |
| 8 | H-Σ4 | Busca bidirecional (da meta e do início): passos ≈ d/2 | 6.3, Σ4 | — | médio |
| 9 | H-Σ2 | Destilar S2→S1 ao longo da "vida" | 1.2, Σ2 | — | médio |
| 10 | H-Σ5 | Energia restante (S0) como entrada do S3 | 0.1, 0.3, Σ5 | S3 D11 | médio |
| 11 | H-Σ6 | Agentes inventam o próprio código discreto | 5.2, Σ6 | S5 D11 | alto |

## Átomos por status

Ver `docs/SISTEMAS.md`. Resumo: 🟩 6 · 🟨 1 · 🟥 2 · ⬜ 20 (29 átomos).
