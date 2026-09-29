# E010 — Relatório: memória de trabalho latente

**Veredito: PROMOVER.** Habilidade **H06 desbloqueada**; o **S2 sobe de D05 para D06**.
Nível: **N2** (pré-registrado, 10 sementes, sementes de teste derivadas do commit `6802ec9`, reprodução limpa, guarda OK). **Novidade: baixa** (memória/contadores em redes neurais são conhecidos); o valor está na forma: um único passo relacional sobre (lugar × contador) que extrapola 16× em k e 8× em N.

## Previsões
| # | Previsto | Prob. | Obtido | Status |
|---|---|---|---|---|
| P1 | MEMORIA IQM ≥ 0,95 nas 9 células | 0,75 | 1,00 em todas | ✅ |
| P2 | MEMORIA (64, 64): 0 colapsos | 0,75 | 0/10 | ✅ |
| P3 | SEM_MARCAS ≥ 0,95 em (64, 64) | 0,70 | 1,00 | ✅ |
| P4 | SEM_MEMORIA (64, 64) ≤ 0,10 | 0,90 | 0,06 | ✅ |
| P5 | CONTROLADOR (64, 64) ≥ 0,95 | 0,90 | 1,00 | ✅ |

**Brier: 0,05.**

## O que foi mostrado
1. **O próprio pensamento conta.** O controlador roda sempre 72 passos sem saber k; o estado anda exatamente k saltos e **para sozinho**, com 100% de acerto até k = 64 (treino: k ≤ 4) e N = 64 (treino: N = 8), num espaço de 4.160 estados.
2. **Sem memória não dá:** o mesmo ponteiro sem contador acerta 6% em N = 64 (acaso).
3. **A parada emerge da geometria do registro:** sem as marcas "está em zero", o motor funciona igual (1,00 em (64,64); 0,97 no pior caso). No contador 0 não existe a transição "decrementar", então a fronteira do espaço de estados força a parada. Nada precisou dizer "pare".
4. **A lei de nitidez se manteve** num espaço de 4.160 estados: o passo aprendeu uma margem grande o bastante (coerente com A11/A12).

## Revisor hostil
1. *"As relações 'decrementa/mantém' são dadas."* Sim, declarado: memória **estruturada**. Aprende-se o que fazer com elas, não a noção de contar.
2. *"T2 com k na entrada é fácil."* É a menor tarefa em que a memória é necessária (SEM_MEMORIA prova isso). Tarefas com memória mais rica (pilha, vários registros) ficam para D06+.
3. *"A ablação não quebrou; então o que foi testado?"* A ablação mostrou que as marcas eram desnecessárias (o achado 3). A peça essencial é o registro em si, e isso a SEM_MEMORIA testou.

## Hipóteses semeadas
- **H-pilha:** dois registros (ou pilha) para tarefas como "siga π k vezes e depois σ j vezes".
- **H-fronteira-geometrica:** "comportamentos de parada emergem de fronteiras do espaço de estados" vale para outros comportamentos (por exemplo, rebater em paredes num modelo de mundo, H16)?
