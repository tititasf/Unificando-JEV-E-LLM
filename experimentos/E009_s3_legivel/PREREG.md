# E009 — Pré-registro: S3 em dois tempos (metacognição legível em qualquer escala)

**Escrito antes de rodar o teste. Não editar depois da primeira execução completa.**
Trilha B. Átomos: 3.1, 3.2. Nível de partida: S3 em D03 (E001); falha de escala A4/A8 (E002, E004).
Habilidade-alvo: **H07** (topo da bússola, prioridade 14). Nó pai: **E004**. Operador: **MELHORAR** (acrescenta a leitura do regime pela lei de nitidez).

## Hipótese
H1: um S3 que (1) **antes de pensar** compara o vazamento do primeiro passo da instância
com o ε_c(m) da teoria de campo médio (E007d), e (2) **durante** para por ponto fixo,
responde quando o pensamento é legível e o orçamento basta, se abstém quando o orçamento
não basta, e **nunca responde errado** quando o pensamento está dissolvido, de N=12 a N=1024,
sem nenhum ajuste por escala.
H2 (reinterpretação do A4): no regime dissolvido o S2 acerta só por sorte (~50%); abster-se
ali é correto. Portanto o limiar absoluto (ABS) do E001 também pode passar quando o critério
é "não errar", e o ganho do tempo 1 é **custo**, não acerto.

## Relação com a literatura
Predição seletiva e parada adaptativa (PonderNet; FPRM usa ponto fixo). A peça que falta
na literatura que conheço: **prever, a partir de um passo, se a dinâmica iterada vai se
manter legível** (lei de nitidez + teoria de Hopfield), e abster-se antes de gastar o
pensamento. Novidade esperada: baixa a média.

## Piloto (declarado)
Sementes 990, 991 (fora da faixa), 15 exemplos por célula. DOIS_TEMPOS: cobertura 0,99,
abstenção fora do orçamento 1,00, 0/90 erros no regime dissolvido. SEMPRE/CONV/PONDER:
42/90 erros no regime dissolvido. ABS: cobertura 1,00, 0/90 erros. Foi o piloto que
mostrou H2 e mudou a métrica do regime dissolvido para "erros" (o G2 exige zero erros
confiantes, não abstenção a qualquer custo) e acrescentou o custo em passos.

## Montagem
- Motor: T1, treino idêntico ao E001. Sementes de treino **900–909** (10).
- Por modelo: margem efetiva m (vazamento em N=30), ε_c(m) pela teoria (E007d), N̂ = N com ε(N) = ε_c(m).
- Condições (d sorteado; T definido):
  - **DENTRO**: N ∈ {12, 24, N̂/2, N̂/1,5} ∩ [12, N̂/1,5]; T = d+6 → deve responder certo.
  - **FORA_ORC**: mesmos N; d ≥ 4; T = d−3 → deve se abster.
  - **FORA_REG**: N ∈ {⌈1,5 N̂⌉, 3N̂, 1024} ∩ [1,5 N̂, 1024]; T = d+6 → não pode responder errado.
  - A zona N̂/1,5 < N < 1,5N̂ fica de fora (fronteira da transição), declarado.
- Braços: **SEMPRE** (sem S3), **ABS** (E001), **CONV** (só o tempo 2; ponto fixo publicado), **SO_ANTES** (ablação: só o tempo 1), **PONDER** (PonderNet, `lab/baselines.py`, treinada em N=12), **DOIS_TEMPOS** (proposto).
- Sementes de teste derivadas do commit deste PREREG; **20 exemplos por célula**.

## Sementes e poder
- ~80–160 instâncias por condição por braço (10 sementes × 2–4 N × 20). Com 0 erros em 150, o IC95% de Wilson da taxa de erro fica em [0; ~0,025].
- Custo estimado: ~5 min de CPU.

## Previsões
| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1 | DOIS_TEMPOS: cobertura DENTRO ≥ 0,99 e acurácia seletiva ≥ 0,995 | 0,55 | cobertura < 0,95 → **H1 morta** |
| P2 | DOIS_TEMPOS: abstenção FORA_ORC ≥ 0,99 | 0,85 | < 0,95 → H1 morta |
| P3 | DOIS_TEMPOS: erros em FORA_REG ≤ 1% das instâncias | 0,80 | > 5% → H1 morta |
| P4 | CONV: erros em FORA_REG ≥ 20% | 0,80 | — |
| P5 | PONDER: erros em FORA_REG ≥ 20% | 0,80 | — |
| P6 | SO_ANTES: abstenção FORA_ORC < 0,50 (o tempo 2 é necessário) | 0,90 | — |
| P7 (H2) | ABS também cumpre P1–P3 | 0,60 | — |
| P8 | passos em FORA_REG: DOIS_TEMPOS ≤ 0,10 × ABS | 0,85 | — |

**H07 desbloqueada** se P1, P2 e P3 passam (N2). Se P7 também passar, o registro diz com todas as letras: o que resolve a escala é tratar o regime dissolvido como "não sei"; o tempo 1 acrescenta custo menor, não acerto.

## Guarda do avaliador
```
experimentos/E009_s3_legivel/e009.py          : 2d7694f89eae8102
experimentos/E007_lei_eps/diagnostico.py      : 25bbd568f306c2dd
experimentos/E006_lei_margem/passo_rapido.py  : 3aa24574de9b4029
lab/baselines.py                              : b93abd354fc2b361
experimentos/E001_mlu/mlu.py                  : 601604873fae9691
lab/sementes.py                               : 4a5e4da1269f9b77
```

## Ameaças conhecidas
- A zona de transição (N̂/1,5 a 1,5N̂) é excluída: o teste não diz como o S3 se sai exatamente na fronteira.
- T1 continua sendo uma tarefa-atrator; FORA_REG com d grande tem "sorte de atrator", e por isso a métrica é erro, não abstenção.
- O critério de H07 fala em "se abstém ≥ 99% quando não dá"; aqui, no regime dissolvido, "não dá" é operacionalizado como "não responder errado". Declarado.
