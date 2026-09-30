# LIVRO DE ETAPAS

*Gerado por `python3 -m lab.registro livro` a partir de `registro/arvore.jsonl`. Não editar à mão.*

## Meta-métricas do laboratório (o laboratório medindo a si mesmo)

| métrica | valor |
|---|---|
| ciclos | 13 |
| nós na árvore | 25 (RASCUNHO 6, META 6, MELHORAR 3, DIAGNOSTICAR 6, REPLICAR 4) |
| taxa de morte de hipóteses | 0.23 |
| taxa de promoção/replicação | 0.62 |
| previsões avaliadas / acerto | 67 / 0.69 |
| Brier das previsões (menor = pesquisador mais calibrado) | 0.13 |
| degrau atual por tema | S2 D06, S3 D04, S5 D04, S6 D01, S1 D01 |
| ciclos sem subir degrau | S2 3, S3 4, S5 10, S6 2, S1 1 |
| novidade dos achados | replicacao 1, — 2, baixa 6, baixa-media (instancia de Velickovic 2025) 1, baixa (teoria de Hopfield moderno) 1, nenhuma (replicacao) 1, baixa-media 1 |
| registros antigos corrigidos | 6 |
| CPU médio por nó (s) | 415.80 |
| guarda do avaliador | OK |

## Árvore de experimentos

▲ promover · ✖ matar · ↻ pivotar · ≡ replicado · · informativo · … pendente

```
▲ E001 [RASCUNHO, S2] MLU: S1+S2+S3 em miniatura → PROMOVER N1
    ✖ E002 [MELHORAR, S2] Cristalizacao estabiliza o pensamento? → MATAR N2
        ✖ E004 [RASCUNHO, S3] S3 invariante a escala → MATAR N2
            · E004d [DIAGNOSTICAR, S2] Diagnostico: transicao de fase do S2 → INFORMATIVO N1
            ▲ E009 [MELHORAR, S3] S3 em dois tempos: metacognicao legivel em qualquer escala → PROMOVER N2
    ↻ E003 [RASCUNHO, S5] Cristal Comum: mensagem simbolica vs analogica → PIVOTAR N2
        · E003d [DIAGNOSTICAR, S5] Diagnostico: N fixo e bracos cruzados → INFORMATIVO N1
    ✖ E005 [REPLICAR, S2] Motor S2 na tarefa T2 sem atrator → MATAR N2
        · E005d [DIAGNOSTICAR, S2] Diagnostico: margem aprendida e lei N*=e^margem → INFORMATIVO N1
            ↻ E006 [REPLICAR, S2] Lei N*: o vazamento de um passo preve a dissolucao? → PIVOTAR N2 (negativo)
                · E006d [DIAGNOSTICAR, S2] Diagnostico: limiar real eps_c ~ 0,07 → INFORMATIVO N1
                    ▲ E007 [REPLICAR, S2] Lei de nitidez fora da amostra (eps_c congelado) → PROMOVER N2
                        · E007d [DIAGNOSTICAR, S2] Diagnostico: teoria de campo medio (bifurcacao sela-no) → INFORMATIVO N1
                        ▲ E013 [MELHORAR, S2] Temperatura derivada da lei de nitidez: nitidez em qualquer escala → PROMOVER N2
        ▲ E010 [RASCUNHO, S2] Memoria de trabalho latente: pares (no x contador) → PROMOVER N2
            ▲ E011 [RASCUNHO, S6] Modelo de mundo com o mesmo passo: particula numa caixa → PROMOVER N2
        ▲ E012 [RASCUNHO, S1] JEV como S1 externo real: sozinho e iterado pelo S2 → PROMOVER N2
            · M007 [DIAGNOSTICAR, S3] Piloto: S3 seletivo sobre o JEV nao transfere entre escalas → INFORMATIVO N0
    ≡ E008 [REPLICAR, S3] PonderNet reimplementada como linha de base → REPLICADO N2
· M001 [META, LAB] Regua de evidencia + estatistica → INFORMATIVO 
    · M002 [META, LAB] Protocolo Scalata (escada de 30 degraus) → INFORMATIVO 
        … M003 [META, LAB] Integracao RSI: arvore, operadores, politica de busca, guarda, meta-metricas → PENDENTE 
            … M004 [META, LAB] Bussola: goals, arvore de habilidades e fronteira priorizada → PENDENTE 
                … M005 [META, LAB] Controle de qualidade: checar, sementes do commit, poder, baselines, CLRS, stack → PENDENTE 
                    · M006 [META, LAB] Piloto: overthinking ausente no motor estruturado; criterio de H22 revisado → INFORMATIVO N0
```

