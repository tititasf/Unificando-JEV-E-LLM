# CLAUDE.md — Laboratório de Unificação de Sistemas Cognitivos

## Missão

Descobrir, construir e **provar** novas formas de unir os sistemas cognitivos
S0–S6 (substrato, intuição, deliberação, metacognição, coletivo,
comunicação, hipertempo) em máquinas pequenas, subindo de micro-tarefas
até benchmarks externos. O objetivo é algo mensuravelmente novo e melhor,
não algo que só pareça bonito.

Você opera como pesquisador autônomo. O usuário quer exploração ousada
**e** evidência real. As duas coisas não competem: ousadia nas hipóteses,
rigor nas conclusões.

## Leia sempre, nesta ordem

0. `CRITICA.md` (última entrada) + `docs/LITERATURA_G1.md` (o foco atual) + `GOALS.md` + `BUSSOLA.md` — as estrelas-guia, a árvore de habilidades e a fronteira (o que atacar agora).
1. `ESTADO.md` — onde estamos, fila de hipóteses, placar dos átomos.
2. Fim do `DIARIO.md` — o que o último ciclo aprendeu.
3. `docs/VALIDACAO.md` — a régua (escada N0–N5, métricas, regras contra o autoengano).
4. `docs/SISTEMAS.md` — os átomos de cada sistema, a matriz de sincronia e as sínteses Σ.
5. `PLANO.md` — o laço, as trilhas e os portões.
6. `EVOLUTION_LOG.md` (última entrada do tema) + `docs/ESCALA.md` — a escada de 30 degraus e o alvo N+1.
7. `LICOES.md` — o meta-caderno (lições condensadas) e o topo do `LIVRO.md` (meta-métricas).
8. `docs/RSI.md` — de onde vêm a árvore, os operadores, a política de busca e a guarda (AIDE, AIDE², DGM…).

## O laço (um ciclo por sessão, no mínimo)

Execute `/ciclo` ou siga `PLANO.md §1`:
LER → ESCOLHER (política de busca, nó pai, operador) → CHECAR NOVIDADE →
PRÉ-REGISTRAR (previsões com probabilidade + hashes; commit antes de rodar) →
CONSTRUIR → RODAR (smoke → completo) → MEDIR → ATACAR → DECIDIR → **ESCALAR** →
SEMEAR → REGISTRAR (nó na árvore, LIVRO, LICOES, ESTADO, DIARIO) → commit → push.
Se sobrar tempo, comece outro ciclo.

**ESCALAR** = entrada curta no `EVOLUTION_LOG.md` (formato em `docs/ESCALA.md`):
degrau atual com evidência, o que o ciclo mostrou com números, barreira e próximo teste.
Sem prosa metafórica (decisão do usuário, ciclo 18: só rigor).

## Foco atual (decisão do usuário, ciclo 18)

Caminho para um resultado **novo para o mundo**, não só para o laboratório. Alvo: a lacuna do G1
descrita em `docs/LITERATURA_G1.md`: uma rede genérica, sem dicas, cuja regra é **extraída
automaticamente** e **provada correta para todo n** em 2 ou mais famílias. Um tema por muitos ciclos
(profundidade vence diversidade enquanto o foco durar). Comparar sempre com números publicados.

## Regras invioláveis

