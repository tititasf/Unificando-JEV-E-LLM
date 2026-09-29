# E002 — Relatório: cristalização do estado latente

**Veredito: H1 MORTA (P1 falhou). H2 MORTA. Achado real, e diferente: falha de calibração do S3 com a escala.**
Nível: N2 para o achado negativo (pré-registrado, 30 sementes, ablação).

## O que aconteceu

| Previsão | Resultado | Status |
|---|---|---|
| P1 colapso CONT em d=128 ≥ 15% | 0/30 | 🟥 morte: o problema não existe |
| P2 CRIST ≤ 1/30 | 0/30 | trivial (sem problema a corrigir) |
| P3 Fisher p<0,01 | p=1 | 🟥 |
| P4 AFIA entre os dois | todos 100% | sem informação |
| P5 margem prevê colapso | ρ=0 (sem variância) | 🟥 H2 morta: margens de 3,25 dariam vazamento enorme pela fórmula, e mesmo assim acertou |

Resultados completos: `resultados.md`, `resultados.json`.

## Por que o E001 parecia mostrar o contrário

O E001 lia a resposta **através do S3** (parar só com confiança ≥ 0,9). O
E002 lê o argmax direto. Diagnóstico (modelo da semente 7 do E001, que
"colapsava"):

| Caso | S3 se absteve | S3 acertou | argmax acertou | confiança final |
|---|---|---|---|---|
| N=64, d=50 | 10/10 | 0/10 | 9/10 | ~0,05 |
| N=128, d=100 | 10/10 | 0/10 | 10/10 | ~0,02 |

**O raciocínio (S2) estava certo. Quem falhava era a metacognição (S3):** o
estado contínuo espalha massa pelos N nós, então a confiança absoluta
cai com N (ainda ~3× acima do uniforme e com o argmax correto), e o limiar
fixo de 0,9 nunca é atingido.

A cristalização "consertava" porque força a confiança para 1. Isso é
**perigoso**: ela esconde a incerteza em vez de medi-la. Um S3 que só
funciona porque não vê a própria dúvida não sabe quando não sabe.

## Correções nos registros anteriores

- A afirmação do E001 "cristalização → 100% em 128 nós, contínuo → 0%" estava **mal atribuída**. O correto é: *o S3 com limiar absoluto se abstém em problemas maiores; o S2 acerta*. `RESULTADOS.md` foi anotado.
- O átomo 1.4 (cristalização) continua aberto, mas **não** por estabilidade do raciocínio nesta tarefa. Ele ainda pode importar para comunicação (E003) e ruído.

## Hipóteses semeadas

- **H-3.2a (S3 invariante à escala):** um sinal de confiança relativo (razão sobre o uniforme, margem top-1 − top-2 ou entropia normalizada por log N) mantém E-AURC≈0 e 0 abstenções indevidas de N=12 até N=128. → E004a.
- **H-1.4b:** a cristalização só ajuda sob **ruído** (canal, pesos, estado). → testada no E003 (canal); falta ruído interno.

## Revisor hostil

1. *"12 exemplos por semente é pouco."* São 360 por braço em d=128, todos corretos; o IC de Wilson para 360/360 é [0,99; 1,0].
2. *"Talvez o E001 tenha tido azar."* O diagnóstico acima mostra o mecanismo diretamente, sem depender de azar.
3. *"A tarefa é fácil demais para o S2."* Sim. Por isso ela não serve mais para testar estabilidade do S2: próximos testes de S2 sobem para T2/T3.
