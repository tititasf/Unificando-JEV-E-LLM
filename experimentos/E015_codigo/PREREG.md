# E015 — Pré-registro: código mínimo corretor (quantas dimensões um código precisa para ter a robustez do one-hot)

**Escrito antes de rodar. Não editar depois da primeira execução completa.**
Trilha: C (S5). Átomos: 5.3/5.4 (código discreto, bits × robustez). Nível de partida: N2 do A6 (E003: mensagem simbólica one-hot robusta).
Habilidade-alvo: **H13** (fronteira da bússola, S5 D05). Nó pai: **E003** · Operador: **MELHORAR**. Degrau-alvo: S5 D05.
Escolha: a regra de diversidade manda. O S5 está parado há 11 ciclos, e a H13 é a habilidade da fronteira dele. H24, H08 e H23 seguem na frente em prioridade (ver ciclo 14 sobre a H24).

## Hipótese
O one-hot do E003 gasta N dimensões por mensagem. Um código **aprendido** por SGD através do canal ruidoso:
- **canal E** (energia fixa por mensagem, que é o canal do E003):
  - com L = N−1, supera o one-hot (o simplex);
  - com L = N/2, empata com ele (limite de Rankin: mais de 2L pontos numa esfera de L dimensões não ficam todos a 90° ou mais);
  - com L = N/4, perde;
- **canal P** (amplitude ≤ 1 por dimensão, canais que saturam): com L = N/4 dimensões erra ≤ metade do one-hot.

## Pilotos (declarados; sementes 1590–1591)
- **N = 16, σ = 0,3:**
  - one-hot 0,079; biortogonal 0,080;
  - aprendido L = 8: 0,080 (razão 1,01); aprendido L = 15: 0,069 (0,87);
  - aprendido L = 4 (0,157) vence o binário feito à mão (0,177).
- **N = 32:** aprendido L = 16 → razão 1,03–1,07; L = 31 → 0,96–0,99.
- **Smoke do avaliador** (N = 16, 1000 iterações): L = 15 dá razão 0,93 e 1,00; simplex à mão 0,92 e 0,93.
- **Bugs do smoke, corrigidos antes deste commit:** sinal do gradiente trocado; dimensões duplicadas quando N/4 = log₂N.

## Relação com a literatura
- Sinalização ortogonal, biortogonal e simplex (teoria clássica de comunicação digital, p. ex. Proakis): o simplex é o ótimo de energia para N sinais equiprováveis; o biortogonal usa N/2 dimensões com a mesma distância mínima do ortogonal.
- Limite de Rankin para códigos esféricos.
- Autoencoders de canal aprendidos (O'Shea & Hoydis 2017, "An introduction to deep learning for the physical layer") aprendem códigos que igualam ou superam códigos clássicos.
- **Novidade: nenhuma** (replicação do resultado clássico com códigos aprendidos). O valor é interno: dá ao S5 o degrau "código mínimo" com a curva bits × robustez medida e com o limite teórico explícito.

## Montagem
- **Canal:** um de N símbolos por L canais, ruído N(0, σ²) por canal; decodificação por máxima verossimilhança (código mais próximo).
- **Tamanhos e ruído:** N ∈ {16, 32}; σ ∈ {0,3; 0,4}; treino com σ = 0,4, 4000 iterações, lote 32.
- **Braços:**
  - ONEHOT (L = N; idêntico nos dois canais);
  - SIMPLEX (L = N−1, referência teórica);
  - BIORT (L = N/2);
  - BIN_E e BIN_P (binário feito à mão, L = log₂N);
  - APREND_{canal}_{L}: canal E com L ∈ {log₂N, N/4, N/2, N−1}; canal P com L ∈ {log₂N, N/4, N/2};
  - ALEAT_{canal}_{L} (código sorteado; ablação do aprendizado).
- **Sementes:** treino 1500–1509. Sementes de teste (ruído e símbolos) derivadas do commit deste PREREG. 10.000 símbolos por (semente, código, σ).

## Previsões e critérios de morte
| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1 | Canal E: APREND com L = N−1 tem erro IQM < ONEHOT em todo N e σ | 0,45 | — |
| P2 | Canal E: APREND com L = N/2 empata (razão IQM em [0,9; 1,15]) e com L = N/4 perde (razão > 1,2), em todo N e σ | 0,65 | L = N/4 com razão ≤ 1,0 → o limite de Rankin não descreve o aprendido |
| P3 | Canal P: APREND com L = N/4 erra ≤ 0,5 × ONEHOT em todo N e σ | 0,85 | razão > 1 → **H morta no canal P** |
| P4 | APREND < ALEAT em ≥ 90% das sementes, em todas as células | 0,90 | — |
| P5 | Canal E: APREND com L = log₂N < BIN_E em todo N e σ | 0,60 | — |

**H13 desbloqueada** (N2) se P3 **e** P1 passam: menos dimensões que o one-hot com robustez ≥ nos dois canais. Registro a ressalva de que no canal de energia a economia é de só 1 dimensão, e que o empate vai até N/2.

## Sementes e poder
- 10 sementes (N2). Com 10.000 símbolos, o erro padrão por semente é ≤ 0,005 com erro ≈ 0,25. `n_para_largura(0,1; 0,01)` = 3458 < 10.000.
- Custo estimado: ~3 min de CPU por semente (N = 32 domina) → ~8 min de parede com 4 processos (~30 min de CPU no total, no teto).

## Guarda do avaliador
```
experimentos/E015_codigo/e015.py : 4a03b293de5d4f64
lab/sementes.py                  : 4a5e4da1269f9b77
lab/estat.py                     : 40af21b3e5c3d582
```

## Ameaças conhecidas
- **Qual canal é o "justo".** No canal P, o ganho vem de os códigos densos usarem mais energia total. Por isso os dois canais são reportados, e o do E003 é o E.
- **O que este teste NÃO mostra:** código que emerge entre agentes numa tarefa (H14). Aqui o código é aprendido por um único par emissor–receptor com o objetivo explícito de decodificar.
