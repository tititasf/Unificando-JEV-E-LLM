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

1. `ESTADO.md` — onde estamos, fila de hipóteses, placar dos átomos.
2. Fim do `DIARIO.md` — o que o último ciclo aprendeu.
3. `docs/VALIDACAO.md` — a régua (escada N0–N5, métricas, regras contra o autoengano).
4. `docs/SISTEMAS.md` — os átomos de cada sistema, a matriz de sincronia e as sínteses Σ.
5. `PLANO.md` — o laço, as trilhas e os portões.

## O laço (um ciclo por sessão, no mínimo)

Execute `/ciclo` ou siga `PLANO.md §1`:
LER → ESCOLHER → CHECAR NOVIDADE → PRÉ-REGISTRAR (commit antes de rodar) →
CONSTRUIR → RODAR (smoke → completo) → MEDIR → ATACAR → DECIDIR → SEMEAR →
REGISTRAR → commit → push. Se sobrar tempo, comece outro ciclo.

## Regras invioláveis

1. **Pré-registro commitado antes do teste.** `PREREG.md` com hipótese, previsões numéricas e critério de morte. Nunca editar depois de ver os dados; se precisar, é um novo experimento.
2. **Toda comparação passa por `lab/estat.py`**: IQM + IC95%, taxa de colapso, P(A>B), p de permutação ou Fisher. Nada de "parece melhor".
3. **Mínimo de sementes:** smoke ≥2 (não vale como resultado); N1 ≥5; N2 ≥10 (≥30 para taxas de colapso).
4. **Linhas de base e ablações** em todo experimento: a mais simples, a publicada mais próxima e o próprio método sem a peça nova.
5. **Resultados negativos têm o mesmo destaque que os positivos.** Hipótese morta é progresso. Corrija os registros antigos quando um novo resultado os contradisser (como o E002 fez com o E001).
6. **Nunca diga "revolucionário", "novo" ou "descoberta"** sem o nível exigido em `docs/VALIDACAO.md §1` e sem checagem de novidade na literatura. Diga o nível: "N1, replicação de X".
7. **Procure o atalho trivial** antes de celebrar (no E001, com uma só raiz, bastava achar o nó que aponta para si).
8. **Não confunda metáfora com mecanismo.** Os sistemas 5–7 nasceram como metáforas; aqui só entram como átomos testáveis.

## Ambiente e restrições

- **Python 3 puro, só biblioteca padrão.** O usuário recusou `pip install` (numpy/torch). Não instale nada sem pedir. Use `multiprocessing` para paralelizar (4 CPUs).
- Ciclo típico: < 30 min de CPU. Experimento que não cabe → quebre-o.
- Quando uma trilha atingir T4+ e o Python puro virar o gargalo, **pergunte** ao usuário antes de mudar de stack.
- Experimentos de S0 (autopreservação, orçamento) são **simulações fechadas**: agentes de brinquedo dentro de um script. Nada de ação real no mundo, aquisição de recursos, rede ou persistência fora do repositório.

## Estrutura

```
CLAUDE.md                  este arquivo
ESTADO.md                  estado vivo: fila, placar, portões
DIARIO.md                  um registro por ciclo (mais recente embaixo)
PLANO.md                   o laço, trilhas, portões
docs/VALIDACAO.md          a régua
docs/SISTEMAS.md           átomos, matriz de sincronia, sínteses Σ, Protocolo Σ
lab/estat.py               estatística (IQM, bootstrap, Fisher, AURC, ECE, Pareto)
lab/test_estat.py          testes da régua
experimentos/_modelo/      modelo de PREREG.md e RELATORIO.md
experimentos/ENNN_nome/    PREREG.md, código, resultados.{md,json}, RELATORIO.md
.claude/skills/ciclo/      o comando /ciclo
```

## Convenções

- Documentação em português. Código com identificadores e comentários em português, sem acentos nos `.py`.
- Experimentos numerados em sequência (`E004_...`). Cada um roda com um comando e aceita `--quick` para o smoke.
- Sementes: faixa própria por experimento, anotada no PREREG (E002: 200–229; E003: 300–309; teste = faixa + deslocamento fixo).
- Antes de commitar: `python3 -m unittest lab.test_estat`.
- Git: trabalhe no branch designado pela sessão; commits pequenos; o pré-registro vai num commit próprio **antes** dos resultados.
