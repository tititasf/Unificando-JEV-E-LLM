# E010 - resultados 

10 sementes x 15 exemplos; treino N=8, k<=4; teste com contador de tamanho 64 e 72 passos fixos; base das sementes de teste = 6802ec9bdc4e

Célula: IQM da acurácia entre sementes [IC95%] (colapsos < 0,5).

| braço | N | k=4 | k=16 | k=64 |
|---|---|---|---|---|
| MEMORIA | 8 | 1.00 [1.00,1.00] (0) | 1.00 [1.00,1.00] (0) | 1.00 [1.00,1.00] (0) |
| MEMORIA | 32 | 1.00 [1.00,1.00] (0) | 1.00 [1.00,1.00] (0) | 1.00 [1.00,1.00] (0) |
| MEMORIA | 64 | 1.00 [1.00,1.00] (0) | 1.00 [1.00,1.00] (0) | 1.00 [1.00,1.00] (0) |
| SEM_MARCAS | 8 | 1.00 [1.00,1.00] (0) | 1.00 [1.00,1.00] (0) | 1.00 [1.00,1.00] (0) |
| SEM_MARCAS | 32 | 1.00 [1.00,1.00] (0) | 1.00 [0.97,1.00] (0) | 0.97 [0.90,1.00] (0) |
| SEM_MARCAS | 64 | 1.00 [0.99,1.00] (0) | 1.00 [0.99,1.00] (0) | 1.00 [1.00,1.00] (0) |
| SEM_MEMORIA | 8 | 0.42 [0.28,0.49] (8) | 0.67 [0.62,0.73] (0) | 0.49 [0.40,0.56] (5) |
| SEM_MEMORIA | 32 | 0.17 [0.12,0.22] (10) | 0.22 [0.17,0.27] (10) | 0.13 [0.08,0.23] (10) |
| SEM_MEMORIA | 64 | 0.03 [0.00,0.10] (10) | 0.09 [0.07,0.16] (10) | 0.06 [0.02,0.10] (10) |
| CONTROLADOR | 8 | 1.00 [1.00,1.00] (0) | 1.00 [1.00,1.00] (0) | 1.00 [1.00,1.00] (0) |
| CONTROLADOR | 32 | 1.00 [1.00,1.00] (0) | 1.00 [1.00,1.00] (0) | 1.00 [1.00,1.00] (0) |
| CONTROLADOR | 64 | 1.00 [1.00,1.00] (0) | 1.00 [1.00,1.00] (0) | 1.00 [1.00,1.00] (0) |

## Checagem das previsões

- P1 MEMORIA IQM >= 0,95 em todas as células: True
- P2 MEMORIA em (N=64, k=64): IQM 1.00, colapsos 0/10
- P3 SEM_MARCAS em (N=64, k=64): IQM 1.00; MEMORIA vs SEM_MARCAS: P(A>B) = 0.50, p = 1.0000
- P4 SEM_MEMORIA em (N=64, k=64): IQM 0.06
- P5 CONTROLADOR (limite superior) em (N=64, k=64): IQM 1.00
- CPU total: 3602s
