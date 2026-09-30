# E018 — Relatório: extrair da rede genérica ou sintetizar direto?

**Veredito: INFORMATIVO (N1, 5 sementes por família).** H-rede-supérflua é **aceita pelo critério pré-registrado** (P1 e P6). A leitura honesta, porém, é dividida por família:

| família | a rota rede → extração → prova funciona? | a rede é necessária? |
|---|---|---|
| **SP (min,+)** | **sim, 5/5**, nas rotas mecanística e comportamental | não: a síntese direta também acerta 5/5 |
| **WP (max,min)** | **não, 0/5**: a rede leva a extração a um programa errado | não: só a síntese acerta (5/5) |

## Números (IQM [IC95%], acurácia de ponteiro)

| família | rede n=16 | rede n=32 | rede n=64 | programa reconhecido em n=256 |
|---|---|---|---|---|
| SP | 0,952 [0,941; 0,966] | 0,921 [0,883; 0,932] | 0,799 [0,773; 0,830] | **1,000** (todas as rotas) |
| WP | 0,984 [0,909; 0,994] | 0,956 [0,869; 0,985] | 0,892 [0,713; 0,964] | **1,000** (síntese) |

- **Programas reconhecidos como a relaxação exata do semianel** (regra, ponteiro e início):

  | família | mecanística | comportamental | síntese direta |
  |---|---|---|---|
  | SP | 5/5 | 5/5 | 5/5 |
  | WP | 0/5 | 0/5 | 5/5 |

  Somando as famílias: síntese 10/10 contra comportamental 5/10, Fisher p = 0,033.
- **O que as rotas da rede extraem no WP:** `media(x_v, média_u min(½·x_u, w) + ½)` e variantes, com erro 0,037–0,044 contra a saída da rede.
  - A relaxação correta erra **0,050–0,106** contra a mesma saída.
  - A rede WP é imprecisa nos valores de um jeito que uma regra de média imita melhor que a regra max-min.
- **No SP, o erro do semianel contra a rede é 0,016–0,043.** A rede SP aproxima o Bellman-Ford melhor do que a rede WP aproxima o max-min, mesmo tendo acurácia de ponteiro menor.
- **P4:** os 20 programas reconhecidos acertam 1,000 em n = 256 (16× o treino). A própria rede cai para 0,80 (SP) e 0,89 (WP) em n = 64.
- **CPU:** 6997 s (~117 min; ~36 min de parede). Passou do teto de 60 min, como estava declarado.

## Previsões (todas pós-piloto)
| # | prob. | resultado |
|---|---|---|
| P1-SP síntese ≥ 4/5 | 0,90 | ✅ 5/5 |
| P1-WP síntese ≥ 4/5 | 0,90 | ✅ 5/5 |
| P2-SP comportamental ≥ 4/5 | 0,55 | ✅ 5/5 |
| P2-WP comportamental ≥ 4/5 | 0,20 | 🟥 0/5 |
| P3-SP mecanística ≥ 4/5 | 0,45 | ✅ 5/5 |
| P3-WP mecanística ≥ 4/5 | 0,15 | 🟥 0/5 |
| P4 reconhecidos = 1,000 em n = 256 | 0,95 | ✅ (20/20) |
| P5-SP rede < 0,99 em n = 64 | 0,97 | ✅ 0,799 |
| P5-WP rede < 0,99 em n = 64 | 0,90 | ✅ 0,892 |
| P6 síntese > comportamental | 0,75 | ✅ 10/10 contra 5/10 |

## Ataque (3 objeções mais fortes)
1. **"A rede é supérflua."** Confirmado: nas duas famílias a síntese direta, sem rede, acha o programa provável. O sucesso da rota da rede no SP não prova que a rede foi útil, só que ela não atrapalhou.
   - A rota "rede genérica → extração → prova" só se justifica numa família em que a síntese direta **não** alcança a regra: a linguagem de regras é grande demais para enumerar, ou o programa tem estado auxiliar que a verdade de entrada → saída não revela.
   - Esse é o próximo teste.
2. **"A mecanística é a comportamental disfarçada."** Nas 10 execuções a mecanística escolheu a mesma forma e os mesmos coeficientes que a comportamental.
   - As transições internas geram candidatos certos no SP, mas a escolha final é por circuito fechado contra a saída.
   - A contribuição mecanística própria não foi isolada. Um braço sem a escolha comportamental ficou por fazer.
3. **"O WP tem ponteiro trivial"** (aresta mais pesada = pai válido, árvore geradora máxima; achado no smoke e declarado).
   - Por isso os programas errados do WP ainda dão 1,000 de ponteiro, e a acurácia de ponteiro não serve de métrica ali. Só o reconhecimento da regra de valor discrimina, e ele discriminou (0/5).

## O que aprendemos
- **No SP, uma rede genérica sem dicas guarda nas transições internas a relaxação exata do Bellman-Ford.** A extração automática a recupera com o início correto em 5/5 sementes, e a prova por redução ao teorema clássico vale para todo n.
  - Isso preenche a lacuna do G1 para uma família, **mas a síntese direta faz o mesmo sem rede**. O valor para o mundo é baixo enquanto a síntese bastar.
- **Uma rede boa em ponteiro não é necessariamente fiel ao algoritmo nos valores.** A rede WP acerta 0,98 dos ponteiros em n = 16, mas os seus valores são melhor explicados por uma regra de média.
  - Extrair da rede herda os erros dela; a extração comportamental é tão boa quanto a fidelidade da rede.
- **Para o foco G1:** o próximo experimento precisa de uma família em que a síntese direta falhe por tamanho de busca, e só então medir se a rede encurta a busca.

## Correções em registros antigos
Nenhuma. O E017 (a lei de temperatura) fica como está: ele usa estrutura dada à mão, e este experimento usa rede genérica.
