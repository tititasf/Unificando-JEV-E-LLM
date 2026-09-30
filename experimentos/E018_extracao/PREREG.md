# E018 — Pré-registro: extrair da rede genérica ou sintetizar direto? (caminho mínimo e caminho mais largo)

**Escrito antes de rodar. Não editar depois da primeira execução completa.**
Trilha: B (T3, algoritmos). Foco G1 (`docs/LITERATURA_G1.md`, CRITICA ciclo 18: PIVOTAR). Nível de partida: N0.
Habilidade-alvo: **H19** (programa extraído e provado; declarada pela regra 19 acima da fronteira da bússola).
Nó pai: **E017** · Operador: **RASCUNHO**. Degrau-alvo: S2 D18. É um salto sobre o N+1, autorizado pela CRITICA do ciclo 18; o ponto de partida é o E017 (D11).

## Pergunta
A lacuna do G1 pede uma rede **genérica e sem dicas** cuja regra seja extraída automaticamente e provada para todo n. Antes de investir nessa rota, o teste que um revisor hostil faria primeiro é este:

**Nestas famílias, a rede acrescenta algo?** Ou a mesma linguagem de regras, ajustada direto aos pares entrada → verdade (síntese, sem rede), já acha o programa provável?

## Hipótese
**H-rede-supérflua.** Em caminho mínimo (min,+) e caminho mais largo (max,min):
- a síntese direta recupera a relaxação exata do semianel (com início correto) em ≥ 80% das sementes;
- a extração a partir da rede genérica (comportamental ou mecanística) recupera em menos sementes, porque a rede imperfeita puxa a escolha para um programa que imita os erros dela.

Se a hipótese vale, a rota "rede → extração → prova" só tem valor em famílias onde a síntese direta falha. O próximo ciclo procura essa família.

## Pilotos (declarados; sementes 0, 7 e 1890–1896, fora da faixa)
- **Rede genérica** (MPNN, agregação max, 4000 passos, n = 16), acurácia de ponteiro em n = 16 / 32 / 64:

  | família | n = 16 | n = 32 | n = 64 |
  |---|---|---|---|
  | SP | 0,943 | 0,887 | 0,815 |
  | WP | 0,980 | 0,975 | 0,948 |

  - Treino: ~570 s de CPU por família, com 1 fio.
  - Sonda anterior (M010, `g1_sonda.py`): o estado acompanha o BF de k saltos.
- **Extração v1**, com início tirado da decodificação de h0: falhou nas duas famílias.
  - A decodificação intermediária x^t = Linear(h^t) não tem escala treinada.
  - A regra certa ficou em 2º lugar no SP.
- **Extração v2** (este avaliador), numa rede por família:

  | rota | SP | WP |
  |---|---|---|
  | síntese direta | exata, erro 0 | exata, erro 0 |
  | mecanística | min(x_v, min_u x_u + w), mas com início 1,0 | `media`/`minf` (errada; erro 0,043 contra a rede) |
  | comportamental | igual à mecanística | igual à mecanística |

  - O início 1,0 no SP basta porque as distâncias em ER p = 0,5 são < 1; ele não é provável para todo grafo.
  - Por isso a ordem de desempate foi fixada **antes deste PREREG**: primeiro o início que nada supõe, ±∞. É uma escolha pós-piloto e está declarada.
- **Smoke** (300 passos, 2 sementes): achou um bug no ponteiro, que incluía o próprio nó e não fixava a fonte; corrigido.
- **O smoke revelou um atalho trivial no WP (regra 7).** argmax_u w_uv (a aresta mais pesada) é sempre um pai válido.
  - Prova: c_v ≤ w_max e c_u* ≥ min(c_v, w_max) = c_v.
  - A árvore do caminho mais largo é a árvore geradora máxima. O ponteiro do WP não precisa dos valores.
  - O reconhecimento aceita esse ponteiro, que é provadamente correto. A parte do WP que testa a extração é a **regra de valor**.
- **Todas as probabilidades abaixo são pós-piloto** (`pos_piloto: true`).

## Relação com a literatura
- **MINAR** (2025/26): circuitos em redes genéricas sem dicas; sem extração de programa, sem prova.
- **MIPS** (Michaud et al. 2024): extração automática de programa, só em RNN.
- **Cranmer et al. 2020**: regressão simbólica das mensagens de uma GNN (física).
- **DNAR, Nerem 2026, Wittig 2026**: provas feitas à mão, com dicas ou alinhamento.
- **Síntese de programas por exemplos** (a linha de base "sem rede"): clássica.

O que este experimento acrescenta é o **teste de necessidade da rede**. Não achei trabalho que compare extração de GNN e síntese direta na mesma linguagem para algoritmos de grafos. **Novidade esperada: baixa.** O valor está em direcionar o foco.

## Montagem
- **Famílias:** SP (caminho mínimo) e WP (caminho mais largo), em ER p = 0,5 com pesos U(0,1).
  - A verdade vem de Bellman-Ford / Dijkstra de gargalo, com o conjunto de pais válidos.
