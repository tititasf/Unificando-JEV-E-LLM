# E005 — Relatório: o motor S2 numa tarefa sem atrator (T2)

**Veredito: H1 MATAR** (a cristalização não era necessária) · **degrau S2 D05 ATINGIDO** pelo estado contínuo.
**Nível: N2** (pré-registrado, 10 sementes, reproduzido de checkout limpo, guarda OK). **Novidade: baixa** (replicação de extrapolação por iteração).
**Portão da Fase 1 formalmente atingido:** o passo latente iterado tem N2 em duas famílias de tarefas (T1: E002; T2: E005).

## Previsões

| # | Previsto | Prob. | Obtido | Status |
|---|---|---|---|---|
| P1 | CRIST ≥ 0,99 nas 20 células | 0,75 | 1,00 em todas | ✅ |
| P2 | CONT ≤ 0,50 em (128, 64) | 0,75 | 1,00 | 🟥 → H1 morta |
| P3 | CONT ≥ 0,95 em (12, 64) | 0,50 | 1,00 | ✅ |
| P4 | AFIA estritamente entre CONT e CRIST | 0,45 | todos 1,00 | 🟥 |
| P5 | SEM_ITER ≤ 0,10 para todo k ≥ 4 | 0,95 | até 0,37 em N=12 e 0,13 em N=32; ≤ 0,05 em N ≥ 64 | 🟥 |
| P6 | CRIST > CONT, p < 0,01 | 0,70 | P=0,50, p=1 | 🟥 |
| P7 | CONT (128, 16) ≤ 0,50 | 0,70 | 1,00 | 🟥 |

**Brier deste ciclo: 0,42** (acerto 2/7). As previsões com prob. alta erraram: o pesquisador estava **superconfiante** na teoria do acúmulo de erro.

**P5 e a validade.** Pelo critério pré-registrado, as células com N=12 e N=32 ficam **inválidas**: em permutações pequenas, ciclos curtos fazem π^k(s) = π(s) por acaso (é chance estrutural, não um atalho que explique 100%). As conclusões abaixo usam só **N=64 e N=128**, onde P5 vale (≤ 0,05). Essa restrição é pós-hoc e está declarada.

## Números principais (N ≥ 64; 10 sementes × 10 exemplos)

| braço | N=64, k=4…64 | N=128, k=4…64 | razão de extrapolação em k |
|---|---|---|---|
| SEM_ITER | 0,00–0,05 | 0,00–0,05 | — |
| CONT | 1,00 em todas | 1,00 em todas | 16× (k=64 vs treino k≤4), N 10× o treino |
| AFIA | 1,00 | 1,00 | 16× |
| CRIST | 1,00 | 1,00 | 16× |

Reprodução: execução do commit `f4dfd67` num worktree limpo gerou `resultados.json` **idêntico**.

## Diagnóstico pós-hoc: por que o contínuo não acumulou erro (`diagnostico.md`)

| | margem aprendida (pai − 2º) | máx z após 64 passos (N=128) | N* = e^margem | contínuo em N=256/512/1024, k=32 |
|---|---|---|---|---|
| T2 (4 sementes) | 9,2–10,8 | 0,995–0,999 | ~10⁴–5·10⁴ | 1,00 / 1,00 / 1,00 |
| T1, mesmas sementes | 4,3–6,7 | (dissolve em N=128, E004d) | ~70–800 | — |

1. **A softmax é um cristalizador suave.** Com o estado concentrado num nó, o passo seguinte volta a concentrar: o vazamento por passo ≈ (N−1)·e^(−margem) **não se acumula**, é reposto a cada passo. O estado fica estacionário em ~0,997.
2. **Lei candidata:** o regime difusivo (A9) aparece quando **N ≳ e^margem**. Em T2 (margem ~10) isso fica em ~20.000 nós; em T1 (margem ~4–7) fica entre ~70 e ~800, o que é compatível com a difusão vista em N=128 no E004. Unifica A4, A9 e E005 num só mecanismo. **N1 (4 sementes); precisa de teste pré-registrado.**
3. **Por que T1 aprende margem menor:** numa tarefa-atrator o erro se autocorrige, então o treino não cobra precisão. **A tarefa de treino decide a precisão do pensamento.**

## Revisor hostil

1. *"O 'contínuo' aqui não é contínuo de verdade: é uma distribuição sobre nós discretos."* Correto, e é a limitação mais importante. A teoria de acúmulo de ruído (2602.01148) fala de vetores latentes livres. Nosso estado já é quase simbólico. Testar Σ1 de verdade exige um latente vetorial livre (degrau D09 do S2). → H-latente-livre.
2. *"Os atributos de aresta entregam o algoritmo."* Sim: o teste é de precisão ao longo de muitos passos, não de descoberta. Declarado no PREREG.
3. *"P5 invalida o experimento."* Só nas células pequenas; as conclusões usam N ≥ 64, onde a linha de base é ≤ 0,05.

## Correções em registros anteriores
- A9 (E004d): o regime difusivo não é uma propriedade de "N grande", e sim de **N grande em relação a e^margem**. Anotado no ESTADO.
- A5 (E002) e E005 juntos: a cristalização não foi necessária em nenhuma das duas famílias, **com este tipo de estado latente**.

## Hipóteses semeadas
- **H-lei-margem** (promover A9 → N2): prever, para cada semente de T1, o N em que o regime muda (N* = e^margem) e testar N ∈ {N*/4, N*, 4N*}. Previsão quantitativa forte e barata.
- **H-latente-livre** (S2 D09, Σ1 de verdade): substituir a distribuição sobre nós por um vetor latente livre de dimensão d. Aí o acúmulo de ruído deve aparecer, e a cristalização (quantização) deve voltar a importar.
- **H-precisão-treino:** treinar em T1 com uma penalidade de margem, ou misturando T2, elimina o regime difusivo em T1?
