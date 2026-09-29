# E010 — Pré-registro: memória de trabalho latente (o próprio pensamento conta os saltos)

**Escrito antes de rodar o teste. Não editar depois da primeira execução completa.**
Trilha A. Átomos: 2.1, 2.2. Nível de partida: S2 em D05 (E005: o controlador contava os passos).
Habilidade-alvo: **H06** (topo da bússola, prioridade 9,5; abre 9 habilidades e G1, G3, G4). Nó pai: **E005**. Operador: **RASCUNHO**.

## Hipótese
H1: um estado sobre pares (nó, contador), atualizado por **um único passo aprendido** a partir
de atributos do par, aprende a "andar enquanto o contador > 0 e parar no zero", sem que isso
esteja codificado. Treinado com N=8 e k ≤ 4, resolve T2 com **k só na entrada** (o controlador
roda sempre 72 passos e não sabe k) até k=64 (16×) e N=64 (8×).
H2 (piloto): a parada **emerge da fronteira do registro**: no contador 0 não existe a transição
"decrementar", então as marcas explícitas "a = 0 / b = 0" são desnecessárias.

## Relação com a literatura
Memória externa/registradores em redes neurais (NTM, DNC, Neural GPU, máquinas de pilha
diferenciáveis) e contadores em RNNs (LSTMs aprendem a contar; Weiss et al. 2018). O que
difere: um único passo sobre o produto (lugar × contador), com atributos relacionais
invariantes a tamanho, extrapolando 16× em k e 8× em N sem re-treino. Novidade esperada: baixa.

## Piloto (declarado)
Sementes 1090, 1091 (fora da faixa), 6 exemplos por célula: MEMORIA 1,0 em (8,4), (8,16),
(32,16), (64,64); SEM_MARCAS 1,0 em quase tudo (0,83 numa célula). Por isso H2 e as
probabilidades abaixo.

## Montagem
- Tarefa T2 (permutação, todo erro é fatal), k na entrada como posição inicial do contador.
- Treino do motor: N=8, K=4, k ∈ 1..4, T=8, supervisão em (alvo, contador 0) de t=k até t=8 (tem de chegar **e** ficar); 400 iterações de Adam com BPTT denso. Sementes de treino **1000–1009** (10).
- Teste: contador de tamanho 64 (k em one-hot), **72 passos fixos** para todos os k; N ∈ {8, 32, 64}, k ∈ {4, 16, 64}; 15 exemplos por célula; passo estruturado O(N·K), verificado contra o denso (erro < 1e−16). Sementes de teste derivadas do commit deste PREREG.
- Braços: **MEMORIA** (proposto); **SEM_MARCAS** (ablação: sem os atributos a=0, b=0); **SEM_MEMORIA** (só o ponteiro do E005, 72 passos: a linha de base recorrente sem memória, estilo Deep Thinking); **CONTROLADOR** (ponteiro com o controlador contando k: limite superior "trapaceiro").

## Sementes e poder
- 10 sementes × 15 exemplos = 150 por célula e braço. Custo estimado: ~16 min de CPU.

## Previsões
| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1 | MEMORIA: IQM ≥ 0,95 em todas as 9 células | 0,75 | alguma célula < 0,90 → **H1 morta** |
| P2 | MEMORIA em (64, 64): 0 colapsos em 10 sementes | 0,75 | ≥ 3 colapsos → H1 morta |
| P3 (H2) | SEM_MARCAS: IQM ≥ 0,95 em (64, 64) | 0,70 | — (se falhar, as marcas eram necessárias) |
| P4 | SEM_MEMORIA em (64, 64): IQM ≤ 0,10 | 0,90 | > 0,10 → a tarefa tem atalho; experimento inválido |
| P5 | CONTROLADOR em (64, 64): IQM ≥ 0,95 | 0,90 | — |

**H06 desbloqueada** se P1, P2 e P4 passam (N2).

## Guarda do avaliador
```
experimentos/E010_memoria/e010.py           : 1a9071a42b4de23d
experimentos/E010_memoria/memoria.py        : 988b14c875cd8c84
experimentos/E005_t2_salto/tarefa_t2.py     : b62e43a6a77ab648
lab/baselines.py                            : b93abd354fc2b361
experimentos/E001_mlu/mlu.py                : 601604873fae9691
lab/sementes.py                             : 4a5e4da1269f9b77
```

## Ameaças conhecidas
- Os atributos "decrementa / mantém" são dados. O que se aprende é **o que fazer** com eles (quando avançar, quando parar), não a noção de contagem. Declarado: é memória de trabalho **estruturada**.
- A nitidez: o espaço de pares tem N·(K+1) = 4160 estados em (64, 64). Pela lei de nitidez, isso só funciona se a margem aprendida vencer ~log(4160). O piloto sugere que vence.
- N=8 no treino e no teste com k grande: ciclos curtos podem fazer SEM_MEMORIA acertar por acaso em N=8 (como a P5 do E005). P4 usa só N=64.
