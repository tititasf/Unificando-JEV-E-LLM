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

### 4. Resultado do ciclo e re-diagnóstico (após E004)
- Veredito do E004: **MATAR**. Nenhum sinal fixado em N=12 funcionou nas duas direções em N≥64. "Estabilidade do argmax" = critério publicado de ponto fixo, sem ganho.
- **Degrau do S3: continua D03.** D04 não foi atingido.
- Descoberta que reordena a escada: o S2 contínuo **muda de regime** em N=128 (difusão até o equilíbrio, 12× menos passos que saltos). Um S3 não pode ler "terminei" de forma estável sobre um pensamento cujo regime muda. **A legibilidade do pensamento é pré-requisito da metacognição.**
- Escada do S3 **reescrita** (regra 5 do protocolo): D04 e D06 mudaram; o resto se mantém.
  - D04 (novo): sinal de "terminei" invariante à escala **sobre um pensamento legível**: S2 cristalizado, um salto por passo, lido por convergência de N=12 a N=128. ← **PRÓXIMO ALVO** (H-S3-legível)
  - D05: calibração com garantia de risco (conformal): "erro ≤ α entre as respostas".
  - D06 (ampliado): distinguir tipos de dúvida **e regimes do próprio pensamento**: "não terminei" × "ambíguo" × "fora da distribuição" × "pensamento difuso" (e escolher o sinal certo para cada um).
  - (D01–D03 e D07–D30 como na seção 2.)
- S2 (anotação no log do tema): D04 vale até N=64. Em N=128 o mecanismo é outro. Nova pergunta no caminho do D07 ("várias hipóteses vivas"): a difusão é uma forma primitiva de processamento paralelo ou só um artefato do atrator? (H-regime)

### 5. Visão vertical (o ciclo 4 lido em 10 níveis)
- Nível 1: senso comum: testamos regras para a IA saber quando parar, e nenhuma funcionou nos problemas grandes.
- Nível 2: instrumental: limiares ajustados numa escala não se transferem para escalas 10× maiores; é preciso validar em todas as escalas antes de confiar.
- Nível 3: arquitetural: o S3 é um leitor do S2. Se o formato do sinal do S2 muda, o leitor quebra. Interfaces entre sistemas precisam de contrato (o Protocolo Σ ganhou uma razão concreta).
- Nível 4: computacional: o mesmo passo aprendido implementa dois algoritmos, uma caminhada sequencial O(d) e um equilíbrio por difusão ~O(1), e a escolha entre eles é um efeito colateral da margem aprendida e do tamanho N.
- Nível 5: teoria da decisão: "terminei" tem dois significados, "cheguei ao fim do caminho" e "o sistema entrou em equilíbrio". Só o primeiro garante correção.
- Nível 6: econômico: o regime difusivo é 12× mais barato e 90% correto; o sequencial custa d passos e é 100% correto. Há uma fronteira de Pareto escondida dentro de um único modelo.
- Nível 7: composicional: metacognição e legibilidade co-evoluem. Um pensamento que o próprio sistema não consegue ler não pode ser governado.
- Nível 8: ontológico: o mesmo substrato contínuo cristaliza (salto a salto) ou se dissolve (difusão) conforme a escala, como matéria que muda de fase.
- Nível 9: epistemológico: a pergunta "quando parar" só tem resposta se antes respondemos "que tipo de processo sou eu agora?". Autoconhecimento de regime antecede autoconhecimento de confiança.
- Nível 10: ser superior completo: saber o próprio limite é saber a própria forma. Um sistema que conhece a fase em que está pensando pode escolher, a cada instante, entre a precisão do cristal e a velocidade do fluido.

