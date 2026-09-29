# E003 — Relatório: Cristal Comum (S2 ↔ S4/S5)

**Veredito: PIVOTAR.** Nível: **N2** para "mensagem simbólica > analógica sob ruído,
com conhecimento fragmentado" (pré-registrado, 10 sementes, Fisher p < 1e-45).
**Novidade: baixa** (é o princípio da comunicação digital). **Σ1 na forma
original morta:** a vantagem vem de *codificar a mensagem*, não de cristalizar o pensamento.

## Previsões

| # | Previsto | Obtido | Status |
|---|---|---|---|
| Q1 | σ=0: ambos ≈100% | 1,00 / 1,00 | ✅ |
| Q2 | algum σ com SIMB ≥ CONT+20 pts em d=32, p<0,01 | +0,59 (σ=1), +0,78 (σ=2), +0,81 (σ=4); p ≤ 2e-47 | ✅ |
| Q3 | vantagem cresce com d | cresceu nos números (+0,39 → +0,81), mas **confundido com N** (N=d+5). Com N fixo (diagnóstico): sem crescimento | 🟥 |
| Q4 | σ=4 derruba os dois | CONT 0,07; SIMB 0,88 (d=32) e 0,57 (d=8) | ✅ (ruído não trivial) |

Números completos: `resultados.md`. Diagnóstico: `diagnostico.md`.

## Diagnóstico pós-hoc (N fixo = 37, 6 sementes)

| d | σ | CONT | CONT_EST (estado cristal) | SIMB_SUAVE (mensagem cristal) | SIMB (ambos) |
|---|---|---|---|---|---|
| 8 | 1 | 0,46 | 0,98 | 1,00 | 1,00 |
| 8 | 2 | 0,16 | 0,33 | 1,00 | 1,00 |
| 8 | 4 | 0,07 | 0,07 | 0,97 | 0,93 |
| 32 | 1 | 0,44 | 0,97 | 1,00 | 1,00 |
| 32 | 2 | 0,26 | 0,44 | 1,00 | 1,00 |
| 32 | 4 | 0,03 | 0,08 | 0,93 | 0,97 |

Leitura:
1. **A mensagem é o que importa.** Concentrar toda a potência num símbolo (índice discreto) dá SNR muito maior que espalhá-la num vetor de logits. É modulação digital.
2. **Cristalizar o estado do receptor** regenera o sinal com ruído moderado (σ=1: 0,46→0,98), mas não salva com ruído alto.
3. **d não importa com N fixo.** A tarefa "achar a raiz" é um **atrator**: um salto errado que cai em outro nó da mesma árvore ainda chega à raiz certa. A tarefa se autocorrige, e isso mascara o acúmulo de erros.
4. **Custo:** o SIMB envia log₂N bits por passo (≈5 bits para N=37) contra N números reais no CONT. Mais robusto **e** ~200× mais compacto.

## Revisor hostil

1. *"É só Shannon."* Sim. O valor está em mostrar que um raciocínio **aprendido e fragmentado** pode ser cortado em mensagens discretas sem re-treino, e em medir quanto se ganha.
2. *"A potência igual favorece o símbolo."* Potência igual é a comparação justa num canal físico. Com *bits* iguais a vantagem seria ainda maior.
3. *"A tarefa se autocorrige."* Correto, e é o achado metodológico mais importante daqui: tarefas-atrator não servem para medir acúmulo de erros. → nova tarefa T2 sem atrator.

## Correções

- `docs/SISTEMAS.md` Σ1: reescrito. "Pensamento = símbolo" não é suportado (E002 + E003). O que foi suportado: **"comunicação = símbolo"**.

## Hipóteses semeadas

- **H-T2-salto-exato:** tarefa sem atrator (seguir exatamente k ponteiros numa permutação, em que qualquer erro é fatal). Refazer E002/E003 nela. *Prioridade alta:* sem isso os testes de ruído e estabilidade ficam cegos.
- **H-Σ1b (ruído interno):** com ruído **dentro** do estado do S2 (não no canal), a cristalização passa a ajudar o pensamento?
- **H-5.4 (compressão):** qual o menor código (bits por passo) que mantém ≥99% sob σ=1? Existe código melhor que o one-hot (ex.: códigos com distância, corretores de erro aprendidos)?
