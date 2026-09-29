# E006 — Relatório: a lei N* (quando o pensamento se dissolve)

**Veredito: PIVOTAR.** A lei com o limiar pré-registrado (vazamento de um passo = 0,5) **errou o ponto de transição por um fator > 4**.
Os critérios formais de morte não dispararam, mas as previsões centrais (P1, P3) falharam.
O diagnóstico achou uma lei corrigida candidata: **transição quando o vazamento de um passo ε ≈ 0,07** (N1, pós-hoc, 12 sementes).
Nível: N2 para o negativo (30 sementes, pré-registrado). **Novidade:** baixa a média (instância de Veličković et al. 2025).

## Previsões

| # | Previsto | Prob. | Obtido | Status |
|---|---|---|---|---|
| P1 | acc ≥ 0,95 em N*/4 em ≥ 90% das sementes | 0,60 | **0 de 30**; o estado já estava dissolvido (máx z ≈ 0,01) | 🟥 |
| P2 | acc ≤ 0,5 em 4N* em ≥ 90% | 0,55 | 29 de 29 | ✅ (trivial: tudo já estava dissolvido) |
| P3 | N_c ∈ [N*/2, 2N*] em ≥ 80% | 0,45 | 36% (n=14; as curvas estavam planas perto do acaso, cruzamentos ruidosos) | 🟥 |
| P4 | Spearman(N*, N_c) > 0,7 | 0,50 | 0,65 | 🟥 (não atinge a morte ≤ 0,3) |
| P5 | atalho do atrator em 4N* | 0,50 | **não avaliado**: nenhuma semente teve 4N* ≤ 2048 | — |

**Brier deste ciclo: 0,25** (4 previsões avaliadas), contra 0,42 no ciclo 5. As probabilidades moderadas (lição 10) funcionaram como proteção.

**Falhas de desenho (minhas):** (1) a grade começou em N*/4, alto demais, e nunca viu o regime sequencial; (2) a grade B dependia de 4N* ≤ 2048, que nenhuma semente cumpriu, então P5 nunca foi testada. Lição: fazer um smoke com o **modelo completo** antes de congelar grades que dependem de uma quantidade estimada.

## Diagnóstico pós-hoc: a lei corrigida (`diagnostico.md`, 12 sementes, grade N = 24…256, d = 20)

| | valor |
|---|---|
| N_c (onde acc cruza 0,5) | 58 a 192 (varia **3×** entre sementes) |
| vazamento de um passo em N_c, ε(N_c) | **IQM 0,071**; 8 de 12 entre 0,061 e 0,083; 3 valores altos (0,12; 0,12; 0,18) em curvas não monotônicas (10 exemplos por célula) |

O vazamento de um passo **prevê** a transição; o limiar certo é ~0,07, não 0,5.
Em T2 (E005), ε em N=128 ficou entre 0,003 e 0,013, bem abaixo de 0,07, **o que é consistente** com o contínuo nunca ter se dissolvido lá.

Pergunta aberta: **ε_c é constante ou ε_c · d é constante?** Se a dissolução é um efeito acumulado ao longo dos d passos, ε_c ∝ 1/d; se é um efeito por passo (instabilidade do ponto fixo do mapa softmax), ε_c não depende de d. As duas previsões são opostas e testáveis.

## Revisor hostil
1. *"O ε_c ≈ 0,07 foi achado nos mesmos dados que o sugerem."* Sim: é N1 pós-hoc. Precisa de teste fora da amostra com ε_c congelado (H-lei-eps).
2. *"10 exemplos por célula; curvas não monotônicas."* Por isso 3 de 12 sementes saem do padrão. O próximo teste usa mais exemplos perto da transição.
3. *"Por que chamar de lei?"* Ainda não é. É uma regularidade candidata com uma previsão fora da amostra pronta.

## Correções em registros anteriores
- A11 ("N* = e^margem"): a forma estava errada. O que prevê a transição é o vazamento de um passo, com limiar ~0,07, não ~0,5 nem e^margem. Anotado no ESTADO.

## Hipóteses semeadas
- **H-lei-eps:** congelar ε_c = 0,071 (destes 12 diagnósticos) e prever N_c de 30 sementes novas; e testar d ∈ {10, 20, 40} para decidir entre "ε_c constante" e "ε_c · d constante".
- **H-temperatura-adaptativa:** a correção de Veličković et al. (temperatura que cresce com N) aplicada ao passo iterado mantém ε < ε_c e evita a dissolução, sem cristalizar.
