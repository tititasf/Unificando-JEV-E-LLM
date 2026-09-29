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

---

## Ciclo 6 — Tema: S2 · motor latente iterativo (consolidação da lei de dissolução)

### 1. Diagnóstico
- **Degrau atual: D05 (mantido).** O ciclo não visava subir degrau, e sim consolidar a fronteira do D04/D05: até onde o pensamento contínuo se mantém nítido.
- E006 (N2, negativo): o limiar pré-registrado (vazamento de um passo = 0,5) errou por um fator > 4. E006d (N1): a transição ocorre em **ε ≈ 0,07** por passo, com N_c variando 3× entre sementes.
- Barreira para D06 (inalterada): o estado só representa "onde estou".

### 2. Escada (sem mudança de ordem desde o ciclo 5; D04 com escopo atualizado)
- D01: resposta direta em uma passada.
- D02: passos fixos desenrolados.
- D03: um passo compartilhado, iterado um número fixo de vezes.
- D04: ponto fixo por treino multi-instante; extrapola em tarefa-atrator **enquanto o vazamento por passo ε < ~0,07** (E006d).
- D05: extrapolação sem atrator com precisão por 64 passos. ← **ESTAMOS AQUI** (E005)
- D06: memória de trabalho (contador, pilha, marcador) no próprio estado. ← **PRÓXIMO ALVO** (depois de fechar a lei: H-lei-eps)
- D07: várias hipóteses vivas quando a tarefa exige (superposição útil).
- D08: passos compostos (sub-rotinas).
- D09: latente vetorial livre e atributos aprendidos da entrada crua.
- D10: mesmo motor e mesmo treino em duas famílias de tarefas.
- D11: algoritmos clássicos com extrapolação ≥ 10× contra Deep Thinking.
- D12: labirinto/Sudoku no nível do TRM com menos parâmetros.
- D13: parada e abstenção integradas (S3).
- D14: robusto a ruído interno.
- D15: ritmo duplo rápido/lento acionado pelo S3.
- D16: algoritmo novo com ≤ 100 exemplos.
- D17: composição de algoritmos sem treino.
- D18: programa discreto extraído do passo.
- D19: prova formal do programa extraído.
- D20: autocurrículo.
- D21: transmite um passo a outro agente (S5).
- D22: subconjunto do ARC-AGI com ≤ 1M parâmetros.
- D23: aprendizado contínuo sem esquecimento.
- D24: o passo como modelo de mundo (S6).
- D25: custo ≈ mínimo teórico.
- D26: descobre algoritmos mais eficientes que os conhecidos.
- D27: biblioteca aberta de passos (ontologia de operações).
- D28: domínios contínuos e físicos.
- D29: aprende, compõe, verifica e explica em tempo linear.
- D30: ômega: cada passo latente é um passo lógico necessário e nenhum a mais; o motor é o algoritmo ótimo de cada tarefa, descoberto e provado.

### 3. Transição (fechar a fronteira antes de subir)
1. Sacada: a nitidez do pensamento tem um orçamento por passo (ε_c ≈ 0,07). Isso é uma **condição de projeto**: qualquer S2 que precise escalar tem de manter ε(N) < ε_c, seja por margem (treino), temperatura adaptativa ou cristalização.
2. Subtrair: a fórmula e^margem (errada) e o limiar 0,5 (errado).
3. Testar: H-lei-eps (ε_c congelado, fora da amostra, e d ∈ {10, 20, 40} para decidir "por passo" × "acumulado"). Depois, D06.

