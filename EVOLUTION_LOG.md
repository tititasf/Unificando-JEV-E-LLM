# EVOLUTION LOG — escadas de 30 degraus por tema

Protocolo em `docs/ESCALA.md`. Degrau "atingido" = sustentado por evidência
≥ N1. O resto é projeção. A entrada mais recente de cada tema define o alvo N+1.

Temas abertos: **S2 motor latente** · **S3 metacognição** · **S5 comunicação**.

---

## Ciclo 3 (retroativo) — Tema: S2 · motor latente iterativo (pensar sem texto)

### 1. Diagnóstico
- Degrau atual: **D04**. Sustentado por: E001 (N1, 10 sementes) e E002 (N2, 30 sementes, 0 colapsos em d=128).
- O que funciona: um passo de 33 parâmetros, com pesos compartilhados, iterado até o ponto fixo; extrapola ≥32× a profundidade do treino, sem *overthinking*.
- Barreira para D05: só foi testado numa tarefa-**atrator** (erros se autocorrigem). Não sabemos se funciona quando todo erro é fatal.

### 2. Escada
- D01: resposta direta em uma passada, sem iteração.
- D02: passos fixos desenrolados em camadas diferentes (profundidade fixa).
- D03: um único passo com pesos compartilhados, iterado um número fixo de vezes.
- D04: treino em vários instantes → a resposta vira ponto fixo; extrapola sem *overthinking*. ← **ESTAMOS AQUI** (E001/E002)
- D05: extrapolação numa tarefa **sem atrator** (salto exato: qualquer erro é fatal). ← **PRÓXIMO ALVO** (H-T2)
- D06: memória de trabalho explícita para estados maiores que "onde estou" (contador, pilha).
- D07: estado latente que mantém várias hipóteses vivas quando a tarefa exige (superposição útil).
- D08: passos compostos: um passo invoca sub-passos (sub-rotinas latentes).
- D09: o passo aprende os próprios atributos a partir da entrada crua (sem atributos de aresta feitos à mão).
- D10: o mesmo motor resolve duas famílias de tarefas diferentes (T1+T2).
- D11: algoritmos clássicos (BFS, caminho mínimo) com extrapolação ≥10×.
- D12: labirinto/Sudoku no nível do TRM com menos parâmetros.
- D13: parada e abstenção integradas (S3) em todas as tarefas.
- D14: robusto a ruído interno (pesos e estado) sem perda de acerto.
- D15: ritmo duplo rápido/lento (estilo HRM), acionado pelo S3 só quando necessário.
- D16: aprende um algoritmo novo com ≤100 exemplos.
- D17: compõe algoritmos aprendidos para resolver tarefas novas sem treino.
- D18: extrai o programa discreto equivalente ao passo (autômato legível).
- D19: prova formal de que o programa extraído é correto para todo N.
- D20: gera os próprios exercícios para aprender passos novos (autocurrículo).
- D21: transmite um passo a outro agente (ponte com S5).
- D22: resolve um subconjunto do ARC-AGI com ≤1M parâmetros.
- D23: aprendizado contínuo sem esquecer passos antigos.
- D24: o mesmo passo serve como modelo de mundo para planejar (ponte com S6).
- D25: custo por problema ≈ mínimo teórico (nº de passos = profundidade lógica real).
- D26: descobre algoritmos mais eficientes que os conhecidos.
- D27: biblioteca aberta de passos que cresce e se reorganiza (uma ontologia de operações).
- D28: o mesmo motor raciocina em domínios contínuos e físicos.
- D29: aprende, compõe, verifica e explica cada passo em tempo linear, quase sem atrito.
- D30: ômega. O pensamento *é* a estrutura do problema: cada passo latente é um passo lógico necessário e nenhum a mais; o motor é o algoritmo ótimo de cada tarefa, descoberto e provado.

