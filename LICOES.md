# LIÇÕES — o meta-caderno (ler no início de todo ciclo)

Curto de propósito (operador de resumo do AIDE). **Reescrever, não só
acrescentar**: se uma lição nova contradiz uma antiga, trocar. Máximo ~15 itens.

## Sobre tarefas
1. **Procure o atalho trivial antes de celebrar.** E001: com uma só raiz, bastava achar o nó que aponta para si.
2. **Tarefas-atrator escondem erros.** Na "achar a raiz", um salto errado ainda chega à raiz certa. Para medir acúmulo de erro, use tarefas em que todo erro é fatal (T2).
3. **Varie uma coisa por vez.** E003: d e N variavam juntos e a conclusão Q3 saiu confundida.

## Sobre o S2 (pensamento latente)
4. **O regime do pensamento depende de N relativo a e^margem** (E004d, E005d, N1). Abaixo de N* = e^margem, o S2 anda um salto por passo; acima, dissolve em difusão. Sempre reporte a margem aprendida e N*.
5. **A softmax já é um cristalizador suave.** Antes de adicionar um mecanismo, teste se o sistema já o tem embutido (E005: a cristalização explícita foi desnecessária).
5b. **A tarefa de treino decide a precisão.** Tarefas-atrator produzem margens pequenas (erro não custa nada no treino).
5c. Nosso "contínuo" é uma distribuição sobre nós, quase simbólica. Conclusões sobre latente contínuo *livre* ainda não foram testadas.

## Sobre o S3 (metacognição)
6. **Limiares absolutos não escalam** (E002, E004). Nenhum sinal fixado em N=12 funcionou em N≥64.
7. **Legibilidade antes de metacognição.** O S3 só lê "terminei" com segurança se o regime do S2 for estável.
8. Um sinal que força confiança (cristalizar) pode **esconder** a dúvida em vez de medi-la.

## Sobre comunicação (S5)
9. **Discretizar a mensagem dá robustez enorme; discretizar o pensamento não ajudou** (E003 vs E002).

## Sobre o processo
10. **Estou superconfiante.** Acerto de previsões 38% (21 previsões); Brier 0,42 no ciclo 5, **pior que responder sempre 50%** (0,25). Até o Brier cair abaixo de 0,25, use probabilidades entre 0,35 e 0,65 salvo evidência direta, e escreva *por que* o resultado pode sair ao contrário.
11. Diagnósticos pós-hoc baratos (minutos) explicaram todas as surpresas até agora. Faça-os sempre que um resultado contradisser a expectativa.
12. Quando um resultado contradisser um registro antigo, **corrija o registro antigo** na hora.