## Etapas em ordem

### E001 — MLU: S1+S2+S3 em miniatura (ciclo 1, 2026-09-29)
- **Operador:** RASCUNHO · **pai:** — · **tema:** S2 · **degrau-alvo:** —
- **Hipótese:** Unir S1 (1 passada), S2 (passo latente iterado) e S3 (parada/abstencao) supera cada um isolado.
- **Veredito:** PROMOVER · **nível:** N1 · **novidade:** replicacao
- **Métrica principal:** acc S2+S3 (N=12, d 0..9, 10 sementes) = 1.0
- **Lição:** O primeiro gerador tinha um atalho (so uma raiz): sempre procurar o atalho trivial.
- **Lição:** Colar S1 na frente por confianca piora (0,976 vs 1,000).
- **Semeou:** E002
- **Arquivos:** [relatorio](experimentos/E001_mlu/RELATORIO.md) · [reavaliacao](experimentos/E001_mlu/reavaliacao.md)
- **Commits:** pré-registro `None` · resultado `3c3b874`

### M001 — Regua de evidencia + estatistica (ciclo 1, 2026-09-29)
- **Operador:** META · **pai:** — · **tema:** LAB · **degrau-alvo:** —
- **Hipótese:** Uma regua explicita (N0-N5, IQM, IC, colapso) evita autoengano.
- **Veredito:** INFORMATIVO · **nível:** — · **novidade:** —
- **Lição:** A regua pegou um exagero ja no primeiro uso (cristalizacao p=0,46).
- **Arquivos:** [regua](docs/VALIDACAO.md) · [codigo](lab/estat.py)
- **Commits:** pré-registro `—` · resultado `bba72e5`

### E002 — Cristalizacao estabiliza o pensamento? (ciclo 2, 2026-09-29)
- **Operador:** MELHORAR · **pai:** E001 · **tema:** S2 · **degrau-alvo:** —
- **Hipótese:** Colapsar o estado a cada passo reduz colapsos em extrapolacao extrema.
- **Veredito:** MATAR · **nível:** N2 · **novidade:** —
- **Métrica principal:** colapsos CONT d=128 (30 sementes) = 0/30
- **Previsões:** P1 🟥; P3 🟥; P5 🟥
- **Lição:** O 'colapso' do E001 era do S3 (limiar absoluto), nao do S2.
- **Corrige:** E001: cristalizacao mal atribuida
- **Semeou:** H-3.2a
- **Arquivos:** [prereg](experimentos/E002_cristalizacao/PREREG.md) · [relatorio](experimentos/E002_cristalizacao/RELATORIO.md)
- **Commits:** pré-registro `44dbaa3` · resultado `bba72e5`

### E003 — Cristal Comum: mensagem simbolica vs analogica (ciclo 3, 2026-09-29)
- **Operador:** RASCUNHO · **pai:** E001 · **tema:** S5 · **degrau-alvo:** —
- **Hipótese:** O mesmo colapso discreto serve para pensar e para comunicar (Sigma1).
- **Veredito:** PIVOTAR · **nível:** N2 · **novidade:** baixa
- **Métrica principal:** SIMB-CONT d=32 sigma=2 = 0.78
- **Previsões:** Q1 ✅; Q2 ✅; Q3 🟥; Q4 ✅
- **Lição:** O ganho vem de codificar a mensagem, nao o estado.
- **Lição:** Tarefas-atrator mascaram acumulo de erro.
- **Semeou:** H-T2, H-Sigma1b, H-5.4
- **Arquivos:** [prereg](experimentos/E003_cristal_comum/PREREG.md) · [relatorio](experimentos/E003_cristal_comum/RELATORIO.md)
- **Commits:** pré-registro `b7861f2` · resultado `bba72e5`

