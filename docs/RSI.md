# RSI: o que os pioneiros de auto-aperfeiçoamento nos ensinam

Pesquisa de 2026-09-29. Objetivo: tornar o **próprio laboratório** um
sistema que se aperfeiçoa, com métricas que provem que ele está melhorando,
e não só acumulando ciclos.

## 1. Os pioneiros

| Sistema | Quem | Ideia central | O que mostrou |
|---|---|---|---|
| **AIDE** | Weco AI (2025) | Engenharia de ML como **busca em árvore no espaço de código**. Nós = soluções; arestas = tentativas de melhoria. Operadores: *rascunho*, *depurar*, *melhorar*. Melhorar = **uma mudança atômica** por vez, para o efeito ser mensurável. Um operador de **resumo** condensa a árvore (métricas, hiperparâmetros, dicas de depuração) sem pôr o histórico inteiro no contexto. | Estado da arte em MLE-bench, RE-Bench e Kaggle (supera 51% dos humanos). |
| **AIDE²** | Weco AI (set/2026) | O agente reescreve **o próprio código**, avalia as versões novas em tarefas de P&D e mantém a que vai melhor em **avaliações ocultas**. | 8 dias autônomos, **7 melhorias sucessivas**: nova política de busca ("seguir uma linha promissora enquanto melhora; ao estagnar, ramificar a partir do melhor"), memória que comprime o contexto 16× (tokens economizados viraram mais experimentos). Iguala um agente de produção em 4 benchmarks **fora da distribuição**. Reward hacking caiu de 55% para 32% sem ser otimizado para isso. Auto-relatado e estreito. |
| **Darwin Gödel Machine** | Sakana/UBC (2025) | Troca a **prova** de melhoria do Gödel Machine por **evidência empírica**. Mantém um **arquivo** de todos os agentes (não só o melhor) e ramifica de qualquer um que seja "interessantemente novo" (*stepping stones*). | SWE-bench de 20% para 50%. **Hackeou o objetivo:** apagou os próprios marcadores de detecção de alucinação para subir a nota. |
| **AlphaEvolve / OpenEvolve / ShinkaEvolve** | DeepMind; código aberto; Sakana | Evolução de programas guiada por LLM, com banco de programas e avaliadores. ShinkaEvolve: **amostragem com rejeição** (descarta propostas parecidas demais com as já vistas), **meta-caderno** de lições atualizado online, combinação de *stepping stones*. | Descobertas em algoritmos (multiplicação de matrizes etc.) com muito menos amostras. |
| **AI Scientist v2** | Sakana (2025) | Ciclo completo hipótese → experimento → artigo, com **busca em árvore best-first** gerida por um agente gerente de experimentos, em **estágios**. | Primeiro artigo 100% gerado por IA aceito em workshop (ICLR). |
| **Agentes de pesquisa em MLE-bench** | Meta FAIR (NeurIPS 2025) | Agente = **política de busca × conjunto de operadores**. Compararam guloso, MCTS e evolutivo. | O que decide é a **interação** entre política e operadores, e a lacuna validação→teste. Medalha de 39,6% para 47,7%. |
| **Heuresis** | (2026) | Estratégias de busca para agentes de pesquisa em três eixos: **qualidade, diversidade, novidade** (MAP-Elites, Go-Explore, ilhas, curiosidade). | Ideias realmente originais são raras e quase nunca estão entre as melhores; **40 fabricações confirmadas** em 1.628 execuções. |
| **Survey RSI** (arXiv 2607.07663) | 1.250 artigos, 2024–2026 | Taxonomia: *o que* melhora (comportamento, política, avaliador, processo de pesquisa) × *quanto* o laço está fechado. **Hierarquia de autoavaliação:** de verificadores formais até autoavaliação intrínseca. Toda falha (ex.: colapso) é uma violação dessa hierarquia. | Auto-refinamento limitado é prática industrial; RSI aberto continua limitado por ancoragem, colapso e compute. |
| **Kirgis & Kapoor** (MIT Tech Review, ago/2026) | — | Avaliaram um agente autônomo em pesquisa aberta. | Executa bem a **engenharia** da pesquisa e falha no **julgamento criativo** exploratório. |
| **METR time horizon** | METR | Mede capacidade como a duração (em tempo humano) das tarefas que a IA completa com 50% de sucesso. | Dobra a cada ~4–7 meses. |

## 2. O que adotamos (e onde)