### 3. Transição D04 → D05
1. Sacada: a tarefa escolhida escondia a fragilidade. Primeiro trocar o chão (a tarefa), depois o motor.
2. Subtrair: a raiz que aponta para si (o atrator). Na tarefa nova não existe ponto fixo natural; o motor tem de contar os saltos.
3. Construir: T2 "salto exato": permutação aleatória, seguir exatamente k ponteiros, k dado como entrada. → H-T2.

---

## Ciclo 3 (retroativo) — Tema: S5 · comunicação entre agentes

### 1. Diagnóstico
- Degrau atual: **D04**. Sustentado por: E003 (N2, 10 sementes, pré-registrado).
- O que funciona: dois agentes com metade do conhecimento cada, mensagem simbólica (índice + potência concentrada); vence o canal analógico por até +0,81 sob ruído, com ~200× menos dados.
- Barreira para D05: o código é one-hot fixo, escolhido à mão. Não sabemos quantos bits bastam nem se existe código melhor.

### 2. Escada
- D01: agentes isolados, sem comunicação.
- D02: compartilhar o estado bruto inteiro, sem ruído.
- D03: canal analógico com ruído (E003, CONT).
- D04: mensagem simbólica discreta com potência concentrada (E003, SIMB). ← **ESTAMOS AQUI**
- D05: código mínimo: bits por passo × robustez; códigos corretores de erro. ← **PRÓXIMO ALVO** (H-5.4)
- D06: a mensagem carrega confiança (Protocolo Σ) e o receptor pondera.
- D07: o emissor escolhe entre cristal e distribuição conforme a própria dúvida.
- D08: mais de 2 agentes, com roteamento de quem fala com quem.
- D09: canal com perdas e atrasos, com reenvio.
- D10: código aprendido (não one-hot), otimizado para o canal.
- D11: vocabulário que emerge do zero (Σ6).
- D12: vocabulário composicional (símbolos combináveis, gramática mínima).
- D13: metacomunicação ("não sei", "preciso de X").
- D14: pergunta ativa: pedir exatamente o dado que falta.
- D15: consenso robusto com agentes defeituosos (bizantinos).
- D16: ensinar uma habilidade (um passo) por mensagens.
- D17: compressão perto do limite de Shannon da tarefa.
- D18: tradução entre agentes com ontologias diferentes.
- D19: ontologia compartilhada que evolui sem quebrar a compatibilidade.
- D20: modelo do receptor (teoria da mente mínima): mandar o que *ele* precisa.
- D21: mensagens sobre futuros simulados (ponte com S6).
- D22: negociação de recursos pelo protocolo (ponte com S0/S4).
- D23: humano e máquina no mesmo protocolo tipado.
- D24: mensagens com provas curtas verificáveis.
- D25: 100+ agentes com coordenação emergente estável.
- D26: a língua melhora o pensamento interno de quem fala.
- D27: protocolo autodescritivo: um agente novo aprende a língua só pelo uso.
- D28: custo de comunicação ≈ informação nova (zero redundância).
- D29: fusão temporária: agentes pensam como um só quando útil e se separam depois.
- D30: ômega. Comunicação sem perda nem atrito: cada agente sabe exatamente o que o outro precisa saber e transmite só isso, na forma que o outro já entende; a fronteira entre pensar junto e pensar sozinho desaparece.

### 3. Transição D04 → D05
1. Sacada: o one-hot gasta N dimensões para carregar log₂N bits. A robustez vem da *distância* entre códigos, não do one-hot em si.
2. Subtrair: a suposição de que um símbolo precisa de uma dimensão só para ele.
3. Construir: comparar one-hot × código binário × código com distância (repetição/Hamming) no mesmo canal, medindo bits × acerto. → H-5.4.

---

## Ciclo 4 — Tema: S3 · metacognição (quanto pensar e quando não sabe)