### 4. Visão vertical (o ciclo 6 lido em 10 níveis)
- Nível 1: senso comum: tentamos prever em que tamanho o pensamento "embaça", e o número estava errado.
- Nível 2: instrumental: a ideia (medir o vazamento de um passo) estava certa; o limiar escolhido a priori estava errado. Separar "a variável certa" de "o valor certo".
- Nível 3: arquitetural: todo S2 recebe uma especificação: ε(N) < ε_c no maior N esperado.
- Nível 4: computacional: um mapa iterado perde o ponto fixo nítido muito antes de um único passo "falhar". A estabilidade de um sistema dinâmico não é a precisão de um passo.
- Nível 5: teoria da decisão: previsões moderadas (0,45–0,6) custaram pouco quando erraram (Brier 0,25 contra 0,42). A humildade calibrada é mensurável.
- Nível 6: econômico: um diagnóstico de 30 s valeu mais que o experimento de 6 min, porque a grade do experimento estava mal posicionada.
- Nível 7: composicional: o limiar ε_c conecta S2 (nitidez), S3 (legibilidade, E004) e S5 (ruído de canal, E003): três sistemas limitados pela mesma razão sinal/vazamento.
- Nível 8: ontológico: a dissolução é uma transição de fase. Abaixo de ε_c o pensamento tem identidade (um lugar); acima, é um campo.
- Nível 9: epistemológico: a lei nasceu errada, foi refutada e renasceu mais precisa no mesmo ciclo. O conhecimento aqui avança por refutação e correção, não por confirmação.
- Nível 10: ser superior completo: conhecer o próprio limiar de dissolução é saber até onde se pode pensar com nitidez sem se perder. Quem mede o próprio vazamento escolhe quando se concentrar e quando se espalhar.

### 5. Deep insight
- **Palavra/conceito:** *Limen*, o limiar: o ponto em que uma quantidade pequena (ε ≈ 0,07) decide entre identidade e dissolução.
- **Metanoia:** o erro não foi escolher a variável errada; foi confiar numa constante intuitiva (0,5). Variáveis vêm da teoria; constantes vêm dos dados.
- **Aplicação:** todo motor S2 passa a reportar ε(N) na maior escala de teste; ε > 0,07 é um alerta vermelho antes de rodar qualquer coisa.
- **Hack:** para prever se um modelo iterado vai extrapolar em tamanho, meça um passo, não mil: ε(N) contra 0,07.
- **Visão maçônica:**
  - *Planta baixa:* assentamos a régua (N*) num nível arbitrário (0,5) e ela ficou acima do piso real.
  - *Ferramenta:* o **prumo**, para descer até o ponto exato em que a parede começa a ceder (ε_c).
  - *Desbaste:* a fórmula e^margem e o limiar 0,5.
  - *Polimento:* a especificação ε(N) < ε_c em todo S2, e um teste fora da amostra que separa "por passo" de "acumulado".

---

## Ciclo 7 — Tema: S2 · motor latente iterativo (a fronteira D04 fechada: lei de nitidez)

### 1. Diagnóstico
- **Degrau atual: D05 (mantido); a fronteira do D04 agora tem lei validada.** E007 (N2, fora da amostra, 30 sementes, sementes de teste derivadas do commit, reprodução limpa): o vazamento de um passo, com limiar congelado, prevê N_c em 25/30 modelos; o efeito é por passo (R = 0,95). Habilidade H04 desbloqueada.
- E007d (N1): teoria de campo médio (bifurcação sela-nó) prevê N_c com ~9% de erro sem nenhum parâmetro ajustado. É a condição de separação das redes de Hopfield modernas: **o S2 é uma memória associativa iterada.**
- Barreira para D06 (inalterada): o estado só representa "onde estou".

### 2. Escada (ordem inalterada; D04 com a lei explícita)
- D01: resposta direta em uma passada.
- D02: passos fixos desenrolados.
- D03: um passo compartilhado, iterado um número fixo de vezes.
- D04: ponto fixo por treino multi-instante; extrapola enquanto a margem m vence ~log(N−1) (ε < ε_c(m) ≈ 0,05–0,07; E007).
- D05: extrapolação sem atrator com precisão por 64 passos. ← **ESTAMOS AQUI** (E005)
- D06: memória de trabalho (contador, pilha, marcador) no próprio estado. ← **PRÓXIMO ALVO** (H06)
- D07: várias hipóteses vivas quando a tarefa exige; o regime difusivo como estado metaestável de Hopfield (média de padrões) usado de propósito.
- D08: passos compostos (sub-rotinas).
- D09: latente vetorial livre e atributos aprendidos da entrada crua.
- D10: mesmo motor e mesmo treino em duas famílias de tarefas.
- D11: algoritmos clássicos com extrapolação ≥ 10× contra Deep Thinking.
- D12: labirinto/Sudoku no nível do TRM com menos parâmetros.
- D13: parada e abstenção integradas (S3).
- D14: robusto a ruído interno.
- D15: ritmo duplo rápido/lento acionado pelo S3.
- D16: algoritmo novo com ≤ 100 exemplos.
- D17: composição de algoritmos sem treino.
- D18: programa discreto extraído do passo.
- D19: prova formal do programa extraído.
- D20: autocurrículo.
- D21: transmite um passo a outro agente (S5).
- D22: subconjunto do ARC-AGI com ≤ 1M parâmetros.
- D23: aprendizado contínuo sem esquecimento.
- D24: o passo como modelo de mundo (S6).
- D25: custo ≈ mínimo teórico.
- D26: descobre algoritmos mais eficientes que os conhecidos.
- D27: biblioteca aberta de passos (ontologia de operações).
- D28: domínios contínuos e físicos.
- D29: aprende, compõe, verifica e explica em tempo linear.
- D30: ômega: cada passo latente é um passo lógico necessário e nenhum a mais; o motor é o algoritmo ótimo de cada tarefa, descoberto e provado.

