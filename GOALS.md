# GOALS — as estrelas-guia e a árvore de habilidades

Este é o **norte** do laboratório. A imaginação (escadas de 30 degraus), os
ciclos (experimentos) e o RSI (o laboratório se aperfeiçoando) convergem
aqui: a imaginação propõe **para onde**, a árvore diz **o que falta para
chegar**, os ciclos **desbloqueiam** habilidades com evidência, e o RSI
torna o caminho **mais rápido**.

Estado calculado (progresso, fronteira, prioridades): [`BUSSOLA.md`](BUSSOLA.md),
gerado por `python3 -m lab.bussola` a partir de `registro/habilidades.json`.

```
   IMAGINAÇÃO (Scalata, D30)  ──propõe──►  GOALS (estrelas-guia)
                                              ▲
                                              │ exigem
   CICLOS (experimentos)  ──desbloqueiam──►  HABILIDADES (árvore)
                                              ▲
                                              │ acelera
   RSI (META, meta-métricas)  ───────────────┘
```

## 1. As seis estrelas-guia

Cada goal nasce de uma **lacuna documentada no mundo**, tem um **marco
falsificável** e um **nível de evidência exigido**. Nenhum é "fazer um
chatbot melhor"; todos são capacidades que hoje não existem ou só existem
de forma estreita.

| Goal | O que falta no mundo (lacuna) | Marco que faria dizer "uau" | Nível | Sistemas |
|---|---|---|---|---|
| **G1 · Pensador de tamanho livre, com prova** | Circuitos de softmax aprendidos **precisam** se dispersar com o tamanho (Veličković et al., ICML 2025). Provas de generalização de tamanho só existem com alinhamento algorítmico feito à mão (Wang/UCSD 2025). | Um motor aprendido **do zero**, cujo programa é extraído e **provado correto para todo N automaticamente** pelo próprio laboratório, em 2+ famílias de tarefas. | N4 | S2 |
| **G2 · Saber exatamente quando não sabe** | Estimadores de confiança estão "quebrados" até em classificadores fortes (estudo com 84 modelos ImageNet); limiares não transferem entre escalas (nosso E004). | **Zero** respostas erradas com confiança sob mudança de escala 10× e de família de tarefa, sem reajuste, com cobertura ≥ 95% onde acertar é possível. | N3 | S3 + S1 |
| **G3 · Uma língua que nasce, ensina e pensa** | Não se sabe que condições geram linguagem emergente composicional; quase não há transferência de habilidades multi-passo por ela. | Agentes inventam do zero um código que **transmite um algoritmo** de um agente a outro, e esse código vira a representação interna do pensamento de quem aprende. | N4 | S5 + S4 + S2 |
| **G4 · Descobrir regras de um mundo desconhecido** | ARC-AGI-3 (2026): humanos 100%; melhor sistema público ~30%. Explorar e aprender regras em tempo real segue em aberto. | Um sistema de ≤ 1M parâmetros que descobre regras ocultas de ambientes interativos novos e vence um subconjunto público do ARC-AGI-3. | N4 | S2 + S3 + S6 |
| **G5 · Pensar com o custo certo** | Computação é alocada por limiar fixo ou por aprendizado caro; não existe um "sentido de energia" governando quanto pensar. | Um S0+S3 que domina a fronteira de Pareto acerto × custo de PonderNet e de limiar fixo em 3 famílias, com o mesmo mecanismo. | N3 | S0 + S3 |
| **G6 · Auto-aperfeiçoamento recursivo demonstrado** | AIDE² (set/2026) é a primeira evidência de RSI em P&D de IA, estreita e auto-relatada; medição confiável de RSI é o nicho mais vazio (survey 2607.07663). | O próprio laboratório mostra, com avaliação oculta, que suas mudanças de processo **aceleram a descoberta**: ciclos-por-degrau cai pela metade e o Brier do pesquisador < 0,15, com a causa atribuída a nós META. | N3 | LAB |

## 2. Os quatro patamares de "uau" (honestidade primeiro)

Um marco só é anunciado no patamar que a evidência sustenta:

| Patamar | Exige | O que se pode dizer |
|---|---|---|
| **M1 · Marco de laboratório** | N2 local, pré-registrado | "Funciona aqui, em tarefas nossas." |
| **M2 · Marco de campo** | N3 + benchmark externo, empatando com o publicado | "Chegamos onde a área está, com menos recursos." |
| **M3 · Marco de fronteira** | N4: supera o estado da arte **ou** resolve um problema aberto documentado, com checagem de novidade | "Nunca foi feito." |
| **M4 · Marco de humanidade** | N5: um terceiro independente reproduz, e a capacidade abre uma área | "Descoberta." |

Um goal só é considerado **alcançado** no patamar do seu nível exigido. Até
lá, o que existe é progresso na árvore.

## 3. A árvore de habilidades

