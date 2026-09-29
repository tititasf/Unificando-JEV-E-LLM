# E007 — Relatório: a lei de nitidez fora da amostra

**Veredito: PROMOVER.** Habilidade **H04 desbloqueada** (N2: pré-registrado, 30 sementes novas, sementes de teste derivadas do commit `13d7855`, reproduzido de checkout limpo, guarda OK).
**Novidade: baixa.** O diagnóstico mostra que o S2 aprendido segue a teoria de recuperação das redes de Hopfield modernas (Ramsauer et al., 2020; teoria de bifurcação, arXiv 2609.07757). O valor está em ter um **preditor por modelo, validado fora da amostra**, e uma regra de projeto com base teórica.

## Previsões

| # | Previsto | Prob. | Obtido | Status |
|---|---|---|---|---|
| P1 | N_c (regime) dentro de 1,5× de N̂_c em ≥ 80% | 0,65 | **25/30 = 0,83** | ✅ |
| P2 | cruzamento dentro da grade em ≥ 90% | 0,70 | 30/30 | ✅ |
| P3 | lei melhor que a constante 137, p < 0,01 | 0,70 | erro \|ln\| 0,219 [0,173; 0,268] vs 0,584; P(lei melhor) = 0,79; **p = 0,0002** | ✅ |
| P4 | por passo: mediana de R = N_c(40)/N_c(10) em [0,67; 1,5] | 0,65 | **mediana 0,95**; as 14 razões entre 0,73 e 1,29 | ✅ |
| P5 | acumulado: mediana de R ≤ 0,4 | 0,15 | 0,95 | 🟥 (esperado) |
| P6 | N_c abaixo do previsto em ≥ 70% | 0,55 | 27/30 | ✅ |

**Brier deste ciclo: 0,11** (6 previsões). Primeira vez abaixo de 0,25.

## O que foi mostrado
1. **Um número medido num único passo prevê onde o pensamento se dissolve.** Com ε_c congelado (0,071), 25 de 30 modelos novos tiveram N_c dentro de 1,5× do previsto; o erro é 2,7× menor que o da melhor constante.
2. **A dissolução é uma instabilidade por passo, não acúmulo.** N_c não muda quando a profundidade vai de 10 a 40 (R ≈ 0,95).
3. **É uma transição de fase abrupta.** A nitidez média cai de ~1,0 para ~0,05 dentro de um fator 1,4 em N.
4. **A acurácia engana em tarefa-atrator.** Pela acurácia, só 16/30 ficaram dentro de 1,5× (o caminho longo "acerta por sorte" mesmo dissolvido). A métrica certa é o regime (nitidez), decisão tomada no piloto e declarada no PREREG.

## Diagnóstico pós-hoc: teoria de campo médio (`diagnostico.md`)

Modelo: massa a no nó atual; a' = 1/(1 + K·e^(−m·a)), com K = N−1. O estado nítido
some numa **bifurcação sela-nó** quando m·a·(1−a) = 1, que só existe para margem
m ≥ 4. Isso dá ε_c(m) em forma fechada, **sem parâmetro ajustado**:

| | erro médio \|ln(N_c real / previsto)\| | dentro de 1,5× |
|---|---|---|
| limiar fixo 0,071 (pré-registrado) | 0,219 | 25/30 |
| **teoria de campo médio** (m medido em N=30) | **0,086** (~9%) | **29/30** |

P(teoria melhor) = 0,86, p = 0,0004. As margens efetivas dos modelos ficaram entre 6,05 e 7,79, onde a teoria dá ε_c entre ~0,05 e 0,07, o que explica o valor empírico 0,071 e o viés de P6.

Checagem de novidade: a forma é a **condição de separação das redes de Hopfield modernas**, em que a margem × β precisa superar ~log N para a recuperação não cair num estado metaestável. O nosso passo z ← softmax(S·z) é essa atualização. **Replicação de teoria conhecida**, agora aplicada a um passo aprendido e iterado.

## Revisor hostil
1. *"O limiar 0,071 veio do E006d e o piloto informou as probabilidades."* Sim, declarado. O teste principal usou 30 sementes que nunca tinham sido vistas, e as sementes de teste vieram do hash do commit.
2. *"A teoria de campo médio é pós-hoc."* É, e por isso fica em N1. Mas ela não tem nenhum parâmetro ajustado aos dados do E007. O próximo teste é pré-registrá-la numa distribuição diferente (T2, sem raízes).
3. *"Isso é só Hopfield."* Exatamente, e é útil saber: o S2 é uma memória associativa iterada, e toda a teoria de capacidade e temperatura de Hopfield passa a valer como guia de projeto.

## Hipóteses semeadas
- **H-campo-médio-T2:** a mesma teoria, com margem medida em N=30, prevê o N_c em T2 (permutações), onde o E005 viu 100% até N=1024.
- **H-temperatura-logN (→ H05):** multiplicar os logits por β(N) = log(N−1)/log(N_treino−1) mantém a nitidez em qualquer N, **sem re-treino**. Previsto pela teoria (a condição depende de m − log K).
