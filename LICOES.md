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
5b2. **Dissolução é normalização** (E013): o argmax do passo não depende de N; o que se perde é a nitidez da softmax. A lei dá a temperatura mínima (β = 1 + ln((N−1)/(N_tr−1))/m) sem re-treino. Antes de chamar uma afiação de mecanismo, compare com β constante e argmax.
5b3. **Superposição é forma, não temperatura** (E014): softmax da soma (produto) é biestável para hipóteses desiguais (dissolve ou o vencedor leva tudo, em qualquer β); soma de softmaxes (mistura, normalizar por origem) guarda todas com os mesmos pesos. Normalize por origem para propagar crenças; por destino para escolher.
5b4. **Extrapolar = cancelar a descida da normalização, medida no próprio dado** (E016, E017): o soft-min desce por ln(grau)/β (empates) e deriva nas arestas baratas (1/w_min). Com β = κ·ln(g)/(a·w_min) e **nenhum viés aditivo livre**, o caminho mínimo extrapola 20×. O treino em n pequeno prefere compensar com viés, e o viés quebra em n grande.
5b5. **Antes de extrair da rede, tente sintetizar sem ela** (E018). Na mesma linguagem de regras, a síntese direta dos pares entrada → verdade achou os programas prováveis do SP e do WP (10/10). A rota da rede acertou 5/10: SP sim, WP não. Uma rede boa em ponteiro pode ser infiel nos valores, e a extração herda os erros dela. A rota "rede → extração → prova" só vale onde a síntese não alcança. Acurácia de ponteiro não mede fidelidade ao algoritmo; meça o erro da regra contra a rede.
5b6. **Sem alvo de valor, a rede inventa a variável oculta** (E019). Treinada só com o ponteiro, a GNN guarda a distância numa direção linear (|r| ≥ 0,95 em 5/5). Ela pode ser achada sem verdade, exigindo que a leitura feche numa regra simbólica (z^{t+1} ≈ R(z^t)). O gargalo é escolher a regra, não achar a variável. E previsão pré-piloto é outra coisa: Brier 0,127 contra 0,05–0,11 das pós-piloto.
5c. Nosso "contínuo" é uma distribuição sobre nós, quase simbólica. Conclusões sobre latente contínuo *livre* ainda não foram testadas.

## Sobre o S3 (metacognição)
6. **"Não sei" no lugar certo resolve a escala** (E009, N2). No regime dissolvido o S2 acerta só por sorte (~50%): o S3 tem de se abster ali. A antiga lição "limiares fixos param de funcionar em N grande" era leitura errada: a métrica contava acertos de sorte (A4/A8 reinterpretados).
6b. **Meça erros confiantes, não só acurácia.** PonderNet e ponto fixo acertam 100% no regime legível e erram 51% no dissolvido.
7. **Legibilidade antes de metacognição.** O S3 só lê "terminei" com segurança se o regime do S2 for estável.
8. Um sinal que força confiança (cristalizar) pode **esconder** a dúvida em vez de medi-la.

8b. **Valide o concorrente antes de se comparar a ele** (E008: PonderNet reimplementada reproduz o artigo; só então a comparação de custo vale).
8c. Um pré-requisito do concorrente pode não existir na sua arquitetura (M006: sem overthinking, o progressive loss não tem o que corrigir). Pilote antes de pré-registrar.

8d. **Comportamentos de parada podem emergir de fronteiras do espaço de estados** (E010: sem marcas de "zero", o contador para igual). Antes de ensinar uma regra, veja se a geometria do registro já a impõe.

8e. **Extrapolação perfeita é suspeita:** procure o atributo que a garante (E011: distância à parede truncada tornou a física uma tabela local; a extrapolação em L veio do desenho).

8f. **Um S1 rápido não compõe; decomponha e meça q.** Com o acerto por passo q, o acerto de k passos é ≈ q^k (E012, JEV). Investir em q vale mais que em k.
8g. **Confiança calibrada é o recurso mais valioso de um S1** (E012: 0/516 erros com p ≥ 0,9). O S3 deve ler a confiança antes de ler a resposta.
8h. Sistemas externos não determinísticos: grave as respostas brutas, analise do arquivo e reproduza reprocessando (`lab.reproduzir --dados`).

## Sobre comunicação (S5)
9. **Discretizar a mensagem dá robustez enorme; discretizar o pensamento não ajudou** (E003 vs E002).

9b. **O código ótimo depende do recurso escasso** (E015): com energia fixa por mensagem, espalhar (one-hot/simplex) é quase ótimo e comprimir abaixo de N/2 dimensões custa robustez (Rankin); com amplitude fixa por canal, comprimir ganha com folga. Declare o custo antes de pedir "menos bits".

## Sobre o processo
10. **Estou superconfiante.** Acerto de previsões 38% (21 previsões); Brier 0,42 no ciclo 5, **pior que responder sempre 50%** (0,25); no ciclo 6, com probabilidades moderadas, caiu para 0,25; no ciclo 7, com piloto, 0,11; no ciclo 8, 0,04; no ciclo 9, 0,07; ciclo 10, 0,05; ciclo 11, 0,03; ciclo 12, 0,12 (subestimei a queda do JEV com N); ciclo 13, 0,05; ciclo 14, 0,13; ciclo 15, 0,18; ciclo 16, 0,16 (subestimei o DT); ciclo 17, 0,05. **Pilotos com o modelo completo são o que mais melhorou a calibração.** Até o Brier cair abaixo de 0,25, use probabilidades entre 0,35 e 0,65 salvo evidência direta, e escreva *por que* o resultado pode sair ao contrário.
11. Diagnósticos pós-hoc baratos (minutos) explicaram todas as surpresas até agora. Faça-os sempre que um resultado contradisser a expectativa.
11b. **Grades que dependem de uma quantidade estimada (como N*) precisam de um smoke com o modelo completo antes de congelar** (E006: a grade começou alta demais e P5 nunca rodou).
11c. Variáveis vêm da teoria; constantes vêm dos dados. Não congele um limiar intuitivo (0,5) sem medi-lo.
11d. **Em tarefa-atrator, meça o regime (nitidez), não a acurácia**: a acurácia acerta "por sorte" com o estado dissolvido (E007: 25/30 pelo regime contra 16/30 pela acurácia).
11e. **Antes de chamar algo de lei nova, procure a teoria clássica com a mesma forma** (E007d era Hopfield moderno).
12. Quando um resultado contradisser um registro antigo, **corrija o registro antigo** na hora.
12a. **Examine a pergunta antes de construir** (ciclo 14): se o verificador de uma solução é o próprio resolvedor exato, a questão de custo é vazia; troque de família.
12c. **Amortização verificada só paga quando resolver ≫ verificar** (M009): verificar custa Ω(entrada). Se o resolvedor clássico já é quase linear (caminho mínimo), o chute do S1 não tem o que economizar. A H24 pertence à busca.
12b. **Guarda de commit pelo código de saída:** `python3 -m lab.checar >/dev/null && git commit ...`. Um `| tail` no meio engole o erro (ciclo 12).
13. **Decisão compilada:** o que foi feito à mão 2 vezes vira ferramenta na terceira. O S2 (o pesquisador) compila reflexos para o laboratório; não repete deliberação.
