# Piloto do ciclo 13: um S3 seletivo sobre o JEV transfere entre escalas? (N0, diagnóstico)

Objetivo: decidir se vale pré-registrar a H-JEV-seletivo (→ H08: risco seletivo garantido sob mudança de escala).
Dados: os saltos gravados no E012 (`../respostas_jev.jsonl`, 2.488 chamadas de um salto) e 150 chamadas `Noul` novas (`piloto_noul.py`, respostas não gravadas; só resumo abaixo).

## 1. Limiar na confiança do `Choice` (dados do E012)
Limiar escolhido em T2 N=8 para risco empírico ≤ 2%, aplicado sem reajuste:

| escore | T2 N=8 | T2 N=32 | T2 N=64 | T1 N=8 | T1 N=32 | T1 N=64 |
|---|---|---|---|---|---|---|
| p(escolha) | 0,026 | 0,050 | **0,113** | 0,059 | 0,076 | 0,078 |
| margem p1−p2 | 0,019 | 0,069 | **0,159** | 0,061 | 0,086 | 0,132 |
| razão p1/p2 | 0,019 | 0,093 | **0,201** | 0,062 | 0,113 | 0,167 |
| 1 − H/log N | 0,020 | 0,098 | **0,246** | 0,057 | 0,133 | 0,185 |
| `confidence` | 0,021 | 0,061 | **0,153** | 0,056 | 0,084 | 0,093 |

(risco seletivo por salto). Nenhum escore transfere: o risco sobe 4–12× de N=8 para N=64, e a cobertura cai (p ≥ 0,9: 0,57 → 0,06).

## 2. Verificação por `Noul` ("ponteiros[no] == candidato?"), 25 saltos certos + 25 errados por N
- Separação fraca: média 0,42–0,45 nos certos, 0,22–0,31 nos errados; nenhum certo passa de 0,9.
- λ = 0,5 aceita 0/25 errados em N=8 e 32, mas **5/25 em N=64**, com só ~9/25 certos aceitos.

## Conclusão
Nesta interface, nenhum sinal do JEV sustenta um limiar que transfira de N=8 para N=64: é a mesma lacuna do E004 (limiares não transferem entre escalas), agora num S1 externo. A H-JEV-seletivo **não** foi pré-registrada; fica como hipótese que precisa de um sinal novo (ex.: calibração Mondrian por escala com poucos rótulos, ou temperatura adaptativa, H05).

---

# Piloto do ciclo 16 (M008): o escore da lei de nitidez transfere? (N0, diagnóstico)
Script: `piloto_m008.py` (só os dados gravados do E012; nenhuma chamada nova).
Ideia: se a lei do S2 (E007/E013) valesse para o S1 externo, a margem m = ln(p₁(N−1)/(1−p₁)) seria invariante em N e um limiar nela transferiria.

| escore | limiar (T2 N=8, risco ≤ 2%) | T2 N=32 | T2 N=64 | T1 N=8 | T1 N=32 | T1 N=64 |
|---|---|---|---|---|---|---|
| p₁ (= logit) | 0,66 | 0,048 (cob 0,70) | 0,111 (0,46) | 0,056 | 0,073 | 0,076 |
| m (lei) | 2,61 | **0,149** (0,99) | **0,283** (1,00) | 0,056 | 0,178 | 0,285 |

A correção por ln(N−1) **piora**: o JEV não fica menos nítido com N; os erros em N grande são confiantes. A lei de nitidez descreve o S2 interno, não o S1 externo. H08 continua sem sinal que transfira.
