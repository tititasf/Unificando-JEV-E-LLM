# Fragmentação dos Sistemas: átomos, sincronias e sínteses

Cada sistema é quebrado em **funções atômicas**. Para cada átomo:
*como existe hoje* (biologia / IA) → *átomo testável* (a menor versão que
cabe num micro-experimento) → *métrica* → *com quem se sincroniza*.

O S7 ("colapso quântico / engenharia da realidade") fica **fora do escopo
experimental**: não tem hoje átomo testável honesto. Os outros sete
(S0–S6) têm.

Status dos átomos: ⬜ não testado · 🟨 em teste · 🟩 evidência N1+ · 🟥 hipótese morta.

---

## S0 — Substrato (o templo que se mantém)

| Átomo | Biologia | IA hoje | Átomo testável | Métrica | Status |
|---|---|---|---|---|---|
| 0.1 Orçamento | glicose/ATP limitam o cérebro | limite de tokens/FLOPs fixo | agente com energia finita escolhe quanto pensar | Pareto acc×custo | ⬜ |
| 0.2 Integridade | reparo de DNA, sono | checkpoints, ECC | detectar e reparar corrupção de pesos/estado **em execução** | acc após dano de x% | ⬜ |
| 0.3 Interocepção | sinais viscerais de fome/dor | quase inexistente | expor sinais internos (energia, erro, carga) como entrada do S3 | ganho do S3 com vs. sem | ⬜ |
| 0.4 Redundância | dois hemisférios, plasticidade | ensembles, réplicas | réplicas baratas que votam | colapso com k réplicas | ⬜ |

## S1 — Intuição (uma passada)

| Átomo | Biologia | IA hoje | Átomo testável | Métrica | Status |
|---|---|---|---|---|---|
| 1.1 Reconhecimento | córtex visual feedforward | classificadores, "modelos de decisão" tipo JEV | MLP de 1 passada | acc por dificuldade | 🟩 E001: bom só em d=0 |
| 1.5 S1 externo real (JEV) | — | JEV (TypeSafe System One) | JEV respondendo T1/T2 como Choice, respostas gravadas | acc × tamanho, ECE, erros confiantes | 🟩 E012: S1 de um salto (0,90→0,63 com N), composição no acaso; iterado segue q^k; 0/516 erros confiantes |
| 1.2 Hábito / amortização | prática vira automático (gânglios da base) | destilação | S2 ensina S1 ao longo da "vida" | custo médio × tempo de vida | ⬜ |
| 1.3 Saliência | amígdala, pulvinar | roteadores MoE | decidir o que merece S2 | E-AURC do roteador | 🟥 E001: roteador por confiança piora |
| 1.4 Categorização / colapso | percepção categórica | argmax, VQ | cristalização do estado | colapso de sementes, ruído | 🟥 E002: não estabiliza o pensamento em T1 (retestar com ruído interno, H-Σ1b) |

## S2 — Deliberação (pensar iterando)

| Átomo | Biologia | IA hoje | Átomo testável | Métrica | Status |
|---|---|---|---|---|---|
| 2.1 Passo reutilizável | circuitos recorrentes corticais | recorrentes com pesos compartilhados, TRM | mesmo passo aplicado T vezes | razão de extrapolação | 🟩 N2 em T1 (E002) e T2 (E005, sem atrator, 16× em k); regime muda quando a margem deixa de vencer ~log N (lei de nitidez, E007, N2; tipo Hopfield); **escala resolvida pela temperatura derivada da lei: 100% até N=4096 sem re-treino (E013, N2)** |
| 2.2 Memória de trabalho | córtex pré-frontal | *recall* (Deep Thinking), contexto | reinjetar o problema a cada passo | overthinking | 🟩 E001: sem overthinking até T=200 |
| 2.3 Múltiplas hipóteses | exploração mental paralela | beam search, superposição latente | tarefa com ambiguidade (ciclos, vários caminhos) | acc contínuo vs. cristalizado | ⬜ E004 |
| 2.4 Composição | *chunking* | subrotinas, programas | passos que chamam passos | extrapolação composicional | ⬜ |

## S3 — Metacognição (pensar sobre o pensar)

| Átomo | Biologia | IA hoje | Átomo testável | Métrica | Status |
|---|---|---|---|---|---|
| 3.1 Parada | sensação de "já sei" | ACT, PonderNet | parar quando o estado converge | economia de compute | 🟩 E001: −54% (regra fixa) |
| 3.2 Saber que não sabe | sentimento de dúvida | predição seletiva | abster-se se não convergiu | E-AURC, erros/respondidas | 🟩 E009 (N2): S3 em dois tempos, 0/600 erros no regime dissolvido de N=12 a N=1024, sem ajuste |
| 3.3 Verificação | checar a conta | verificadores, provas | invariante barato ("a raiz aponta para si") | acc de chutar-e-verificar vs. S2 | ⬜ |
| 3.4 Alocação | escolher estratégia | roteamento | quanto S1, quanto S2, dado o orçamento S0 | Pareto | ⬜ |
| 3.5 Aprender a aprender | plasticidade dirigida | meta-learning | ajustar o próprio limiar por experiência | regret | ⬜ |

