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

## Ciclo 4 — 2026-09-29 — E004 S3 invariante à escala (pré-registrado) + protocolo Scalata
- Novo: protocolo de 30 degraus (`docs/ESCALA.md`, `EVOLUTION_LOG.md`) integrado ao laço como passo ESCALAR, com disciplina N+1 e a regra "degrau atingido só com evidência ≥ N1".
- Hipótese: estabilidade do argmax é um sinal de "terminei" que funciona de N=12 a N=128.
- Veredito: **MATAR**. Em N=128 nenhum sinal funciona nas duas direções; o proposto é idêntico ao critério publicado (ponto fixo).
- Surpresa: **transição de fase do S2**. Até N=64 anda 1 salto/passo; em N=128 resolve por difusão até o equilíbrio, 12× mais rápido e 90% correto. A condição "fora do orçamento" deixou de ser impossível. A escada do S3 foi reordenada: legibilidade do pensamento antes da metacognição.
- Semeado: H-S3-legível, H-regime, H-híbrido.

## Ciclo 5 — 2026-09-29 — E005 motor S2 na tarefa T2 sem atrator (pré-registrado) + integração RSI
- Antes do ciclo: pesquisa RSI (AIDE, AIDE², DGM, ShinkaEvolve, AI Scientist v2, Heuresis, survey). Adotados: árvore de experimentos, operadores, política seguir/ramificar, guarda do avaliador por hash, reprodução limpa, meta-caderno (LICOES.md), livro de etapas gerado (LIVRO.md) e Brier do pesquisador.
- Hipótese: sem atrator, o estado contínuo acumula erro e só o cristalizado extrapola.
- Veredito: **MATAR** a hipótese, mas **S2 sobe para D05** (N2, reproduzido de checkout limpo): o contínuo acerta 100% até k=64 e N=128 (1024 no diagnóstico). Portão da Fase 1 formalmente atingido (mecanismo conhecido).
- Surpresa: a softmax já é um cristalizador suave; a margem aprendida em T2 (~10) é bem maior que em T1 (~4–7). Lei candidata N* = e^margem unifica A4, A9 e E005. P5 falhou nas células pequenas (ciclos curtos em permutações), que ficaram inválidas.
- Meta: Brier 0,42, pior que chutar 50%. Estou superconfiante; lição registrada.
- Semeado: H-lei-margem, H-latente-livre, H-precisão-treino, H-memória.