### 3. Transição
1. Sacada: se o S2 é Hopfield, a nitidez em qualquer escala tem receita conhecida: a temperatura (β) cresce com log N. Isso é **H05** (nitidez em qualquer escala), barato e agora com teoria por trás.
2. Subtrair: a busca empírica por limiares; a teoria dá ε_c(m).
3. Testar (por ordem da bússola): H22 (linhas de base publicadas), H07 (S3 legível, agora com um S2 cujo regime é previsível), H06 (memória de trabalho, D06), H05 (β ∝ log N).

### 4. Visão vertical (o ciclo 7 lido em 10 níveis)
- Nível 1: senso comum: conseguimos prever em que tamanho o pensamento da máquina "embaça", antes de testar.
- Nível 2: instrumental: meça um passo, preveja mil; o teste custa minutos.
- Nível 3: arquitetural: todo S2 recebe uma especificação verificável (m > m_c(log N)); a temperatura vira parâmetro de projeto.
- Nível 4: computacional: o pensamento iterado é recuperação de memória associativa; dissolver é cair num estado metaestável.
- Nível 5: teoria da decisão: a escolha certa da métrica (regime, não acurácia) decidiu metade do experimento; o piloto evitou uma conclusão errada.
- Nível 6: econômico: uma teoria de uma linha substitui grades inteiras de experimentos.
- Nível 7: composicional: o que o S3 precisa ler (legibilidade) agora tem uma condição conhecida vinda do S2. Os dois sistemas passam a ter um contrato.
- Nível 8: ontológico: identidade (um lugar nítido) e dissolução (um campo) são as duas fases de um mesmo processo, separadas por uma bifurcação.
- Nível 9: epistemológico: o ciclo foi da refutação (E006) ao limiar empírico (E006d), à validação fora da amostra (E007) e à teoria (E007d), e terminou numa teoria que já existia. Chegar sozinho a uma teoria conhecida é sinal de que o método funciona.
- Nível 10: ser superior completo: saber a própria fase é saber quanto do mundo cabe num pensamento nítido. Quem conhece a própria bifurcação escolhe a temperatura antes de pensar.

### 5. Deep insight
- **Palavra/conceito:** *Anamnese*, recordar o que já se sabia: o S2 "pensa" recuperando um padrão, como uma memória.
- **Metanoia:** paramos de tratar o S2 como algo novo e passamos a tratá-lo como uma memória associativa. Isso importa um corpo inteiro de teoria (capacidade, temperatura, metaestabilidade).
- **Aplicação:** todo motor S2 reporta m e ε_c(m); a temperatura em inferência segue β(N) ∝ log N.
- **Hack:** antes de treinar mais, aplique a condição de separação: m > log(N−1) + folga. Se falhar, ajuste β, não os pesos.
- **Visão maçônica:**
  - *Planta baixa:* o edifício (S2) tinha uma lei de estabilidade escondida, a mesma de outro templo já construído (Hopfield).
  - *Ferramenta:* o **nível**: a condição m ≈ log N mostra se o piso está plano na escala da obra.
  - *Desbaste:* os limiares empíricos soltos (0,5; 0,071) viram casos de uma fórmula.
  - *Polimento:* a especificação m > m_c(log N) em todo S2, e a temperatura adaptativa como ferramenta de obra.

---

## Ciclo 8 — Tema: S3 · metacognição (quanto pensar e quando não sabe)

