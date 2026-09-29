# LIÇÕES — o meta-caderno (ler no início de todo ciclo)

Curto de propósito (operador de resumo do AIDE). **Reescrever, não só
acrescentar**: se uma lição nova contradiz uma antiga, trocar. Máximo ~15 itens.

## Sobre tarefas
1. **Procure o atalho trivial antes de celebrar.** E001: com uma só raiz, bastava achar o nó que aponta para si.
2. **Tarefas-atrator escondem erros.** Na "achar a raiz", um salto errado ainda chega à raiz certa. Para medir acúmulo de erro, use tarefas em que todo erro é fatal (T2).
3. **Varie uma coisa por vez.** E003: d e N variavam juntos e a conclusão Q3 saiu confundida.

## Sobre o S2 (pensamento latente)
4. **O S2 é uma memória associativa tipo Hopfield** (E007, N2; E007d, N1). Ele se dissolve numa bifurcação quando a margem m deixa de vencer ~log(N−1); o vazamento de um passo prevê N_c fora da amostra. Sempre reporte m e ε(N) na maior escala de teste. Para escalar, ajuste a temperatura (β ∝ log N) antes de retreinar.
5. **A softmax já é um cristalizador suave.** Antes de adicionar um mecanismo, teste se o sistema já o tem embutido (E005: a cristalização explícita foi desnecessária).
5b. **A tarefa de treino decide a precisão.** Tarefas-atrator produzem margens pequenas (erro não custa nada no treino).
5c. Nosso "contínuo" é uma distribuição sobre nós, quase simbólica. Conclusões sobre latente contínuo *livre* ainda não foram testadas.

## Sobre o S3 (metacognição)
6. **Limiares absolutos não escalam** (E002, E004). Nenhum sinal fixado em N=12 funcionou em N≥64.
7. **Legibilidade antes de metacognição.** O S3 só lê "terminei" com segurança se o regime do S2 for estável.
8. Um sinal que força confiança (cristalizar) pode **esconder** a dúvida em vez de medi-la.

8b. **Valide o concorrente antes de se comparar a ele** (E008: PonderNet reimplementada reproduz o artigo; só então a comparação de custo vale).
8c. Um pré-requisito do concorrente pode não existir na sua arquitetura (M006: sem overthinking, o progressive loss não tem o que corrigir). Pilote antes de pré-registrar.

## Sobre comunicação (S5)
9. **Discretizar a mensagem dá robustez enorme; discretizar o pensamento não ajudou** (E003 vs E002).

## Sobre o processo
10. **Estou superconfiante.** Acerto de previsões 38% (21 previsões); Brier 0,42 no ciclo 5, **pior que responder sempre 50%** (0,25); no ciclo 6, com probabilidades moderadas, caiu para 0,25; no ciclo 7, com piloto, 0,11; no ciclo 8, 0,04. **Pilotos com o modelo completo são o que mais melhorou a calibração.** Até o Brier cair abaixo de 0,25, use probabilidades entre 0,35 e 0,65 salvo evidência direta, e escreva *por que* o resultado pode sair ao contrário.
11. Diagnósticos pós-hoc baratos (minutos) explicaram todas as surpresas até agora. Faça-os sempre que um resultado contradisser a expectativa.
11b. **Grades que dependem de uma quantidade estimada (como N*) precisam de um smoke com o modelo completo antes de congelar** (E006: a grade começou alta demais e P5 nunca rodou).
11c. Variáveis vêm da teoria; constantes vêm dos dados. Não congele um limiar intuitivo (0,5) sem medi-lo.
11d. **Em tarefa-atrator, meça o regime (nitidez), não a acurácia**: a acurácia acerta "por sorte" com o estado dissolvido (E007: 25/30 pelo regime contra 16/30 pela acurácia).
11e. **Antes de chamar algo de lei nova, procure a teoria clássica com a mesma forma** (E007d era Hopfield moderno).
12. Quando um resultado contradisser um registro antigo, **corrija o registro antigo** na hora.
