# Unificando JEV e LLM — laboratório de sistemas cognitivos

Laboratório autônomo que tenta unir, em máquinas minúsculas, os sistemas
cognitivos: S0 substrato, S1 intuição (decisão em uma passada, estilo
"modelo de decisão tipada"/JEV), S2 deliberação (raciocínio latente sem
texto), S3 metacognição, S4 coletivo, S5 comunicação, S6 simulação do
futuro. Tudo é medido com uma régua de evidência explícita.

| Arquivo | Para quê |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Instruções de operação autônoma |
| [`ESTADO.md`](ESTADO.md) | Placar de achados e fila de hipóteses |
| [`DIARIO.md`](DIARIO.md) | Um registro por ciclo |
| [`PLANO.md`](PLANO.md) | O laço de evolução, trilhas e portões |
| [`docs/VALIDACAO.md`](docs/VALIDACAO.md) | Como medir se algo é real (e revolucionário) |
| [`docs/SISTEMAS.md`](docs/SISTEMAS.md) | Cada sistema em átomos, matriz de sincronia, sínteses Σ |
| [`lab/estat.py`](lab/estat.py) | Estatística da régua (Python puro) |
| [`experimentos/`](experimentos/) | E001–E003 com pré-registros e relatórios |

```bash
python3 -m unittest lab.test_estat
python3 experimentos/E003_cristal_comum/e003.py
```

No Claude Code: `/ciclo` roda um giro do laço.