- **Rede:** idêntica nas duas famílias.
  - MPNN genérico, sem dicas; treino em n = 16, T ~ U{8..24};
  - perda de ponteiro por pais válidos + MSE do valor final;
  - 4000 passos, Adam 5e-4, corte de gradiente 1,0.
- **Braços:**

  | braço | coeficientes vêm de | alvo da escolha |
  |---|---|---|
  | mecanística | transições internas da rede, arredondadas a 1/2 | saída final da rede |
  | comportamental | grade | saída final da rede |
  | síntese direta (atalho trivial / linha de base) | grade | a verdade, sem rede |

  - Os três usam a mesma linguagem: 18 formas; grade {0, ½, 1, 1½, 2}² × {−½, 0, ½}; inícios {−∞, +∞, 0, 1}.
  - Escolha em circuito fechado em n = 32, com 8 grafos.
- **Linha de base de rede:** a própria rede, por acurácia de ponteiro em n = 16, 32 e 64 (64 grafos por n).
- **Programa:** executado em Python puro em n = 16, 64 e 256 (20 grafos por n).
- **Reconhecimento automático** = forma, coeficientes e início exatamente os da relaxação do semianel. Nesse caso vale o teorema clássico do ponto fixo (prova por redução, **não** assistente de provas).

## Previsões e critérios de morte (todas `pos_piloto`)
| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1-SP | síntese direta reconhecida em ≥ 4/5 sementes | 0,90 | < 4/5 → a linguagem ou a grade não contém o programa; o avaliador é inútil |
| P1-WP | idem | 0,90 | idem |
| P2-SP | comportamental reconhecida em ≥ 4/5 | 0,55 | — |
| P2-WP | comportamental reconhecida em ≥ 4/5 | 0,20 | — |
| P3-SP | mecanística reconhecida em ≥ 4/5 | 0,45 | — |
| P3-WP | mecanística reconhecida em ≥ 4/5 | 0,15 | — |
| P4 | todo programa reconhecido acerta 1,000 em n = 256 | 0,95 | < 1,000 → o reconhecimento ou a prova por redução tem furo |
| P5-SP | a rede fica < 0,99 em n = 64 | 0,97 | — |
| P5-WP | a rede fica < 0,99 em n = 64 | 0,90 | — |
| P6 | síntese reconhece mais que a comportamental, somando as famílias (Fisher reportado) | 0,75 | síntese ≤ comportamental → **H-rede-supérflua morre**: a rede ajuda (ou empata) na recuperação |

- **H-rede-supérflua é aceita** se P1 (as duas famílias) e P6 passam.
- **H19 não é desbloqueada por este experimento em nenhum caso.** O critério exige extração **da rede** em nível N3; aqui só medimos se a rota se justifica.

## Sementes e poder
- **Sementes de treino:** 1800–1804, 5 por família (N1).
- **Sementes de teste:** `lab.sementes.derivar(base_teste(__file__), 5)`, derivadas do commit deste PREREG.
- **Tamanho das células:** 10 recuperações por braço (5 × 2 famílias).
  - `n_para_diferenca(0,2; 0,9; alfa = 0,05)` = 7 ≤ 10: separa uma taxa de 20% de uma de 90%.
  - Diferenças menores ficam fora do alcance; está declarado.
- **Custo:** ~12 min de CPU por (semente, família) × 10 ≈ 120 min de CPU, ~36 min de parede com 4 processos.
  - Passa do teto de 60 min de CPU do ciclo. Decisão autônoma, registrada na CRITICA: o treino da rede genérica é o custo irredutível da pergunta.

## Guarda do avaliador
```
{
 "experimentos/E018_extracao/e018.py": "f6bb6bab1251c388",
 "lab/tarefas_clrs.py": "fd2b3258eb55e4f4",
 "lab/sementes.py": "4a5e4da1269f9b77",
 "lab/estat.py": "40af21b3e5c3d582"
}
```

## Ameaças conhecidas
- **A linguagem de regras foi escrita por quem conhece a resposta.** Ela contém as duas relaxações e 16 distratores.
  - A síntese direta mede se a linguagem basta, não se ela seria descoberta sem esse viés.
  - É a mesma limitação de qualquer DSL (Cranmer, MIPS).
- **A preferência por ±∞ no empate foi fixada depois do piloto.** Ela favorece o início correto quando o erro empata, e vale igualmente para os três braços.
- **Distribuição única** (ER p = 0,5): as distâncias são curtas.
  - O programa com início 1,0 acertaria em teste e não é provável; por isso o reconhecimento exige o início do semianel.
- **O ponteiro do WP é trivial** (aresta mais pesada; ver pilotos). Só a regra de valor do WP discrimina as rotas.
- **O que não mostra:** que nenhuma rede ajude em nenhuma família. Só estas duas, com esta linguagem e este treino.