### E003d — Diagnostico: N fixo e bracos cruzados (ciclo 3, 2026-09-29)
- **Operador:** DIAGNOSTICAR · **pai:** E003 · **tema:** S5 · **degrau-alvo:** —
- **Hipótese:** Separar efeito de d e de N; qual metade do cristal importa.
- **Veredito:** INFORMATIVO · **nível:** N1 · **novidade:** —
- **Arquivos:** [diagnostico](experimentos/E003_cristal_comum/diagnostico.md)
- **Commits:** pré-registro `—` · resultado `bba72e5`

### M002 — Protocolo Scalata (escada de 30 degraus) (ciclo 4, 2026-09-29)
- **Operador:** META · **pai:** M001 · **tema:** LAB · **degrau-alvo:** —
- **Hipótese:** Imaginacao vertical ligada a regua orienta o proximo passo (disciplina N+1).
- **Veredito:** INFORMATIVO · **nível:** — · **novidade:** —
- **Arquivos:** [protocolo](docs/ESCALA.md) · [log](EVOLUTION_LOG.md)
- **Commits:** pré-registro `—` · resultado `2cec81c`

### E004 — S3 invariante a escala (ciclo 4, 2026-09-29)
- **Operador:** RASCUNHO · **pai:** E002 · **tema:** S3 · **degrau-alvo:** S3:D04
- **Hipótese:** Estabilidade do argmax e um sinal de 'terminei' que funciona de N=12 a N=128.
- **Veredito:** MATAR · **nível:** N2 · **novidade:** —
- **Métrica principal:** placar ESTAVEL N=128 = 0.537
- **Previsões:** P1 🟥; P2 🟥; P3 ✅; P4 🟥; P5 ✅; P6 ✅; P7 🟥
- **Lição:** Estabilidade do argmax = criterio publicado de ponto fixo.
- **Lição:** Legibilidade do pensamento vem antes da metacognicao.
- **Semeou:** H-S3-legivel, H-regime, H-hibrido
- **Arquivos:** [prereg](experimentos/E004_s3_escala/PREREG.md) · [relatorio](experimentos/E004_s3_escala/RELATORIO.md)
- **Commits:** pré-registro `2cec81c` · resultado `61ad865`

### E004d — Diagnostico: transicao de fase do S2 (ciclo 4, 2026-09-29)
- **Operador:** DIAGNOSTICAR · **pai:** E004 · **tema:** S2 · **degrau-alvo:** —
- **Hipótese:** Em N grande o S2 continuo anda salto a salto ou chega em paralelo?
- **Veredito:** INFORMATIVO · **nível:** N1 · **novidade:** possivelmente nova
- **Lição:** Ate N=64 anda 1 salto/passo; em N=128 resolve por difusao ate o equilibrio, 12x mais rapido, 90% correto.
- **Corrige:** E001/E002: extrapolacao por iteracao so vale ate N=64
- **Arquivos:** [diagnostico](experimentos/E004_s3_escala/diagnostico.md)
- **Commits:** pré-registro `—` · resultado `61ad865`

### M003 — Integracao RSI: arvore, operadores, politica de busca, guarda, meta-metricas (ciclo 4, 2026-09-29)
- **Operador:** META · **pai:** M002 · **tema:** LAB · **degrau-alvo:** —
- **Hipótese:** Arvore de experimentos (AIDE), politica seguir/ramificar (AIDE2), arquivo e guarda do avaliador (DGM), meta-caderno (ShinkaEvolve) e Brier do pesquisador aceleram a subida de degraus e melhoram a calibracao nos proximos ciclos.
- **Veredito:** PENDENTE · **nível:** — · **novidade:** —
- **Lição:** Linha de base das meta-metricas: acerto de previsoes 43% (sem probabilidades), morte 50%, degraus S2 D04 / S3 D03 / S5 D04.
- **Arquivos:** [pesquisa](docs/RSI.md) · [codigo](lab/registro.py) · [licoes](LICOES.md)
- **Commits:** pré-registro `—` · resultado `—`

