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

## Ciclo 19 — 2026-09-30
Painel: 23 experimentos, a última candidata a nova foi no ciclo 6, **0/23 externos**, Brier dos últimos 5 ciclos 0,107 (inflado: as previsões do E018 foram todas pós-piloto).

1. **Novo para o mundo?** Não. O E018 mostrou que, em SP e WP, a síntese direta acha o programa sem rede (10/10 contra 5/10). O acerto da rota da rede no SP é real, mas não serve para nada que a síntese não faça.
2. **Trabalho mais próximo:**
   - Rodionov & Prokhorenkova (NeurIPS 2023): sem dicas, com regularização autossupervisionada;
   - MINAR: circuitos;
   - Cranmer 2020: regressão simbólica das mensagens, supervisionada.
   Nenhum deles descobre, sem supervisão, **qual variável oculta** a rede inventou e a regra que ela segue. Nós também ainda não.
3. **Escolha honesta:** o E018 importava, porque respondeu à objeção nº 1 de qualquer revisor. A pergunta seguinte tem de ser uma em que a síntese direta **não** baste. O caso natural é o protocolo do CLRS, em que a saída é **só o ponteiro** e a distância é estado oculto: a síntese precisa inventar a variável.
4. **Profundidade:**
   - o foco G1 ainda tem hipótese viva: a rede inventa a variável oculta, que pode ser lida sem supervisão por fechamento dinâmico, z^{t+1} ≈ R(z^t);
   - chance estimada de resultado novo: 20–30%;
   - conta como avanço mensurável: o E018 deu SP 5/5;
   - APROFUNDAR.
5. **Autoengano:**
   - as previsões pós-piloto inflam o Brier. Neste ciclo, **as previsões do PREREG saem antes de qualquer piloto da rota nova, e o piloto fica separado**;
   - atalho trivial: a síntese com ponteiro só também pode achar o programa por enumeração conjunta. Ela entra de novo como braço, e o custo de busca é medido.
6. **Revisor hostil:**
   - "a variável lida é a distância porque vocês procuraram a distância". Resposta: a leitura não conhece a verdade; o reconhecimento compara com a verdade só depois;
   - "controle negativo?". O WP tem ponteiro trivial (a aresta mais pesada), então a rede não precisa de estado oculto ali. A leitura **não** deve achar max-min no WP.
7. **Norte:** mantido (G1), com a pergunta refinada para "a rede como geradora das dicas que o CLRS escreve à mão".
8. **Crítica anterior** (PIVOTAR para o G1): foi seguida e deu um resultado claro em um ciclo. Faltava uma pergunta que teria antecipado o E018: **"qual é o atalho não neural (síntese/enumeração) e ele já foi rodado?"**. Acrescentada ao `lab/critica.py` (pergunta 9).

Decisão: APROFUNDAR
