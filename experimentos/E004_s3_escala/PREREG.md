# E004 — Pré-registro: metacognição invariante à escala (S3, degrau D03→D04)

**Escrito antes de rodar. Não editar depois da primeira execução completa.**
Trilha B. Átomos: 3.1, 3.2. Alvo: degrau **D04** do tema S3 (`EVOLUTION_LOG.md`, ciclo 4).
Nível de partida: D03 (E001, N1). Barreira: A4 (E002).

## Hipótese
O sinal "terminei" baseado na **estabilidade da decisão** (argmax parado por
3 passos + estado quase parado) funciona sem reajuste de N=12 a N=128:
responde quando o orçamento basta e se abstém quando não basta. Sinais
baseados em **nitidez** (máximo absoluto, entropia normalizada) não escalam.

## Relação com a literatura
FPRM (*Fixed-Point Reasoning*, ICML 2026) usa convergência a ponto fixo
para parar, e relata traços com oscilações período-2 como caso difícil.
PonderNet/ACT aprendem a parada. O que aqui é diferente: (a) medir a
**transferência de limiares fixados numa escala** para escalas 10× maiores;
(b) exigir **abstenção** quando o orçamento é insuficiente. Novidade esperada: baixa a média.

## Montagem
- Tarefa T1 (achar a raiz), treino idêntico ao E001 (N=12, d≤4, 600 iterações). Sementes 400–409 (**10**).
- Teste congelado: sementes 60000+s. N ∈ {12, 32, 64, 128}; d ∈ {⌊N/2⌋−2, N−5}; 10 exemplos por (N, d, condição).
  - **DENTRO** do orçamento: T = d+6 (dá para chegar à raiz e ver estabilidade).
  - **FORA** do orçamento: T = max(1, d−3) (impossível chegar à raiz → deve se abster).
- Todos os braços leem **a mesma trajetória** z₁…z_T; param no primeiro t que satisfaz a regra; se nenhum t satisfaz, abstêm-se.
- Limiares fixados **a priori**, sem ajuste:

| Braço | Regra de parada | Papel |
|---|---|---|
| SEMPRE | nunca se abstém; responde argmax(z_T) | sem S3 (D01) |
| ABS | máx z ≥ 0,9 e ‖z_t − z_{t−1}‖₁ < 0,02 | E001 (D03) |
| CONV | ‖z_t − z_{t−1}‖₁ < 0,02 | publicado mais próximo (ponto fixo, estilo FPRM) |
| ENT | H(z)/log N ≤ 0,5 e ‖Δz‖₁ < 0,02 | nitidez normalizada |
| UNIF | N · máx z ≥ 2 e ‖Δz‖₁ < 0,02 | razão sobre o uniforme |
| ESTAVEL | argmax igual nos últimos 3 passos e ‖Δz‖₁ < 0,02 | **proposto** |
| ESTAVEL_PURO | argmax igual nos últimos 3 passos | ablação (sem condição de estado parado) |

## Métricas
- cobertura DENTRO (fração respondida), abstenção FORA, acurácia seletiva (acertos ÷ respondidas, nas duas condições), erros absolutos.
- **placar** = (acertos DENTRO + abstenções FORA) ÷ total. Máximo 1,0.
- Por semente; agregado com IQM + IC95%; comparação ESTAVEL × ABS em N=128 por P(A>B) e permutação.

## Previsões e critérios de morte
| # | Previsão | Morte se |
|---|---|---|
| P1 | ABS: cobertura DENTRO em N=128 ≤ 10% (replica A4) | > 50% → A4 não se replica; rever E002 |
| P2 | **ESTAVEL: em todo N, cobertura DENTRO ≥ 99%, abstenção FORA ≥ 99%, acurácia seletiva ≥ 99,5%** | algum N com cobertura < 95% **ou** abstenção < 95% **ou** acc. seletiva < 99% → **H morta** |
| P3 | ENT: cobertura DENTRO em N=128 < 50% | ≥ 95% → "nitidez normalizada" também escala; hipótese do mecanismo errada |
| P4 | UNIF passa (≥ 95% nos três critérios) em todo N, com folga pequena | — (informativa) |
| P5 | ESTAVEL_PURO ≈ ESTAVEL (±1 ponto no placar) | — (se pior, a condição de estado parado é necessária) |
| P6 | CONV: abstenção FORA < 90% em algum N (convergência pura se engana com estados que andam devagar) | — (informativa; se CONV = ESTAVEL, o proposto não acrescenta nada ao publicado) |
| P7 | placar ESTAVEL > ABS em N=128 com P(A>B) = 1 e p < 0,01 | p ≥ 0,01 → inconclusivo |

## Ameaças conhecidas
- Tarefa-atrator (A7): a condição FORA ainda testa abstenção de verdade (a raiz não é alcançável), mas a trajetória DENTRO é "fácil" de estabilizar. Repetir em T2 quando existir.
- Os limiares a priori podem favorecer um braço por sorte. Mitigação: valores redondos, escolhidos antes, e a análise pós-hoc de sensibilidade (sem mudar o veredito).
- Não testa parada aprendida (PonderNet): fica como limitação declarada.