### E005 — Motor S2 na tarefa T2 sem atrator (ciclo 5, 2026-09-29)
- **Operador:** REPLICAR · **pai:** E001 · **tema:** S2 · **degrau-alvo:** S2:D05
- **Hipótese:** O passo S2 extrapola em T2 (sem atrator) so se o estado for cristalizado; o continuo acumula erro.
- **Veredito:** MATAR · **nível:** N2 · **novidade:** baixa
- **Métrica principal:** CONT acc N=128 k=64 (10 sementes) = 1.0
- **Previsões:** P1 ✅ (p=0.75); P2 🟥 (p=0.75); P3 ✅ (p=0.5); P4 🟥 (p=0.45); P5 🟥 (p=0.95); P6 🟥 (p=0.7); P7 🟥 (p=0.7)
- **Lição:** A softmax ja e um cristalizador suave: com margem ~10 o estado nao acumula erro por 64 passos.
- **Lição:** Lei candidata: regime difusivo quando N > e^margem (unifica A4, A9, E005).
- **Lição:** Tarefas-atrator no treino produzem margens pequenas (pensadores imprecisos).
- **Lição:** Nosso 'continuo' e uma distribuicao sobre nos, nao um vetor livre: nao testa Sigma1 de verdade.
- **Corrige:** A9: regime difusivo depende de N relativo a e^margem, nao de N grande
- **Semeou:** H-lei-margem, H-latente-livre, H-precisao-treino
- **Arquivos:** [prereg](experimentos/E005_t2_salto/PREREG.md) · [relatorio](experimentos/E005_t2_salto/RELATORIO.md)
- **Commits:** pré-registro `f4dfd67` · resultado `—`

### E005d — Diagnostico: margem aprendida e lei N*=e^margem (ciclo 5, 2026-09-29)
- **Operador:** DIAGNOSTICAR · **pai:** E005 · **tema:** S2 · **degrau-alvo:** —
- **Hipótese:** Por que o continuo nao acumula erro em T2?
- **Veredito:** INFORMATIVO · **nível:** N1 · **novidade:** possivelmente nova (lei quantitativa)
- **Lição:** Margem T2 ~10 vs T1 ~4-7; continuo 100% ate N=1024.
- **Arquivos:** [diagnostico](experimentos/E005_t2_salto/diagnostico.md)
- **Commits:** pré-registro `—` · resultado `—`

### E006 — Lei N*: o vazamento de um passo preve a dissolucao? (ciclo 6, 2026-09-29)
- **Operador:** REPLICAR · **pai:** E005d · **tema:** S2 · **degrau-alvo:** consolida S2 D04/D05
- **Hipótese:** O N em que o S2 se dissolve e previsto por N* = N com vazamento de um passo = 0,5.
- **Veredito:** PIVOTAR · **nível:** N2 (negativo) · **novidade:** baixa-media (instancia de Velickovic 2025)
- **Métrica principal:** acc>=0,95 em N*/4 (30 sementes) = 0/30
- **Previsões:** P1 🟥 (p=0.6); P2 ✅ (p=0.55); P3 🟥 (p=0.45); P4 🟥 (p=0.5); P5 — (p=0.5)
- **Lição:** O limiar de dissolucao e vazamento ~0,07 por passo, nao 0,5.
- **Lição:** Grades que dependem de uma quantidade estimada precisam de smoke com o modelo completo antes de congelar.
- **Corrige:** A11: lei N*=e^margem substituida por limiar de vazamento eps_c~0,07
- **Semeou:** H-lei-eps, H-temperatura-adaptativa
- **Arquivos:** [prereg](experimentos/E006_lei_margem/PREREG.md) · [relatorio](experimentos/E006_lei_margem/RELATORIO.md)
- **Commits:** pré-registro `1ee79ba` · resultado `—`