## S4 — Coletivo (enxame e coexistência)

| Átomo | Biologia/sociedade | IA hoje | Átomo testável | Métrica | Status |
|---|---|---|---|---|---|
| 4.1 Conhecimento fragmentado | cada formiga vê um pedaço | multiagente, federado | 2+ agentes com metade do grafo cada | acc vs. agente único | 🟩 E003: passo treinado sozinho funciona fragmentado, sem re-treino |
| 4.2 Consenso | quórum em abelhas | votação, debate | k agentes ruidosos convergem | acc × k | ⬜ |
| 4.3 Especialização | divisão de trabalho | MoE | agentes idênticos se especializam sozinhos | entropia de papéis | ⬜ |
| 4.4 Normas de coexistência | regras sociais, ecologia | mecanismos, contratos | recurso compartilhado limitado; regras emergentes evitam a tragédia dos comuns | bem-estar total, desigualdade | ⬜ |

## S5 — Comunicação direta ("ressonância")

| Átomo | Biologia | IA hoje | Átomo testável | Métrica | Status |
|---|---|---|---|---|---|
| 5.1 Canal latente vs. simbólico | hormônios (analógico) × linguagem (discreto) | JSON/texto × embeddings | mesma tarefa, canal contínuo vs. cristalizado, com ruído | acc × σ × d | 🟩 E003 (N2): simbólico vence por até +0,81, ~200× menos dados |
| 5.2 Ontologia emergente | linguagem nasce do uso | comunicação emergente | agentes inventam o vocabulário discreto do zero | acc, tamanho do vocabulário, composicionalidade | ⬜ |
| 5.3 Transferência de habilidade | ensino | destilação, cópia de pesos | agente A passa o "passo" a B por mensagens | exemplos até B aprender | ⬜ |
| 5.4 Compressão | sinais mínimos | quantização | menor nº de bits por passo que mantém acc | bits × acc | ⬜ |

## S6 — Hipertempo (simular futuros, raciocinar do fim)

| Átomo | Biologia | IA hoje | Átomo testável | Métrica | Status |
|---|---|---|---|---|---|
| 6.1 Modelo de mundo | hipocampo prevê | world models, JEPA | prever o próximo estado do ambiente | erro de previsão × horizonte | 🟩 E011: caixa com paredes, 0 erros em 16 passos, L 8→64 (atributos dados) |
| 6.2 Rollout | imaginar antes de agir | MCTS, MuZero | simular k futuros latentes e escolher | acc × k | ⬜ |
| 6.3 "Voz de atrator" (do fim para o começo) | planejar pela meta | busca bidirecional, *backward chaining* | na tarefa da raiz: busca vinda da meta encontra a vinda do início | passos até resolver | ⬜ |
| 6.4 Crédito temporal | dopamina e atraso | TD-learning | recompensa atrasada k passos | acc × k | ⬜ |

---

## A matriz de sincronia

O que cada sistema **entrega** a outro. As sínteses (Σ) são as hipóteses de
que uma dessas pontes cria algo que nenhum sistema tem sozinho.

```
            para → S0        S1             S2              S3            S4/S5          S6
de S0            ·         -          -            orçamento,       cota de          horizonte
                                                     interocepção     recurso          permitido
de S1          custo      ·          chute inicial,   confiança        símbolo          -
                                      cristal (Σ1)
de S2           -       destilação     ·             trajetória,      estado para      passo = modelo
                         (Σ2)                        convergência     enviar (Σ1)      de mundo (Σ4)
de S3        pedido de  limiar        parar /           ·             "não sei"         quando
             energia                  continuar                        coletivo         planejar
de S4/S5        -       vocabulário   conhecimento    consenso de       ·               futuros de
                        compartilhado  fragmentado     confiança                         outros
de S6           -          -          meta a atingir   custo previsto   planos            ·
                                       (Σ4)            (Σ5)
```

## As sínteses (novas perspectivas a testar)

