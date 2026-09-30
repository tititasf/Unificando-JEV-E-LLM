# Piloto do ciclo 17 (M009): a H24 no caminho mínimo (N0, diagnóstico)

Pergunta: em Bellman-Ford, onde verificar distâncias custa O(E) (certificado d_v ≤ d_u + w em toda aresta), um S1 barato mais a corte do S3 barateiam o S2?
Script: `piloto_h24.py` (sementes 5 e 6; 10 grafos por célula). Custo medido em relaxações de aresta.

## 1. Certificado global (tudo ou nada)
- S1 = estimativa de 2 saltos (d̂_v = min(w_sv, min_u w_su + w_uv)).
- Certificado aceito: **0/60 grafos**, tanto em ER p = 0,5 (n = 16, 64, 256) quanto na grade (4², 8², 16²).
- Custo relativo ao Jacobi: 0,72–1,04. O chute nunca se paga.

## 2. Reparo localizado (o S3 aponta as violações; o S2 corrige a partir delas, com lista de trabalho)
| família | n | S1: acerto por nó | Jacobi / composto | SPFA frio / composto |
|---|---|---|---|---|
| ER | 16 | 0,67 | 1,82 | 0,88 |
| ER | 64 | 0,30 | 2,40 | 0,87 |
| ER | 256 | 0,16 | 2,93 | 0,89 |
| grade | 4² | 0,77 | 2,09 | 0,72 |
| grade | 8² | 0,72 | 4,00 | 0,66 |
| grade | 16² | 0,68 | 5,40 | 0,56 |

Leitura:
- O ganho contra o Jacobi vem da **lista de trabalho**, e não do S1: o SPFA frio é mais barato que o composto em todas as células.
- Verificar custa Ω(E), e o resolvedor clássico já é quase linear, então não sobra o que amortizar. A razão possível é no máximo (custo do S2)/E.

## Conclusão
A H24 não cabe no caminho mínimo. Ela precisa de uma família em que resolver custe muito mais que verificar: busca (SAT, quebra-cabeças, planejamento). Lá o S1 entra como heurística de ordenação e o S3 como verificador O(tamanho). Fica semeada como **H-busca-cert**.
