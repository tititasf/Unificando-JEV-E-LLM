# E007 — Pré-registro: a lei de nitidez fora da amostra (ε_c congelado)

**Escrito antes de rodar o teste. Não editar depois da primeira execução completa.**
Trilha A. Átomos: 2.1, 2.3. Nível de partida: A11 em N1 (E006d, pós-hoc, 12 sementes).
Habilidade-alvo: **H04** (prioridade 22 na bússola; gargalo de G1, G2, G4, G5). Nó pai: **E006d**. Operador: **REPLICAR** (fora da amostra).

## Hipótese
H1: um único número medido no **passo** do modelo prevê o tamanho em que o
pensamento se dissolve: N̂_c = o N em que o vazamento de um passo ε(N) = **0,071**
(valor congelado do E006d). O regime do S2 muda (de nítido para dissolvido) em N_c ≈ N̂_c.
H2 (por passo × acumulado): a dissolução é uma instabilidade **por passo** do mapa
iterado; o N_c **não depende** da profundidade d. A alternativa ("acumulado", ε_c·d
constante) prevê N_c(d=40) ≈ N_c(d=10)/4.

## Relação com a literatura
Veličković et al. (ICML 2025) provam que a softmax aprendida **precisa** se dispersar
com o tamanho, mas não dão o ponto em que um passo **iterado** perde a nitidez nem um
preditor por modelo. O que testamos: um preditor de um passo, com limiar congelado,
fora da amostra, contra uma linha de base nula. Novidade esperada: baixa a média.

## Piloto (declarado)
Antes deste pré-registro rodei um piloto com o **modelo completo** (lição 11b), em
sementes **fora da faixa** do experimento (790, 791), para validar a grade:
- Previsto 193 / 82; N_c pelo regime 158 / 68 (≈ 0,83 do previsto); pela acurácia 180 / 79.
- Pelo regime, o N_c não variou com d (158/163/154 e 68/71/69 para d = 20/10/40). A acurácia com d=40 ficava alta mesmo dissolvida (o caminho ocupa metade do grafo: "sorte de atrator", A9).
- Consequências para o desenho: (1) métrica **primária = regime** (nitidez média máx z = 0,5), acurácia secundária; (2) bisseção começa em N=24 (bug achado no piloto). As probabilidades abaixo usam o piloto e estão declaradas como informadas por ele.

## Montagem
- Treino idêntico ao E001 (T1, N=12, d≤4, 600 iterações). Sementes de treino **700–729** (30 novas).
- N̂_c por semente: bisseção em log N de ε(N) = 0,071 (5 grafos de prova com d=20, sementes fixas; só o modelo, sem olhar acurácia).
- Teste congelado: sementes de teste **derivadas do commit deste PREREG** (`lab.sementes.derivar`).
  - Grade principal: d=20, N = N̂_c × {0,5; 0,71; 1; 1,41; 2}, **40 exemplos por célula**.
  - Teste de d (sementes 700–714): d ∈ {10, 40}, N = N̂_c × {0,25; 0,35; 0,5; 0,71; 1; 1,41; 2} (N ≥ d+8).
- N_c = primeira queda da nitidez média abaixo de 0,5 subindo N (interpolação geométrica); "abaixo"/"acima" se fora da grade.
- **Linha de base nula:** prever N_c = 137 (mediana do E006d) para todas as sementes.

## Sementes e poder
- 40 exemplos por célula: `n_para_diferenca(0,5; 0,95)` = 22 e `n_para_largura(0,5; 0,15)` = 39.
- 30 sementes: permite estimar uma fração (P1) com IC de Wilson de ±~0,15.
- Custo estimado (docs/STACK.md): ~700 s de CPU.

## Previsões
| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1 | N_c (regime) dentro de 1,5× de N̂_c em ≥ 80% das sementes | 0,65 | < 50% → **lei morta** |
| P2 | cruzamento dentro da grade em ≥ 90% das sementes | 0,70 | — |
| P3 | erro médio \|ln(N_c/N̂_c)\| da lei < o da constante 137, com p < 0,01 | 0,70 | lei ≥ constante → **lei morta** (não informa mais que um número fixo) |
| P4 (H2 por passo) | R = N_c(40)/N_c(10) com mediana em [0,67; 1,5] | 0,65 | — |
| P5 (acumulado) | mediana de R ≤ 0,4 | 0,15 | — |
| P6 | N_c medido fica abaixo do previsto em ≥ 70% das sementes (viés do piloto) | 0,55 | — |

**H04 desbloqueada** se P1 e P3 passam (≥ N2: pré-registrado, 30 sementes, fora da amostra) e P4 ou P5 decide o papel de d.

## Guarda do avaliador
```
experimentos/E007_lei_eps/e007.py             : d1af7d75fff8e546
experimentos/E006_lei_margem/e006.py          : ddd1da34a5896d90
experimentos/E006_lei_margem/passo_rapido.py  : 3aa24574de9b4029
experimentos/E001_mlu/mlu.py                  : 601604873fae9691
lab/sementes.py                               : 4a5e4da1269f9b77
```

## Ameaças conhecidas
- A mesma família de grafos gera a previsão (ε) e o teste: a lei vale para esta distribuição; outra distribuição exige outro teste.
- O limiar 0,071 veio de um diagnóstico com 10 exemplos por célula; se ele estiver enviesado, P6 e P1 mostram.
- Transições abruptas + grade discreta: a interpolação dá resolução de ~1,4×; P1 usa 1,5× por isso.
