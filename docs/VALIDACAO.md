# Como saber se criamos algo revolucionário (e não nos enganamos)

> "O primeiro princípio é que você não deve se enganar — e você é a pessoa
> mais fácil de enganar." — Feynman

Este documento é a **régua**. Nenhum resultado entra no `ESTADO.md` como
"avanço" sem passar por ela. O código da régua está em `lab/estat.py`.

## 1. A escada de evidência

Todo achado recebe um nível. Só se sobe um degrau cumprindo o degrau inteiro.

| Nível | Nome | O que exige | Peso |
|---|---|---|---|
| **N0** | Anedota | Rodou uma vez e "pareceu bom". | Nenhum. Serve só para gerar hipótese. |
| **N1** | Micro-resultado | ≥5 sementes, IC95%, teste feito **uma vez** num conjunto congelado. | Fraco: pode ser artefato da tarefa. |
| **N2** | Resultado controlado | N1 + hipótese **pré-registrada** + linhas de base fortes com o mesmo orçamento de ajuste + ablações que isolam a causa + ≥10 sementes + taxa de colapso relatada. | Moderado: o efeito é real *nesta tarefa*. |
| **N3** | Resultado geral | N2 em **≥3 tarefas de famílias diferentes**, incluindo ao menos uma tarefa externa padronizada (seção 4). | Forte: o efeito provavelmente é um princípio. |
| **N4** | Resultado externo | N3 + comparação com o estado da arte publicado no mesmo benchmark + checagem de novidade na literatura + código que um terceiro roda com um comando. | Publicável. |
| **N5** | Replicado | Um terceiro independente reproduz. | Conhecimento. |

**"Revolucionário"** só pode ser dito em N4+, e só se, além disso:
- **domina a fronteira de Pareto** (desempenho × custo) do melhor método publicado, com IC que não se sobrepõe; **ou**
- resolve uma classe de problema que os métodos existentes **não resolvem** (ex.: extrapolação ≥10× onde o SOTA fica perto de 0%); **e**
- a melhoria vale para **escalas diferentes** (a curva não se achata quando o problema cresce).

## 2. Métricas obrigatórias (o "painel")

Todo experimento relata, por semente e agregadas:

| Dimensão | Métrica | Por quê |
|---|---|---|
| Acerto | Acurácia por dificuldade, IQM entre sementes + **IC95% bootstrap** | A média esconde sementes ruins; o IQM é robusto a elas (Agarwal et al. 2021). |
| Confiabilidade | **Taxa de colapso** (fração de sementes com acurácia < 50%) | O IQM esconde colapsos. Um método que falha 1 vez em 10 não está pronto. |
| Comparação | **P(A>B)** (probabilidade de melhoria), p de permutação, d de Cohen | "A>B" exige P(A>B) com IC acima de 0,5 **e** p < 0,01. |
| Generalização | **Razão de extrapolação** = maior dificuldade resolvida com ≥95% ÷ maior dificuldade do treino | É aqui que o raciocínio de verdade se separa da memorização. |
| Custo | FLOPs por exemplo, passos latentes, parâmetros | Ganho que custa 100× mais não é ganho. |
| Eficiência | **Fronteira de Pareto** acurácia × custo | Diz se o método domina ou só troca custo por acerto. |
| Metacognição (S3) | **E-AURC** (risco × cobertura), **ECE** (calibração), erros entre as respostas dadas | Saber quando não sabe é mensurável. |
| Robustez | *Overthinking*: acurácia com T ≫ necessário | Um bom pensador iterativo não se desfaz se pensar demais (Bansal et al. 2022). |
| Dados | Eficiência amostral (acurácia × nº de exemplos de treino) | Inteligência é generalizar a partir de pouco. |

## 3. Regras contra o autoengano

1. **Pré-registro.** Antes de rodar, escrever em `PREREG.md`: hipótese, previsão numérica, **critério de morte** (o resultado que refuta), métricas e sementes. Nada disso muda depois de ver os dados. Se mudar, vira outro experimento.
2. **Conjuntos congelados.** Treino, validação e teste gerados com sementes fixas e separadas. O teste é tocado **uma vez** por hipótese. Ajuste só na validação.
3. **Linhas de base honestas.** Toda linha de base recebe o mesmo orçamento de ajuste do método novo. Sempre incluir: (a) a mais simples possível; (b) o método publicado mais próximo; (c) o próprio método sem a peça nova (ablação).
4. **Ablações.** Remover cada componente e medir. Se remover a peça "revolucionária" não piora, ela não é a causa.
5. **Controle de vazamento.** Perguntar sempre: "existe um atalho trivial?" (no E001 existia: com só uma raiz, bastava achar o nó que aponta para si). Testar uma heurística boba contra a tarefa.
6. **Resultados negativos são registrados.** Vão para o `DIARIO.md` com o mesmo destaque dos positivos.
7. **Checagem de novidade antes de afirmar.** Buscar na literatura. Se já existe, o achado é **replicação** (valioso, mas não é novidade).
8. **Hierarquia de autoavaliação** (survey RSI 2607.07663): usamos só o topo, verificadores exatos com verdade calculável. Nada de juiz-LLM ou de o modelo avaliar a si mesmo como métrica.
9. **Guarda do avaliador e reprodução limpa:** hashes no PREREG e reprodução de um checkout limpo antes de promover a N2+ (lições do DGM e do Heuresis; ver `docs/RSI.md`).
10. **Sementes que ninguém escolhe e poder estatístico:** sementes de teste derivadas do commit do pré-registro (`lab/sementes.py`) e tamanho de amostra calculado antes (`lab.estat.n_para_diferenca`).
11. **Coerência entre registros:** `lab/checar.py` antes de todo commit.
12. **Um revisor hostil.** Antes de promover um nível, escrever os 3 argumentos mais fortes contra o resultado e respondê-los com dados.

