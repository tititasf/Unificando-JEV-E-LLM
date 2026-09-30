# E019 — Previsões antecipadas (commitadas ANTES de qualquer piloto ou smoke da rota nova)

Pergunta:
- Uma rede genérica treinada **só com o ponteiro** (protocolo CLRS, sem dicas, sem valor) inventa a distância como variável oculta?
- Essa variável e a regra dela podem ser lidas **sem supervisão**: uma leitura linear z = h·a + b cuja dinâmica fecha numa regra da linguagem do E018, z^{t+1} ≈ R(z^t)?

Controle negativo: WP, cujo ponteiro é trivial (a aresta mais pesada); a rede não precisa de estado oculto ali.

| # | Previsão | Prob. (antes de ver qualquer dado) |
|---|---|---|
| P1 | Rede SP treinada só com o ponteiro: acurácia em n = 64 ≥ 0,75 (IQM, 5 sementes) | 0,60 |
| P2 | SP, rota mecanística (leitura + regra ajustadas sem verdade): programa reconhecido como a relaxação min-plus (regra, ponteiro e início) em ≥ 4/5 sementes | 0,35 |
| P3 | SP: a leitura z da regra escolhida correlaciona com a distância verdadeira com \|r\| ≥ 0,9 em ≥ 4/5 sementes | 0,45 |
| P4 | WP (controle): a leitura escolhida correlaciona com a largura verdadeira com \|r\| < 0,5 em ≥ 4/5 sementes | 0,50 |
| P5 | Síntese direta a partir dos ponteiros verdadeiros (enumeração conjunta de regra, início e ponteiro): reconhecida no SP em ≥ 4/5 | 0,85 |
| P6 | Todo programa reconhecido acerta 1,000 em n = 256 | 0,95 |

Os detalhes da montagem, os hashes e as sementes vão no PREREG.md. Estas probabilidades não mudam depois do smoke.
