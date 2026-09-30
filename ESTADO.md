# ESTADO — onde estamos

Atualizado no fim de cada ciclo. Última atualização: ciclo 18 (2026-09-30).

> Norte (ciclo 18, regra 19): a **lacuna do G1** ([`docs/LITERATURA_G1.md`](docs/LITERATURA_G1.md)), decidida em [`CRITICA.md`](CRITICA.md). A bússola ([`BUSSOLA.md`](BUSSOLA.md)) passou a ser consultiva.

## Fase atual

**Fase 1 — Micro (T1–T2): portão formalmente atingido no ciclo 5** (passo latente iterado com N2 em T1 e T2). Ressalva: mecanismo **conhecido** (replicação).
Antes da Fase 2 (T3, algoritmos contra Deep Thinking): ~~fechar a lei de nitidez (H04)~~ ✅ ciclo 7; ~~validar as linhas de base publicadas (H22)~~ ✅ ciclo 8; ~~protocolo CLRS reimplementado (H23)~~ ✅ ciclo 16 (E016).
Infra disponível: T2 sem atrator (`experimentos/E005_t2_salto/tarefa_t2.py`), passo O(N) (`experimentos/E006_lei_margem/passo_rapido.py`), linhas de base (`lab/baselines.py`), tarefas CLRS (`lab/tarefas_clrs.py`), sementes derivadas do commit (`lab/sementes.py`), controle de qualidade (`lab/checar.py`).
Calibração do pesquisador: ver `LIVRO.md` (Brier do último ciclo: 0,05).
JEV (S1 externo real): **conectado e medido** (E012, 3.298 chamadas, `jev-1.13.0`); wrapper `lab/jev.py`, skill `/jev`, credencial persistente no ambiente. Ver `docs/JEV.md`.

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
| A17 | **JEV = S1 de um salto; S2∘S1 segue q^k; o JEV sabe quando não sabe:** uma passada acerta um salto (0,90→0,63 de N=8 a 64) e fica no acaso com k≥2; iterado um salto por chamada, acc(k) ≈ q^k (8/9 células); T1 com parada por ponto fixo 0,55 vs 0,06; p(escolha) 0,65 nos acertos vs 0,22 nos erros, **0/516 erros com p ≥ 0,9** | **N2** (respostas gravadas, reprodução idêntica) | baixa | E012 |
| A18 | **Temperatura derivada da lei (nitidez em qualquer escala):** β(N) = 1 + ln((N−1)/11)/m, com a margem m medida sem rótulos, leva T1 e T2 de 17% e 0% (β=1) a **100% em N=4096** (341× o treino), 10/10 sementes; em T2 mantém o vazamento do treino (razão 0,91). **Ressalva (atalho):** qualquer afiação (β=3, Scalable-Softmax, argmax) também acerta; a TEORIA é a afiação mínima e prevista. Em T1 a razão fica ≈0,5 (o vazamento para o próprio nó também some) | **N2** (reproduzido limpo) | baixa (forma do Scalable-Softmax, coeficiente derivado) | E013 |
| A19 | **Várias hipóteses vivas = forma do passo, não temperatura:** a mesma tabela treinada em uma hipótese, como **mistura** de softmaxes, recupera o conjunto em superposição (F ≤ 8, k ≤ 64) e BFS, 100% até N=4096, massa (1 − ε)^k em 120/120; a forma **global** falha em qualquer β (dissolve ou o vencedor leva tudo; 0/240 em SUP) | **N2** (reproduzido limpo) | baixa | E014 |
| A20 | **Código mínimo = função do custo do canal:** com energia fixa por mensagem (canal do E003), o código aprendido com N−1 dimensões supera o one-hot (0,83–0,99), com N/2 empata (limite de Rankin) e abaixo perde; com amplitude fixa por canal, N/4 dimensões erram 0,1–12% do one-hot. O aprendido vence o sorteado (24/24) e o binário à mão | **N2** (reproduzido limpo) | nenhuma (replicação da teoria clássica) | E015 |
| A21 | **Dilema do viés no Bellman-Ford suave (CLRS n=16→64):** o soft-min desce até ln(grau)/β abaixo do mínimo; o viés aprendido b > 0 compensa, mas b pequeno **diverge** (distâncias descem sem fim) e b grande penaliza saltos; o b estável cresce com n. Motor de 5 parâmetros: 0,91 → 0,62; o Bellman-Ford duro com a·w+b prevê o motor em 4/5 sementes; **Deep Thinking vence** (0,84 em n=64) porque a perda progressiva empurra b para a faixa estável | N1 (reproduzido limpo) | baixa | E016 |
| A22 | **Lei de temperatura da relaxação suave (T3, 20× o treino):** a descida do soft-min tem duas fontes medidas sem rótulo, 1/w_min (deriva nos 2-ciclos) e ln(grau) (empates). Com β = κ·ln(g_max)/(a·w_min), b = 0 e κ aprendido em n=16, o caminho mínimo fica em 0,993 (n=160) e 0,991 (n=320), contra DT 0,615 (p = 0,0002). Ablações: sem a lei 0,58, com b livre 0,44. BFS satura (DT = LEI = 1). **Ressalva:** o β efetivo é quase o min duro; a lei diz quanto afiar, que o treino sozinho não acha | **N2** (reproduzido limpo) | baixa | E017 |
| A23 | **Rede genérica sem dicas → programa provado (SP), mas a rede é supérflua:** um MPNN genérico (mensagem MLP, agregação max), treinado só com entrada → saída em n=16, guarda nas transições internas a relaxação exata do Bellman-Ford. A extração automática a recupera com início correto em **5/5** sementes, e o programa acerta 1,000 em n=256 (a rede: 0,80 em n=64). **No caminho mais largo, 0/5:** a rede imprecisa puxa a extração para uma regra de média. A **síntese direta sem rede acha os dois (10/10 contra 5/10, Fisher p=0,033)**. O ponteiro do WP é trivial (aresta mais pesada) | N1 | baixa (a síntese basta) | E018 |
| A12 | **O S2 é uma memória associativa tipo Hopfield:** teoria de campo médio (bifurcação sela-nó, m·a(1−a)=1) prevê N_c por modelo com ~9% de erro, sem parâmetros ajustados | N1 (pós-hoc, 30 sementes) | baixa (condição de separação de Hopfield moderno) | E007d |

