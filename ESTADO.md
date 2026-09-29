# ESTADO — onde estamos

Atualizado no fim de cada ciclo. Última atualização: ciclo 11 (2026-09-29).

> Norte: [`GOALS.md`](GOALS.md) · o que atacar agora: [`BUSSOLA.md`](BUSSOLA.md) (fronteira: H05 → H24 → H08 → H23/H10/H13/H16 → H21 → H26).

## Fase atual

**Fase 1 — Micro (T1–T2): portão formalmente atingido no ciclo 5** (passo latente iterado com N2 em T1 e T2). Ressalva: mecanismo **conhecido** (replicação).
Antes da Fase 2 (T3, algoritmos contra Deep Thinking): ~~fechar a lei de nitidez (H04)~~ ✅ ciclo 7; ~~validar as linhas de base publicadas (H22)~~ ✅ ciclo 8; protocolo CLRS reimplementado (H23, depende de H06).
Infra disponível: T2 sem atrator (`experimentos/E005_t2_salto/tarefa_t2.py`), passo O(N) (`experimentos/E006_lei_margem/passo_rapido.py`), linhas de base (`lab/baselines.py`), tarefas CLRS (`lab/tarefas_clrs.py`), sementes derivadas do commit (`lab/sementes.py`), controle de qualidade (`lab/checar.py`).
Calibração do pesquisador: ver `LIVRO.md` (Brier do último ciclo: 0,03).
JEV (S1 externo real): SDK instalado, wrapper `lab/jev.py`, skill `/jev`; **ainda sem chamadas** (rede bloqueia `api.typesafe.ai`). Ver `docs/JEV.md`.

## Placar de achados

| Id | Achado | Nível | Novidade | Fonte |
|---|---|---|---|---|
| A1 | Iterar um passo latente de 33 parâmetros extrapola 25× a profundidade do treino (T1) | N1 | replicação (Deep Thinking) | E001 |
| A2 | Parar por convergência economiza 54% do compute sem perder acerto | N1 | replicação (ACT/PonderNet) | E001 |
| A3 | Colar S1 (confiança) na frente do S2 piora: 0,976 vs 1,000 | N1 | pequena | E001 |
| A4 | ~~S3 com limiar absoluto de confiança não escala~~ **(reinterpretado no E009):** o limiar absoluto se abstinha em N≥64 porque o S2 estava dissolvido e só acertava por sorte de atrator; a abstenção era correta | N2 (negativo, pré-registrado) | — | E002, E009 |
| A5 | Cristalizar o estado **não** estabiliza o pensamento em T1 (0/30 colapsos sem ela) | N2 (negativo) | — | E002 |
| A6 | **Mensagens simbólicas > analógicas** sob ruído, com conhecimento fragmentado entre 2 agentes, sem re-treino: +0,59 a +0,81, p<1e-45, ~200× menos dados por passo | N2 | baixa (comunicação digital) | E003 |
| A7 | Tarefas-atrator mascaram o acúmulo de erros | N1 (diagnóstico) | metodológica | E003 |
| A8 | Nenhum sinal de parada fixado em N=12 funciona em N≥64; "estabilidade do argmax" = critério publicado de ponto fixo, sem ganho | N2 (negativo) | — | E004 |
| A9 | **Transição de fase do S2:** até N=64 o pensamento anda 1 salto/passo; em N=128 resolve por difusão até o equilíbrio, 12× mais rápido e 90% correto | N1 (diagnóstico) | possivelmente nova; ver A11 | E004 |
| A10 | **S2 extrapola sem atrator:** T2, treino k≤4 e N=12 → 100% até k=64 e N=128 (e N=1024 no diagnóstico), sem cristalização | N2 (reproduzido limpo) | baixa (replicação) | E005 |
| A11 | **Lei de nitidez (validada fora da amostra):** o vazamento de um passo prevê onde o S2 se dissolve (25/30 dentro de 1,5×; p=0,0002 contra a constante); o efeito é por passo (independe de d); transição de fase abrupta | **N2** (E007, reproduzido limpo) | baixa | E006, E006d, E007 |
| A13 | **PonderNet reimplementada reproduz o efeito publicado:** passos = d+6, 100% inclusive fora da distribuição; em N=12 a parada por ponto fixo é ~1,9× mais barata com o mesmo acerto (PonderNet não ajustada). Deep Thinking: sem overthinking no motor estruturado | N2 | nenhuma (replicação) | E008, M006 |
| A14 | **S3 em dois tempos:** prever o regime pela lei de nitidez antes de pensar + ponto fixo durante → 100% de cobertura onde dá, 100% de abstenção sem orçamento e **0/600 erros** no regime dissolvido, de N=12 a N=1024, sem ajuste; PonderNet e ponto fixo publicados erram ~51% ali; 19× menos passos que o limiar absoluto | **N2** (reproduzido limpo) | baixa-média | E009 |
| A15 | **Memória de trabalho latente:** pares (nó × contador) num passo relacional; k na entrada, sem controlador contando; treino k≤4, N=8 → 100% até k=64, N=64 (4.160 estados); sem registro, 6%; **a parada emerge da fronteira do registro** (sem marcas de zero, igual) | **N2** (reproduzido limpo) | baixa | E010 |
| A16 | **Modelo de mundo com o mesmo passo (S6):** passo relacional sobre (posição × velocidade) prevê uma partícula numa caixa com paredes, 0 erros em 16 passos, treino L=8 → teste L=64; sem o atributo de parede, 13% de erro. **Ressalva:** os atributos dados tornam a física uma tabela local de 12 casos; a extrapolação em L vem do desenho | **N2** (reproduzido limpo) | baixa | E011 |
| A12 | **O S2 é uma memória associativa tipo Hopfield:** teoria de campo médio (bifurcação sela-nó, m·a(1−a)=1) prevê N_c por modelo com ~9% de erro, sem parâmetros ajustados | N1 (pós-hoc, 30 sementes) | baixa (condição de separação de Hopfield moderno) | E007d |

