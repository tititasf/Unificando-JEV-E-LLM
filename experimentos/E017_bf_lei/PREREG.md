# E017 — Pré-registro: lei de temperatura da relaxação suave (caminho mínimo e BFS, n = 16 → 160)

**Escrito antes de rodar. Não editar depois da primeira execução completa.**
Trilha: B (T3, algoritmos). Átomos: 2.1 (lei de nitidez em família nova).
Nível de partida: N1 (E016: o dilema do viés).
Habilidade-alvo: **H11** (fronteira; S2 D11). Nó pai: **E016** · Operador: **MELHORAR**. Degrau-alvo: S2 D11 (na trilha T3; o degrau atual do tema S2 é D07, e o D08 segue como alvo da trilha A).

## Por que este e não H24/H08
- **H24, piloto M009 deste ciclo.** No caminho mínimo, um S1 local (estimativa de 2 saltos, ou uma heurística de direção na grade) nunca acerta o grafo inteiro (0/60), então o certificado global sempre falha.
  - Com o reparo localizado (o S3 aponta os nós que violam o certificado e o S2 corrige a partir deles), o custo fica 0,56–0,89× o de um SPFA frio. O chute não se paga.
  - O ganho contra o Jacobi (1,8–5,4×) vem da lista de trabalho, não do S1.
  - Motivo: verificar custa Ω(E) e o resolvedor clássico já é quase linear. A H24 precisa de uma família em que resolver custe muito mais que verificar (busca), não de caminho mínimo.
- **H08:** continua sem sinal que transfira (M007, M008).
- A H11 é o seguimento direto do E016.

## Hipótese
O erro fora da distribuição do motor de relaxação suave (E016) vem da **descida do soft-min**, e ela tem duas fontes mensuráveis no próprio grafo, sem rótulos:
- **(i) o termo de volta numa aresta barata**, d_u + a·w ≈ d_v + 2a·w, que compete com o pai verdadeiro. O motor deriva para baixo enquanto β·a·w_min ≲ 1.
- **(ii) os k pais empatados**, que descem o valor por ln(k)/β. É a lei ln N do E013.

A lei β = κ·ln(g_max)/(a·w_min), com b = 0 e κ aprendido em n = 16, dispensa o viés compensador do E016 e extrapola para 10× (n = 160) e 20× (n = 320).

## Pilotos (declarados; sementes 11, 12, 1790–1796, fora da faixa)
- **Com b = 0 e β constante**, o β necessário cresce com n:
  - n = 64 precisa de β ≈ 1024;
  - n = 160 não chega a 0,95 com 1024.
  - Com D0 = 0, que é um limite inferior, o motor não sobe mais; D0 precisa ser um limite superior.
- **Com β = κ/w_min, a = 1 e κ = 2 fixos (sem treino):** acerto 1,000 em n = 16, 64 e 160, em 8–12 passos.
- **Smoke do avaliador** (40 iterações, 2 sementes):

  | braço | BF n=160 | BF n=320 |
  |---|---|---|
  | LEI | 0,978 | 0,972 |
  | LEI_B | 0,47 | — |
  | CONST_B0 | 0,52 (sem convergir) | — |

  Em BFS: LEI 1,000 e DT 1,000.
- **A primeira versão da lei**, só κ/(a·w_min), **divergiu em BFS** (w_min = 1). Faltava o fator de empate ln(g_max). Corrigido antes deste commit.

## Relação com a literatura
- **Wittig et al., *Which Algorithms Can GNNs Learn?*** (ICML 2026; arXiv 2602.13106) provam a generalização de tamanho do Bellman-Ford aprendido. As condições são alinhamento algorítmico, conjunto de treino pequeno e curado, e regularização diferenciável.
- **Scalable-Softmax / E013:** temperatura que cresce com log N.
- **Veličković et al. 2025** (*softmax is not enough*): a dispersão da softmax com o tamanho.

O que difere: a temperatura sai de uma lei derivada do **mecanismo de falha medido** (a deriva nos 2-ciclos e os empates), com as grandezas lidas do próprio grafo, e não de uma regularização nem de um conjunto curado. **Novidade: baixa.**

## Montagem
- **Motor do E016** (importado; hash guardado), com os parâmetros efetivos por grafo em `efetivo()`.
- **Treino:**
  - n = 16, 200 grafos por semente e família;
  - 300 iterações, Adam com lr 0,1, diferenças centrais, lote 8;
  - **progressive loss em todos os braços** (T ~ U{1..32}).
