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

## Ciclo 6 — 2026-09-29 — E006 lei N* (pré-registrado)
- Hipótese: o vazamento de um passo (= 0,5) prevê o N em que o S2 se dissolve.
- Veredito: **PIVOTAR** (N2 negativo). Em N*/4 já estava tudo dissolvido (0/30). Falhas de desenho minhas: a grade começou alta e a grade B nunca rodou.
- Surpresa: o diagnóstico achou a lei corrigida. O vazamento de um passo **prevê** a transição, mas o limiar é **ε_c ≈ 0,07**, quase constante entre sementes, enquanto N_c varia 3×. Instância de Veličković et al. 2025.
- Meta: Brier 0,25 (contra 0,42): as probabilidades moderadas protegeram.
- Semeado: H-lei-eps (fora da amostra + "por passo × acumulado"), H-temperatura-adaptativa.

## Ciclo 7 — 2026-09-29 — E007 lei de nitidez fora da amostra (pré-registrado) + controle de qualidade
- Antes do ciclo: seis melhorias de processo (verificador de coerência `lab/checar.py`, sementes de teste derivadas do commit, cálculo de amostra, linhas de base Deep Thinking/PonderNet, protocolo CLRS, teto do Python medido em `docs/STACK.md`) e gancho de início de sessão. O verificador achou 2 afirmações obsoletas no primeiro uso.
- Piloto com o modelo completo (lição 11b) achou um bug (bisseção abaixo do N mínimo) e uma métrica confundida (acurácia com "sorte de atrator"); a métrica primária virou o regime.
- Hipótese: ε_c = 0,071 congelado prevê N_c em modelos novos; o efeito é por passo.
- Veredito: **PROMOVER** (N2, reproduzido limpo). 25/30 dentro de 1,5×; p = 0,0002 contra a constante; R = 0,95 (por passo). **H04 desbloqueada**, a primeira habilidade conquistada pela bússola.
- Surpresa: uma teoria de campo médio sem parâmetros (bifurcação sela-nó) prevê N_c com ~9% de erro. É a condição de separação das redes de Hopfield modernas: o S2 é uma memória associativa iterada. Novidade baixa, valor de projeto alto.
- Meta: Brier 0,11, o primeiro abaixo de 0,25.
- Semeado: H-temperatura-logN (→ H05), H-campo-médio-T2.

## Ciclo 8 — 2026-09-29 — E008 PonderNet como linha de base (pré-registrado)
- Piloto M006: nenhum overthinking no motor estruturado (100% em T=200, com e sem progressive loss). Critério de H22 revisado **antes** do pré-registro, com a versão antiga guardada.
- Hipótese: a PonderNet reimplementada aprende passos crescentes com a dificuldade, mantendo o acerto.
- Veredito: **REPLICADO** (N2, reproduzido limpo). Passos = d+6 (Spearman 1,0), 100% inclusive d = 5..9. **H22 desbloqueada.**
- Surpresa: em N=12 a parada por ponto fixo acerta igual e custa ~1,9× menos que a PonderNet não ajustada.
- Meta: Brier 0,04. O S3 está parado desde o ciclo 1 e agora é o topo da bússola (H07).
- Semeado: H-custo-ponder.

## Ciclo 9 — 2026-09-29 — E009 S3 em dois tempos (pré-registrado)
- Piloto: sem S3, o S2 erra ~47% no regime dissolvido; o limiar absoluto (ABS) também não erra ali → a métrica do regime dissolvido virou "erros" (o G2 pede zero erros confiantes) e acrescentei custo em passos.
- Hipótese: prever o regime pela lei de nitidez antes de pensar + ponto fixo durante → metacognição que funciona de N=12 a N=1024 sem ajuste.
- Veredito: **PROMOVER** (N2, reproduzido limpo). 8/8 previsões certas. Cobertura 100% onde dá, abstenção 100% sem orçamento, **0/600 erros** no regime dissolvido; PonderNet e ponto fixo erram ~51% ali. **H07 desbloqueada; S3 sobe para D04** (parado desde o ciclo 1).
- Surpresa: o ABS também passa. O que resolve é tratar a dissolução como "não sei"; o tempo 1 economiza 19× em passos. A4/A8 foram reinterpretados e registrados como obsoletos.
- Meta: Brier 0,07.
- Semeado: H-S3-fronteira (→ H08), H-S3-T2.

