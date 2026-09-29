# E005 — Pré-registro: o motor S2 numa tarefa sem atrator (T2 "salto exato")

**Escrito antes de rodar (nem o smoke rodou). Não editar depois da primeira execução completa.**
Trilha A. Átomos: 2.1, 1.4. Nível de partida: N1 em T1 (E001), só numa família de tarefas.
Nó pai: **E001**. Operador: **REPLICAR** (mesmo motor, nova família de tarefas). Degrau-alvo: **S2 D05**.

## Hipótese
H1: o passo latente S2 (33 parâmetros, o mesmo do E001), treinado com k ≤ 4 saltos em
N=12, extrapola para k=64 e N=128 numa tarefa sem atrator **se o estado for
cristalizado a cada passo**; com estado contínuo, o erro se acumula e ele falha.
H2 (sobre A9): o atalho difusivo do E004d depende do atrator; aqui, sem atrator, o
contínuo em N=128 **não** acerta por difusão.

## Relação com a literatura
- *Capabilities and Fundamental Limits of Latent Chain-of-Thought* (arXiv 2602.01148): o raciocínio latente acumula ruído sem quantização discreta; o CoT explícito corrige erros pela escolha de tokens. **Prevê exatamente H1.**
- *Learning Compositional Functions with Transformers from Easy-to-Hard Data* (2505.23683): composição de permutações de k saltos; o erro cresce exponencialmente em k, a menos que o erro por passo seja super-polinomialmente pequeno.
- Deep Thinking (Bansal 2022): extrapolação por iteração, mas em tarefas com estrutura espacial.
- Novidade esperada: **baixa**. O valor está no contraste limpo com o T1: a mesma cristalização que não ajudou numa tarefa-atrator (E002) deve ser decisiva numa tarefa sem atrator.

## Montagem
- Tarefa T2: permutação aleatória π de N nós, início s, k saltos → π^k(s). Verificador exato.
- Treino: N=12, k ∈ {1..4}, 20.000 exemplos, 600 iterações de Adam, BPTT supervisionando só t=k. Sementes **500–509** (10).
- Teste congelado: sementes 80000+s; N ∈ {12, 32, 64, 128}; k ∈ {4, 8, 16, 32, 64}; 10 exemplos por célula.
- Braços (mesmo modelo treinado):
  - **SEM_ITER** (linha de base mais simples): 1 passada, responde após 1 salto.
  - **CONT** (publicado mais próximo: recorrente com pesos compartilhados, estilo Deep Thinking): estado contínuo, k passos.
  - **AFIA** (ablação: afiar sem discretizar): z ← z⁴ normalizado a cada passo.
  - **CRIST** (proposto): argmax a cada passo.
- Métricas: IQM da acurácia entre sementes + IC95%, colapsos (<0,5) por célula, razão de extrapolação (maior k com IQM ≥ 0,95 ÷ 4), P(A>B) e permutação CRIST × CONT em (128, 64).

## Previsões e critérios de morte
| # | Previsão numérica | Prob. | Morte se |
|---|---|---|---|
| P1 | CRIST: IQM ≥ 0,99 em **todas** as 20 células, 0 colapsos | 0,75 | alguma célula < 0,95 → **H1 morta** (S2 fica em D04) |
| P2 | CONT: IQM ≤ 0,50 em (N=128, k=64) | 0,75 | ≥ 0,95 → cristalizar é desnecessário (H1 morta na parte "contínuo falha"; D05 atingido pelo contínuo) |
| P3 | CONT: IQM ≥ 0,95 em (N=12, k=64) | 0,50 | — (informativa: acúmulo de erro depende de N) |
| P4 | AFIA em (128, 64): IQM estritamente entre CONT e CRIST | 0,45 | — (se = CRIST, o mecanismo é "afiar", não "discretizar") |
| P5 | SEM_ITER: IQM ≤ 0,10 para todo k ≥ 4 | 0,95 | > 0,10 → a tarefa tem atalho trivial; **experimento inválido** |
| P6 | CRIST > CONT em (128, 64) com P(A>B) = 1 e p < 0,01 | 0,70 | p ≥ 0,01 → inconclusivo |
| P7 (H2) | CONT em (128, 16) ≤ 0,50 (sem atrator, a difusão não salva) | 0,70 | ≥ 0,95 → existe um atalho difusivo mesmo sem atrator: rever A9 |

**Degrau S2 D05 atingido** se algum braço tiver IQM ≥ 0,95 até k=64 (16× o treino) e N=128, sem atrator.

## Guarda do avaliador (hashes no momento do pré-registro)
```
experimentos/E005_t2_salto/tarefa_t2.py : b62e43a6a77ab648
experimentos/E005_t2_salto/e005.py      : 41f23921c9dc6ddc
experimentos/E001_mlu/mlu.py            : 601604873fae9691
lab/estat.py                            : 0d5d3bc108a6b4ba
```

## Ameaças conhecidas
- Atalho trivial: em permutações há pontos fixos e ciclos curtos (π^k(s) = s às vezes). P5 controla: se responder "1 salto" já acerta muito, há atalho.
- Os atributos de aresta (i = π(j)) dão ao passo um viés forte: aprender "siga o ponteiro" é fácil. O teste é sobre **precisão ao longo de muitos passos**, não sobre descobrir o algoritmo.
- O controlador conhece k (conta os passos). A parada (S3) não é testada aqui.