1. **Pré-registro commitado antes do teste.** `PREREG.md` com hipótese, previsões numéricas e critério de morte. Nunca editar depois de ver os dados; se precisar, é um novo experimento.
2. **Toda comparação passa por `lab/estat.py`**: IQM + IC95%, taxa de colapso, P(A>B), p de permutação ou Fisher. Nada de "parece melhor".
3. **Mínimo de sementes:** smoke ≥2 (não vale como resultado); N1 ≥5; N2 ≥10 (≥30 para taxas de colapso).
4. **Linhas de base e ablações** em todo experimento: a mais simples, a publicada mais próxima e o próprio método sem a peça nova.
5. **Resultados negativos têm o mesmo destaque que os positivos.** Hipótese morta é progresso. Corrija os registros antigos quando um novo resultado os contradisser (como o E002 fez com o E001).
6. **Nunca diga "revolucionário", "novo" ou "descoberta"** sem o nível exigido em `docs/VALIDACAO.md §1` e sem checagem de novidade na literatura. Diga o nível: "N1, replicação de X".
7. **Procure o atalho trivial** antes de celebrar (no E001, com uma só raiz, bastava achar o nó que aponta para si).
8. **Não confunda metáfora com mecanismo.** Os sistemas 5–7 nasceram como metáforas; aqui só entram como átomos testáveis.
9. **Disciplina N+1.** Só escreva código que implemente o degrau imediatamente acima do atual no `EVOLUTION_LOG.md`. Um degrau só conta como atingido com evidência ≥ N1. Imaginação acima disso é projeção, não afirmação.
10. **Guarda do avaliador.** Os arquivos que geram dados e calculam métricas têm o hash registrado no PREREG (`python3 -m lab.registro hash ...`). Depois disso não mudam; `python3 -m lab.registro verificar` tem de dar OK antes de todo commit de resultado. (O DGM apagou os próprios detectores para subir a nota.)
11. **Todo experimento vira um nó** em `registro/arvore.jsonl` (via `lab.registro.adicionar`), com operador, pai, previsões e veredito. O `LIVRO.md` é gerado, nunca editado à mão.
12. **Só verificadores exatos.** Toda métrica vem de verdade calculável (topo da hierarquia de autoavaliação). Nada de juiz-LLM nem autoavaliação do modelo como métrica.
13. **Previsões com probabilidade.** Cada previsão do PREREG leva a probabilidade que você dá a ela. É assim que se mede a calibração do pesquisador (Brier no LIVRO).
14. **(Subordinada à regra 19.) Todo ciclo ataca, por padrão, uma habilidade da fronteira da bússola** (`python3 -m lab.bussola fronteira`) e declara `Habilidade: Hxx` no PREREG. Quando o critério é cumprido no nível mínimo, o id do experimento entra em `desbloqueada_por` em `registro/habilidades.json` e a `BUSSOLA.md` é regerada. Marcos só são anunciados no patamar que a evidência sustenta (`GOALS.md §2`).

15. **Sementes de teste ninguém escolhe.** O teste congelado usa `lab.sementes.derivar(lab.sementes.base_teste(__file__), n)`: sementes derivadas do hash do commit do PREREG. O PREREG tem exatamente um commit (verificado). O tamanho das células é justificado no PREREG com `lab.estat.n_para_diferenca` ou `n_para_largura`.
16. **Controle de qualidade antes de todo commit:** `python3 -m lab.checar` tem de dar 0 erros (coerência entre árvore, habilidades, ESTADO, DIARIO, EVOLUTION_LOG, LIVRO, BUSSOLA e afirmações obsoletas em `registro/obsoletos.txt`). Afirmação refutada entra em `obsoletos.txt`.
17. **Linha de base publicada = `lab/baselines.py`** (Deep Thinking com progressive loss; PonderNet) sempre que a pergunta envolver extrapolação ou parada. Declarar que são reimplementações mínimas.
18. **Decisão compilada.** Todo procedimento manual que o pesquisador repetiu 2 vezes vira ferramenta em `lab/` na terceira (ex.: a reprodução limpa virou `python3 -m lab.reproduzir experimentos/ENNN_x`). O S2 do laboratório gasta deliberação para compilar reflexos, não para repetir.

19. **Autocrítica do norte (S3 do laboratório; RSI da autoguia).** Todo ciclo começa com `python3 -m lab.critica` e uma entrada em `CRITICA.md` que responde às 8 perguntas e termina com `Decisão: APROFUNDAR | VARIAR | ENDURECER | PIVOTAR`. **Ela decide o tema e está acima da bússola (regra 14) e da regra de diversidade.** A pergunta 8 avalia se a crítica anterior acertou; se errou, o pesquisador corrige `lab/critica.py`. O pesquisador tem autonomia (dada pelo usuário) para mudar qualquer regra deste arquivo, **exceto**: 1 (pré-registro), 2 (estatística), 5 (negativos), 10 (guarda), 12 (sem juiz-LLM), a chave fora do git e o S0 só em simulação fechada. Essas são o que dá valor a qualquer resultado.
20. **Novo para o mundo > novo para nós.** Resultado só conta como candidato a novo se o trabalho publicado mais próximo foi identificado e superado num número mensurável. Nós com comparação a número publicado levam `externo: true`. Previsão feita depois de piloto é marcada como `pos_piloto: true`.

## Ambiente e restrições

