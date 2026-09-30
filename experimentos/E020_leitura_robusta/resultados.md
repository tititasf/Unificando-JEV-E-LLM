# E020 - resultados 

10 sementes por familia; redes so com ponteiro; rede: 64 grafos por n; programa: 20 grafos por n.

| família | quem | n | ponteiro IQM [IC95%] |
|---|---|---|---|
| SP | rede (só ponteiro) | 16 | 0.949 [0.940,0.959] |
| SP | rede (só ponteiro) | 32 | 0.898 [0.883,0.911] |
| SP | rede (só ponteiro) | 64 | 0.754 [0.691,0.792] |
| SP | programa (escolha nova) | 16 | 0.559 [0.534,0.641] |
| SP | programa (escolha nova) | 64 | 0.514 [0.502,0.592] |
| SP | programa (escolha nova) | 256 | 0.505 [0.501,0.569] |
| SP | programa (escolha antiga) | 16 | 0.897 [0.697,1.000] |
| SP | programa (escolha antiga) | 64 | 0.852 [0.568,1.000] |
| SP | programa (escolha antiga) | 256 | 0.836 [0.488,1.000] |
| WP | rede (só ponteiro) | 16 | 0.988 [0.974,0.992] |
| WP | rede (só ponteiro) | 32 | 0.900 [0.807,0.966] |
| WP | rede (só ponteiro) | 64 | 0.445 [0.174,0.778] |
| WP | programa (escolha nova) | 16 | 1.000 [1.000,1.000] |
| WP | programa (escolha nova) | 64 | 1.000 [1.000,1.000] |
| WP | programa (escolha nova) | 256 | 1.000 [1.000,1.000] |
| WP | programa (escolha antiga) | 16 | 0.983 [0.924,1.000] |
| WP | programa (escolha antiga) | 64 | 0.995 [0.927,1.000] |
| WP | programa (escolha antiga) | 256 | 0.999 [0.923,1.000] |