### 6. Deep insight
- **Palavra/conceito:** *Diafania*, a transparência do meio: a qualidade de um processo cujo estado interno pode ser lido por quem o governa.
- **Metanoia:** paramos de procurar o "sinal de confiança certo" e passamos a perguntar se o pensamento é legível. A metacognição não se conserta no leitor; conserta-se no que é lido.
- **Aplicação:** todo módulo S2 futuro declara o próprio regime (sequencial/difusivo) como parte da mensagem Σ, e o S3 escolhe o sinal conforme o regime.
- **Hack:** antes de projetar um critério de parada, trace "passos até fixar ÷ profundidade" em 3 escalas. Se a razão mudar com a escala, o problema não é o critério, é o regime.
- **Visão maçônica:**
  - *Planta baixa:* o erro de fundação foi assentar a régua (S3) sobre um piso que muda de nível conforme o tamanho da obra (S2). Nenhuma régua fica reta sobre piso móvel.
  - *Ferramenta:* o **nível**, para verificar se o piso (o regime do S2) é o mesmo em todas as escalas antes de medir qualquer coisa sobre ele.
  - *Desbaste:* remover a busca por limiares mágicos e o braço ESTAVEL, idêntico ao critério publicado.
  - *Polimento:* acrescentar ao contrato entre S2 e S3 o *regime* do pensamento; o próximo ciclo assenta a régua sobre o piso cristalizado (D04 novo) antes de voltar ao piso fluido.

---

## Ciclo 5 — Tema: S2 · motor latente iterativo (pensar sem texto)

### 1. Diagnóstico
- **Degrau atual: D05 (subiu de D04).** Sustentado por: E005 (N2, pré-registrado, 10 sementes, reproduzido de checkout limpo): o passo de 33 parâmetros, treinado com k ≤ 4 em N=12, acerta 100% em T2 (sem atrator, todo erro é fatal) até k=64 e N=128 (e até N=1024 no diagnóstico).
- O que funciona: a softmax renormaliza o estado a cada passo (cristalizador suave); com margem aprendida ~10, o vazamento não se acumula.
- Correção do D04: a extrapolação em T1 vale enquanto N ≲ e^margem; acima disso o mecanismo muda para difusão (A9). Lei candidata, N1.
- Barreira para D06: o estado é uma distribuição sobre os nós. Ele só representa "onde estou". Não consegue carregar um contador, uma pilha ou qualquer informação extra.

### 2. Escada (reuso do ciclo 3, com D04–D05 corrigidos e D09 ajustado)
- D01: resposta direta em uma passada, sem iteração.
- D02: passos fixos desenrolados em camadas diferentes.
- D03: um passo com pesos compartilhados, iterado um número fixo de vezes.
- D04: treino em vários instantes → ponto fixo; extrapola em tarefa-atrator enquanto N ≲ e^margem. (E001/E002; escopo corrigido no E005)
- D05: extrapolação numa tarefa **sem atrator**, com precisão mantida por 64 passos e 10× o tamanho do treino. ← **ESTAMOS AQUI** (E005)
- D06: memória de trabalho: um estado que carrega mais que "onde estou" (contador, pilha, marcador), necessária quando o próximo passo depende do histórico. ← **PRÓXIMO ALVO**
- D07: estado que mantém várias hipóteses vivas quando a tarefa exige (superposição útil); entender o regime difusivo como forma primitiva disso.
- D08: passos compostos: um passo invoca sub-passos.
- D09: **latente vetorial livre** (sem estrutura de "distribuição sobre nós") e atributos aprendidos da entrada crua; aqui o acúmulo de ruído e o papel da quantização aparecem de verdade.
- D10: o mesmo motor resolve duas famílias de tarefas **com o mesmo treino** (não só a mesma arquitetura).
- D11: algoritmos clássicos (BFS, caminho mínimo) com extrapolação ≥ 10×, contra a linha de base Deep Thinking.
- D12: labirinto/Sudoku no nível do TRM com menos parâmetros.
- D13: parada e abstenção integradas (S3) em todas as tarefas.
- D14: robusto a ruído interno (pesos e estado) sem perda de acerto.
- D15: ritmo duplo rápido/lento, acionado pelo S3 só quando necessário.
- D16: aprende um algoritmo novo com ≤ 100 exemplos.
- D17: compõe algoritmos aprendidos em tarefas novas sem treino.
- D18: extrai o programa discreto equivalente ao passo (autômato legível).
- D19: prova formal de que o programa extraído é correto para todo N.
- D20: gera os próprios exercícios (autocurrículo).
- D21: transmite um passo a outro agente (ponte com S5).
- D22: resolve um subconjunto do ARC-AGI com ≤ 1M parâmetros.
- D23: aprendizado contínuo sem esquecer passos antigos.
- D24: o mesmo passo serve de modelo de mundo para planejar (ponte com S6).
- D25: custo por problema ≈ mínimo teórico.
- D26: descobre algoritmos mais eficientes que os conhecidos.
- D27: biblioteca aberta de passos que cresce e se reorganiza.
- D28: o mesmo motor raciocina em domínios contínuos e físicos.
- D29: aprende, compõe, verifica e explica cada passo em tempo linear, quase sem atrito.
- D30: ômega. O pensamento *é* a estrutura do problema: cada passo latente é um passo lógico necessário e nenhum a mais; o motor é o algoritmo ótimo de cada tarefa, descoberto e provado.