- **Braços:**
  - **DT**: o do E016 (β, β_p e b aprendidos); é a linha de base publicada, reimplementação mínima do princípio;
  - **LEI**: método; b = 0;
  - **LEI_B**: ablação; lei com b aprendido;
  - **CONST_B0**: ablação; β constante aprendido, b = 0;
  - **GULOSO**;
  - **EXATO** (= 1).
- **Famílias:**
  - **BF**: Erdős–Rényi p = 0,5, pesos U(0,1). Métrica: acurácia de ponteiros CLRS (pai único quase certamente).
  - **BFS**: mesmos grafos com pesos 1. Métrica: **pai válido** (vizinho na distância d−1). Isso é um desvio declarado da convenção de fila do CLRS, que um motor local não representa.
- **Teste:**
  - n ∈ {16, 64, 160}, com 10, 10 e 5 grafos por semente;
  - em BF, também n = 320 (3 grafos), **só LEI**, por custo;
  - parada por ponto fixo (tol 1e−7; orçamento 4n).
- **Sementes:** treino **1700–1709** (N2: 10). Sementes de teste derivadas do commit deste PREREG.

## Previsões e critérios de morte
| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1-BF | LEI em n = 160: IQM ≥ 0,95 | 0,80 | < 0,90 → **a lei não extrapola** |
| P1-BFS | LEI em n = 160: IQM ≥ 0,95 | 0,85 | — |
| P2-BF | LEI > DT em n = 160, permutação p < 0,05 | 0,85 | DT ≥ LEI → a lei não acrescenta ao DT |
| P2-BFS | LEI > DT em n = 160, permutação p < 0,05 | 0,10 | — (o piloto mostra DT = LEI = 1,000; ver critério) |
| P3 | CONST_B0 em n = 160 (BF) ≤ 0,90 | 0,75 | ≥ 0,95 → **a lei é desnecessária** (atalho: basta um β constante aprendido) |
| P4 | LEI_B < LEI − 0,03 em n = 160 (BF) | 0,65 | — |
| P5 | LEI em n = 320 (BF, 20×) ≥ 0,95 | 0,70 | — |

**H11 desbloqueada** (N2) se P1-BF, P1-BFS e P2-BF passam **e** LEI ≥ DT − 0,01 em BFS.
- O critério da H11 ("batendo o DT com IC") só discrimina em BF.
- Em BFS com p = 0,5 e pai válido, os dois saturam. Declaro isso **antes** dos dados de teste, e a ressalva vai para o registro da habilidade.

## Sementes e poder
- 10 sementes (N2).
- Por semente, n = 160 dá 5 × 160 = 800 ponteiros. Para separar 0,84 de 0,97, `n_para_diferenca(0,84; 0,97)` = 118 ponteiros; a variação que resta é entre sementes, e ela é o que o IC e a permutação medem.
- `n_para_largura(0,97; 0,02)` = 312 < 800.
- Custo estimado: ~200 s de CPU por semente (DT e CONST_B0 a n = 160 esgotam o orçamento de 640 passos) → ~33 min de CPU, ~9 min de parede. É o motor estruturado do `docs/STACK.md`, então o gatilho de stack não dispara.

## Guarda do avaliador
```
experimentos/E017_bf_lei/e017.py : d559dac668fc57bf
experimentos/E016_clrs/e016.py   : 9f98f6d6015ae077
lab/tarefas_clrs.py              : fd2b3258eb55e4f4
lab/sementes.py                  : 4a5e4da1269f9b77
lab/estat.py                     : 40af21b3e5c3d582
```

## Ameaças conhecidas
- **Atalho trivial (regra 7):** com a = 1, b = 0 e β → ∞, o motor **é** o Bellman-Ford (piloto: β = 1024 constante dá 0,97 em n = 160).
  - O teste é se a afiação **mínima, prevista pela lei e aprendida em n = 16** basta, e se um β constante **aprendido** (CONST_B0) não basta.
  - Não é um teste de capacidade.
- **A lei usa w_min e g_max do grafo de teste.** São grandezas de entrada, sem rótulo, como a margem do E013.
- **BFS com p = 0,5** tem profundidade ~2. É uma família fácil, e a métrica de pai válido é mais branda que a do CLRS.