### E006d — Diagnostico: limiar real eps_c ~ 0,07 (ciclo 6, 2026-09-29)
- **Operador:** DIAGNOSTICAR · **pai:** E006 · **tema:** S2 · **degrau-alvo:** —
- **Hipótese:** Onde fica a transicao real e qual o vazamento nela?
- **Veredito:** INFORMATIVO · **nível:** N1 · **novidade:** possivelmente nova
- **Lição:** N_c varia 3x entre sementes, mas eps(N_c) fica ~0,07 (8 de 12 entre 0,061 e 0,083).
- **Arquivos:** [diagnostico](experimentos/E006_lei_margem/diagnostico.md)
- **Commits:** pré-registro `—` · resultado `—`

### M004 — Bussola: goals, arvore de habilidades e fronteira priorizada (ciclo 6, 2026-09-29)
- **Operador:** META · **pai:** M003 · **tema:** LAB · **degrau-alvo:** —
- **Hipótese:** Uma arvore de habilidades com goals ancorados em lacunas reais e prioridade calculada direciona os ciclos para o que desbloqueia mais descobertas.
- **Veredito:** PENDENTE · **nível:** — · **novidade:** —
- **Lição:** A bussola calculada concordou com a fila manual (H04 no topo): checagem de consistencia.
- **Arquivos:** [goals](GOALS.md) · [bussola](BUSSOLA.md) · [dados](registro/habilidades.json)
- **Commits:** pré-registro `—` · resultado `—`

### M005 — Controle de qualidade: checar, sementes do commit, poder, baselines, CLRS, stack (ciclo 6, 2026-09-29)
- **Operador:** META · **pai:** M004 · **tema:** LAB · **degrau-alvo:** —
- **Hipótese:** Verificador de coerencia, sementes que ninguem escolhe, calculo de amostra, linhas de base publicadas e protocolo externo reduzem erros de processo e desbloqueiam a Fase 2.
- **Veredito:** PENDENTE · **nível:** — · **novidade:** —
- **Lição:** O verificador achou 2 afirmacoes obsoletas no ESTADO no primeiro uso.
- **Lição:** Teto do Python puro medido: 2,9e7 op/s; gatilho de stack previsto em H09/H11.
- **Arquivos:** [checar](lab/checar.py) · [sementes](lab/sementes.py) · [baselines](lab/baselines.py) · [clrs](lab/tarefas_clrs.py) · [stack](docs/STACK.md)
- **Commits:** pré-registro `—` · resultado `—`

### E007 — Lei de nitidez fora da amostra (eps_c congelado) (ciclo 7, 2026-09-29)
- **Operador:** REPLICAR · **pai:** E006d · **tema:** S2 · **degrau-alvo:** H04
- **Hipótese:** O vazamento de um passo com limiar congelado 0,071 preve o N em que o S2 se dissolve, e o efeito e por passo (independe de d).
- **Veredito:** PROMOVER · **nível:** N2 · **novidade:** baixa (teoria de Hopfield moderno)
- **Métrica principal:** N_c dentro de 1,5x (30 sementes novas) = 25/30
- **Previsões:** P1 ✅ (p=0.65); P2 ✅ (p=0.7); P3 ✅ (p=0.7); P4 ✅ (p=0.65); P5 🟥 (p=0.15); P6 ✅ (p=0.55)
- **Lição:** Um numero medido num passo preve a transicao de fase do pensamento fora da amostra.
- **Lição:** Em tarefa-atrator, meca o regime (nitidez), nao a acuracia.
- **Lição:** O piloto com o modelo completo achou um bug e uma metrica confundida antes do pre-registro.
- **Semeou:** H-campo-medio-T2, H-temperatura-logN
- **Arquivos:** [prereg](experimentos/E007_lei_eps/PREREG.md) · [relatorio](experimentos/E007_lei_eps/RELATORIO.md)
- **Commits:** pré-registro `13d7855` · resultado `—`