## Fila de hipóteses (topo = próximo)

Alvos N+1 atuais (EVOLUTION_LOG): S2 → D07 (várias hipóteses) · S3 → D05 (H-S3-fronteira) · S5 → D05 (H-5.4) · S6 → D02 (H-mundo-cru).
Política: a bússola põe H05 e H24 no topo; H-Σ3 é a ponte para o JEV (H26) assim que a rede liberar. S5 está parado há 8 ciclos: diversidade no ciclo 12 ou 13.

| Pri | Id | Hipótese | Nó pai · operador | Degrau-alvo | Custo |
|---|---|---|---|---|---|
| 1 | **H-temperatura-logN** (→ H05) | β(N) ∝ log(N−1) nos logits mantém a nitidez em qualquer N sem re-treino | E007d · MELHORAR | S2 | baixo |
| 2 | **H-Σ3** (→ H24/H12) | Chutar (S1) e verificar com invariante O(1) (S3), S2 só quando falha: domina a fronteira de Pareto do S2 sozinho | E009 · RASCUNHO | S3 D09 | baixo |
| 3 | H-mundo-cru (→ S6 D02) | Modelo de mundo com atributos aprendidos da posição crua (sem distância à parede dada) | E011 · MELHORAR | S6 D02 | médio |
| 4 | **H-S3-fronteira** (→ H08) | Predição conformal mantém risco seletivo ≤ α na zona de transição | E009 · MELHORAR | S3 D05 | médio |
| 5 | H-S3-T2 | O S3 em dois tempos transfere para T2 sem ajuste | E009 · REPLICAR | S3 D14 | baixo |
| 6 | H-custo-ponder | PonderNet ajustada alcança o custo do CONV? | E008 · MELHORAR | G5 | baixo |
| 7 | H-campo-médio-T2 | A teoria de campo médio prevê o N_c em T2 | E007d · REPLICAR | — | baixo |
| 8 | H-5.4 (→ H13) | Código mínimo: bits por passo × robustez | E003 · MELHORAR | S5 D05 | médio |
| 9 | H-latente-livre | Latente vetorial livre (bloqueado pelo teto do Python) | E005 · RASCUNHO | S2 D09 | alto |
| 10 | H-pilha | Dois registros/pilha: siga π k vezes e depois σ j vezes | E010 · MELHORAR | S2 D07 | médio |
| 11 | E-JEV (→ H26) | JEV real em T1/T2 codificadas como Choice (assim que a rede liberar) | — · RASCUNHO | S1 | baixo |
| 12 | H-Σ5 | Energia restante (S0) como entrada do S3 | — · RASCUNHO | S0/S3 | médio |

Diversidade: S6 recebeu o primeiro nó no ciclo 11 (E011). Ainda sem nós: **S0, S4 (além de E003)**; a regra 7 fica adiada com justificativa: nenhuma habilidade de S0/S4/S6 está na fronteira. H16 (modelo de mundo, S6) abre quando H06 for desbloqueada, e é o próximo passo de diversidade. S3 subiu para D04 no ciclo 9.

## Átomos por status

Ver `docs/SISTEMAS.md`. Resumo: 🟩 6 · 🟨 1 · 🟥 2 · ⬜ 20 (29 átomos).