## Fila de hipóteses (topo = próximo)

Alvos N+1 atuais (EVOLUTION_LOG): S1 → D02 (H-JEV-seletivo, pendente de sinal novo) · S2 → D08 (H-pilha) · S3 → D05 (H-S3-fronteira) · S5 → D06 (mensagem com confiança) · S6 → D02 (H-mundo-cru).
Política: H05 (c13), H10 (c14), H13 (c15), H23 (c16) e H11 (c17) fechadas. A H24 precisa de uma família de busca (M009: no caminho mínimo não amortiza). A H08 segue sem sinal que transfira (M007, M008). S6 e S3 são os próximos candidatos de diversidade.

| Pri | Id | Hipótese | Nó pai · operador | Degrau-alvo | Custo |
|---|---|---|---|---|---|
| G1a | **H-G1-busca** (foco G1) | Achar uma família em que a síntese direta **falha** (linguagem grande demais para enumerar, ou estado auxiliar invisível na entrada → saída: MST/Prim com chave, fluxo, DFS com pilha) e medir se as transições da rede encurtam a busca da síntese (candidatos mecanísticos contra enumeração cega, com o mesmo orçamento) | E018 · RASCUNHO | S2 D18 | alto |
| G1b | **H-mec-pura** | Isolar a contribuição mecanística: escolher a regra só pelo ajuste nas transições, sem circuito fechado contra a saída; mede se o interior da rede é mais fiel ao algoritmo que a saída (WP: 0/5 pela saída) | E018 · ABLAR | S2 D18 | baixo |
| G1c | **H-G1-externo** | Rodar a rede genérica no CLRS-30 oficial (dm-clrs) em BF/Dijkstra/MST e comparar com os números publicados (MINAR, Triplet-GMPNN), com `externo: true` | E018 · REPLICAR | — | médio |
| 0c′ | ~~H-bf-prova~~ | **Coberta pelo E018** na forma forte: rede genérica, não o motor LEI | — | — | — |
| 0 | ~~H-bf-cert~~ → **H-busca-cert** (→ H24) | **Piloto M009:** no caminho mínimo o chute não se paga (verificar Ω(E), e o SPFA já é quase linear). Levar a H24 para uma família de busca (SAT, quebra-cabeça), em que resolver ≫ verificar: o S1 ordena, o S3 verifica em O(tamanho), o S2 busca | M009 · RASCUNHO | S3 D08 | médio |
| 0b | ~~H-bf-lei~~ | **Feito no E017 (N2): H11 desbloqueada** (a lei certa inclui 1/w_min) | — | — | — |
| 0c | **H-bf-prova** (→ H19, G1) | Extrair o programa do motor LEI e verificar automaticamente que é o Bellman-Ford (para todo n) | E017 · MELHORAR | S2 D18–D19 | médio |
| 0d | **H-lei-unificada** | A mesma receita (β pela descida da normalização medida no dado) em BFS esparso, árvore geradora mínima e T1/T2 | E017/E013 · MELHORAR | S2 D10 | médio |
| 1 | ~~H-JEV-seletivo~~ (→ H08) | **Pilotado no ciclo 13 (M007): nenhum sinal do JEV transfere um limiar de N=8 para N=64** (risco por salto 2% → 11–25%); no ciclo 16 (M008) a margem da lei de nitidez piora (0,28 em N=64). Precisa de sinal novo: Mondrian por escala ou temperatura | E012 · MELHORAR | S1 D02 | — |
| 2 | **H-temp-S3** (→ H24/H08) | O S3 em dois tempos (E009) sobre o S2 com temperatura TEORIA: cobertura 100% até N=4096 sem abstenção e 0 erros confiantes | E013 · MELHORAR | S3 D05 | baixo |
| 2b | ~~H-temp-mínima-D07~~ | **Caiu no E014:** nenhuma temperatura do passo global preserva hipóteses desiguais; a superposição vem da mistura | — | — | — |
| 2d | **H-sup-limiar** (→ H08) | O S3 lê R sem conhecer \|R\|: limiar pela lei da mistura (w·(1 − ε)^k), risco controlado | E014 · MELHORAR | S3 D05 | baixo |
| 2e | H-mist-JEV | O S2 propaga a distribuição `Choice` do JEV como mistura em vez do argmax: acc(k) acima de q^k? | E012/E014 · MELHORAR | S1 D03 | baixo |
| 2f | H-mist-treino | Treinar já na forma de mistura (T2) e testar T1 | E014 · MELHORAR | S2 | médio |
| 2c | H-temp-JEV | Codificar o Choice do JEV em blocos (menos opções efetivas) recupera q(N) como a lei prevê | E012/E013 · MELHORAR | S1 D05 | baixo |
| 3 | H-mundo-cru (→ S6 D02) | Modelo de mundo com atributos aprendidos da posição crua (sem distância à parede dada) | E011 · MELHORAR | S6 D02 | médio |
| 4 | **H-S3-fronteira** (→ H08) | Predição conformal mantém risco seletivo ≤ α na zona de transição | E009 · MELHORAR | S3 D05 | médio |
| 5 | H-S3-T2 | O S3 em dois tempos transfere para T2 sem ajuste | E009 · REPLICAR | S3 D14 | baixo |
| 6 | H-custo-ponder | PonderNet ajustada alcança o custo do CONV? | E008 · MELHORAR | G5 | baixo |
| 7 | H-campo-médio-T2 | A teoria de campo médio prevê o N_c em T2 | E007d · REPLICAR | — | baixo |
| 8 | ~~H-5.4~~ | **Feito no E015** (N2): curva bits × robustez medida | — | — | — |
| 8b | **H-código-agentes** (→ H14) | O código emerge entre dois agentes treinados só pela tarefa (E003) e chega à curva do E015? | E015 · MELHORAR | S5 D10 | médio |
| 8c | H-custo-canal | O S0 fixa o recurso escasso e o código aprendido muda de forma (espalhado × denso) | E015 · MELHORAR | S5/S0 | baixo |
| 9 | H-latente-livre | Latente vetorial livre (bloqueado pelo teto do Python) | E005 · RASCUNHO | S2 D09 | alto |
| 10 | H-pilha | Dois registros/pilha: siga π k vezes e depois σ j vezes | E010 · MELHORAR | S2 D07 | médio |
| 11 | H-JEV-autoponteiro | `Noul` "x aponta para si?" separado corrige os 58 falsos/omitidos pontos fixos do ITER_PF | E012 · MELHORAR | S1 D07 | baixo |
| 11b | H-JEV-nitidez | q(N) do JEV segue a forma da lei de nitidez (ponte S1 ↔ S2) | E012 · DIAGNOSTICAR | S1 D05 | baixo |
| 12 | H-Σ5 | Energia restante (S0) como entrada do S3 | — · RASCUNHO | S0/S3 | médio |

Diversidade: S6 recebeu o primeiro nó no ciclo 11 (E011). Ainda sem nós: **S0, S4 (além de E003)**; a regra 7 fica adiada com justificativa: nenhuma habilidade de S0/S4/S6 está na fronteira. H16 (modelo de mundo, S6) abre quando H06 for desbloqueada, e é o próximo passo de diversidade. S3 subiu para D04 no ciclo 9.

## Átomos por status

Ver `docs/SISTEMAS.md`. Resumo: 🟩 8 · 🟨 1 · 🟥 2 · ⬜ 18 (29 átomos).