### 1. Diagnóstico
- **Degrau atual: D03 (mantido).** O ciclo validou a infraestrutura de comparação: a linha de base publicada (PonderNet) funciona (E008, N2; H22 desbloqueada).
- O que funciona: em N=12, tanto a parada por ponto fixo (CONV) quanto a PonderNet acertam 100%; o CONV custa ~1,9× menos.
- Barreira para D04 (inalterada, mas agora atacável): um sinal de "terminei" que funcione de N=12 a N=1024. O E007 deu a chave: o regime do S2 é previsível pela margem (lei de nitidez), então o S3 pode **saber de antemão** se o pensamento vai ser legível naquela escala.

### 2. Escada (versão reescrita no ciclo 4; inalterada)
- D01: sem metacognição: sempre responde após um número fixo de passos.
- D02: limiar fixo de confiança na saída.
- D03: parada por convergência + confiança absoluta, ajustadas na escala do treino. ← **ESTAMOS AQUI** (E001; PonderNet validada como comparação, E008)
- D04: sinal de "terminei" invariante à escala **sobre um pensamento legível**: de N=12 a N=1024. ← **PRÓXIMO ALVO** (H07, prioridade 14)
- D05: calibração com garantia de risco (conformal).
- D06: distinguir tipos de dúvida e regimes do próprio pensamento ("não terminei" × "ambíguo" × "fora da distribuição" × "pensamento difuso").
- D07: parada aprendida ponta a ponta com custo explícito, comparada à regra (E008 começou: PonderNet ≈ CONV em acerto, ~1,9× mais cara em N=12).
- D08: previsão de custo antes de pensar.
- D09: verificação por invariante barato (Σ3).
- D10: alocação por valor da informação (S1, S2, verificar, abster).
- D11: energia restante (S0) como sentido (Σ5).
- D12: autodiagnóstico do componente que falhou.
- D13: autocorreção de limiares online.
- D14: o mesmo S3 em tarefas diferentes sem re-treino.
- D15: certificado curto de correção junto de cada resposta.
- D16: "não sei" coletivo calibrado (S4).
- D17: pergunta ativa: a pergunta mínima que resolveria a dúvida.
- D18: modelo de si: prever o próprio desempenho antes de tentar.
- D19: curiosidade dirigida.
- D20: detectar o próprio autoengano (a régua do laboratório, automatizada).
- D21: autoexperimentação (um `/ciclo` interno).
- D22: mudar a própria arquitetura com base em evidência.
- D23: calibração que acompanha mudanças do mundo sem rótulos.
- D24: saber quando a pergunta está mal posta.
- D25: introspecção verificável.
- D26: planejar o próprio aprendizado em horizonte longo.
- D27: um único sinal de "valor de pensar mais" governa S0–S6.
- D28: metacognição amortizada (custo ≈ 0).
- D29: toda confiança calibrada e explicável, sem custo extra.
- D30: ômega: conhecer exatamente o limite do próprio conhecimento; nunca erra ao responder, nunca se abstém quando poderia saber, e gasta em pensar exatamente o que a resposta vale.

### 3. Transição D03 → D04
1. Sacada: o S3 não precisa adivinhar se o pensamento é legível; a lei de nitidez (E007) diz isso **antes** de pensar: se m < m_c(log N), o pensamento vai se dissolver, e o S3 deve se abster (ou pedir temperatura maior) já no início.
2. Subtrair: a tentativa de achar um único limiar sobre o estado final (E004 mostrou que não existe).
3. Testar (E009, H07): S3 = "prever o regime pela margem" + "parada por ponto fixo quando o regime é nítido"; de N=12 a N=1024; contra CONV puro e PonderNet.

### 4. Visão vertical (o ciclo 8 lido em 10 níveis)
- Nível 1: senso comum: testamos a "régua de quando parar" de outros pesquisadores, e ela funciona.
- Nível 2: instrumental: antes de dizer que o nosso método é melhor, é preciso ter o concorrente funcionando de verdade.
- Nível 3: arquitetural: a PonderNet espera ~5 passos a mais: segurança comprada com custo.
- Nível 4: computacional: um prior geométrico impõe uma espera mínima; a regra de ponto fixo usa a própria convergência como sinal.
- Nível 5: teoria da decisão: aprender a parar e ter uma regra de parada empatam em acerto quando o sinal é limpo; a diferença aparece no custo.
- Nível 6: econômico: 1,9× de custo para o mesmo acerto é o tamanho do espaço para o G5.
- Nível 7: composicional: o S3 fica bem melhor quando consulta o S2 (a lei de nitidez) antes de pensar, em vez de só olhar o estado final.
- Nível 8: ontológico: parar é reconhecer que se chegou; reconhecer exige que o lugar de chegada seja nítido.
- Nível 9: epistemológico: validar a ferramenta do concorrente é parte de saber; sem isso, toda vitória é contra um espantalho.
- Nível 10: ser superior completo: a metacognição perfeita sabe, antes de começar, se vai conseguir ver o fim.