## Ciclo 10 — 2026-09-29 — E010 memória de trabalho latente (pré-registrado)
- Piloto com o modelo completo antes de congelar (lição 11b); passo acelerado de O(N·K²) para O(N·K), verificado exato.
- Hipótese: um passo relacional sobre pares (nó × contador), com k na entrada, anda exatamente k saltos e para sozinho.
- Veredito: **PROMOVER** (N2, reproduzido limpo). 5/5 previsões. 100% em todas as 9 células até k=64, N=64 (treino k≤4, N=8); sem registro, 6%. **H06 desbloqueada; S2 sobe para D06.**
- Surpresa: a ablação SEM_MARCAS não quebrou nada: a parada emerge da fronteira do espaço de estados (no contador 0 não há "decrementar").
- Meta: Brier 0,05. Paralelo ao ciclo: JEV instalado (SDK oficial, wrapper, skill), acesso ainda bloqueado pela rede; nenhum resultado deste ciclo usa o JEV.
- Semeado: H-pilha, H-fronteira-geometrica (→ H16, testada no E011).

## Ciclo 11 — 2026-09-29 — E011 modelo de mundo com o mesmo passo (pré-registrado)
- Escolha pela regra de diversidade: S6 não tinha nós; H16 entrou na fronteira com H06.
- Hipótese: o passo relacional do S2 sobre (posição × velocidade) aprende a física de uma caixa com paredes e extrapola 8× em tamanho; o rebote precisa do atributo "distância à parede".
- Veredito: **PROMOVER** (N2, reproduzido limpo). 4/4 previsões. 0 erros em 16 passos em L=8, 32 e 64; sem parede 13–15%; sem rebote 81%. **H16 desbloqueada; S6 → D01.**
- Atalho trivial achado no ATACAR: com os atributos dados, a física é uma tabela local de 12 casos; a extrapolação vem do desenho. Declarado no RELATORIO e no degrau (D01, não D02).
- Radar de lacunas (atrasado desde o ciclo 6) feito: G4 segue aberto para ≤ 1M parâmetros; G6 ganhou um benchmark externo (AI4AI-Bench). GOALS §5b.
- JEV: SDK oficial `typesafe-sdk`, `lab/jev.py` e skill `/jev` prontos; o usuário forneceu a chave (fora do git). **Bloqueio: a rede nega `api.typesafe.ai`.** Nenhum resultado usa o JEV. Orientação "Ultra-Sistema 1" traduzida em átomos (SISTEMAS), H26 criada.
- Meta: Brier 0,03.
- Semeado: H-mundo-cru, H-mundo-2p, H-imaginar.

## Ciclo 12 — 2026-09-30 — E012 o JEV como S1 externo real (pré-registrado)
- Acesso ao JEV confirmado (rede liberada; credencial `TYPESAFE` persistente no ambiente). Critério da H26 revisto antes do pré-registro. `lab/reproduzir` ganhou `--dados` (reprocessar respostas gravadas de sistemas não determinísticos).
- Escolha: H26 sobrepondo H05 (política "infra que desbloqueia"): o JEV é o S1 real do laboratório e destrava a H24.
- Hipótese: o JEV é um S1 de um salto; um controlador S2 que o chama um salto por vez recupera o acerto segundo q^k; em T1, parada por ponto fixo (S3) supera a passada única.
- Veredito: **PROMOVER** (N2, reprodução IDÊNTICA). 7/9 previsões. Uma passada: um salto 0,90/0,83/0,63; k≥2 no acaso; T1 falha até com d=1. Iterado: k=4 0,53 vs 0,08 (p=1,6e-11); lei q^k em 8/9 células; T1 0,55 vs 0,06. **0/516 erros confiantes**, ECE 0,074. **H26 desbloqueada; S1 → D01.**
- Surpresas: (1) até o salto único se dissolve com N (0,94 → 0,71): a lei de nitidez aparece num S1 comercial; (2) o atalho não é π(s) (só 19%); em N=8 k=8 o acerto de 0,40 vem de responder o início com ciclos curtos (11/12); (3) as falhas do ITER_PF são metade de reconhecimento de auto-ponteiro.
- Meta: Brier 0,12. Errei P1 (subestimei a queda com N) e P3.
- Semeado: H-JEV-seletivo, H-JEV-autoponteiro, H-JEV-nitidez.

## Ciclo 13 — 2026-09-30 — M007 (piloto negativo) + E013 temperatura derivada da lei (H05)
- Piloto M007 (N0), sobre os saltos gravados do E012 e 150 chamadas `Noul` novas: nenhum escore de confiança do JEV (p1, margem, razão, entropia, `confidence`) nem a verificação `Noul` sustenta um limiar calibrado em N=8: o risco por salto de 2% vira 11–25% em N=64. É a lacuna do E004 num S1 externo. H-JEV-seletivo não foi pré-registrada.
- Então o ciclo foi para o topo da bússola: H05 (nitidez em qualquer escala).