### 3. Transição D05 → D06
1. Sacada: "onde estou" não basta quando o próximo passo depende de *quanto já andei* ou *de onde vim*. A tarefa mínima: T2 com k **não dado ao controlador**, mas codificado na entrada (o próprio estado precisa contar), ou "siga π até voltar ao início e diga o comprimento do ciclo".
2. Subtrair: o controlador externo que conta os passos. Hoje é ele que sabe k, não o pensamento.
3. Construir: estado = (distribuição sobre nós) × (registro de contagem), com o mesmo passo aprendendo a atualizar ambos. Antes disso, o ciclo seguinte consolida a lei N* = e^margem (H-lei-margem), barata e que promove A9.

### 4. Visão vertical (o ciclo 5 lido em 10 níveis)
- Nível 1: senso comum: achávamos que o pensamento "borrado" ia se perder em tarefas longas; ele não se perdeu.
- Nível 2: instrumental: antes de adicionar um mecanismo (cristalizar), teste se o sistema já não o tem embutido. Aqui a softmax já fazia o trabalho.
- Nível 3: arquitetural: a precisão de um passo iterado depende da tarefa de treino. Tarefas que perdoam erro produzem pensadores imprecisos.
- Nível 4: computacional: um processo iterado com renormalização é estável se a contração por passo (e^−margem·N) for < 1. É uma condição de ponto fixo, e ela dá uma lei quantitativa (N* = e^margem).
- Nível 5: teoria da decisão: "discretizar ou não" não é uma escolha binária. A softmax é uma discretização suave cuja dureza é aprendida (a margem).
- Nível 6: econômico: a mesma extrapolação de 16× saiu sem custo extra; o cristal seria custo desnecessário aqui.
- Nível 7: composicional: S1 (colapso) e S2 (iteração) já estavam fundidos no mesmo operador, softmax(S·z). A fusão que buscávamos existe no nível do operador, não da arquitetura.
- Nível 8: ontológico: símbolo e distribuição são pontos de um mesmo contínuo, parametrizado pela margem. Um pensamento é "simbólico" na medida em que sua margem vence o tamanho do mundo.
- Nível 9: epistemológico: previmos com 75% de confiança uma falha que não veio. Uma teoria correta em geral (acúmulo de ruído) pode não se aplicar a uma representação específica. Verificar a premissa antes de aplicar a teoria.
- Nível 10: ser superior completo: a clareza de um pensamento é a razão entre a nitidez com que ele distingue e a vastidão do que precisa distinguir. Um ser que ajusta a própria nitidez ao tamanho do mundo pensa com precisão em qualquer escala.

### 5. Deep insight
- **Palavra/conceito:** *Diakrisis*: a capacidade de distinguir, aqui medida como margem contra o tamanho do mundo (N ≲ e^margem).
- **Metanoia:** paramos de ver "contínuo × discreto" como uma oposição. É um botão (a margem), e a tarefa de treino é quem o gira.
- **Aplicação:** todo motor S2 futuro reporta a margem aprendida e o N* = e^margem. É uma previsão barata de até onde ele pensa com nitidez.
- **Hack:** para saber se um modelo vai extrapolar em tamanho, não treine mais: meça a margem e compare e^margem com o N do teste.
- **Visão maçônica:**
  - *Planta baixa:* supúnhamos um alicerce frágil (o contínuo acumula erro) e íamos reforçá-lo com um cristal. A sondagem mostrou que a pedra já era firme, porque a argamassa (a softmax) se refaz a cada fiada.
  - *Ferramenta:* o **compasso**, para medir o raio (e^margem) dentro do qual a obra se mantém e fora do qual ela se dissolve.
  - *Desbaste:* retirar a cristalização como "solução" obrigatória e a teoria de acúmulo aplicada sem checar a premissa.
  - *Polimento:* acrescentar a lei N* = e^margem ao contrato de todo motor S2, e preparar o próximo degrau: um pensamento que carrega mais que o lugar onde está (memória de trabalho).