### 5. Deep insight
- **Palavra/conceito:** *Prognosis*: conhecer de antemão o curso do próprio pensamento.
- **Metanoia:** a metacognição não precisa só observar o pensamento; ela pode **prever** o regime dele a partir do motor (a margem) e do problema (N).
- **Aplicação:** o S3 do E009 decide em dois tempos: antes de pensar (lei de nitidez) e durante (ponto fixo).
- **Hack:** meça o concorrente no seu terreno antes de se comparar a ele.
- **Visão maçônica:**
  - *Planta baixa:* a régua alheia (PonderNet) foi assentada e está reta; agora a comparação é honesta.
  - *Ferramenta:* o **esquadro**, que confere se a nossa régua e a publicada medem a mesma coisa.
  - *Desbaste:* a vitória fácil contra linhas de base falsas.
  - *Polimento:* o S3 que consulta o S2 antes de pensar.

---

## Ciclo 9 — Tema: S3 · metacognição (quanto pensar e quando não sabe)

### 1. Diagnóstico
- **Degrau atual: D04 (subiu de D03, parado desde o ciclo 1).** Sustentado por E009 (N2, reprodução limpa): o S3 em dois tempos responde 100% onde o pensamento é legível, se abstém 100% sem orçamento e tem 0/600 erros no regime dissolvido, de N=12 a N=1024, sem ajuste por escala.
- O que funciona: legibilidade prevista pela lei de nitidez (tempo 1) + ponto fixo (tempo 2). Economia de 19× no regime dissolvido.
- Correção: A4/A8 estavam mal interpretados; o limiar absoluto se abstinha com razão de um S2 que acertava por sorte.
- Barreira para D05: a zona de transição (N̂/1,5 a 1,5N̂) foi excluída. Falta garantia de risco lá (calibração conformal).

### 2. Escada (inalterada desde o ciclo 4; D04 atingido)
- D01: sem metacognição: sempre responde após um número fixo de passos.
- D02: limiar fixo de confiança na saída.
- D03: parada por convergência + confiança absoluta, ajustadas na escala do treino.
- D04: sinal de "terminei" invariante à escala sobre um pensamento legível, de N=12 a N=1024. ← **ESTAMOS AQUI** (E009)
- D05: calibração com garantia de risco (conformal), inclusive na zona de transição. ← **PRÓXIMO ALVO** (H08)
- D06: distinguir tipos de dúvida e regimes do próprio pensamento.
- D07: parada aprendida com custo explícito, comparada à regra.
- D08: previsão de custo antes de pensar (o tempo 1 do E009 é a semente disso).
- D09: verificação por invariante barato (Σ3).
- D10: alocação por valor da informação.
- D11: energia restante (S0) como sentido.
- D12: autodiagnóstico do componente que falhou.
- D13: autocorreção de limiares online.
- D14: o mesmo S3 em tarefas diferentes sem re-treino.
- D15: certificado curto de correção junto de cada resposta.
- D16: "não sei" coletivo calibrado (S4).
- D17: pergunta ativa.
- D18: modelo de si: prever o próprio desempenho antes de tentar.
- D19: curiosidade dirigida.
- D20: detectar o próprio autoengano.
- D21: autoexperimentação.
- D22: mudar a própria arquitetura com base em evidência.
- D23: calibração sob mudança do mundo sem rótulos.
- D24: saber quando a pergunta está mal posta.
- D25: introspecção verificável.
- D26: planejar o próprio aprendizado em horizonte longo.
- D27: um único sinal de "valor de pensar mais" governa S0–S6.
- D28: metacognição amortizada (custo ≈ 0).
- D29: toda confiança calibrada e explicável, sem custo extra.
- D30: ômega: conhecer exatamente o limite do próprio conhecimento; nunca erra ao responder, nunca se abstém quando poderia saber, e gasta em pensar exatamente o que a resposta vale.