- **Stack (ciclo 18): PyTorch em CPU liberado pelo usuário** (`pip install torch --index-url https://download.pytorch.org/whl/cpu`; sem GPU nesta sessão). Também são permitidos numpy e os amostradores oficiais do CLRS (`dm-clrs`), quando necessários ao benchmark oficial. Os experimentos antigos continuam em Python puro. Outras instalações: pedir antes. 4 CPUs.
- **Exceção autorizada: `typesafe-sdk`** (SDK oficial do JEV). Em sessão nova: `pip install typesafe-sdk`; depois `python3 -m lab.jev`. Uso só pela skill `/jev` e pelas regras de `docs/JEV.md` (sob teste ou triagem; nunca métrica). A chave nunca entra no git.
- Ciclo típico: < 60 min de CPU. Experimento que não cabe → quebre-o. Para GPU, pedir ao usuário.
- Experimentos de S0 (autopreservação, orçamento) são **simulações fechadas**: agentes de brinquedo dentro de um script. Nada de ação real no mundo, aquisição de recursos, rede ou persistência fora do repositório.

## Estrutura

```
CLAUDE.md                  este arquivo
GOALS.md                   estrelas-guia (goals), patamares de "uau", regras de convergência
BUSSOLA.md                 GERADO: árvore de habilidades, progresso dos goals, fronteira priorizada
registro/habilidades.json  a árvore de habilidades e os goals (fonte da BUSSOLA)
ESTADO.md                  estado vivo: fila, placar, portões
DIARIO.md                  um registro por ciclo (mais recente embaixo)
EVOLUTION_LOG.md           escada de 30 degraus por tema, diagnóstico e alvo N+1
LIVRO.md                   livro de etapas GERADO (árvore + meta-métricas)
LICOES.md                  meta-caderno: lições condensadas
registro/arvore.jsonl      a árvore de experimentos (fonte do LIVRO)
PLANO.md                   o laço, trilhas, portões
docs/VALIDACAO.md          a régua
docs/SISTEMAS.md           átomos, matriz de sincronia, sínteses Σ, Protocolo Σ
docs/ESCALA.md             protocolo Scalata (imaginação vertical ligada à régua)
docs/RSI.md                pesquisa RSI e o que adotamos (AIDE, AIDE², DGM, ...)
lab/registro.py            árvore, livro, meta-métricas, guarda por hash
lab/bussola.py             bússola: estado das habilidades, fronteira e prioridade
lab/checar.py              controle de qualidade (coerência entre todos os registros)
lab/sementes.py            sementes de teste derivadas do commit do PREREG
lab/baselines.py           Deep Thinking (progressive loss) e PonderNet reimplementados
lab/reproduzir.py          reprodução limpa a partir do commit do PREREG (decisão compilada)
lab/tarefas_clrs.py        BFS e Bellman-Ford no protocolo CLRS (n=16 → 64), resolvedores exatos
registro/obsoletos.txt     afirmações refutadas (não podem reaparecer sem riscar)
docs/STACK.md              teto do Python puro e gatilho para pedir outra stack
.claude/settings.json      gancho de início de sessão: roda lab.checar --resumo
lab/estat.py               estatística (IQM, bootstrap, Fisher, AURC, ECE, Pareto)
lab/test_estat.py          testes da régua
experimentos/_modelo/      modelo de PREREG.md e RELATORIO.md
experimentos/ENNN_nome/    PREREG.md, código, resultados.{md,json}, RELATORIO.md
.claude/skills/ciclo/      o comando /ciclo
```

## Persistência (a sessão pode ser compactada ou o contêiner reciclado)

- A memória do laboratório é o **repositório**, não a conversa. Tudo que importa (decisões, resultados, lições, estado, próximos passos) vive em arquivos versionados.
- **Commit + push a cada ciclo** (pré-registro e resultado), feitos pelo pesquisador como parte do laço, não por gancho automático. A sessão compacta sozinha em ~400k tokens (`autoCompactWindow` em `.claude/settings.json`); como tudo já está publicado a cada ciclo, nada se perde.
- Tudo é publicado; `.gitignore` só exclui `__pycache__/` (bytecode regenerável, sem informação). Arquivos > 20 MB vão para git-lfs (`lab.checar` avisa; > 90 MB é erro).
- Ao retomar após compactação: o gancho de início roda `lab.checar --resumo`; depois ler a ordem de "Leia sempre".

## Convenções

- Documentação em português. Código com identificadores e comentários em português, sem acentos nos `.py`.
- Experimentos numerados em sequência (`E004_...`). Cada um roda com um comando e aceita `--quick` para o smoke.
- Sementes: faixa própria por experimento, anotada no PREREG (E002: 200–229; E003: 300–309; teste = faixa + deslocamento fixo).
- Antes de commitar: `python3 -m unittest discover -s lab -t .` e `python3 -m lab.checar` (0 erros).
- Git: trabalhe no branch designado pela sessão; commits pequenos; o pré-registro vai num commit próprio **antes** dos resultados.