### E007d — Diagnostico: teoria de campo medio (bifurcacao sela-no) (ciclo 7, 2026-09-29)
- **Operador:** DIAGNOSTICAR · **pai:** E007 · **tema:** S2 · **degrau-alvo:** —
- **Hipótese:** Uma teoria sem parametros ajustados preve eps_c e N_c por modelo?
- **Veredito:** INFORMATIVO · **nível:** N1 · **novidade:** baixa (condicao de separacao de Hopfield)
- **Lição:** Teoria de campo medio: erro de ~9% (29/30 dentro de 1,5x) contra 22% do limiar fixo, p=0,0004.
- **Lição:** O S2 e uma memoria associativa iterada tipo Hopfield: margem precisa vencer ~log N.
- **Arquivos:** [diagnostico](experimentos/E007_lei_eps/diagnostico.md)
- **Commits:** pré-registro `—` · resultado `—`

### M006 — Piloto: overthinking ausente no motor estruturado; criterio de H22 revisado (ciclo 8, 2026-09-29)
- **Operador:** META · **pai:** M005 · **tema:** LAB · **degrau-alvo:** —
- **Hipótese:** O motor S2 estruturado sofre overthinking que o progressive loss (Deep Thinking) corrige?
- **Veredito:** INFORMATIVO · **nível:** N0 · **novidade:** —
- **Lição:** Sem overthinking (100% em T=200 com treino so no instante final, 3 sementes): o ponto fixo da raiz ja cumpre o papel do progressive loss.
- **Lição:** Criterio de H22 revisado ANTES do pre-registro; versao anterior guardada em criterio_anterior.
- **Commits:** pré-registro `—` · resultado `—`

### E008 — PonderNet reimplementada como linha de base (ciclo 8, 2026-09-29)
- **Operador:** REPLICAR · **pai:** E001 · **tema:** S3 · **degrau-alvo:** H22
- **Hipótese:** A cabeca de parada estilo PonderNet aprende passos crescentes com a dificuldade mantendo o acerto.
- **Veredito:** REPLICADO · **nível:** N2 · **novidade:** nenhuma (replicacao)
- **Métrica principal:** Spearman(d, passos) mediano = 1.0
- **Previsões:** P1 ✅ (p=0.85); P2 ✅ (p=0.85); P3 ✅ (p=0.75); P4 🟥 (p=0.2)
- **Lição:** PonderNet reimplementada: passos = d+6 e 100% (inclusive fora da distribuicao).
- **Lição:** Em N=12 a parada por ponto fixo e ~1,9x mais barata com o mesmo acerto (PonderNet nao ajustada).
- **Semeou:** H-custo-ponder
- **Arquivos:** [prereg](experimentos/E008_ponder/PREREG.md) · [relatorio](experimentos/E008_ponder/RELATORIO.md)
- **Commits:** pré-registro `487586f` · resultado `—`

### E009 — S3 em dois tempos: metacognicao legivel em qualquer escala (ciclo 9, 2026-09-29)
- **Operador:** MELHORAR · **pai:** E004 · **tema:** S3 · **degrau-alvo:** S3:D04
- **Hipótese:** S3 que preve o regime pela lei de nitidez antes de pensar e para por ponto fixo durante responde quando da, se abstem sem orcamento e nunca erra no regime dissolvido, de N=12 a N=1024.
- **Veredito:** PROMOVER · **nível:** N2 · **novidade:** baixa-media
- **Métrica principal:** erros no regime dissolvido (DOIS_TEMPOS) = 0/600
- **Previsões:** P1 ✅ (p=0.55); P2 ✅ (p=0.85); P3 ✅ (p=0.8); P4 ✅ (p=0.8); P5 ✅ (p=0.8); P6 ✅ (p=0.9); P7 ✅ (p=0.6); P8 ✅ (p=0.85)
- **Lição:** Tratar o pensamento dissolvido como 'nao sei' elimina os erros confiantes em qualquer escala; PonderNet e ponto fixo erram ~51% ali.
- **Lição:** Prever o regime antes de pensar economiza 19x no regime dissolvido.
- **Lição:** A4/A8 estavam mal interpretados: o limiar absoluto se abstinha com razao.
- **Corrige:** A4/A8: o limiar absoluto nao 'falhava ao escalar'; o S2 so acertava por sorte de atrator
- **Semeou:** H-S3-fronteira, H-S3-T2
- **Arquivos:** [prereg](experimentos/E009_s3_legivel/PREREG.md) · [relatorio](experimentos/E009_s3_legivel/RELATORIO.md)
- **Commits:** pré-registro `b1804f8` · resultado `—`

