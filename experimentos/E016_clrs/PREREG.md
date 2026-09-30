# E016 — Pré-registro: protocolo CLRS reimplementado (Bellman-Ford, n = 16 → 64) com um motor aprendido e Deep Thinking

**Escrito antes de rodar. Não editar depois da primeira execução completa.**
Trilha: B (algoritmos, T3). Átomos: 2.1 em família nova. Nível de partida: N0 (os geradores e os resolvedores de `lab/tarefas_clrs.py` já estão testados em `lab/test_tarefas_clrs.py`).
Habilidade-alvo: **H23** (fronteira, prioridade 3). Nó pai: **E008** (linhas de base) · Operador: **RASCUNHO**. Degrau-alvo: S2 D11 (algoritmos clássicos), só a infraestrutura.

## Por que este e não H24/H08
- **H24 (piloto do ciclo 14):** nas tarefas T1/T2, verificar custa o mesmo que resolver.
- **H08 (piloto deste ciclo, M008):**
  - o escore da lei de nitidez sobre o JEV, m = ln(p₁(N−1)/(1−p₁)), piora a transferência: com o limiar calibrado em N=8 a 2%, o risco é 0,15 em N=32 e 0,28 em N=64;
  - os erros do JEV em N grande são confiantes, então a lei do S2 não descreve o S1 externo.
- A H23 abre o G1 e dá à H24 uma família (caminho mínimo) em que verificar um certificado custa O(E), contra O(VE) para resolver.

## Hipótese
Um motor de relaxação suave com 5 parâmetros, treinado em n = 16, degrada em n = 64. A causa não é a temperatura, e sim o **viés sistemático** dos pesos aprendidos (a·w + b com b > 0): as diferenças entre o caminho ótimo e o segundo melhor encolhem com n, e um viés fixo passa a decidir. Um substituto duro (Bellman-Ford exato com os pesos a·w + b aprendidos) prevê a acurácia do motor.

## Pilotos (declarados; sementes 1690–1692)
- Com o termo do próprio nó, a relaxação suave desce para sempre (não converge). Foi removido.
- Afiar β até 32× não recupera n = 64 (0,87 → 0,84): **não é temperatura** (diferente do E013).
- Semente 1692 (300 iterações), acurácia de ponteiros:

  | n | APREND | SURR | DT | GULOSO |
  |---|---|---|---|---|
  | 16 | 0,844 | 0,844 | 0,797 | 0,57 |
  | 32 | 0,836 | 0,832 | 0,738 | 0,48 |
  | 64 | 0,705 | 0,701 | 0,600 | 0,54 |

  Parâmetros aprendidos: a = 0,992; b = 0,045.
- Em outra semente, de outro piloto: 0,97 / 0,95 / 0,87. A variação entre sementes vem de quanto b chega perto de 0.

## Relação com a literatura
- **CLRS-30** (Veličković et al., ICML 2022): protocolo n = 16 → 64 e acurácia de ponteiros. O Bellman-Ford dos GNNs de referência fica em ~0,9+ fora da distribuição.
- **Neural execution of graph algorithms** (Veličković et al. 2020): o alinhamento da agregação min com o algoritmo.
- **Deep Thinking com progressive loss** (Bansal et al. 2022), reimplementação mínima do princípio.

O que difere: o motor tem 5 parâmetros e o alinhamento é dado (o operador é soft-min). A pergunta é de onde vem o erro fora da distribuição. **Novidade: baixa.** A reimplementação não é comparável 1:1 com os números do CLRS (sem o dataset oficial, sem hints; declarado em `lab/tarefas_clrs.py`).

## Montagem
- Grafos Erdős–Rényi com p = 0,5, pesos U(0,1), fonte aleatória; verdade = `lab.tarefas_clrs.bellman_ford`.
- Treino: 200 grafos com n = 16; 300 iterações de Adam com gradiente por diferenças centrais; lote de 8.
- Teste: n ∈ {16, 32, 64}, 20 grafos por n e semente; parada por ponto fixo (tol 1e−7; orçamento 4n).
- Braços:
  - **APREND** (T = 16 fixo no treino);
  - **DT** (progressive: T ~ U{1..32});
  - **SURR** (diagnóstico);
  - **GULOSO** (vizinho de menor peso);
  - **EXATO** (= 1).
- Sementes de treino **1600–1604** (N1: 5). Sementes de teste derivadas do commit deste PREREG.

## Previsões e critérios de morte
| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1 | APREND em n = 16 ≥ 0,95 (IQM) | 0,35 | — |
| P2 | APREND em n = 64 ≤ (n = 16) − 0,05 | 0,80 | APREND em 64 ≥ APREND em 16 → não há degradação a explicar |
| P3 | DT em n = 64 não supera APREND por mais de 0,03 | 0,75 | — |
| P4 | SURR prevê APREND em n = 64 (±0,03) em ≥ 80% das sementes | 0,80 | ≤ 40% → **a hipótese do viés morre** |
| P5 | GULOSO < APREND em n = 16 | 0,85 | — |

**H23 desbloqueada** (N1) se a avaliação completa rodar (5 sementes, todos os braços, todos os n, com IC) e a reprodução for idêntica. O critério da H23 é de infraestrutura e não exige desempenho.

## Sementes e poder
- N1: 5 sementes × 20 grafos por n; ~16–64 ponteiros por grafo. A variação dominante é entre sementes (o valor de b), e é ela que o IC reporta.
- Custo: ~1–2 min de CPU por semente (n = 64 domina) → ~3 min de parede.

## Guarda do avaliador
```
experimentos/E016_clrs/e016.py : 9f98f6d6015ae077
lab/tarefas_clrs.py            : fd2b3258eb55e4f4
lab/sementes.py                : 4a5e4da1269f9b77
lab/estat.py                   : 40af21b3e5c3d582
```

## Ameaças conhecidas
- **Atalho trivial:** com a = 1, b = 0 e β → ∞, o motor **é** o Bellman-Ford (acurácia 1,0). O motor aprendido só pode errar por não chegar lá. É um teste de precisão do aprendizado, não de capacidade.
- **Otimizador:** diferenças centrais com 300 iterações é um otimizador fraco. Outro otimizador reduziria b. Isso é declarado; o resultado vale para este procedimento de treino.
