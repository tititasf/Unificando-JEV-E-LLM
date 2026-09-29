# LIVRO DE ETAPAS

*Gerado por `python3 -m lab.registro livro` a partir de `registro/arvore.jsonl`. Não editar à mão.*

## Meta-métricas do laboratório (o laboratório medindo a si mesmo)

| métrica | valor |
|---|---|
| ciclos | 6 |
| nós na árvore | 14 (RASCUNHO 3, META 4, MELHORAR 1, DIAGNOSTICAR 4, REPLICAR 2) |
| taxa de morte de hipóteses | 0.50 |
| taxa de promoção/replicação | 0.17 |
| previsões avaliadas / acerto | 25 / 0.36 |
| Brier das previsões (menor = pesquisador mais calibrado) | 0.36 |
| degrau atual por tema | S2 D05, S3 D03, S5 D04 |
| ciclos sem subir degrau | S2 1, S3 5, S5 3 |
| novidade dos achados | replicacao 1, — 2, baixa 2, baixa-media (instancia de Velickovic 2025) 1 |
| registros antigos corrigidos | 4 |
| CPU médio por nó (s) | 203.70 |
| guarda do avaliador | OK |

## Árvore de experimentos

▲ promover · ✖ matar · ↻ pivotar · ≡ replicado · · informativo · … pendente

```
▲ E001 [RASCUNHO, S2] MLU: S1+S2+S3 em miniatura → PROMOVER N1
    ✖ E002 [MELHORAR, S2] Cristalizacao estabiliza o pensamento? → MATAR N2
        ✖ E004 [RASCUNHO, S3] S3 invariante a escala → MATAR N2
            · E004d [DIAGNOSTICAR, S2] Diagnostico: transicao de fase do S2 → INFORMATIVO N1
    ↻ E003 [RASCUNHO, S5] Cristal Comum: mensagem simbolica vs analogica → PIVOTAR N2
        · E003d [DIAGNOSTICAR, S5] Diagnostico: N fixo e bracos cruzados → INFORMATIVO N1
    ✖ E005 [REPLICAR, S2] Motor S2 na tarefa T2 sem atrator → MATAR N2
        · E005d [DIAGNOSTICAR, S2] Diagnostico: margem aprendida e lei N*=e^margem → INFORMATIVO N1
            ↻ E006 [REPLICAR, S2] Lei N*: o vazamento de um passo preve a dissolucao? → PIVOTAR N2 (negativo)
                · E006d [DIAGNOSTICAR, S2] Diagnostico: limiar real eps_c ~ 0,07 → INFORMATIVO N1
· M001 [META, LAB] Regua de evidencia + estatistica → INFORMATIVO 
    · M002 [META, LAB] Protocolo Scalata (escada de 30 degraus) → INFORMATIVO 
        … M003 [META, LAB] Integracao RSI: arvore, operadores, politica de busca, guarda, meta-metricas → PENDENTE 
            … M004 [META, LAB] Bussola: goals, arvore de habilidades e fronteira priorizada → PENDENTE 
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
