# E015 — Relatório: código mínimo corretor

**Veredito: PROMOVER.** P1 e P3 passam, e com elas o critério da H13. **H13 desbloqueada; S5 → D05** (primeiro passo do S5 em 12 ciclos).
Nível: **N2**: pré-registrado; 10 sementes × 10.000 símbolos por (semente, código, σ); sementes de teste derivadas do commit `370354e`; reprodução IDÊNTICA; guarda OK.
**Novidade: nenhuma.** É a replicação, com códigos aprendidos, de resultados clássicos: simplex, biortogonal, limite de Rankin, autoencoders de canal.

## Previsões
| # | Previsto | Prob. | Obtido | Status |
|---|---|---|---|---|
| P1 | Canal E: APREND com L = N−1 < ONEHOT | 0,45 | razão 0,83 · 0,91 (N=16) · 0,96 · 0,99 (N=32) | ✅ |
| P2 | Canal E: L = N/2 empata [0,9; 1,15] e L = N/4 perde (> 1,2) | 0,65 | empate 0,95–1,07 ✔; N/4: 1,86 · 1,37 · 1,43 · **1,18** (N=32, σ=0,4) | 🟥 |
| P3 | Canal P: APREND com L = N/4 ≤ 0,5 × ONEHOT | 0,85 | 0,027 · 0,117 · 0,001 · 0,021 | ✅ |
| P4 | APREND < ALEAT em ≥ 90% das sementes | 0,90 | 24/24 células | ✅ |
| P5 | Canal E: APREND com L = log₂N < binário à mão | 0,60 | 0,154 < 0,178 · 0,342 < 0,360 · 0,266 < 0,296 · 0,480 < 0,507 | ✅ |

**Brier: 0,18.**

## O que foi mostrado (a curva bits × robustez)
1. **No canal do E003 (energia fixa por mensagem), o one-hot está a uma dimensão do ótimo.**
   - O código aprendido com L = N−1 supera o one-hot e chega perto do simplex teórico (N=16: 0,069 contra 0,068 do simplex e 0,083 do one-hot).
   - Com L = N/2 ele **empata**, igual ao biortogonal.
   - Abaixo de N/2 perde, e perde mais quanto menos dimensões houver.
   - A curva segue o limite geométrico: mais de 2L pontos numa esfera de L dimensões não ficam todos a 90° ou mais. Economizar dimensões custa energia.
2. **Num canal que satura por dimensão (amplitude ≤ 1), códigos densos ganham com folga.** Com N/4 dimensões, o erro é 3 a 12% do one-hot; com N/2, ≈ 0. O ganho vem de usarem mais energia total, e por isso os dois canais são reportados.
3. **O aprendizado importa:** o código aprendido vence o sorteado em todas as 24 células e vence o binário feito à mão em L = log₂N.
4. **Lição para o S5:** a escolha do código depende do recurso escasso. Se o recurso é energia por mensagem, espalhar a mensagem (one-hot, simplex) é quase ótimo. Se o recurso é amplitude por canal (neurônios que saturam), comprimir em código denso é muito melhor. A pergunta "quantos bits por passo" não tem resposta sem dizer qual é o custo.

## Revisor hostil
1. *"Isto é um livro-texto de comunicação digital."* Sim. A novidade declarada é nenhuma. O valor é interno: o S5 passa a ter a curva medida e o limite explícito antes de tentar códigos que emergem entre agentes (H14).
2. *"No canal E a economia é de uma dimensão."* Exato, e o experimento mostra por quê: abaixo de N/2 não há como empatar (Rankin). A H13 foi desbloqueada com essa ressalva escrita.
3. *"O canal P é injusto com o one-hot."* Ele é justo com canais que saturam, e injusto se o custo é energia. Ambos estão reportados.

## Correções e notas
- O PREREG cita `n_para_largura(0,1; 0,01)` = 3458; o valor correto é 3679. A conclusão (< 10.000 símbolos) não muda; o PREREG não foi editado.
- P2 falhou por pouco (1,18 contra o limiar de 1,2) numa das quatro células de N/4. O empate em N/2 foi confirmado nas quatro.

## Hipóteses semeadas
- **H-código-agentes (→ H14):** o código emerge entre dois agentes do E003 treinados só pela tarefa (encadear saltos), sem objetivo de decodificação; ele chega à curva do E015?
- **H-custo-canal:** o S0 fixa o recurso escasso (energia ou amplitude), e o código aprendido muda de forma (espalhado ou denso) conforme o custo.
