# E014 — Pré-registro: várias hipóteses vivas no S2, produto contra mistura de softmaxes

**Escrito antes de rodar. Não editar depois da primeira execução completa.**
Trilha: A (S2). Átomos: 2.3 (múltiplas hipóteses), 2.1. Nível de partida: N0 (pilotos).
Habilidade-alvo: **H10** (fronteira da bússola, S2 D07). Nó pai: **E013** · Operador: **MELHORAR**. Degrau-alvo: S2 D07.
Escolha: H24 e H08 estão acima na bússola. A H24, examinada neste ciclo, cai no atalho trivial da regra 7 nas tarefas estruturadas: o verificador O(d) de uma trajetória **é** o resolvedor exato, então o custo do S2 latente não tem o que amortizar. Ela precisa de uma família em que verificar seja mais barato que resolver (certificados de Bellman-Ford, H23). A H08 depende de um sinal que o M007 não achou. A H10 é o degrau N+1 do S2, e o E013 semeou a pergunta (H-temp-mínima-D07).

## Hipótese
O passo do S2 treinado em T2 (uma hipótese, N = 12), aplicado sem re-treino:
- **H-a (impossibilidade):** na forma atual, a softmax **global** da soma dos logits (um produto de especialistas), não sustenta hipóteses de pesos desiguais em **nenhuma** temperatura. Com β baixo o estado se dissolve e com β alto o vencedor leva tudo.
- **H-b (construção):** a mesma tabela aplicada como **mistura** de softmaxes (cada nó distribui a própria massa; uma cadeia de Markov) mantém todas as hipóteses, recupera o conjunto exato em superposição e em BFS e segue a lei multiplicativa: massa em R = (1 − ε₁)^k.

## Pilotos (declarados; sementes 1590–1591, fora da faixa)
1. **Atalho achado e removido:** no primeiro gerador (cadeias saindo de s), os alvos tinham grau de entrada 2. No regime dissolvido, o ranking vinha desse viés estático e não do caminho. Os geradores atuais (permutação; união de duas permutações) têm grau de entrada uniforme.
2. **GLOBAL com hipóteses desiguais**, β de 0,1 a 16:
   - β ≥ 1,5 → vencedor leva tudo (massa 1,0 no mais pesado; razão mín/máx 0,00);
   - β ≤ 1 → dissolvido (massa ≈ 0,02); recupera o conjunto só com k = 4 e β ≤ 0,25;
   - nenhum β recupera com k ≥ 16.
3. **GLOBAL com pesos iguais** (cadeias simétricas): recupera por empate, mas a massa se dissolve quando β·m/F < ~ln N (lei de capacidade da superposição).
4. **MISTURA:** 3/3 em todas as células (SUP F = 4 e 8, k até 64; BFS k = 3 e 5; N até 1024).
5. Smoke do avaliador (sementes 1490–1491): todas as previsões abaixo passaram; P4 ficou com 15/16, na borda.

## Relação com a literatura
- **Reasoning by Superposition** (Zhu et al., arXiv 2505.12514): o pensamento contínuo codifica várias fronteiras de busca (BFS paralela) e resolve alcançabilidade em D passos; o CoT discreto escolhe um caminho.
- **Hopfield moderno** (Ramsauer et al. 2020): pontos fixos de média global, estados metaestáveis e padrão único, governados por β.
- **Mixture of Softmaxes** (Yang et al. 2018): a soma de softmaxes escapa do gargalo da softmax única.

O que difere: aqui a forma do passo (produto × mistura) é a única variável, com os **mesmos** pesos treinados em uma hipótese. A previsão é que a forma global não tem **nenhuma** temperatura que funcione com pesos desiguais. **Novidade: baixa.**

## Montagem
- Treino: `tarefa_t2` (N = 12, k ≤ 4, 600 iterações), sementes **1400–1409** (rng = semente + 1000). A tabela de afinidade usa os atributos (i ∈ succ(j), j ∈ succ(i), i = j), com os de raiz desligados, pois não há raízes.
- Margem m sem rótulos (como no E013, N = 30) e β_TEO(N) = 1 + ln((N−1)/11)/m.
- Tarefas, com N ∈ {256, 1024, 4096}:
  - **SUP:** permutação; F ∈ {4, 8} inícios com pesos 1..F normalizados; k ∈ {16, 64}; R = {π^k(sᵢ)}.
  - **BFS:** união de duas permutações; início único; k ∈ {3, 5}; R = alcançáveis em exatamente k saltos.
