---
name: ciclo
description: Executa um ciclo completo do laço de pesquisa do laboratório (ler estado, escolher hipótese, checar novidade, pré-registrar, construir, rodar, medir, atacar, decidir, semear, registrar, commitar). Use quando o usuário pedir /ciclo, "roda um ciclo", "continua a exploração" ou "próximo experimento".
---

# /ciclo — um giro do laço de evolução

Argumento opcional: id de hipótese da fila (ex.: `H-3.2a`) ou trilha (`A`..`E`). Sem argumento, escolha pelo `PLANO.md §3`.

## Passos

0. **CRITICAR (regra 19).** `python3 -m lab.critica`; responda às 8 perguntas em `CRITICA.md` (`## Ciclo N — data`) e termine com a decisão. A decisão manda no passo 2: APROFUNDAR (seguir o foco), VARIAR (outro tema), ENDURECER (mesma pergunta com teste mais sério, externo ou adversarial) ou PIVOTAR (novo norte, com revisão de literatura).

1. **LER.** `GOALS.md` e `BUSSOLA.md` (rode `python3 -m lab.bussola fronteira`), `CLAUDE.md`, `ESTADO.md`, `LICOES.md`, as últimas 2 entradas do `DIARIO.md`, a última entrada do `EVOLUTION_LOG.md` de cada tema, o topo do `LIVRO.md` (meta-métricas). Rode `python3 -m unittest discover -s lab -t .` e `python3 -m lab.checar --resumo` (0 erros antes de começar).
2. **ESCOLHER.** Siga a decisão da CRÍTICA; por padrão, escolha a **habilidade-alvo** na fronteira da bússola (maior prioridade, salvo justificativa). Aplique a política de busca do `PLANO.md §3` (seguir a linha / ramificar se `ciclos_sem_subir` ≥ 2 / promover antes de explorar / infra que desbloqueia / diversidade). Defina **nó pai** e **operador** (RASCUNHO, MELHORAR, DEPURAR, REPLICAR, ABLAR). Rejeite duplicatas: procure a hipótese em `registro/arvore.jsonl`. O alvo tem de ser o degrau **N+1** do tema. Diga em uma linha por quê.
3. **CHECAR NOVIDADE.** Leia `docs/LITERATURA_G1.md` (ou a revisão do goal atacado) e faça buscas pela ideia central até achar o trabalho mais próximo; uma ideia que já existe não é pré-registrada como nova. Anote no PREREG, na seção "Relação com a literatura", o trabalho mais próximo e o que difere. Se já existe exatamente, reclassifique como replicação (ainda pode valer) ou escolha outra hipótese.
4. **PRÉ-REGISTRAR.** Copie `experimentos/_modelo/PREREG.md` para `experimentos/ENNN_nome/`. Preencha habilidade-alvo (Hxx), nó pai, operador, previsões **numéricas com probabilidade** e critérios de morte. Escreva o gerador/avaliador **antes** do commit, com as sementes de teste vindas de `lab.sementes` (derivadas do commit do PREREG) e o tamanho das células justificado por `lab.estat.n_para_diferenca`/`n_para_largura`; estime o custo pela fórmula de `docs/STACK.md`. Cole os hashes (`python3 -m lab.registro hash <arquivos>`). Commit **só do PREREG + avaliador** ("ENNN: pre-registro").
5. **CONSTRUIR.** O mínimo que testa. Reuse `lab/` e experimentos anteriores por import. `--quick` para smoke.
6. **RODAR.** Smoke primeiro (conserte bugs; o smoke não conta). Depois o completo, em segundo plano se for demorar. Não mexa em parâmetros pré-registrados.
7. **MEDIR.** Painel de `docs/VALIDACAO.md §2` com `lab/estat.py`. Salve `resultados.md` e `resultados.json`.
8. **ATACAR.** Rode `python3 -m lab.registro verificar` (o avaliador não pode ter mudado). Se for promover a N2+, reproduza a partir do commit do PREREG: `python3 -m lab.reproduzir experimentos/ENNN_nome` (tem de dar IDENTICA). Escreva as 3 objeções mais fortes. Se uma derrubar o resultado e der para testar em minutos, teste agora (é diagnóstico, não muda o veredito pré-registrado).
9. **DECIDIR.** Para cada previsão: ✅ / 🟥. Veredito: PROMOVER (novo nível) | MATAR | PIVOTAR. Escreva o `RELATORIO.md` a partir do modelo. Se o resultado contradisser registros antigos, anote a correção neles.
9b. **ESCALAR.** Protocolo Scalata (`docs/ESCALA.md`): acrescente ao `EVOLUTION_LOG.md` a entrada curta do ciclo (formato em `docs/ESCALA.md`): degrau atual com evidência, o que o ciclo mostrou com números, barreira, próximo teste; a escada D01–D30 só é colada quando reescrita. Sem prosa metafórica. Se o experimento derrubou um degrau, registre a descida.
10. **SEMEAR.** 1–3 novas hipóteses na fila do `ESTADO.md`, cada uma com o átomo ou a síntese (Σ) que testa.
11. **REGISTRAR.** Se o critério da habilidade foi cumprido no nível mínimo, acrescente o id do experimento em `desbloqueada_por` (`registro/habilidades.json`); se uma evidência antiga caiu, retire. Se o ciclo revelou uma capacidade intermediária, crie a habilidade (critério numérico + pré-requisitos). Regere a bússola (`python3 -m lab.bussola`). Acrescente o nó na árvore (`lab.registro.adicionar` com operador, pai, previsões com `prob` e `acertou`, veredito, nível, novidade, degrau_atingido, lições, commits, custo). Regere o livro (`python3 -m lab.registro livro`). Se alguma afirmação foi refutada, acrescente-a em `registro/obsoletos.txt`. Rode `python3 -m lab.checar` até dar 0 erros. Reescreva o `LICOES.md` se algo mudou. Atualize `ESTADO.md` (placar, fila, status dos átomos em `docs/SISTEMAS.md`) e acrescente uma entrada no `DIARIO.md`. Commit e push.
12. **CONTINUAR?** Se ainda houver orçamento na sessão, volte ao passo 1.

## Formato da entrada no DIARIO.md

```
## Ciclo N — AAAA-MM-DD — ENNN nome
- Hipótese: ...
- Veredito: PROMOVER/MATAR/PIVOTAR (nível)
- O que aprendemos (1–3 linhas, inclusive o que surpreendeu)
- Semeado: H-..., H-...
```
