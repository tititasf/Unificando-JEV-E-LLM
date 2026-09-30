# E018 - resultados 

5 sementes por familia; rede: 64 grafos por n; programa: 20 grafos por n.

| família | quem | n | ponteiro IQM [IC95%] |
|---|---|---|---|
| SP | rede | 16 | 0.952 [0.941,0.966] |
| SP | rede | 32 | 0.921 [0.883,0.932] |
| SP | rede | 64 | 0.799 [0.773,0.830] |
| SP | programa (mecanistica) | 16 | 1.000 [1.000,1.000] |
| SP | programa (mecanistica) | 64 | 1.000 [1.000,1.000] |
| SP | programa (mecanistica) | 256 | 1.000 [1.000,1.000] |
| SP | programa (comportamental) | 16 | 1.000 [1.000,1.000] |
| SP | programa (comportamental) | 64 | 1.000 [1.000,1.000] |
| SP | programa (comportamental) | 256 | 1.000 [1.000,1.000] |
| SP | programa (sintese) | 16 | 1.000 [1.000,1.000] |
| SP | programa (sintese) | 64 | 1.000 [1.000,1.000] |
| SP | programa (sintese) | 256 | 1.000 [1.000,1.000] |
| WP | rede | 16 | 0.984 [0.909,0.994] |
| WP | rede | 32 | 0.956 [0.869,0.985] |
| WP | rede | 64 | 0.892 [0.713,0.964] |
| WP | programa (mecanistica) | 16 | 1.000 [0.998,1.000] |
| WP | programa (mecanistica) | 64 | 1.000 [0.743,1.000] |
| WP | programa (mecanistica) | 256 | 1.000 [0.429,1.000] |
| WP | programa (comportamental) | 16 | 1.000 [0.998,1.000] |
| WP | programa (comportamental) | 64 | 1.000 [0.743,1.000] |
| WP | programa (comportamental) | 256 | 1.000 [0.429,1.000] |
| WP | programa (sintese) | 16 | 1.000 [1.000,1.000] |
| WP | programa (sintese) | 64 | 1.000 [1.000,1.000] |
| WP | programa (sintese) | 256 | 1.000 [1.000,1.000] |

| família | método | reconhecido (regra+ponteiro+início) | só a regra |
|---|---|---|---|
| SP | mecanistica | 5/5 | 5/5 |
| SP | comportamental | 5/5 | 5/5 |
| SP | sintese | 5/5 | 5/5 |
| WP | mecanistica | 0/5 | 0/5 |
| WP | comportamental | 0/5 | 0/5 |
| WP | sintese | 5/5 | 5/5 |

