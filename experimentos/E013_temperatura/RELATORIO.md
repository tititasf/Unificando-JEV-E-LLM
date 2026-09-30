# E013 — Relatório: temperatura derivada da lei de nitidez

**Veredito: PROMOVER** (critério da H05 cumprido; a previsão quantitativa P3 falhou em T1, com causa diagnosticada). **H05 desbloqueada.**
Nível: **N2** (pré-registrado, 10 sementes de treino × 10 instâncias por célula, sementes de teste derivadas do commit `2accfb8`, reprodução IDÊNTICA, guarda OK).
**Novidade: baixa.** É a forma do Scalable-Softmax (β afim em log N), com o coeficiente derivado da margem medida (1/m) em vez de aprendido.

## Previsões
| # | Previsto | Prob. | Obtido | Status |
|---|---|---|---|---|
| P1 | B1 em 4096 ≤ 0,30 | 0,85 | T1 0,17 · T2 0,00 | ✅ |
| P2 | TEORIA em 4096 ≥ 0,95, 0 colapsos | 0,80 | 1,00 e 1,00, 0/10 e 0/10 | ✅ |
| P3 | TEORIA ε(N)/ε(12) ∈ [0,5; 2] em ≥ 90% das sementes (4 células) | 0,35 | T2: 10/10 e 10/10; **T1: 6/10 e 5/10** (razão ≈ 0,51–0,55) | 🟥 |
| P4 | atalhos em 4096 ≥ 0,95 | 0,85 | todos 1,00 | ✅ |
| P5 | SSMAX afia demais (razão < 0,1) | 0,75 | 0,000 e 0,000 | ✅ |
| P6 | TEORIA ε(4096) < ε_c(m), todas as sementes | 0,80 | sim | ✅ |

**Brier: 0,05.**

## O que foi mostrado
1. **Uma temperatura com zero parâmetros livres dá nitidez em qualquer escala.** β(N) = 1 + ln((N−1)/11)/m, com m medido no próprio modelo sem rótulos, leva T1 e T2 de 17% e 0% (β = 1) a 100% em N = 4096 (341× o tamanho de treino), 10/10 sementes.
2. **Em T2 a lei prevê o vazamento quantitativamente:** ε(4096)/ε(12) = 0,91 (IQM), contra 315× sem o mecanismo e ≈ 0 com Scalable-Softmax. A temperatura é a **mínima** que mantém o regime do treino.
3. **Em T1 a razão fica em ≈ 0,5, estável de 256 a 4096.** Diagnóstico pós-hoc (3 sementes): a parte do vazamento que depende de N (para nós genéricos e raízes) fica **constante** com β(N) (ex.: 0,0042 → 0,0042; 0,0072 → 0,0079). O que some é o vazamento para o **próprio nó** (0,0077 → 0,0001): um competidor específico, cuja margem não cresce com N e que o β > 1 também suprime. A lei acerta o componente que modela; a P3 errou porque normalizou pelo vazamento total.
4. **Atalho (regra 7):** β = 3, Scalable-Softmax e argmax também dão 100%. Neste motor estruturado o argmax não depende de N; a dissolução é só da normalização do softmax. O que a TEORIA acrescenta é ser a afiação **mínima e prevista**, e não uma afiação qualquer.

## Revisor hostil
1. *"Então é só afiar."* Sim, para acertar. A diferença é quanto afiar: a TEORIA preserva o vazamento do treino (a gradação que o S3 do E009 lê e a superposição que o D07 precisa); SSMAX e argmax a destroem. Essa vantagem ainda é argumento; o teste é D07/H10.
2. *"m medido em N = 30 é informação de escala."* É um número por modelo, obtido sem rótulos, do próprio passo; não usa nenhuma instância de teste.
3. *"Motor com atributos dados."* Declarado desde o E001; H09 (latente livre) é onde isso cai.

## Correções
- **(E014)** O argumento do revisor hostil 1 ("a TEORIA preserva a superposição que o D07 precisa") caiu: no passo global, nenhuma temperatura sustenta hipóteses de pesos desiguais; a superposição vem da forma de mistura (E014).
- A frase "precisa de mecanismo para escalar" (H05 pendente desde o E006) está resolvida para o motor estruturado. A dissolução do S2 (A9, A11) é um efeito da normalização, removível por uma temperatura prevista pela própria lei.

## Hipóteses semeadas
- **H-temp-S3:** o S3 em dois tempos (E009) com TEORIA: cobertura 100% até 4096 sem abstenção (o regime dissolvido deixa de existir onde a margem basta).
- **H-temp-mínima-D07:** a afiação mínima preserva várias hipóteses vivas quando a tarefa as exige, e o argmax não (→ H10).
- **H-temp-JEV:** o JEV mostra a mesma dissolução com N (E012); uma codificação que reduza o número efetivo de opções (Choice em blocos) testa a mesma lei no S1 externo.