### E010 — Memoria de trabalho latente: pares (no x contador) (ciclo 10, 2026-09-29)
- **Operador:** RASCUNHO · **pai:** E005 · **tema:** S2 · **degrau-alvo:** S2:D06
- **Hipótese:** Um passo relacional sobre pares (no x contador), com k na entrada e sem controlador contando, anda exatamente k saltos e para sozinho, extrapolando de k<=4,N=8 para k=64,N=64.
- **Veredito:** PROMOVER · **nível:** N2 · **novidade:** baixa
- **Métrica principal:** acerto MEMORIA em (N=64,k=64) = 1.00 (0/10 colapsos)
- **Previsões:** P1 ✅ (p=0.75); P2 ✅ (p=0.75); P3 ✅ (p=0.7); P4 ✅ (p=0.9); P5 ✅ (p=0.9)
- **Lição:** A parada emerge da fronteira do espaco de estados: no contador 0 nao ha transicao 'decrementar'.
- **Lição:** Sem registro (SEM_MEMORIA) o mesmo ponteiro fica no acaso (6%).
- **Lição:** A lei de nitidez se manteve num espaco de 4.160 estados.
- **Semeou:** H-pilha, H-fronteira-geometrica
- **Arquivos:** [prereg](experimentos/E010_memoria/PREREG.md) · [relatorio](experimentos/E010_memoria/RELATORIO.md)
- **Commits:** pré-registro `6802ec9` · resultado `—`

### E011 — Modelo de mundo com o mesmo passo: particula numa caixa (ciclo 11, 2026-09-29)
- **Operador:** RASCUNHO · **pai:** E010 · **tema:** S6 · **degrau-alvo:** S6:D01
- **Hipótese:** O passo relacional do S2 sobre (posicao x velocidade) aprende a fisica de uma caixa com paredes e preve 16 passos com erro < 1% em caixas 8x maiores; o rebote precisa do atributo 'distancia a parede'.
- **Veredito:** PROMOVER · **nível:** N2 · **novidade:** baixa
- **Métrica principal:** erro por passo MUNDO em L=64 = 0.0000 (10/10 sementes)
- **Previsões:** P1 ✅ (p=0.8); P2 ✅ (p=0.8); P3 ✅ (p=0.8); P4 ✅ (p=0.9)
- **Lição:** Raciocinio (S2) e fisica (S6) cabem no mesmo passo; muda o espaco de estados e as bordas.
- **Lição:** Atalho: atributos dados tornam a fisica uma tabela local de 12 casos; a extrapolacao em L vem do desenho.
- **Lição:** Sem a distancia a parede, 13-15% de erro concentrado nos choques.
- **Semeou:** H-mundo-cru, H-mundo-2p, H-imaginar
- **Arquivos:** [prereg](experimentos/E011_mundo/PREREG.md) · [relatorio](experimentos/E011_mundo/RELATORIO.md)
- **Commits:** pré-registro `078a745` · resultado `—`

