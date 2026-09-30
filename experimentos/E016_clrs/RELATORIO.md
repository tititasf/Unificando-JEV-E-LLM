# E016 — Relatório: protocolo CLRS reimplementado (Bellman-Ford, n = 16 → 64)

**Veredito: PROMOVER (infraestrutura).** A avaliação completa rodou: 5 sementes, todos os braços e todos os n, com IC; a reprodução deu IDÊNTICA. Com isso o critério da H23 está cumprido e **a H23 está desbloqueada** (N1).
- P2, P4 e P5 passam; P1 e P3 falham.
- A hipótese do viés **sobrevive** (P4, 4/5), mas o diagnóstico achou um segundo modo de erro, a **divergência**. Os dois modos juntos formam um dilema.

Nível: **N1**:
- pré-registrado;
- 5 sementes × 20 grafos por n;
- sementes de teste derivadas do commit `32a42b0`;
- reprodução IDÊNTICA;
- guarda OK.

**Novidade: baixa.** O protocolo é o do CLRS-30. Esta reimplementação mínima não é comparável 1:1 com ele.

## Previsões
| # | Previsto | Prob. | Obtido | Status |
|---|---|---|---|---|
| P1 | APREND n=16 ≥ 0,95 | 0,35 | 0,909 [0,83; 0,94] | 🟥 |
| P2 | APREND n=64 ≤ n=16 − 0,05 | 0,80 | 0,616 contra 0,909 | ✅ |
| P3 | DT n=64 não supera APREND por > 0,03 | 0,75 | **DT 0,839** [0,74; 0,88] contra 0,616 | 🟥 |
| P4 | SURR prevê APREND em n=64 (±0,03) em ≥ 80% das sementes | 0,80 | 4/5; exceção: semente 1601 (SURR 0,93, APREND 0,58) | ✅ |
| P5 | GULOSO < APREND n=16 | 0,85 | 0,552 < 0,909 | ✅ |

**Brier: 0,16.**

## Painel (acurácia de ponteiros, IQM [IC95%])
| n | APREND | DT | SURR | GULOSO |
|---|---|---|---|---|
| 16 | 0,909 [0,83; 0,94] | 0,948 [0,93; 0,97] | 0,913 | 0,552 |
| 32 | 0,765 [0,68; 0,88] | 0,914 [0,87; 0,94] | 0,830 | 0,529 |
| 64 | 0,616 [0,53; 0,75] | 0,839 [0,74; 0,88] | 0,678 | 0,502 |

Parâmetros aprendidos:
- APREND: b = 0,00 a 0,10 e D0 ≈ 3,9.
- DT: b = 0,015 a 0,043 e D0 ≈ 0,4 a 0,76.

## O que foi mostrado
1. **O dilema do viés (causa do erro fora da distribuição).**
   - O soft-min fica abaixo do mínimo verdadeiro por até ln(grau)/β. Um b > 0 aprendido compensa essa descida.
   - O mesmo b, porém, soma uma penalidade por salto e favorece caminhos com menos arestas.
   - O ponto de equilíbrio depende do grau e, portanto, de n.
   - **Diagnóstico** (fora do pré-registro, semente 1601, 10 grafos):

     | b | n = 16 | n = 64 |
     |---|---|---|
     | 0,0002 | 0,86 | **0,59**, sem convergir: 256 passos, d mínimo −3,15 |
     | 0,01 | 0,94 | 0,77, sem convergir: 163 passos, d mínimo −0,67 |
     | 0,03 | 0,95 | 0,80, converge em 18 passos |
     | 0,06 | 0,87 | 0,68, converge; erro de viés, SURR 0,68 |

   - Com b pequeno o motor **diverge** (as distâncias descem sem fim, como num ciclo negativo). Com b grande ele **erra por viés**. O b que é estável em n = 16 deixa de ser em n = 64.
   - É o análogo, nas distâncias, da lei do E007/E013: o que vence em n pequeno (margem, ou aqui compensação) não acompanha o log do tamanho.
2. **O SURR prevê o motor quando ele converge.** Em 4/5 sementes a diferença entre os dois fica dentro de ±0,03. A exceção é justamente o modo divergente.
3. **O Deep Thinking vence com folga (P3 caiu).**
   - A perda progressiva, com T sorteado, pune a deriva nos T longos e empurra b para a faixa estável e pequena (0,015 a 0,043).
   - Ela também puxa D0 para perto de 0. Com T fixo em 16, D0 ≈ 3,9 era um atalho.
   - A linha de base publicada (princípio) é melhor que o nosso motor.
4. **Infraestrutura da H23:** o motor, o DT e o GULOSO (`e016.py`) sobre os geradores e o exato de `lab/tarefas_clrs.py`, sob o protocolo n = 16 → 64 com IC. Isso abre a H24 numa família com certificado, em que verificar distâncias custa O(E).

## Revisor hostil
1. *"Cinco parâmetros não é um motor aprendido de verdade."* Sim. É um motor alinhado ao algoritmo, e a pergunta foi de onde vem o erro fora da distribuição. O dilema achado vale para qualquer agregação soft-min com viés aditivo, o que inclui GNNs com agregação min suavizada.
2. *"O otimizador é fraco."* Declarado no PREREG. O resultado do DT mostra que o procedimento de treino muda b, e é exatamente essa a variável do dilema.
3. *"P4 passou por pouco (4/5, no limiar)."* Sim. A exceção foi explicada pelo diagnóstico (divergência), que não estava no pré-registro. Tratar isso como evidência exige um novo experimento.

## Literatura achada depois (radar do ciclo 16)
Wittig et al., *Which Algorithms Can GNNs Learn?* (ICML 2026, arXiv 2602.13106), provam a generalização de tamanho do Bellman-Ford aprendido. As condições são alinhamento algorítmico, treino pequeno e curado e uma regularização diferenciável. O E016 é consistente com isso: sem essa regularização, o viés aprendido fica ≠ 0 e o dilema aparece. A comparação direta fica para a H-bf-lei.

## Hipóteses semeadas
- **H-bf-lei (→ S2 D11):** usar a temperatura da lei, β(grau) ∝ ln(grau), com b = 0. A descida do soft-min fica abaixo de metade do menor intervalo entre caminhos em qualquer n e remove o dilema. Prever APREND ≥ DT em n = 64.
- **H-bf-cert (→ H24):** o S1 (motor ou JEV) chuta distâncias, o S3 verifica o certificado (d_v ≤ d_u + w para toda aresta, com igualdade no ponteiro) em O(E), e o S2 (Bellman-Ford) só roda quando o certificado falha.

## Correção (ciclo 17, E017)
A H-bf-lei acima (β ∝ ln(grau)) estava incompleta. No caminho mínimo, o fator dominante é 1/w_min, a deriva nos 2-ciclos das arestas baratas. A lei que funcionou é β = κ·ln(g_max)/(a·w_min) com b = 0: 0,993 em n = 160 e 0,991 em n = 320 (E017, N2).
