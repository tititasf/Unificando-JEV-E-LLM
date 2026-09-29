# Unificando JEV e LLM

Exploração em micro-escala: o que acontece quando se une um "Sistema 1"
(decisão em uma passada, estilo modelo de decisão tipada), um "Sistema 2"
(raciocínio iterativo num estado latente, sem gerar texto) e um "Sistema 3"
(metacognição: quando parar, quando dizer "não sei").

- [`PLANO.md`](PLANO.md) — contexto, reflexão, resultados e plano dos próximos experimentos
- [`RESULTADOS.md`](RESULTADOS.md) — tabelas completas e robustez entre sementes
- [`experimento/mlu.py`](experimento/mlu.py) — código (Python puro, sem dependências, ~30 s)

```bash
python3 experimento/mlu.py
```
