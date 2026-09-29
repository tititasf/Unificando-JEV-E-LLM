# Resultados — MLU (Motor Latente Unificado)

Saída completa da semente 7 (as sementes 1, 2 e 3 estão em `experimento/saida_seed*.txt`).
`flops med.` = multiplicações estimadas por exemplo. `*` = houve abstenções.

```
=== N=12 nos (treino so viu d=0..4) ===
modelo           d=0     d=1     d=2     d=3     d=4     d=5     d=6     d=7     d=8     d=9   flops med.
S1-MLP           94%     57%     53%     55%     58%     59%     62%     64%     68%     66%        1200
S2-fixo         100%    100%    100%    100%    100%    100%    100%    100%    100%    100%        1728
S2+S3           100%    100%    100%    100%    100%    100%    100%    100%    100%    100%         792
MLU              99%     95%     94%     96%     97%     97%     98%     98%     99%    100%        1884
  (* = abstencoes: o modelo disse 'nao sei' em parte dos casos)

Fracao em que o roteador do MLU confiou no S1 (atalho intuitivo):
  d=0: 79%  d=1: 22%  d=2: 20%  d=3: 16%  d=4: 19%  d=5: 13%  d=6: 10%  d=7: 12%  d=8: 12%  d=9: 7%

=== N=16 nos (tamanho nunca visto, T_MAX=12) ===
modelo           d=0     d=2     d=4     d=8    d=11    d=13   flops med.
S1-MLP        (nao aplicavel: tamanho de entrada fixo)
S2-fixo         100%    100%    100%    100%    100%      0%        3072
S2+S3           100%    100%    100%    100%    100%     0%*        1815
  (* = abstencoes: o modelo disse 'nao sei' em parte dos casos)

S3 em N=16: respondeu 1000, errou 0 das respondidas, se absteve 200.

Passos latentes medios do S2+S3 por profundidade (N=12):
  d=0: 1.0  d=1: 2.0  d=2: 3.0  d=3: 4.0  d=4: 5.0  d=5: 6.0  d=6: 7.0  d=7: 8.0  d=8: 9.0  d=9: 10.0

Pensar mais tempo: mesmo modelo de 33 parametros, orcamento maior:
  (continuo = estado latente difuso | cristalizado = colapso discreto a cada passo)
  N= 16 d= 13 T_MAX= 24: continuo 100% | cristalizado 100%
  N= 32 d= 25 T_MAX= 40: continuo 100% | cristalizado 100%
  N= 64 d= 50 T_MAX= 64: continuo   0% | cristalizado 100%
  N=128 d=100 T_MAX=128: continuo   0% | cristalizado 100%
Tempo total: 33s
```

## Robustez entre sementes

| Semente | S1-MLP d≥1 | MLU (colado) d≥1 | S2+S3 N=12 | S3: erros / abstenções (N=16) | contínuo N=64 | contínuo N=128 | cristalizado N=64 / 128 |
|---|---|---|---|---|---|---|---|
| 7 | 53–68 % | 94–100 % | 100 % | 0 / 200 | 0 % | 0 % | 100 % / 100 % |
| 1 | 55–68 % | 92–100 % | 100 % | 0 / 200 | 0 % | 0 % | 100 % / 100 % |
| 2 | 51–71 % | 93–100 % | 100 % | 0 / 200 | 100 % | 100 % | 100 % / 100 % |
| 3 | 53–70 % | 94–100 % | 100 % | 0 / 200 | 100 % | 97 % | 100 % / 100 % |

## Por que o estado contínuo falha em grafos grandes

O passo aprendido separa "pai" dos outros nós por uma margem de ~6,5 em
logits. Isso basta com 12 nós, então o treino para de afiar. Com 64 nós, a
massa que vaza por passo é ~ (N−1)·e^(−6,5) ≈ 9 %, e após poucos passos o
estado vira névoa (máx. 0,046). A cristalização (colapsar para o nó mais
provável a cada passo) zera esse erro acumulado — é correção de erro
digital aplicada ao pensamento, e não exigiu nenhum re-treino.