- Leitura: **recuperação** = os |R| nós de maior massa são exatamente R. Também: massa em R e fração de R viva.
- Braços:
  - **GLOBAL1** (o S2 atual)
  - **GLOBAL_TEO** (β da lei)
  - **GLOBAL3** (β = 3, nítido)
  - **CRIST** (argmax a cada passo)
  - **MIST1**
  - **MIST_TEO**
  - **FEIXE_TEO** (linha de base simples: F execuções independentes de uma hipótese, custo F×; só em SUP)
- Linha de base publicada: não há reimplementação (Coconut e o modelo teórico do Zhu et al. são transformers). A comparação publicada mais próxima é a dicotomia contínuo × discreto, que é o CRIST.

## Previsões e critérios de morte
| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1 | GLOBAL1 e GLOBAL_TEO em SUP: recuperação IQM ≤ 0,10 em todas as células | 0,85 | alguma ≥ 0,5 → **H-a morta** |
| P2 | MIST_TEO: recuperação IQM ≥ 0,95 e 0 sementes < 0,5 em todas as células (SUP e BFS) | 0,85 | alguma célula < 0,8 → **H-b morta** |
| P3 | CRIST: recuperação IQM ≤ 0,05 em todas as células | 0,95 | — |
| P4 | MIST1 em SUP: massa em R dentro de ±0,05 de (1 − ε₁)^k em ≥ 90% das (semente × célula) | 0,55 | < 50% → a lei multiplicativa não descreve a mistura |
| P5 | BFS k = 5: massa em R de MIST_TEO − GLOBAL_TEO ≥ 0,5 em todo N | 0,70 | — |
| P6 | FEIXE_TEO em SUP: recuperação IQM ≥ 0,95 | 0,90 | — |
| P7 | GLOBAL3 em SUP: vencedor leva tudo (recuperação ≤ 0,10, massa em R ≥ 0,9, fração viva ≤ 1/F + 0,1) em todas as células | 0,75 | — |

**H10 desbloqueada** (N2) se P2 e P3 passam: o estado mantém > 1 candidato e acerta onde o cristal falha. Se P1 e P7 também passam, a impossibilidade da forma global vira achado (N2).

## Sementes e poder
- 10 sementes de treino × 10 instâncias por célula = 100 por célula. `n_para_largura(0,95; 0,05) = 86`; `n_para_diferenca(0,05; 0,5) = 22`.
- Sementes de teste: `lab.sementes.derivar(base_teste(__file__), 10)`, derivadas do commit deste PREREG.
- Custo estimado: ~110 s de CPU por semente (N = 4096 domina) → ~5 min de parede com 4 processos.

## Guarda do avaliador
```
experimentos/E014_superposicao/e014.py        : 96c07706fb739455
experimentos/E005_t2_salto/tarefa_t2.py       : b62e43a6a77ab648
experimentos/E006_lei_margem/passo_rapido.py  : 3aa24574de9b4029
experimentos/E001_mlu/mlu.py                  : 601604873fae9691
lab/sementes.py                               : 4a5e4da1269f9b77
lab/estat.py                                  : 40af21b3e5c3d582
```

## Ameaças conhecidas
- **BFS com pesos iguais:** a GLOBAL recupera por empate (piloto: 0,83–1,00). Em BFS a vantagem da mistura é só a massa (P5). A tarefa que discrimina é a SUP.
- A mistura com z one-hot é idêntica ao passo global. A diferença está só na composição, e isso é o que se testa. Não houve re-treino com a mistura.
- O que este teste NÃO mostra:
  - leitura de R sem saber |R| (o S3 precisaria de um limiar);
  - latente livre (H09);
  - custo contra FEIXE: a mistura usa um vetor, o feixe usa F. A vantagem de custo é por construção, não é medida aqui.