| Id | Nome | Afirmação | Experimento |
|---|---|---|---|
| **Σ1** | Cristal Comum | ~~O mesmo colapso discreto estabiliza o pensamento e a comunicação.~~ **Parcial:** discretizar a *mensagem* dá robustez enorme (E003, N2); discretizar o *pensamento* não ajudou em T1 (E002). Aberto: com ruído interno (H-Σ1b) e em tarefa sem atrator (H-T2). | E002, E003 |
| **Σ2** | Ciclo de Amortização (o S2 como compilador) | Um sistema que destila o S2 no S1 durante a "vida" fica mais barato sem perder acerto, como o especialista humano. | E005 |
| **Σ3** | Verificar é mais barato que gerar | S1 chuta, S3 verifica com uma invariante O(1), S2 só entra se falhar. Deve dominar o roteador por confiança do E001. | E006 |
| **Σ4** | Atrator | Pensar a partir da meta (S6) com o mesmo passo do S2 reduz os passos de *d* para ~*d*/2. | E007 |
| **Σ5** | Orçamento como sentido | Dar ao S3 a "sensação" de energia restante (S0) produz alocação melhor que um limiar fixo. | E008 |
| **Σ6** | Ontologia emergente | Agentes que precisam coordenar inventam um código discreto, e esse código vira a representação interna do pensamento de cada um. | E009 (depende de Σ1) |

## O S2 como meta-arquiteto (princípio orientador, ciclo 10)

O S2 mais forte não é o que pensa tudo; é o que **compila** o próprio pensamento
nos outros sistemas e se retira. Tradução testável para cada sistema:

| Sistema | O que o S2 faz por ele | Habilidade / átomo |
|---|---|---|
| S1 | resolve uma vez, destila a resposta num reflexo O(1) | **H24** (amortização verificada), 1.2 |
| S3 | ergue invariantes intocáveis que verificam o S1 e o próprio S2 | H12 (chutar e verificar), H19 (prova) |
| S0 | projeta o orçamento para que a autorregulação não precise pensar | H18 (orçamento como sentido) |
| S4 | desenha regras de coexistência em que a cooperação emerge sem controle central | **H25** (regra cooperativa emergente) |
| S5–S7 | *metáfora* (regra 8). Sombra testável: saber **quando parar de deliberar** e entregar ao reflexo | H24, S3 D08 |

O risco medido: um S1 compilado sem verificação erra com confiança (E001, A3). Por isso
a H24 exige a corte do S3.

## O Ultra-Sistema 1 (orientação do ciclo 11): o que é testável

A orientação propõe inverter a hierarquia: o S1 como **hiper-heurística não-local** (vê o
padrão inteiro de uma vez), e o S2 rebaixado a **compilador/tradutor a posteriori** (explica e
verifica o que o S1 já viu). Tradução para átomos (regra 8: o resto fica como metáfora):

| Ideia | Átomo testável | Onde |
|---|---|---|
| S1 não-local vê a resposta inteira | um S1 de uma passada (JEV real ou MLP) acerta T1/T2 em que tamanhos? Onde para de ver? | H26 (E-JEV), 1.1, 1.5 |
| S2 como tradutor a posteriori | o S2 só verifica/corrige o chute do S1; custo total e erros confiantes contra o S2 sozinho | H12, H24 |
| S3 como repulsa somática (ética como invariante) | invariante O(1) que veta a resposta sem deliberar (E009 é a versão mínima: "dissolvido = não sei") | H07 ✔, H12 |
| S0 corpo como instrumento | orçamento como entrada do S3 (H-Σ5) | H18 |
| S4 sincronia estigmérgica | agentes coordenam por marcas no ambiente, sem mensagem direta | H25 (variante) |
| S5–S7 vantagem nativa, Mushin | **metáfora**. Sombra testável: menos deliberação com o mesmo acerto (Pareto acerto × custo) | G5 |

Aposta registrável: se o Ultra-S1 existe em miniatura, a união S1(JEV)+S3 cobre boa parte
das instâncias em O(1), e o S2 entra só no resto, dominando a fronteira de Pareto do S2
sozinho **com zero erros confiantes**. É o experimento H24/H26 assim que o JEV responder.

## Protocolo Σ: a mensagem universal (ontologia comum)

Proposta de interface única entre módulos, testada experimento a experimento:

```
Mensagem = (
  conteudo    : cristal (índice discreto)  |  distribuição (quando a dúvida importa)
  confianca   : [0,1]          ← S3 lê
  custo       : passos/FLOPs   ← S0 lê
  origem      : sistema e agente
  horizonte   : agora | futuro simulado (S6)
)
```

A ideia é a do "modelo de decisão tipado" (JEV), só que generalizada:
**cada sistema fala por mensagens tipadas e pequenas**, e a escolha entre
cristal e distribuição é ela mesma uma decisão metacognitiva. Se Σ1 e Σ6
se confirmarem, essa interface deixa de ser uma convenção de engenharia e
passa a ser o próprio vocabulário do pensamento.
