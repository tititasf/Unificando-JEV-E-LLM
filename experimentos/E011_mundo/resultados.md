# E011 - resultados 

10 sementes x 25 trajetorias de 16 passos; treino L=8; base das sementes de teste = 078a745a017d

| braço | L | erro por passo, IQM [IC95%] | trajetórias 100% certas, IQM | colapsos (traj < 0,5) |
|---|---|---|---|---|
| MUNDO | 8 | 0.0000 [0.0000,0.0000] | 1.00 | 0/10 |
| MUNDO | 32 | 0.0000 [0.0000,0.0000] | 1.00 | 0/10 |
| MUNDO | 64 | 0.0000 [0.0000,0.0000] | 1.00 | 0/10 |
| SEM_PAREDE | 8 | 0.1525 [0.1400,0.1692] | 0.57 | 3/10 |
| SEM_PAREDE | 32 | 0.1483 [0.1121,0.1967] | 0.57 | 3/10 |
| SEM_PAREDE | 64 | 0.1292 [0.0912,0.1737] | 0.72 | 0/10 |
| PERSISTENCIA | 8 | 0.9167 [0.9104,0.9233] | 0.00 | 10/10 |
| PERSISTENCIA | 32 | 1.0000 [1.0000,1.0000] | 0.00 | 10/10 |
| PERSISTENCIA | 64 | 1.0000 [1.0000,1.0000] | 0.00 | 10/10 |
| SEM_REBOTE | 8 | 0.8129 [0.7942,0.8275] | 0.00 | 10/10 |
| SEM_REBOTE | 32 | 0.3650 [0.3212,0.4075] | 0.22 | 10/10 |
| SEM_REBOTE | 64 | 0.2067 [0.1588,0.2750] | 0.63 | 2/10 |

## Checagem das previsões

- P1 MUNDO erro por passo < 0,01 em todo L: True (L=8: 0.0000, L=32: 0.0000, L=64: 0.0000)
- P2 MUNDO trajetórias 100% certas em L=64: IQM 1.00 (previsto >= 0,95)
- P3 SEM_PAREDE erro por passo em L=64: IQM 0.1292 (previsto > 0,05); P(MUNDO melhor) = 1.00, p = 0.0002
- P4 SEM_REBOTE erro por passo em L=8: IQM 0.8129 (previsto > 0,30)
- CPU total: 1494s