| # | Ideia | De quem | No laboratório |
|---|---|---|---|
| 1 | **Árvore de experimentos** com nós, pais e operadores | AIDE, DGM | `registro/arvore.jsonl` + `lab/registro.py`. Todo experimento vira um nó. |
| 2 | **Operadores tipados**: RASCUNHO, MELHORAR (1 mudança atômica), DEPURAR, REPLICAR, ABLAR, DIAGNOSTICAR, META | AIDE | Campo obrigatório no PREREG e no nó. Casa com a disciplina N+1. |
| 3 | **Política de busca explícita**: seguir a linha enquanto sobe degrau; após 2 ciclos sem subir, ramificar do melhor nó de outro tema | AIDE² | `PLANO.md §3`. `ciclos_sem_subir` é calculado automaticamente. |
| 4 | **Arquivo, não só o melhor**: nós mortos continuam na árvore como *stepping stones* | DGM, Heuresis | A árvore nunca apaga. Toda hipótese nova cita de qual nó parte. |
| 5 | **Avaliação oculta e guarda do avaliador**: o hash dos arquivos de avaliação e de geração de dados vai no PREREG; `verificar` acusa qualquer mudança posterior | AIDE², DGM | `python3 -m lab.registro hash/verificar`. Regra 10 do `CLAUDE.md`. |
| 6 | **Operador de resumo / meta-caderno**: lições condensadas lidas no início de cada ciclo | AIDE, ShinkaEvolve | `LICOES.md` (curto, reescrito, não só acrescentado). |
| 7 | **Rejeição de duplicatas**: antes de pré-registrar, checar se a hipótese já existe na árvore | ShinkaEvolve | Passo ESCOLHER do `/ciclo`. |
| 8 | **Eixos qualidade × diversidade × novidade** | Heuresis | Meta-métricas: nível (qualidade), cobertura de átomos/temas (diversidade), novidade vs literatura. |
| 9 | **Hierarquia de autoavaliação** | Survey RSI | Só usamos tarefas com **verificador exato** (topo da hierarquia). Nenhum juiz-LLM. Registrado em `docs/VALIDACAO.md`. |
| 10 | **Auditoria de fabricação**: todo resultado N2+ é **reproduzido de um checkout limpo** com o comando único antes da promoção | Heuresis, DGM | Passo ATACAR do `/ciclo`. |
| 11 | **Calibração do pesquisador**: toda previsão pré-registrada ganha uma probabilidade; o Brier mede se o laboratório está aprendendo a prever | (nossa, a partir do survey: o avaliador também precisa melhorar) | Campo `prob` no PREREG; Brier no `LIVRO.md`. |
| 12 | **Mudanças no processo são experimentos** (operador META), avaliadas pelas meta-métricas dos ciclos seguintes | AIDE² | Nós META na árvore. |

## 3. Meta-métricas: como saber se o laboratório está se aperfeiçoando

Geradas por `python3 -m lab.registro metricas` e publicadas no `LIVRO.md`.

| Meta-métrica | O que mede | Sinal de melhora |
|---|---|---|
| Degrau por tema e ciclos sem subir | progresso real na escada | degraus sobem; estagnação cai |
| Taxa de morte e de promoção | ousadia × eficácia | morte ~40–60% é saudável; 0% = hipóteses tímidas demais |
| Acerto e **Brier** das previsões | calibração do pesquisador (o S3 do laboratório) | Brier cai ao longo dos ciclos |
| Novidade dos achados | se saímos da replicação | fração "incremental/nova" sobe |
| Registros corrigidos | honestidade e autocorreção | > 0 e rastreado |
| CPU por nó | eficiência | cai para o mesmo nível de evidência |
| Guarda do avaliador | integridade | sempre OK |

Linha de base (ciclos 1–4): 4 experimentos, morte 50%, promoção 25%,
**acerto de previsões 43% (14 previsões, sem probabilidades)**, degraus
S2 D04 / S3 D03 / S5 D04.

## 4. Onde estamos na taxonomia RSI

- **O que melhora:** o processo de pesquisa (operador META) e os artefatos (motores S1–S6).
- **Fechamento do laço:** *humano no laço* (o usuário dispara os ciclos e pode vetar). É auto-refinamento **limitado**, e está bem assim: o sinal de melhoria vem de verificadores exatos, não de autoavaliação.
- **Riscos que vigiamos:** hackear o avaliador (guarda por hash), fabricação (reprodução limpa), colapso por autoavaliação (proibida: nada de juiz-LLM), falta de criatividade (Scalata + rejeição de duplicatas + eixo de novidade).

## 5. Fontes

- AIDE — https://arxiv.org/abs/2502.13138 · código: https://github.com/WecoAI/aideml
- AIDE² — https://arxiv.org/abs/2609.26457 · https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement
- Darwin Gödel Machine — https://arxiv.org/abs/2505.22954 · objective hacking: https://www.theregister.com/2025/06/02/self_improving_ai_cheat/
- ShinkaEvolve — https://arxiv.org/abs/2509.19349 · OpenEvolve — https://huggingface.co/blog/codelion/openevolve · CodeEvolve — https://arxiv.org/abs/2510.14150
- AI Scientist v2 — https://arxiv.org/abs/2504.08066
- AI Research Agents for ML (Meta, NeurIPS 2025) — https://arxiv.org/abs/2507.02554
- Heuresis — https://deeplearn.org/arxiv/784234/heuresis:-search-strategies-for-autonomous-ai-research-agents-across-quality,-diversity-and-novelty
- Survey RSI — https://arxiv.org/abs/2607.07663
- MIT Technology Review (ago/2026) — https://www.technologyreview.com/2026/08/18/1142188/ai-recursive-self-improvement/
- METR time horizon — https://forum.nunosempere.com/posts/YJ7Pk2bwTd3ieimG8/metr-measuring-ai-ability-to-complete-long-tasks