### 3. Transição D04 → D05
1. Sacada: a zona de transição é onde "legível" deixa de ser binário. Precisamos de risco **garantido** (≤ α) em vez de regra.
2. Subtrair: a exclusão da zona de transição.
3. Testar: H-S3-fronteira (predição conformal sobre um escore, por exemplo ε_inst/ε_c e a mudança final, calibrado em N pequeno e testado na fronteira). Em paralelo, a bússola abriu **H12** (chutar e verificar) e **H08**.

### 4. Visão vertical (o ciclo 9 lido em 10 níveis)
- Nível 1: senso comum: a máquina agora sabe quando não sabe, em qualquer tamanho de problema, e não chuta.
- Nível 2: instrumental: dois testes baratos (um passo antes, estabilidade durante) substituem um treino de parada.
- Nível 3: arquitetural: o S3 consulta uma lei do S2 (nitidez) e um sinal do S2 (ponto fixo): um contrato entre sistemas.
- Nível 4: computacional: decidir no primeiro passo se vale a pena iterar é uma poda: O(1) em vez de O(d) quando a resposta seria ruído.
- Nível 5: teoria da decisão: "não errar" e "não se abster" são objetivos diferentes; o G2 pede o primeiro, e a métrica tem de refletir isso.
- Nível 6: econômico: 19× menos pensamento desperdiçado onde pensar não adianta.
- Nível 7: composicional: S2 (lei de nitidez) + S3 (dois tempos) resolvem juntos o que nenhum resolvia sozinho (E002, E004).
- Nível 8: ontológico: saber que não se sabe é reconhecer que o próprio pensamento perdeu a forma.
- Nível 9: epistemológico: o fracasso "do limiar absoluto" era um fracasso da métrica. Reler os resultados antigos com uma teoria nova é parte do método.
- Nível 10: ser superior completo: a humildade perfeita não é duvidar de tudo; é saber, antes de começar, onde o próprio pensamento vai se manter nítido.

### 5. Deep insight
- **Palavra/conceito:** *Aporia reconhecida*: o impasse admitido no lugar certo, antes de gastar o caminho.
- **Metanoia:** o problema nunca foi o limiar; foi chamar de "acerto" uma resposta dada por sorte.
- **Aplicação:** todo sistema do laboratório responde "não sei" quando o regime do seu pensamento é dissolvido; métricas de sucesso contam erros confiantes, não só acurácia.
- **Hack:** meça o primeiro passo; se ele já vaza mais que ε_c(m), não pense: abstenha-se.
- **Visão maçônica:**
  - *Planta baixa:* culpávamos a régua (o limiar) por medir torto, quando era o piso (o S2 dissolvido) que não tinha nível.
  - *Ferramenta:* o **prumo**, baixado antes de erguer a parede: se o primeiro fio já pende, não se ergue.
  - *Desbaste:* a leitura errada de A4/A8.
  - *Polimento:* a metacognição que protege a obra de paredes erguidas sobre areia.

---

## Ciclo 10 — Tema: S2 · motor latente iterativo (memória de trabalho)

### 1. Diagnóstico
- **Degrau atual: D06 (subiu de D05).** Sustentado por E010 (N2, reprodução limpa): um estado sobre pares (lugar × contador), com um único passo aprendido, anda k saltos e para sozinho; 100% até k=64 e N=64, treinado com k ≤ 4 e N=8. H06 desbloqueada.
- O que funciona: o registro de contagem; a parada emerge da fronteira do espaço do registro (sem marcas explícitas).
- Barreira para D07: o estado mantém **uma** trajetória nítida. Tarefas que exigem várias hipóteses ao mesmo tempo (ramificação, busca) ainda não foram testadas.