| família | semente | escolha nova | ponteiro | r nova | escolha antiga | r antiga | máx \|r\| 18 |
|---|---|---|---|---|---|---|---|
| SP | 2000 | [['min', 'lin', True], [0.5, 1.0, 0.5], 0.0, 0.0] | [0.480469, 'argmin', 'lin', [1.0, 1.0]] | -0.794 | [['min', 'lin', False], [1.0, 1.0, 0.0], 10000.0, 0.0] [0.875, 'argmin', 'lin', [1.0, 1.0]] | 0.920 | 0.927 |
| WP | 2000 | [['min', 'minf', True], [0.0, 1.0, 1.0], 0.0, 0.0] | [0.757812, 'argmax', 'lin', [1.0, 1.0]] | -0.588 | [['min', 'minf', True], [0.0, 1.0, 1.0], -10000.0, 0.0] [0.757812, 'argmax', 'lin', [0.0, 1.0]] | -0.588 | 0.592 |
| SP | 2001 | [['min', 'maxf', True], [1.5, 1.0, 0.5], 0.0, 0.0] | [0.46875, 'argmin', 'lin', [1.0, 1.0]] | -0.818 | [['min', 'lin', True], [0.5, 1.0, 0.5], 1.0, 0.0] [0.597656, 'argmin', 'lin', [1.0, 1.0]] | -0.888 | 0.966 |
| WP | 2001 | [['max', 'minf', True], [0.5, 1.0, -1.0], -10000.0, 0.0] | [0.664062, 'argmax', 'lin', [0.0, 1.0]] | -0.365 | [['max', 'minf', True], [0.5, 1.0, -1.0], 10000.0, 0.0] [0.699219, 'argmax', 'lin', [1.0, 1.0]] | -0.365 | 0.412 |
| SP | 2002 | [['max', 'minf', True], [0.5, 1.0, -0.5], 1.0, 0.0] | [0.488281, 'argmin', 'lin', [0.0, 1.0]] | 0.964 | [['media', 'lin', False], [1.0, 1.0, -0.5], 1.0, 0.0] [0.546875, 'argmin', 'lin', [1.0, 1.0]] | 0.977 | 0.983 |
| WP | 2002 | [['min', 'minf', True], [0.0, 1.0, 1.0], 0.0, 0.0] | [0.765625, 'argmax', 'lin', [1.0, 1.0]] | -0.568 | [['max', 'maxf', True], [0.0, 1.0, 11.5], -10000.0, 0.0] [0.773438, 'argmax', 'lin', [1.0, 1.0]] | -0.585 | 0.594 |
| SP | 2003 | [['min', 'maxf', True], [1.0, 1.0, 0.0], 0.0, 0.0] | [0.511719, 'argmin', 'lin', [1.0, 1.0]] | -0.977 | [['min', 'maxf', True], [1.0, 1.0, 0.0], 10000.0, 0.0] [0.570312, 'argmin', 'lin', [1.0, 1.0]] | -0.977 | 0.985 |
| WP | 2003 | [['media', 'lin', True], [1.5, 1.0, 0.0], -10000.0, 0.0] | [0.605469, 'argmax', 'lin', [0.0, 1.0]] | 0.505 | [['min', 'maxf', False], [2.0, 1.0, -0.5], -10000.0, 0.0] [0.675781, 'argmax', 'lin', [1.0, 1.0]] | -0.522 | 0.555 |
| SP | 2004 | [['min', 'lin', True], [0.5, 1.0, 0.5], 0.0, 0.0] | [0.585938, 'argmin', 'lin', [1.0, 1.0]] | -0.941 | [['min', 'lin', False], [1.0, 1.0, 0.0], 10000.0, 0.0] [0.890625, 'argmin', 'lin', [1.0, 1.0]] | 0.980 | 0.980 |
| WP | 2004 | [['max', 'minf', True], [1.0, 1.0, 0.0], 1.0, 0.0] | [0.871094, 'argmax', 'lin', [0.0, 1.0]] | -0.453 | [['min', 'lin', True], [0.0, 1.0, 0.5], -10000.0, 0.0] [0.871094, 'argmax', 'lin', [0.0, 1.0]] | -0.386 | 0.529 |
| SP | 2005 | [['min', 'maxf', True], [1.0, 1.0, 0.0], 0.0, 0.0] | [0.523438, 'argmin', 'lin', [1.0, 1.0]] | -0.432 | [['min', 'lin', False], [1.0, 1.0, 0.0], 10000.0, 0.0] [0.914062, 'argmin', 'lin', [1.0, 1.0]] | 0.979 | 0.985 |
| WP | 2005 | [['min', 'maxf', True], [1.5, 1.0, 0.5], 0.0, 0.0] | [0.726562, 'argmax', 'lin', [1.0, 1.0]] | -0.396 | [['min', 'lin', False], [0.5, 1.0, 1.0], -10000.0, 0.0] [0.730469, 'argmax', 'minf', [1.0, 1.0]] | -0.396 | 0.401 |
| SP | 2006 | [['min', 'lin', False], [1.0, 1.0, 0.0], 0.0, 0.0] | [0.890625, 'argmin', 'lin', [1.0, 1.0]] | 0.979 | [['min', 'lin', False], [1.0, 1.0, 0.0], 10000.0, 0.0] [0.933594, 'argmin', 'lin', [1.0, 1.0]] | 0.979 | 0.986 |
| WP | 2006 | [['min', 'minf', True], [0.0, 1.0, 1.0], 0.0, 0.0] | [0.867188, 'argmax', 'lin', [1.0, 1.0]] | -0.264 | [['media', 'lin', True], [1.0, 0.0, -0.5], -10000.0, 0.0] [0.867188, 'argmax', 'lin', [0.0, 1.0]] | -0.266 | 0.274 |
| SP | 2007 | [['min', 'maxf', True], [1.5, 1.0, 0.5], 0.0, 0.0] | [0.539062, 'argmin', 'lin', [1.0, 1.0]] | -0.518 | [['media', 'maxf', True], [1.0, 1.0, -0.5], -10000.0, 0.0] [0.566406, 'argmin', 'maxf', [1.0, 1.0]] | -0.455 | 0.839 |
| WP | 2007 | [['min', 'minf', False], [1.0, 1.0, 0.0], 10000.0, 0.0] | [0.871094, 'argmax', 'lin', [1.0, 1.0]] | 0.281 | [['max', 'minf', False], [0.5, 1.0, 0.0], -10000.0, 0.0] [0.871094, 'argmax', 'lin', [1.0, 1.0]] | 0.094 | 0.345 |
| SP | 2008 | [['min', 'lin', True], [0.5, 1.0, 0.5], 0.0, 0.0] | [0.480469, 'argmin', 'lin', [1.0, 1.0]] | -0.744 | [['min', 'lin', False], [1.0, 1.0, 0.0], 10000.0, 0.0] [0.90625, 'argmin', 'lin', [1.0, 1.0]] | 0.988 | 0.988 |
| WP | 2008 | [['min', 'lin', True], [0.5, 1.0, 0.5], 0.0, 0.0] | [0.847656, 'argmax', 'lin', [1.0, 1.0]] | -0.179 | [['max', 'maxf', True], [0.5, 1.0, 0.0], -10000.0, 0.0] [0.847656, 'argmax', 'lin', [0.0, 1.0]] | -0.138 | 0.287 |
| SP | 2009 | [['min', 'minf', True], [0.0, 1.0, 1.0], 10000.0, 0.0] | [0.484375, 'argmin', 'lin', [0.0, 1.0]] | -0.479 | [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0] [0.894531, 'argmin', 'lin', [1.0, 1.0]] | 0.931 | 0.931 |
| WP | 2009 | [['min', 'lin', True], [0.5, 1.0, 0.0], 0.0, 0.0] | [0.835938, 'argmax', 'lin', [1.0, 1.0]] | 0.348 | [['min', 'lin', True], [0.5, 1.0, 0.0], -10000.0, 0.0] [0.835938, 'argmax', 'lin', [0.0, 1.0]] | 0.348 | 0.653 |

## Checagem das previsões (PREVISOES.md, commitadas antes de qualquer piloto)

- P1 FALHOU: SP escolha nova reconhecida em >= 8/10: 0/10
- P2 FALHOU: SP |r(leitura, distância)| >= 0,9 em >= 8/10: 4/10 [-0.794, -0.818, 0.964, -0.977, -0.941, -0.432, 0.979, -0.518, -0.744, -0.479]
- P3 FALHOU: WP |r(leitura, largura)| < 0,5 em >= 8/10: 7/10 [-0.588, -0.365, -0.568, 0.505, -0.453, -0.396, -0.264, 0.281, -0.179, 0.348]
- P4 FALHOU: SP escolha nova reconhecida em >= 7/10 (regra de parada): 0/10
- P5 FALHOU: escolha nova >= antiga + 2 nas mesmas redes: 0 contra 6
- P6 OK: todo programa reconhecido acerta 1,000 em n=256: min 1.0 (6)
- P7 OK: rede SP só com ponteiro em n=64 >= 0,75: 0.754
- Pareado (discordantes): só a nova 0, só a antiga 6; Fisher nova×antiga p = 0.011; IC95% da taxa nova (0.0, 0.2775401687666166)
- CPU total: 18802s
