# E008 - resultados 

10 sementes x 30 exemplos por d; N=12; T_max=16; base das sementes de teste = 487586fb1fce

| d | acc PonderNet | passos PonderNet | acc CONV | passos CONV | abst CONV | acc FIXO (T=16) |
|---|---|---|---|---|---|---|
| 0 | 1.000 | 6.00 | 1.000 | 1.00 | 0.000 | 1.000 |
| 1 | 1.000 | 7.00 | 1.000 | 2.10 | 0.000 | 1.000 |
| 2 | 1.000 | 8.00 | 1.000 | 3.15 | 0.000 | 1.000 |
| 3 | 1.000 | 9.00 | 1.000 | 4.17 | 0.000 | 1.000 |
| 4 | 1.000 | 10.00 | 1.000 | 5.18 | 0.000 | 1.000 |
| 5 | 1.000 | 11.00 | 1.000 | 6.19 | 0.000 | 1.000 |
| 6 | 1.000 | 12.00 | 1.000 | 7.14 | 0.000 | 1.000 |
| 7 | 1.000 | 13.00 | 1.000 | 8.14 | 0.000 | 1.000 |
| 8 | 1.000 | 14.00 | 1.000 | 9.12 | 0.000 | 1.000 |
| 9 | 1.000 | 14.90 | 1.000 | 10.10 | 0.000 | 1.000 |

## Checagem das previsões

- P1 Spearman(d, passos PonderNet) por semente: mediana 1.00, min 1.00 (previsto mediana >= 0,8)
- P2 acc PonderNet d<=4: IQM 1.000, min 1.000 (previsto >= 0,95)
- P3 acc PonderNet d=5..9 (fora da distribuicao): IQM 1.000, min 1.000 (previsto >= 0,90)
- P4 passos medios PonderNet 10.49 vs CONV 5.63 (previsto: PonderNet <= CONV + 1)
- CPU total: 154s
