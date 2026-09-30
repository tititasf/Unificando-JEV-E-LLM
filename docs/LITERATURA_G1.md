# Revisão de literatura do G1: generalização de tamanho com prova (ciclo 18, 2026-09-30)

Objetivo: achar a lacuna **exata** que ainda está aberta antes de gastar computação. Esta revisão substitui as 1 a 3 buscas por ciclo.

## 1. O que já está resolvido (não atacar)

| Trabalho | O que faz | O que exige |
|---|---|---|
| **FloydNet** (Yu et al., jan/2026, arXiv 2601.19094) | > 99% fora da distribuição em quase todo o CLRS-30; TSP exato | tensor global de todos os pares, O(n³) por camada; sem prova |
| **DNAR**, *Discrete Neural Algorithmic Reasoning* (Rodionov & Prokhorenkova, ICML 2025) | 100% e **prova de correção para qualquer tamanho** | estados discretos **desenhados à mão**, atenção dura e **dicas** (trajetória do algoritmo) |
| **Nerem et al.**, COLT 2026 (arXiv 2503.19173) | prova que uma GNN com perda regularizada por esparsidade implementa K passos de Bellman-Ford e extrapola para qualquer tamanho | arquitetura alinhada; prova escrita à mão, válida só para caminho mínimo |
| **Wittig et al.**, ICML 2026 (arXiv 2602.13106) | condições suficientes para aprender algoritmos com prova (caminho mínimo, árvore geradora mínima, programação dinâmica); impossibilidade para MPNNs padrão | conjunto de treino curado, regularização, prova à mão |
| **Veličković et al.**, ICML 2025 | a softmax **precisa** se dispersar com o tamanho; propõem **temperatura adaptativa** na inferência | — |
| **ASEntmax** (Vasylenko et al., ICLR 2026) | temperatura aprendida como função do comprimento; até 1000× de extrapolação | — |
| **Rodionov & Prokhorenkova**, NeurIPS 2023 | treino **sem dicas**, competitivo no CLRS | sem prova |
| **MIPS** (Michaud, Liao, Tegmark et al., 2024) | extrai automaticamente de RNNs um programa Python verificável (32/62 tarefas) | sequências; RNN pequena; sem grafos |

**Consequência para o laboratório:**
- A lei de temperatura do E017 é uma variante de algo **conhecido**: temperatura adaptativa e Scalable-Softmax.
- Levá-la ao CLRS oficial seria incremental, num benchmark saturado.
- **Decisão: não fazer.** O E017 fica como N2 interno, com novidade baixa.

## 2. A lacuna que continua aberta (nenhum trabalho achado faz as três coisas)

1. **Rede genérica**, sem estados discretos desenhados e sem arquitetura alinhada à mão, treinada **só com pares entrada-saída** (sem dicas);
2. **extração automática** do programa que ela aprendeu (como no MIPS, mas em grafos);
3. **prova automática** de que o programa extraído é correto **para todo n**, em **2 ou mais famílias** de algoritmo.

Quem chega mais perto de cada ponto:
- o DNAR prova, mas com os estados e as dicas dados;
- Nerem e Wittig provam, mas à mão e com alinhamento;
- o MIPS extrai automaticamente, mas não trabalha com grafos nem prova para todo n;
- o FloydNet generaliza, mas sem prova.

**Esse é o marco do G1**, agora com a literatura por trás. Resolver a combinação seria um resultado novo de verdade, em nível de workshop ou conferência se funcionar em 2 famílias.

## 3. Plano (ordem de ataque, cabe em CPU)

1. **Gerador e avaliador oficiais:** os amostradores do `dm-clrs` (Bellman-Ford, BFS e depois árvore geradora mínima), treino n = 16, teste n = 64, com a métrica oficial de ponteiros.
2. **Rede genérica em PyTorch:** MPNN com mensagens MLP e agregação max, sem dicas. Linhas de base: Deep Thinking e perda progressiva.
3. **Extração automática** (o núcleo novo):
   - esparsificar;
   - quantizar as mensagens;
   - fazer regressão simbólica sobre uma linguagem mínima ({min, max, +, seleção, comparação});
   - checar o programa extraído contra o algoritmo em milhares de grafos.
4. **Prova automática para todo n:**
   - reduzir a correção a um invariante local (por exemplo, a relaxação de Bellman-Ford é monótona e tem ponto fixo igual às distâncias);
   - verificar o invariante sobre a regra extraída por enumeração finita ou com um resolvedor SMT, em que o passo indutivo é local e o tamanho do grafo não entra.
5. **Repetir em uma segunda família** (BFS ou árvore geradora mínima). Só com 2 famílias se fala em G1.

**Risco honesto:** o passo 3 pode falhar, porque redes genéricas raramente aprendem algo limpo. Isso também é informativo, e é publicável como resultado negativo bem medido: quando a extração falha e por quê.

## 4. Os outros goals, no mesmo caminho

- **G2 (zero erros confiantes):** um programa extraído e provado dá zero erros por construção. Onde a extração falha, o S3 se abstém. Usar a rede com o programa verificado como corte é a ponte G1 → G2.
- **Medição do JEV (G2, resultado negativo):** é o único dado que ninguém mais tem. Vai ser escrito como nota técnica curta, em paralelo.
- **G4 (ARC-AGI-3) e G6 (RSI):** fora do alcance em CPU agora. Continuam registrados, mas sem ciclos até o G1 dar sinal.

## Fontes
- https://arxiv.org/abs/2601.19094 (FloydNet)
- https://arxiv.org/abs/2402.11628 (DNAR)
- https://arxiv.org/abs/2503.19173 (Nerem et al.)
- https://arxiv.org/abs/2602.13106 (Wittig et al.)
- https://arxiv.org/abs/2410.01104 (Veličković et al.)
- https://arxiv.org/abs/2506.16640 (ASEntmax)
- https://arxiv.org/abs/2306.13411 (NAR sem dicas)
- https://arxiv.org/abs/2402.05110 (MIPS)
- https://arxiv.org/abs/2205.15659 (CLRS-30)
