---
name: ciclo
description: Executa um ciclo completo do laço de pesquisa do laboratório (ler estado, escolher hipótese, checar novidade, pré-registrar, construir, rodar, medir, atacar, decidir, semear, registrar, commitar). Use quando o usuário pedir /ciclo, "roda um ciclo", "continua a exploração" ou "próximo experimento".
---

# /ciclo — um giro do laço de evolução

Argumento opcional: id de hipótese da fila (ex.: `H-3.2a`) ou trilha (`A`..`E`). Sem argumento, escolha pelo `PLANO.md §3`.

## Passos

1. **LER.** `CLAUDE.md`, `ESTADO.md`, as últimas 2 entradas do `DIARIO.md`. Rode `python3 -m unittest lab.test_estat`.
2. **ESCOLHER.** Pegue o topo da fila do `ESTADO.md` (promover N1→N2 vem antes de ideia nova, ~70/30). Diga em uma linha por quê.
3. **CHECAR NOVIDADE.** 1–3 buscas na web pela ideia central. Anote no PREREG, na seção "Relação com a literatura", o trabalho mais próximo e o que difere. Se já existe exatamente, reclassifique como replicação (ainda pode valer) ou escolha outra hipótese.
4. **PRÉ-REGISTRAR.** Copie `experimentos/_modelo/PREREG.md` para `experimentos/ENNN_nome/`. Preencha previsões **numéricas** e critérios de morte. Commit **só do PREREG** ("ENNN: pre-registro").
5. **CONSTRUIR.** O mínimo que testa. Reuse `lab/` e experimentos anteriores por import. `--quick` para smoke.
6. **RODAR.** Smoke primeiro (conserte bugs; o smoke não conta). Depois o completo, em segundo plano se for demorar. Não mexa em parâmetros pré-registrados.
7. **MEDIR.** Painel de `docs/VALIDACAO.md §2` com `lab/estat.py`. Salve `resultados.md` e `resultados.json`.
8. **ATACAR.** Escreva as 3 objeções mais fortes. Se uma derrubar o resultado e der para testar em minutos, teste agora (é diagnóstico, não muda o veredito pré-registrado).
9. **DECIDIR.** Para cada previsão: ✅ / 🟥. Veredito: PROMOVER (novo nível) | MATAR | PIVOTAR. Escreva o `RELATORIO.md` a partir do modelo. Se o resultado contradisser registros antigos, anote a correção neles.
10. **SEMEAR.** 1–3 novas hipóteses na fila do `ESTADO.md`, cada uma com o átomo ou a síntese (Σ) que testa.
11. **REGISTRAR.** Atualize `ESTADO.md` (placar, fila, status dos átomos em `docs/SISTEMAS.md`) e acrescente uma entrada no `DIARIO.md`. Commit e push.
12. **CONTINUAR?** Se ainda houver orçamento na sessão, volte ao passo 1.

## Formato da entrada no DIARIO.md

```
## Ciclo N — AAAA-MM-DD — ENNN nome
- Hipótese: ...
- Veredito: PROMOVER/MATAR/PIVOTAR (nível)
- O que aprendemos (1–3 linhas, inclusive o que surpreendeu)
- Semeado: H-..., H-...
```
