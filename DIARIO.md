# DIÁRIO do laboratório

Uma entrada por ciclo. A mais recente fica embaixo. Resultados negativos têm o mesmo destaque.

## Ciclo 1 — 2026-09-29 — E001 MLU
- Hipótese (não pré-registrada): unir S1+S2+S3 supera cada um.
- Veredito: **N1**, replicação. Iterar um passo latente de 33 parâmetros extrapola 25×; a parada por convergência economiza 54%; colar S1 na frente piora.
- Surpresa: o primeiro gerador de dados tinha um atalho (uma só raiz). Corrigido antes de concluir.
- Semeado: cristalização (→E002).

## Ciclo 1b — 2026-09-29 — E001 reavaliado + régua
- Construída `lab/estat.py` (IQM, bootstrap, Wilson, Fisher, permutação, AURC, ECE, Pareto) com testes.
- 10 sementes: A1–A3 se mantêm. A "cristalização" **não** era significativa (p=0,46), só 1 de 10 sementes colapsava. A régua pegou um exagero meu na primeira rodada.

## Ciclo 2 — 2026-09-29 — E002 cristalização (pré-registrado)
- Hipótese: cristalizar o estado reduz colapsos em extrapolação extrema.
- Veredito: **MATAR** (P1 falhou: 0/30 colapsos sem cristalização em d=128).
- O que aprendemos: o "colapso" do E001 era do **S3**, não do S2. Limiar absoluto de confiança (0,9) não escala com N; o argmax estava certo em 9–10 de 10. A cristalização só mascarava a dúvida. → achado A4.
- Semeado: H-3.2a (confiança invariante à escala).

## Ciclo 3 — 2026-09-29 — E003 Cristal Comum (pré-registrado)
- Hipótese: o mesmo colapso discreto serve para pensar e para comunicar (Σ1).
- Veredito: **PIVOTAR**. Mensagens simbólicas vencem analógicas sob ruído por até +0,81 (N2). Mas o ganho vem de codificar a *mensagem*, não o estado → Σ1 "pensamento = símbolo" não suportada; "comunicação = símbolo" suportada.
- Surpresa: com N fixo, a profundidade não importa. A tarefa da raiz é um atrator que autocorrige erros, então não mede acúmulo de erro. Isso bloqueia testes de robustez em T1.
- Semeado: H-T2 (tarefa sem atrator, prioridade 1), H-Σ1b, H-5.4.