### 1. Diagnóstico
- Degrau atual: **D03**. Sustentado por: E001 (N1): parada por convergência + confiança absoluta; E-AURC≈0 e 54% de economia **na escala do treino**.
- O que funciona: com N=12 o S3 sabe parar e sabe quando não terminou.
- Barreira para D04: E002 (N2) mostrou que o limiar absoluto (máx z ≥ 0,9) não escala. Com N≥64 ele se abstém em 100% dos casos, embora o S2 acerte. O S3 atual só funciona no tamanho em que foi ajustado.

### 2. Escada
- D01: sem metacognição: sempre responde após um número fixo de passos.
- D02: limiar fixo de confiança na saída (responde se máx ≥ τ).
- D03: parada por convergência + confiança absoluta, ajustadas na escala do treino. ← **ESTAMOS AQUI** (E001)
- D04: sinal de "terminei" **invariante à escala**: funciona de N=12 a N=128 sem reajuste, e se abstém quando o orçamento acaba. ← **PRÓXIMO ALVO** (E004)
- D05: calibração com garantia de risco (ex.: predição conformal): "erro ≤ α entre as respostas".
- D06: distinguir tipos de dúvida: "não terminei" × "o problema é ambíguo/impossível" × "fora da distribuição".
- D07: parada aprendida ponta a ponta com custo explícito (estilo PonderNet), comparada ao critério por regra.
- D08: previsão de custo antes de pensar: "este problema vai levar ~k passos".
- D09: verificação por invariante barato em vez de confiança (Σ3: chutar e verificar).
- D10: alocação por valor da informação: escolher entre S1, S2, verificar ou abster.
- D11: a energia restante (S0) entra como sentido na decisão (Σ5).
- D12: autodiagnóstico: detectar *qual* componente falhou (S2 ou S3), como o E002 fez à mão.
- D13: autocorreção: reajustar o próprio limiar/temperatura online.
- D14: o mesmo S3 funciona em tarefas diferentes sem re-treino.
- D15: certificado curto de correção junto de cada resposta.
- D16: metacognição coletiva: "não sei" agregado e calibrado entre agentes (S4).
- D17: pergunta ativa: formular a pergunta mínima que resolveria a dúvida.
- D18: modelo de si: prever o próprio desempenho numa tarefa nova antes de tentar.
- D19: curiosidade dirigida: escolher o que aprender para reduzir a incerteza futura.
- D20: detectar o próprio autoengano (atalhos, vazamentos): a régua do laboratório, automatizada.
- D21: autoexperimentação: formular hipóteses sobre as próprias falhas, pré-registrar e testar (um `/ciclo` interno).
- D22: decidir mudar a própria arquitetura com base em evidência.
- D23: calibração que acompanha mudanças do mundo sem rótulos.
- D24: saber quando a *pergunta* está mal posta (incerteza sobre o objetivo).
- D25: relatos internos fiéis ao estado causal (introspecção verificável).
- D26: planejar o próprio aprendizado em horizonte longo.
- D27: um único sinal de "valor de pensar mais" governa energia, comunicação e simulação (S0–S6).
- D28: a metacognição é amortizada: custo ≈ 0 (vira intuição, S1).
- D29: todo estado tem confiança calibrada e causa explicável, sem custo extra.
- D30: ômega. Conhecer exatamente o limite do próprio conhecimento: nunca erra ao responder, nunca se abstém quando poderia saber, e gasta em pensar exatamente o que a resposta vale.

### 3. Transição D03 → D04
1. Sacada: "terminei" não é "estou confiante". É **"meu estado parou de mudar de um jeito que importa"**. A nitidez do estado depende de N; a *estabilidade da decisão* (o argmax parado) não.
2. Subtrair: o limiar absoluto de nitidez (máx z ≥ 0,9), um número que só faz sentido para um N.
3. Construir: E004 compara sinais de parada (absoluto, entropia normalizada, razão ao uniforme, estabilidade do argmax) de N=12 a N=128, com casos dentro e fora do orçamento. Critério: responder quando dá e se abster quando não dá, em todas as escalas, com limiares fixados em N=12.
