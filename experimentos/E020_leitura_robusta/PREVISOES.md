# E020 — Previsões antecipadas (commitadas ANTES de qualquer piloto ou smoke)

Montagem prevista:
- as redes do E019 (só ponteiro, 4000 passos), em 10 sementes novas por família (SP e controle WP);
- leitura por fechamento dinâmico com 3 reinícios por forma;
- **escolha nova:** a forma cuja regra arredondada tem o menor resíduo de fechamento normalizado na própria leitura;
  - início escolhido pela proximidade do programa com a leitura final da rede;
  - ponteiro pela concordância com a rede;
- **escolha antiga (E019):** concordância com o ponteiro da rede, nos mesmos candidatos, como ablação pareada;
- nenhuma verdade entra em nenhuma escolha.

| # | Previsão | Prob. |
|---|---|---|
| P1 | SP, escolha nova: programa min-plus reconhecido em ≥ 8/10 | 0,35 |
| P2 | SP, escolha nova: \|r(leitura escolhida, distância)\| ≥ 0,9 em ≥ 8/10 | 0,45 |
| P3 | WP (controle): \|r(leitura escolhida, largura)\| < 0,5 em ≥ 8/10 | 0,35 |
| P4 | SP, escolha nova: reconhecido em ≥ 7/10 (a regra de parada: abaixo disso, a linha acaba) | 0,50 |
| P5 | SP, escolha nova reconhece ≥ 2 sementes a mais que a antiga, nas mesmas redes | 0,45 |
| P6 | todo programa reconhecido acerta 1,000 em n = 256 | 0,95 |
| P7 | rede SP só com ponteiro, n = 64: IQM ≥ 0,75 | 0,55 |