### E012 — JEV como S1 externo real: sozinho e iterado pelo S2 (ciclo 12, 2026-09-30)
- **Operador:** RASCUNHO · **pai:** E005 · **tema:** S1 · **degrau-alvo:** S1:D01
- **Hipótese:** O JEV e um S1 de um salto (k=1 ok, k>=2 ~acaso); um controlador S2 que o chama um salto por vez recupera o acerto segundo acc(k)~q^k; em T1, iterar com parada por ponto fixo (S3) supera a passada unica.
- **Veredito:** PROMOVER · **nível:** N2 · **novidade:** baixa
- **Métrica principal:** T2 k=4: ITER vs UMA = 48/90 vs 7/90 (p=1.6e-11); lei q^k em 8/9 celulas; 0/516 erros confiantes
- **Previsões:** P1 🟥 (p=0.45); P2 ✅ (p=0.75); P3 🟥 (p=0.25); P4 ✅ (p=0.85); P5 ✅ (p=0.45); P6 ✅ (p=0.8); P7 ✅ (p=0.7); P8 ✅ (p=0.6); P9 ✅ (p=0.6)
- **Lição:** O JEV e um S1 de um salto; composicao em uma passada ~acaso.
- **Lição:** Ate o salto unico se dissolve com N (0,94->0,71 de N=8 a 64): lei de nitidez num S1 comercial.
- **Lição:** S2 iterando S1 segue acc(k)~q^k: o custo de confiabilidade e calculavel antes de rodar.
- **Lição:** O JEV sabe quando nao sabe: 0/516 erros com p>=0,9; ECE 0,074.
- **Semeou:** H-JEV-seletivo, H-JEV-autoponteiro, H-JEV-nitidez
- **Arquivos:** [prereg](experimentos/E012_jev/PREREG.md) · [relatorio](experimentos/E012_jev/RELATORIO.md)
- **Commits:** pré-registro `3d70ea0` · resultado `—`

### M007 — Piloto: S3 seletivo sobre o JEV nao transfere entre escalas (ciclo 13, 2026-09-30)
- **Operador:** DIAGNOSTICAR · **pai:** E012 · **tema:** S3 · **degrau-alvo:** —
- **Hipótese:** Algum sinal de confianca do JEV (p1, margem, razao, entropia, confidence, ou verificacao Noul) sustenta um limiar calibrado em N=8 que mantem o risco seletivo por salto em N=64 e em T1?
- **Veredito:** INFORMATIVO · **nível:** N0 · **novidade:** —
- **Lição:** Nenhum dos 5 escores do Choice transfere: risco por salto 2% em N=8 vira 11-25% em N=64.
- **Lição:** A verificacao Noul separa mal (0,42 vs 0,22) e aceita errados em N=64.
- **Lição:** H-JEV-seletivo nao foi pre-registrada; precisa de um sinal novo (Mondrian por escala ou temperatura adaptativa).
- **Arquivos:** [relatorio](experimentos/E012_jev/piloto_s3/LEIAME.md)
- **Commits:** pré-registro `—` · resultado `—`

### E013 — Temperatura derivada da lei de nitidez: nitidez em qualquer escala (ciclo 13, 2026-09-30)
- **Operador:** MELHORAR · **pai:** E007 · **tema:** S2 · **degrau-alvo:** S2:D06
- **Hipótese:** beta(N)=1+ln((N-1)/11)/m, com m medido sem rotulos, mantem o vazamento de um passo igual ao do treino e abaixo de eps_c ate N=4096 sem re-treino, em T1 e T2.
- **Veredito:** PROMOVER · **nível:** N2 · **novidade:** baixa
- **Métrica principal:** acerto TEORIA em N=4096 (T1, T2) = 1.00, 1.00 (B1: 0.17, 0.00); T2 eps(4096)/eps(12)=0.91
- **Previsões:** P1 ✅ (p=0.85); P2 ✅ (p=0.8); P3 🟥 (p=0.35); P4 ✅ (p=0.85); P5 ✅ (p=0.75); P6 ✅ (p=0.8)
- **Lição:** A dissolucao do S2 e efeito da normalizacao do softmax; uma temperatura com zero parametros livres, prevista pela lei, a remove ate 341x o treino.
- **Lição:** Em T2 a lei preve o vazamento quantitativamente (razao 0,91); em T1 so a parte dependente de N (competidor 'proprio no' tambem e suprimido).
- **Lição:** Atalho: qualquer afiacao acerta; a TEORIA e a afiacao minima.
- **Corrige:** H05 pendente desde o E006: a dissolucao nao exige re-treino, so a temperatura prevista pela lei
- **Semeou:** H-temp-S3, H-temp-minima-D07, H-temp-JEV
- **Arquivos:** [prereg](experimentos/E013_temperatura/PREREG.md) · [relatorio](experimentos/E013_temperatura/RELATORIO.md)
- **Commits:** pré-registro `2accfb8` · resultado `—`
