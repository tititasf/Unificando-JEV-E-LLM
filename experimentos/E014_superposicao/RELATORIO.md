# E014 — Relatório: várias hipóteses vivas; produto contra mistura de softmaxes

**Veredito: PROMOVER.** O critério da H10 foi cumprido (P2 e P3). **H10 desbloqueada; S2 → D07.** A impossibilidade da forma global também passa (P1, e P7 com a ressalva abaixo).
Nível: **N2**:
- pré-registrado;
- 10 sementes de treino × 10 instâncias por célula, 30 células;
- sementes de teste derivadas do commit `2a3cb34`;
- reprodução IDÊNTICA;
- guarda OK.

**Novidade: baixa.** Superposição em pensamento contínuo (Zhu et al. 2025), estados de Hopfield moderno e mistura de softmaxes (Yang et al. 2018) são conhecidos. O que é específico daqui: com os **mesmos** pesos treinados em uma única hipótese, só a forma de compor o passo decide se a superposição existe.

## Previsões
| # | Previsto | Prob. | Obtido | Status |
|---|---|---|---|---|
| P1 | GLOBAL1 e GLOBAL_TEO em SUP: recuperação ≤ 0,10 | 0,85 | 0,00 nas 24 células | ✅ |
| P2 | MIST_TEO ≥ 0,95 e 0 colapsos (SUP e BFS) | 0,85 | 1,00 em todas as 18 células; pior semente 1,00 | ✅ |
| P3 | CRIST ≤ 0,05 | 0,95 | 0,00 | ✅ |
| P4 | MIST1: massa em R = (1 − ε₁)^k ± 0,05 em ≥ 90% | 0,55 | **120/120** | ✅ |
| P5 | BFS k=5: massa MIST_TEO − GLOBAL_TEO ≥ 0,5 | 0,70 | 0,87 · 0,97 · 0,99 | ✅ |
| P6 | FEIXE_TEO ≥ 0,95 | 0,90 | 1,00 | ✅ |
| P7 | GLOBAL3 = vencedor leva tudo em todas as células de SUP | 0,75 | 10/12 células; em N=4096, F=8 o estado **se dissolve** (massa 0,17, fração viva 0,03) | 🟥 |

**Brier: 0,13.**

## O que foi mostrado
1. **A forma global (produto de especialistas) não guarda hipóteses de pesos desiguais em nenhuma temperatura.**
   - Com β = 1 e com o β da lei, o estado se dissolve (massa em R de 0,001 a 0,03).
   - Com β = 3, o vencedor leva tudo: massa 1,00 concentrada no início mais pesado, fração de R viva = 1/F.
   - Com β = 3 em N=4096 e F=8, volta a se dissolver.
   - Não existe regime intermediário: é a bistabilidade de uma memória de Hopfield (um padrão ou nenhum).
   - Mecanismo: os logits são lineares em z. Uma hipótese de peso w vê a margem β·m·w. Para não se dissolver, a mais leve precisa de β·m·w_min ≳ ln N. Mas então a razão entre pesada e leve se amplifica a cada passo por e^{β·m·(w_max − w_min)}, que é a instabilidade do vencedor leva tudo.
2. **A mistura (cada nó distribui a própria massa) guarda todas.**
   - É a mesma tabela, sem re-treino: 100% de recuperação em todas as células (F até 8, k até 64, N até 4096, BFS com até 32 alcançáveis).
   - A massa segue a lei multiplicativa (1 − ε₁)^k com erro ≤ 0,05 em 120/120 casos. É a mesma lei q^k do E012, agora dentro do S2.
   - Com o β da lei (E013) a massa fica ≥ 0,98 até k = 64.
3. **As duas soluções do laboratório se compõem.** A temperatura do E013 (nitidez) e a mistura (superposição) resolvem problemas diferentes. Juntas dão um estado que é nítido **e** plural.
4. **A GLOBAL em BFS acerta por empate:** 0,72–1,00, com massa dissolvida. Com pesos iguais a simetria preserva o conjunto. A tarefa que discrimina é a SUP (pesos desiguais), e ali a GLOBAL dá 0/240.

## Revisor hostil
1. *"Mistura de softmaxes é só uma cadeia de Markov; claro que propaga uma distribuição."* Sim. O resultado não é que a cadeia funcione. É que o passo **treinado** como softmax global contém uma cadeia de Markov correta, e que a forma global, a usada no treino, **não tem temperatura que funcione**. Para o laboratório, a superposição é uma decisão de forma, não de escala nem de treino.
2. *"O FEIXE também acerta 100%."* Acerta, com F execuções. A mistura usa um vetor. A vantagem de custo é por construção e não foi medida como previsão.
3. *"A leitura supõe |R| conhecido."* Supõe. Ler R sem |R| exige um limiar na massa por nó, que é tarefa do S3; fica semeado (H-sup-limiar).
4. *"Com β alto e pesos iguais, a GLOBAL não mantém tudo?"* Mantém, por empate exato, e é instável: qualquer desigualdade é amplificada (pilotos). Não é superposição utilizável.

## Correções
- E013 (revisor hostil e hipótese H-temp-mínima-D07) dizia que "a afiação mínima preserva a superposição que o D07 precisa". Isso é **falso** para o passo global: nenhuma temperatura preserva hipóteses desiguais. A superposição vem da forma do passo (mistura), não da afiação mínima.

## Atalho encontrado no piloto (regra 7)
No primeiro gerador, os alvos tinham grau de entrada 2 e, no regime dissolvido, o ranking vinha desse viés estático, não do caminho. Os geradores finais têm grau de entrada uniforme.

## Hipóteses semeadas
- **H-sup-limiar (→ H08):** o S3 lê R sem conhecer |R|: limiar pela lei (massa esperada por hipótese = w·(1 − ε)^k) e risco controlado.
- **H-mist-treino:** treinar já na forma de mistura (BPTT) em T2 e testar T1: o atrator da raiz (T1) muda?
- **H-mist-JEV:** o S2 como mistura sobre as distribuições `Choice` do JEV (propagar a incerteza do S1 em vez do argmax): acc(k) melhor que q^k?
