# E013 — Pré-registro: temperatura derivada da lei de nitidez (nitidez em qualquer escala)

**Escrito antes de rodar. Não editar depois da primeira execução completa.**
Trilha: A (S2). Átomos: 2.1, 2.3. Nível de partida: N2 da lei de nitidez (E007).
Habilidade-alvo: **H05** (topo da bússola). Nó pai: **E007** · Operador: **MELHORAR**. Degrau-alvo: S2 (H05 não é degrau novo da escada S2; fecha a pendência de D04).

## Hipótese
Um único número medido sem rótulos, a margem efetiva m do passo treinado em N = 12, define uma temperatura
β(N) = 1 + ln((N−1)/11)/m que mantém o vazamento de um passo **igual** ao do tamanho de treino
(ε(N) ≈ ε(12)), e portanto abaixo de ε_c(m), até N = 4096 sem re-treino, em T1 e T2.

## Relação com a literatura
- **Scalable-Softmax** (Nakanishi 2025): multiplica os logits por s·log n; a escala log n é necessária para manter a nitidez (análise concorrente).
- **Veličković et al.** (ICML 2025): temperatura adaptativa aprendida.
- **ASEntmax** (arXiv 2506.16640): entmax com temperatura aprendida, extrapolação de até 1000×.

O que difere: nossa β(N) tem a mesma forma afim em log N, mas o coeficiente vem da margem medida (1/m), sem parâmetro aprendido, e a previsão é quantitativa: o vazamento fica **constante** (não só "nítido o bastante"). **Novidade: baixa.**

## Pilotos (declarados)
- T1 (sementes 1390–1391): β = 1 dissolve (N = 4096: acerto 0,2). TEORIA (β ≈ 1,85), SSMAX (β = 3,47), β = 3 e argmax dão 100%.
- T2 (sementes 1392–1393): β = 1 dissolve em N = 4096 (acerto 0, ε 0,10–0,15). TEORIA mantém ε(4096) = ε(12) (0,0003 → 0,0003). SSMAX dá ε ≈ 0.
- **Atalho trivial já achado:** qualquer afiação (β = 3, argmax) resolve, porque o argmax do motor estruturado não depende de N. Por isso a previsão central é a **quantitativa** (P3), não "funciona em 4096".
- Smoke do avaliador (sementes 1394–1395, N ≤ 256): em T1 a razão ε_TEORIA(256)/ε(12) ≈ 0,51, na borda da janela. O vazamento de T1 em N = 12 tem estrutura além do modelo de uma margem (raízes distratoras); probabilidade da P3 reduzida por isso.

## Montagem
- Treino: T1 com `mlu.S2Step` (N = 12, d ≤ 4, 600 iterações, BPTT); T2 com `tarefa_t2` (N = 12, k ≤ 4, 600 iterações). Sementes de treino **1300–1309** (T2 usa semente + 1000).
- Margem m: inversão de ε = K e^{−m}/(1 + K e^{−m}) no vazamento médio de 30 nós não-raiz em N = 30 (sem rótulos). ε_c(m): teoria de campo médio (E007d).
- Teste: N ∈ {12, 256, 4096}; T1 com d = 8 (16 passos); T2 com k = 16; 10 instâncias por semente e célula; sementes de teste derivadas do commit deste PREREG.
- Braços:
  - **B1** (β = 1).
  - **TEORIA** (β(N) acima).
  - **SSMAX** (β = ln(N−1)/ln 11; linha de base publicada mais próxima, reimplementação mínima com s fixado para β(12) = 1).
  - **CONST3** (β = 3; atalho).
  - **CRIST** (argmax a cada passo; atalho).
- Passo O(N) genérico (`passo_geral.py`), verificado exato contra o passo original (erro 1e−16).

## Previsões e critérios de morte
| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1 | B1 em N = 4096: acerto IQM ≤ 0,30 em T1 e T2 (o problema existe) | 0,85 | > 0,6 → experimento sem objeto |
| P2 | TEORIA em N = 4096: acerto IQM ≥ 0,95 e 0 colapsos (< 0,5) em T1 e T2 | 0,80 | < 0,8 em alguma tarefa → **H morta** |
| P3 | TEORIA: ε(N)/ε(12) ∈ [0,5; 2] em ≥ 90% das sementes, para N ∈ {256, 4096} em T1 e T2 (4 células) | 0,35 | T2 fora da janela em < 50% das sementes → a lei não prevê o vazamento |
| P4 | Atalhos (SSMAX, CONST3, CRIST) em N = 4096: acerto IQM ≥ 0,95 em T1 e T2 | 0,85 | — |
| P5 | SSMAX afia demais: ε(4096)/ε(12) IQM < 0,1 em T1 e T2 | 0,75 | — |
| P6 | TEORIA: ε(4096) < ε_c(m) em todas as sementes, T1 e T2 | 0,80 | — |

**H05 desbloqueada** se P2 e P6 passam (N2), com a ressalva registrada de que os atalhos também passam (P4).

## Sementes e poder
- 10 sementes de treino (N2). 10 instâncias × 10 sementes = 100 por célula; `n_para_largura(0,95; 0,05) = 86`.
- Custo estimado: ~10 min de CPU (smoke: 25 s para 2 sementes até N = 256; N = 4096 domina).

## Guarda do avaliador
```
experimentos/E013_temperatura/e013.py         : e93bc684ada9f783
experimentos/E013_temperatura/passo_geral.py  : 243c31a48cb816a8
experimentos/E006_lei_margem/passo_rapido.py  : 3aa24574de9b4029
experimentos/E007_lei_eps/diagnostico.py      : 25bbd568f306c2dd
experimentos/E001_mlu/mlu.py                  : 601604873fae9691
experimentos/E005_t2_salto/tarefa_t2.py       : b62e43a6a77ab648
lab/sementes.py                               : 4a5e4da1269f9b77
lab/estat.py                                  : 40af21b3e5c3d582
```

## Ameaças conhecidas
- Atalho: afiar sempre funciona neste motor (argmax invariante a N). O valor da TEORIA está em ser a afiação **mínima**, que preserva a gradação usada pelo S3 (E009) e a superposição (D07). Isso é argumento, não medido aqui.
- A margem é medida em N = 30 com o próprio modelo; é um número por modelo, sem rótulos. Não é "zero informação".
