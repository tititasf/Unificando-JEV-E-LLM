# CRÍTICA — autocrítica do norte (o S3 do próprio laboratório)

Regra 19 do `CLAUDE.md`. No início de todo ciclo, antes de escolher: rode `python3 -m lab.critica`, responda às perguntas aqui (de 5 a 15 linhas) e termine com `Decisão: APROFUNDAR | VARIAR | ENDURECER | PIVOTAR`. O `lab.checar` exige a entrada.
A pergunta 8 avalia a crítica anterior: a própria autoguia é medida e corrigida, e esse é o RSI do processo.

## Ciclo 18 — 2026-09-30
Painel:
- 22 experimentos: nenhuma novidade em 3, baixa em 16, candidata a nova em 3; a última candidata foi no ciclo 6, 11 ciclos atrás;
- **0/22** comparados com número publicado externo;
- Brier nos últimos 5 ciclos: 0,11.

1. **Nada novo para o mundo desde o ciclo 6.** Os 11 ciclos seguintes redescobriram, em miniatura, resultados publicados: Scalable-Softmax, temperatura adaptativa, mistura de softmaxes, teoria de códigos e Bellman-Ford alinhado.
2. **O trabalho mais próximo** do último resultado (E017) é a temperatura adaptativa de Veličković et al. 2025 e de Nerem/Wittig 2026. Não superamos nenhum deles em número algum, porque nunca medimos nada no mesmo benchmark.
3. **As perguntas foram escolhidas porque cabiam** (Python puro, 30 min) e porque a bússola interna mandava, não porque importavam fora daqui. A bússola otimiza a cobertura da nossa própria árvore de habilidades, que é uma métrica interna.
4. **Diversidade demais.** A regra de diversidade espalhou o esforço entre S0 e S6 sem profundidade em nenhum. O foco novo (a lacuna do G1) tem hipótese viva com chance estimada de 15–25% de resultado novo. Isso basta para aprofundar por vários ciclos.
5. **Autoengano:**
   - a calibração boa (Brier 0,05–0,11) vem de previsões feitas depois de pilotos;
   - os motores têm estrutura dada à mão, então o atalho trivial está sempre perto;
   - o "N2" mede reprodutibilidade, não relevância.
6. **Um revisor externo** mataria primeiro: "é o algoritmo exato com 5 parâmetros; não há aprendizado de estrutura". O teste que responde a isso é usar uma rede **genérica**, sem estrutura dada, que é exatamente o próximo experimento.
7. **Norte:** trocar "desbloquear a árvore de habilidades S0–S6" por "a lacuna do G1" (`docs/LITERATURA_G1.md`). A bússola passa a ser consultiva, e a CRÍTICA decide o tema.
8. **Crítica anterior:** não havia. A primeira crítica foi a resposta dada ao usuário no fim do ciclo 17, e ela acertou nos números que este painel confirma.

Mudanças de processo decididas agora:
- (a) a regra 14 (atacar a fronteira da bússola) fica subordinada a esta crítica;
- (b) a regra de diversidade é suspensa enquanto o foco tiver hipótese viva;
- (c) toda previsão feita depois de um piloto é marcada como tal;
- (d) todo nó com comparação a um número publicado leva `externo: true`.

Decisão: PIVOTAR