Cada habilidade é um **degrau atravessável** entre sistemas: tem critério
numérico, pré-requisitos e o experimento que a desbloqueou. Ela só fica
verde com evidência (nós da árvore de experimentos com nível ≥ o mínimo).
Visão resumida (estado vivo e critérios completos na `BUSSOLA.md`):

```
H01 Passo que extrapola ✔ ─┬─ H04 Lei de nitidez ─┬─ H05 Nitidez em qualquer escala ─┐
                           │                      ├─ H07 S3 legível ─┬─ H08 S3 calibrado ──┼─► G2
                           │                      │                  └─ H12 Chutar+verificar ┴─ H18 Orçamento ─► G5
                           │                      └────────┐
                           └─ H06 Memória de trabalho ─────┼─ H09 Latente livre
                                 ├─ H10 Várias hipóteses ──┼─ H17 Planejar da meta ─┐
                                 ├─ H16 Modelo de mundo ───┘                        ├─ H20 Regras desconhecidas ─► G4
                                 └─ H11 Algoritmos (T3) ─ H19 Programa provado ─► G1  (+H08, H10)
H02 Mensagem simbólica ✔ ─ H13 Código mínimo ─ H14 Língua emergente ─ H15 Ensinar um passo ─► G3
H03 Laboratório ✔ ─ H21 RSI medido ─► G6
```

## 4. Regras de convergência (como isto guia cada ciclo)

1. **Todo ciclo declara a habilidade que ataca.** O PREREG diz `Habilidade: Hxx`. Se a hipótese não avança nenhuma habilidade, ou ela entra na árvore como habilidade nova (com critério e pré-requisitos), ou o ciclo não vale.
2. **A fronteira manda.** Só se atacam habilidades 🟨 (todos os pré-requisitos verdes). A ordem sugerida é a prioridade da bússola: (1 + habilidades que dependem desta + 3 × goals que ela abre) ÷ custo. A política de busca do `PLANO.md §3` pode sobrepor com justificativa (estagnação, diversidade).
3. **Desbloquear é um ato registrado.** Quando um experimento cumpre o critério no nível mínimo, o id dele entra em `desbloqueada_por` e a `BUSSOLA.md` é regerada no mesmo commit.
4. **Uma habilidade pode voltar a trancar.** Se um resultado posterior derrubar a evidência (como o E002 fez com o E001), o id sai de `desbloqueada_por` e a queda vai para o DIARIO.
5. **Como nasce um goal novo (convergência).** Uma visão de D25–D30 de alguma escada vira goal quando há: (a) lacuna documentada com fonte; (b) marco numérico falsificável; (c) caminho na árvore (pré-requisitos existentes ou novos, com critério); (d) ≥ 2 direções de exploração que ele abre. Sem os quatro, fica como imaginação no EVOLUTION_LOG.
6. **Como nasce uma habilidade nova.** Quando um ciclo revela uma capacidade intermediária necessária (ex.: E006 revelou a "lei de nitidez"), ela entra na árvore entre as existentes, com critério numérico.
7. **Radar de lacunas.** A cada 5 ciclos, uma busca na literatura por goal: a lacuna ainda existe? Alguém já chegou? Se alguém chegou, o goal sobe a barra ou é substituído, e o registro diz por quê.
8. **O RSI mede o caminho.** As meta-métricas passam a incluir habilidades desbloqueadas por ciclo; o G6 é alcançado quando essa taxa sobe por causa de mudanças META.

## 5. Onde estamos (ciclo 6)

- Verdes: H01 (passo que extrapola), H02 (mensagem simbólica), H03 (laboratório).
- Fronteira, na ordem da bússola: **H04 lei de nitidez** (abre 9 habilidades e 4 goals) → **H06 memória de trabalho** (abre 8 e 3 goals) → H13 código mínimo → H21 RSI medido.
- Isso bate com a fila do `ESTADO.md` (H-lei-eps no topo), mas agora com uma razão calculada: H04 é o gargalo de G1, G2, G4 e G5 ao mesmo tempo.

## Fontes das lacunas

- Veličković et al., *Softmax Is Not Enough (for Sharp Size Generalisation)*, ICML 2025 — https://mlanthology.org/icml/2025/velickovic2025icml-softmax
- Provas de generalização de tamanho com alinhamento algorítmico (Wang, UCSD 2025) — https://simons.berkeley.edu/talks/yusu-wang-ucsd-2025-08-13 · *On Provable Length and Compositional Generalization* — https://arxiv.org/html/2402.04875v6
- Estimadores de confiança "quebrados" (84 classificadores ImageNet) — https://arxiv.org/pdf/2305.15508v2
- Comunicação emergente composicional em aberto — https://arxiv.org/pdf/2012.05011 · https://papers.neurips.cc/paper_files/paper/2021/file/9597353e41e6957b5e7aa79214fcb256-Paper.pdf
- ARC-AGI-3 — https://arcprize.org/results
- AIDE² — https://arxiv.org/abs/2609.26457 · Survey RSI — https://arxiv.org/abs/2607.07663
