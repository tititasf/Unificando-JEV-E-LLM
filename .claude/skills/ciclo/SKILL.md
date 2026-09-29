---
name: ciclo
description: Executa um ciclo completo do laço de pesquisa do laboratório (ler estado, escolher hipótese, checar novidade, pré-registrar, construir, rodar, medir, atacar, decidir, semear, registrar, commitar). Use quando o usuário pedir /ciclo, "roda um ciclo", "continua a exploração" ou "próximo experimento".
---

# /ciclo — um giro do laço de evolução

Argumento opcional: id de hipótese da fila (ex.: `H-3.2a`) ou trilha (`A`..`E`). Sem argumento, escolha pelo `PLANO.md §3`.

## Passos

1. **LER.** `GOALS.md` e `BUSSOLA.md` (rode `python3 -m lab.bussola fronteira`), `CLAUDE.md`, `ESTADO.md`, `LICOES.md`, as últimas 2 entradas do `DIARIO.md`, a última entrada do `EVOLUTION_LOG.md` de cada tema, o topo do `LIVRO.md` (meta-métricas). Rode `python3 -m unittest discover -s lab -t .` e `python3 -m lab.checar --resumo` (0 erros antes de começar).
2. **ESCOLHER.** Escolha a **habilidade-alvo** na fronteira da bússola (maior prioridade, salvo justificativa). Aplique a política de busca do `PLANO.md §3` (seguir a linha / ramificar se `ciclos_sem_subir` ≥ 2 / promover antes de explorar / infra que desbloqueia / diversidade). Defina **nó pai** e **operador** (RASCUNHO, MELHORAR, DEPURAR, REPLICAR, ABLAR). Rejeite duplicatas: procure a hipótese em `registro/arvore.jsonl`. O alvo tem de ser o degrau **N+1** do tema. Diga em uma linha por quê.
3. **CHECAR NOVIDADE.** 1–3 buscas na web pela ideia central. Anote no PREREG, na seção "Relação com a literatura", o trabalho mais próximo e o que difere. Se já existe exatamente, reclassifique como replicação (ainda pode valer) ou escolha outra hipótese.
4. **PRÉ-REGISTRAR.** Copie `experimentos/_modelo/PREREG.md` para `experimentos/ENNN_nome/`. Preencha habilidade-alvo (Hxx), nó pai, operador, previsões **numéricas com probabilidade** e critérios de morte. Escreva o gerador/avaliador **antes** do commit, com as sementes de teste vindas de `lab.sementes` (derivadas do commit do PREREG) e o tamanho das células justificado por `lab.estat.n_para_diferenca`/`n_para_largura`; estime o custo pela fórmula de `docs/STACK.md`. Cole os hashes (`python3 -m lab.registro hash <arquivos>`). Commit **só do PREREG + avaliador** ("ENNN: pre-registro").
5. **CONSTRUIR.** O mínimo que testa. Reuse `lab/` e experimentos anteriores por import. `--quick` para smoke.
6. **RODAR.** Smoke primeiro (conserte bugs; o smoke não conta). Depois o completo, em segundo plano se for demorar. Não mexa em parâmetros pré-registrados.
7. **MEDIR.** Painel de `docs/VALIDACAO.md §2` com `lab/estat.py`. Salve `resultados.md` e `resultados.json`.
8. **ATACAR.** Rode `python3 -m lab.registro verificar` (o avaliador não pode ter mudado). Se for promover a N2+, reproduza o resultado principal a partir de um checkout limpo (`git stash`/worktree) com o comando único. Escreva as 3 objeções mais fortes. Se uma derrubar o resultado e der para testar em minutos, teste agora (é diagnóstico, não muda o veredito pré-registrado).
9. **DECIDIR.** Para cada previsão: ✅ / 🟥. Veredito: PROMOVER (novo nível) | MATAR | PIVOTAR. Escreva o `RELATORIO.md` a partir do modelo. Se o resultado contradisser registros antigos, anote a correção neles.
9b. **ESCALAR.** Protocolo Scalata (`docs/ESCALA.md`): acrescente ao `EVOLUTION_LOG.md` a entrada do ciclo com (1) diagnóstico do degrau atual citando a evidência, (2) a escada completa D01–D30 do tema (sem pular nem juntar degraus; reuse a da entrada anterior, corrigida, se o tema já tiver escada), (3) a transição D→D+1 (sacada, o que subtrair, o que testar), (4) visão vertical em 10 níveis e (5) deep insight. Se o experimento derrubou um degrau, registre a descida.
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
