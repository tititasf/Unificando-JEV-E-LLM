# E011 — Pré-registro: modelo de mundo com o mesmo passo (S6)

**Escrito antes de rodar o teste. Não editar depois da primeira execução completa.**
Trilha E (primeiro nó de S6). Átomos: 6.1. Nível de partida: nenhum nó em S6.
Habilidade-alvo: **H16** (na fronteira desde que H06 foi desbloqueada). Nó pai: **E010**. Operador: **RASCUNHO**.
Escolha pela política: regra 7 (diversidade: um sistema sem nós a cada 5 ciclos, adiada desde o ciclo 10 porque S0/S4/S6 não estavam na fronteira). A bússola punha H12 em primeiro, mas H12 não tem ainda tarefa com verificador O(1) (verificar custa o mesmo que resolver); registrado como pendência.

## Hipótese
H1: o mesmo tipo de passo relacional do S2, sobre o estado-produto (posição × velocidade),
aprende a física de uma partícula numa caixa com paredes (movimento + rebote) a partir de
trajetórias, e prevê trajetórias de 16 passos com erro < 1% por passo em caixas 8× maiores
que a do treino.
H2 (fronteira geométrica, E010): o rebote precisa só de um atributo local ("distância à
parede à frente"); sem ele o modelo não tem como antecipar o rebote e erra.

## Relação com a literatura
Simuladores físicos relacionais que extrapolam para domínios maiores (Interaction Networks,
Battaglia et al. 2016; Graph Network Simulators, Sanchez-Gonzalez et al. 2020). Este é o
princípio em miniatura, com o mesmo passo usado no raciocínio (S2). Novidade: baixa.
Não há reimplementação da linha de base publicada; as linhas de base são as mais simples
(persistência e física ingênua sem paredes) e a ablação.

## Piloto (declarado)
Sementes 1190, 1191 (fora da faixa), 10 trajetórias por L: MUNDO 0 erros em L = 8, 32, 64;
SEM_PAREDE 10–20% de erro por passo; SEM_REBOTE ~85% em L=8 e 12–26% em L=64.

## Montagem
- Mundo: x ∈ 0..L−1, v ∈ {−2, −1, +1, +2}; paredes refletem. Estado inicial aleatório.
- Treino: L = 8, trajetórias de 8 passos supervisionadas em todo t, 400 iterações (BPTT denso). Sementes **1100–1109** (10).
- Teste: L ∈ {8, 32, 64}, 25 trajetórias de 16 passos por L; sementes de teste derivadas do commit deste PREREG.
- Braços: **MUNDO** (proposto), **SEM_PAREDE** (ablação: sem a distância à parede), **PERSISTENCIA** (nada muda), **SEM_REBOTE** (x' = x + v saturando na borda, sem inverter v).
- Métricas: erro por passo (fração de passos com estado previsto ≠ verdadeiro) e fração de trajetórias 100% certas; IQM + IC95% entre sementes.

## Sementes e poder
- 10 sementes × 25 trajetórias × 16 passos = 4.000 passos por (braço, L). Custo estimado: ~10 min.

## Previsões
| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1 | MUNDO: erro por passo < 1% em L = 8, 32 e 64 | 0,80 | ≥ 5% em algum L → **H1 morta** |
| P2 | MUNDO: trajetórias 100% certas em L=64, IQM ≥ 0,95 | 0,80 | < 0,80 → H1 morta |
| P3 | SEM_PAREDE: erro por passo em L=64 > 5%, e MUNDO melhor com p < 0,01 | 0,80 | ≤ 1% → H2 morta (a parede não era necessária) |
| P4 | SEM_REBOTE: erro por passo em L=8 > 30% (a tarefa exige o rebote) | 0,90 | ≤ 10% → tarefa trivial; experimento inválido |

**H16 desbloqueada** se P1, P2 e P4 passam (N2).

## Guarda do avaliador
```
experimentos/E011_mundo/e011.py     : 3a5b6d17118d82ef
experimentos/E011_mundo/mundo.py    : 56e0d383e27e5e5f
lab/baselines.py                    : b93abd354fc2b361
experimentos/E001_mlu/mlu.py        : 601604873fae9691
lab/sementes.py                     : 4a5e4da1269f9b77
```

## Ameaças conhecidas
- Os atributos (dx, relação de velocidade, distância à parede à frente) são escolhidos a dedo; o que se aprende é a regra que os combina. Declarado.
- Mundo determinístico e 1D: não testa incerteza nem interações entre objetos (degraus seguintes).
- 16 passos de horizonte; o critério da H16 é esse.