## 4. Tarefas: a escada de dificuldade

Do micro ao externo. Cada ideia sobe por ela.

| Degrau | Família | Exemplos | Por que |
|---|---|---|---|
| T1 | Grafos/ponteiros | achar a raiz (E001), alcançabilidade, componentes conexos | Dificuldade controlável, verdade exata. |
| T2 | Aritmética/estado | soma/multiplicação de muitos dígitos, paridade, autômatos | Clássico de generalização de comprimento. |
| T3 | Algoritmos (estilo CLRS) | BFS, caminho mínimo, ordenação, busca | Benchmark padrão de raciocínio algorítmico neural (CLRS-30). |
| T4 | Quebra-cabeças | labirintos, Sudoku | Mesmos benchmarks de HRM/TRM e Deep Thinking: comparação direta com o publicado. |
| T5 | Abstração | subconjunto do ARC-AGI-1/2 | Referência pública de raciocínio fluido. |
| T6 | Interativo | ambientes estilo ARC-AGI-3 | Exploração e aprendizado em tempo real. Fronteira atual (humanos ~100%). |

Restrição do ambiente: por enquanto tudo roda em **Python puro** numa CPU.
Isso limita T4+ a instâncias pequenas. É uma escolha consciente: força
modelos minúsculos, que é justamente onde a ideia "estrutura > escala"
precisa se provar.

## 5. Mapa do que já existe (para não reinventar)

| Linha | Referência | Relação com o nosso trabalho |
|---|---|---|
| Pensamento recorrente que extrapola | Schwarzschild et al. 2021; Bansal et al. 2022 ("Deep Thinking", *recall*, *progressive loss*, sem overthinking) | O E001 **replica** o fenômeno em miniatura. |
| Parada adaptativa | Graves 2016 (ACT); Banino et al. 2021 (PonderNet) | O S3 do E001 é uma versão por regra fixa. Falta comparar com a aprendida. |
| Recursão latente pequena | HRM (2025, 27M parâmetros); TRM (Jolicoeur-Martineau 2025, 7M, 45% ARC-AGI-1) | Estado da arte no nosso eixo. Alvo de comparação em T4/T5. |
| Raciocínio latente em LLMs | Coconut (Meta, 2024) e críticas de 2025 ("Do Latent Tokens Think?") | Alerta: o latente pode virar atalho. Precisamos de testes causais. |
| Generalização de comprimento em recorrentes | Buitrago et al. 2025 (hipótese dos estados não explorados) | Explica por que o estado contínuo falha em N grande. Ligado à cristalização. |
| Predição seletiva | risco × cobertura, AURC/E-AURC | Métrica do S3. |
| Avaliação confiável | Agarwal et al. 2021 (*rliable*) | Base da nossa régua. |
| Reprodutibilidade | Checklist NeurIPS (Pineau et al.) | Base do nível N4. |

## 6. Fontes

- Bansal et al., *End-to-end Algorithm Synthesis with Recurrent Networks: Extrapolation without Overthinking*, NeurIPS 2022 — https://arxiv.org/abs/2202.05826
- Banino et al., *PonderNet: Learning to Ponder*, 2021 — https://arxiv.org/abs/2107.05407
- Jolicoeur-Martineau, *Less is More: Recursive Reasoning with Tiny Networks* (TRM), 2025 — https://arxiv.org/abs/2510.04871
- *Tiny Recursive Models on ARC-AGI-1: Inductive Biases, Identity Conditioning, and Test-Time Compute*, 2025 — https://arxiv.org/abs/2512.11847
- Buitrago et al., *Understanding and Improving Length Generalization in Recurrent Models*, ICML 2025 — https://arxiv.org/abs/2507.02782
- *Do Latent Tokens Think? A Causal and Adversarial Analysis of Chain-of-Continuous-Thought*, 2025 — https://arxiv.org/abs/2512.21711
- Agarwal et al., *Deep RL at the Edge of the Statistical Precipice*, NeurIPS 2021 — https://github.com/google-research/rliable
- Pineau et al., *Improving Reproducibility in Machine Learning Research*, JMLR 2021 — https://jmlr.org/papers/v22/20-303.html
- Checklist NeurIPS — https://neurips.cc/public/guides/PaperChecklist
- CLRS Algorithmic Reasoning Benchmark — https://github.com/google-deepmind/clrs
- ARC Prize (ARC-AGI-1/2/3) — https://arcprize.org