- SP 1800: mecanistica: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.043317] ptr [0.921875, 'argmin', 'lin', [1.0, 1.0]] | comportamental: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.043317] ptr [0.921875, 'argmin', 'lin', [1.0, 1.0]] | sintese: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.0] ptr [1.0, 'argmin', 'lin', [1.0, 1.0]] | erro do semianel contra a rede 0.0433
- WP 1800: mecanistica: [['media', 'minf', False], [0.5, 1.0, 0.5], -10000.0, 1.0, 0.044407] ptr [0.878906, 'argmax', 'lin', [0.0, 1.0]] | comportamental: [['media', 'minf', True], [0.5, 1.0, 0.5], -10000.0, 1.0, 0.044407] ptr [0.878906, 'argmax', 'lin', [0.0, 1.0]] | sintese: [['max', 'minf', True], [1.0, 1.0, 0.0], -10000.0, 1.0, 0.0] ptr [1.0, 'argmax', 'lin', [0.0, 1.0]] | erro do semianel contra a rede 0.1056
- SP 1801: mecanistica: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.016325] ptr [0.875, 'argmin', 'lin', [1.0, 1.0]] | comportamental: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.016325] ptr [0.875, 'argmin', 'lin', [1.0, 1.0]] | sintese: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.0] ptr [1.0, 'argmin', 'lin', [1.0, 1.0]] | erro do semianel contra a rede 0.0163
- WP 1801: mecanistica: [['media', 'minf', False], [0.5, 1.5, 0.5], -10000.0, 1.0, 0.039579] ptr [0.777344, 'argmax', 'minf', [1.0, 1.0]] | comportamental: [['media', 'minf', True], [0.5, 1.5, 0.5], -10000.0, 1.0, 0.039579] ptr [0.777344, 'argmax', 'minf', [1.0, 1.0]] | sintese: [['max', 'minf', True], [1.0, 1.0, 0.0], -10000.0, 1.0, 0.0] ptr [1.0, 'argmax', 'lin', [0.0, 1.0]] | erro do semianel contra a rede 0.0501
- SP 1802: mecanistica: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.025484] ptr [0.917969, 'argmin', 'lin', [1.0, 1.0]] | comportamental: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.025484] ptr [0.917969, 'argmin', 'lin', [1.0, 1.0]] | sintese: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.0] ptr [1.0, 'argmin', 'lin', [1.0, 1.0]] | erro do semianel contra a rede 0.0255
- WP 1802: mecanistica: [['media', 'minf', False], [0.5, 1.0, 0.5], -10000.0, 1.0, 0.04325] ptr [0.882812, 'argmax', 'lin', [0.0, 1.0]] | comportamental: [['media', 'minf', True], [0.5, 1.0, 0.5], -10000.0, 1.0, 0.04325] ptr [0.882812, 'argmax', 'lin', [0.0, 1.0]] | sintese: [['max', 'minf', True], [1.0, 1.0, 0.0], -10000.0, 1.0, 0.0] ptr [1.0, 'argmax', 'lin', [0.0, 1.0]] | erro do semianel contra a rede 0.0892
- SP 1803: mecanistica: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.018133] ptr [0.925781, 'argmin', 'lin', [1.0, 1.0]] | comportamental: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.018133] ptr [0.925781, 'argmin', 'lin', [1.0, 1.0]] | sintese: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.0] ptr [1.0, 'argmin', 'lin', [1.0, 1.0]] | erro do semianel contra a rede 0.0181
- WP 1803: mecanistica: [['media', 'maxf', True], [0.0, 0.5, 0.5], -10000.0, 1.0, 0.043806] ptr [0.761719, 'argmax', 'lin', [0.0, 1.0]] | comportamental: [['media', 'lin', True], [0.0, 0.5, 0.5], -10000.0, 1.0, 0.043806] ptr [0.761719, 'argmax', 'lin', [0.0, 1.0]] | sintese: [['max', 'minf', True], [1.0, 1.0, 0.0], -10000.0, 1.0, 0.0] ptr [1.0, 'argmax', 'lin', [0.0, 1.0]] | erro do semianel contra a rede 0.0911
- SP 1804: mecanistica: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.026255] ptr [0.953125, 'argmin', 'lin', [1.0, 1.0]] | comportamental: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.026255] ptr [0.953125, 'argmin', 'lin', [1.0, 1.0]] | sintese: [['min', 'lin', True], [1.0, 1.0, 0.0], 10000.0, 0.0, 0.0] ptr [1.0, 'argmin', 'lin', [1.0, 1.0]] | erro do semianel contra a rede 0.0263
- WP 1804: mecanistica: [['media', 'minf', True], [0.5, 1.0, 0.5], -10000.0, 1.0, 0.036788] ptr [0.90625, 'argmax', 'lin', [0.0, 1.0]] | comportamental: [['media', 'minf', True], [0.5, 1.0, 0.5], -10000.0, 1.0, 0.036788] ptr [0.90625, 'argmax', 'lin', [0.0, 1.0]] | sintese: [['max', 'minf', True], [1.0, 1.0, 0.0], -10000.0, 1.0, 0.0] ptr [1.0, 'argmax', 'lin', [0.0, 1.0]] | erro do semianel contra a rede 0.0731

## Checagem das previsões

- P1 SP OK: síntese direta (sem rede) reconhecida em >= 80%: 5/5
- P1 WP OK: síntese direta (sem rede) reconhecida em >= 80%: 5/5
- P2 SP OK: extração comportamental da rede reconhecida em >= 80%: 5/5
- P2 WP FALHOU: extração comportamental da rede reconhecida em >= 80%: 0/5
- P3 SP OK: extração mecanística da rede reconhecida em >= 80%: 5/5
- P3 WP FALHOU: extração mecanística da rede reconhecida em >= 80%: 0/5
- P4 OK: todo programa reconhecido acerta 1,000 em n=256: min 1.0 (20 programas)
- P5 SP OK: a própria rede fica < 0,99 em n=64: 0.799
- P5 WP OK: a própria rede fica < 0,99 em n=64: 0.892
- P6 OK: a síntese direta reconhece mais que a melhor extração da rede (comportamental), somando as famílias: 10/10 contra 5/10 (Fisher p = 0.033); média rede 5.0
- CPU total: 6997s