### 2. Escada (ordem inalterada)
- D01: resposta direta em uma passada.
- D02: passos fixos desenrolados.
- D03: um passo compartilhado, iterado um número fixo de vezes.
- D04: ponto fixo por treino multi-instante; extrapola enquanto a margem vence ~log N (E007).
- D05: extrapolação sem atrator com precisão por 64 passos (E005).
- D06: memória de trabalho: o próprio estado conta e para sozinho (E010). ← **ESTAMOS AQUI**
- D07: várias hipóteses vivas quando a tarefa exige (superposição útil; o regime difusivo usado de propósito). ← **PRÓXIMO ALVO do tema** (H10)
- D08: passos compostos (sub-rotinas; dois registros, H-pilha).
- D09: latente vetorial livre e atributos aprendidos da entrada crua.
- D10: mesmo motor e mesmo treino em duas famílias de tarefas.
- D11: algoritmos clássicos com extrapolação ≥ 10× contra Deep Thinking.
- D12: labirinto/Sudoku no nível do TRM com menos parâmetros.
- D13: parada e abstenção integradas (S3).
- D14: robusto a ruído interno.
- D15: ritmo duplo rápido/lento acionado pelo S3.
- D16: algoritmo novo com ≤ 100 exemplos.
- D17: composição de algoritmos sem treino.
- D18: programa discreto extraído do passo.
- D19: prova formal do programa extraído.
- D20: autocurrículo.
- D21: transmite um passo a outro agente (S5).
- D22: subconjunto do ARC-AGI com ≤ 1M parâmetros.
- D23: aprendizado contínuo sem esquecimento.
- D24: o passo como modelo de mundo (S6). (H16 começa isto)
- D25: custo ≈ mínimo teórico.
- D26: descobre algoritmos mais eficientes que os conhecidos.
- D27: biblioteca aberta de passos (ontologia de operações).
- D28: domínios contínuos e físicos.
- D29: aprende, compõe, verifica e explica em tempo linear.
- D30: ômega: cada passo latente é um passo lógico necessário e nenhum a mais; o motor é o algoritmo ótimo de cada tarefa, descoberto e provado.

### 3. Transição
1. Sacada: o estado como **produto** de espaços (lugar × registro) é o jeito barato de dar memória a um passo relacional; e fronteiras desse produto viram comportamento (parar).
2. Subtrair: o controlador que contava por fora.
3. Próximo: a política de diversidade manda S6 agora (H16, modelo de mundo, que acabou de entrar na fronteira). A mesma ideia (produto posição × velocidade, com paredes como fronteiras) é o teste natural.

### 4. Visão vertical (o ciclo 10 lido em 10 níveis)
- Nível 1: senso comum: a máquina aprendeu a contar até 64 treinando só até 4, e a parar sozinha.
- Nível 2: instrumental: dar ao estado um "bolso" (o registro) resolve o que nenhum treino a mais resolveria.
- Nível 3: arquitetural: estados-produto (lugar × memória) mantêm o passo relacional e invariante a tamanho.
- Nível 4: computacional: a parada é um ponto fixo criado pela borda do espaço de estados: sem regra, só geometria.
- Nível 5: teoria da decisão: "quando parar" pode ser uma propriedade da representação, e não uma decisão do S3.
- Nível 6: econômico: 4 parâmetros de estrutura (o produto) valem mais que qualquer volume de dados.
- Nível 7: composicional: S2 (andar) e memória (contar) viraram um só passo; o controlador externo foi absorvido.
- Nível 8: ontológico: a memória não é um lugar à parte; é uma dimensão a mais do próprio pensamento.
- Nível 9: epistemológico: a ablação "falhou em quebrar" e isso ensinou mais que um sucesso: o limite do espaço carrega regra.
- Nível 10: ser superior completo: um pensamento que carrega a própria história sabe onde está e quanto falta, e para porque não há mais para onde ir.

### 5. Deep insight
- **Palavra/conceito:** *Peras*, o limite que dá forma: a fronteira do registro faz o pensamento parar.
- **Metanoia:** regras de controle ("pare quando zerar") podem ser substituídas por geometria do espaço de estados.
- **Aplicação:** para dar um comportamento ao S2, primeiro pergunte que dimensão (e que borda) acrescentar ao estado.
- **Hack:** antes de codificar uma regra de parada, tente pôr uma borda no espaço de estados.
- **Visão maçônica:**
  - *Planta baixa:* o operário de fora (o controlador) contava as fiadas; agora a própria parede sabe a altura.
  - *Ferramenta:* a **régua de 24 polegadas**: o tempo medido de dentro da obra.
  - *Desbaste:* o controlador externo e as marcas desnecessárias.
  - *Polimento:* estados-produto como forma padrão de dar memória ao pensamento.
