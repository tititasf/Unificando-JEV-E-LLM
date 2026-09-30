# E020 — Relatório: leitura robusta da variável oculta

**Veredito: MATAR (N2, negativo, 10 sementes por família).** A regra de parada pré-registrada (P4: < 7/10) disparou.

| método | SP reconhecido | observação |
|---|---|---|
| escolha nova (resíduo de fechamento) | **0/10** | |
| escolha antiga (concordância de ponteiro, ablação pareada) | **6/10** | |

- Discordantes: só a antiga 6, só a nova 0; Fisher p = 0,011.
- Nenhum dos dois métodos chega a 7/10. **A linha "ler a regra da rede sem supervisão" fica encerrada**, como combinado na CRITICA do ciclo 20.

## Números
- **Rede treinada só com o ponteiro** (IQM):

  | família | n = 16 | n = 32 | n = 64 |
  |---|---|---|---|
  | SP | 0,949 | 0,898 | 0,754 [0,691; 0,792] |
  | WP | 0,988 | 0,900 | 0,445 [0,174; 0,778] |

- **Escolha nova (SP):**
  - a forma mais escolhida foi min(x_v, min_u ½·x_u + w + ½) ou min/maxf, quase sempre com início 0;
  - \|r\| com a distância ≥ 0,9 em só 4/10.
  - O resíduo de fechamento favorece regras **contrativas** (coeficiente ½ no estado) que imitam os transientes dos primeiros passos da rede, não a relaxação.
- **Escolha antiga (SP):** 6/10 reconhecidas. Somando com o E019: **9/15** = 0,60, IC95% [0,36; 0,80]. Os programas reconhecidos acertam 1,000 em n = 256.
- **Variável oculta (diagnóstico pós-hoc; usa a verdade, não vale como resultado pré-registrado):**

  | família | máximo \|r\| das 18 leituras | leitura |
  |---|---|---|
  | SP | ≥ 0,93 em 9/10; mínimo 0,84 | a distância está lá |
  | WP | ≤ 0,65 em 10/10 | a variável é fraca |

  As faixas não se sobrepõem. É consistente com o E019 (SP ≥ 0,95 em 5/5; WP ≤ 0,78).
- **CPU:** 18.802 s (~5,2 h de CPU, ~80 min de parede).

## Previsões (commitadas antes de qualquer piloto, 3d45084)
| # | prob. | resultado |
|---|---|---|
| P1 nova ≥ 8/10 | 0,35 | 🟥 0/10 |
| P2 \|r\| ≥ 0,9 em ≥ 8/10 | 0,45 | 🟥 4/10 |
| P3 WP \|r\| < 0,5 em ≥ 8/10 | 0,35 | 🟥 7/10 |
| P4 nova ≥ 7/10 (parada) | 0,50 | 🟥 0/10 → **linha encerrada** |
| P5 nova ≥ antiga + 2 | 0,45 | 🟥 0 contra 6 (o contrário) |
| P6 reconhecidos = 1,000 em n = 256 | 0,95 | ✅ |
| P7 rede SP n = 64 ≥ 0,75 | 0,55 | ✅ 0,754 |

Brier (pré-piloto): **0,158**. Errei a direção do efeito principal: previ melhora e a mudança piorou tudo.

## Ataque
1. **"A escolha nova foi mal implementada."** Possível, mas o sintoma é específico e consistente em 10/10: regras com coeficiente ½ no estado e início 0.
   - O resíduo de fechamento é baixo para qualquer regra que aproxime a trajetória da leitura.
   - A trajetória da rede **não** é a do Bellman-Ford passo a passo: o ponto fixo coincide com a distância, a dinâmica não.
   - Isso é uma descoberta, não só um bug: **a rede computa o mesmo ponto fixo por outro caminho.**
2. **"A escolha antiga passou 6/10: não seria para continuar?"** Não. Ela também fica abaixo de 7/10, e ela usa o ponteiro da rede, ou seja, é comportamental.
   - O E018 já mostrou que a síntese direta sem rede faz 100% do trabalho comportamental. A regra de parada vale para as duas.
3. **"A variável oculta existe; isso não é o resultado?"** É um fato robusto (SP 9/10 ≥ 0,93 contra WP ≤ 0,65), mas **pós-hoc**: foi medido com a verdade.
   - Relatado como diagnóstico.
   - Para virar resultado precisaria de pré-registro próprio, e há trabalho próximo: sondas lineares em NAR mostram que as redes codificam as variáveis do algoritmo.

## O que aprendemos
- **A rede genérica sem dicas chega ao mesmo ponto fixo que o Bellman-Ford, mas por outra dinâmica.** Ler a regra pelos passos internos falha (0/10); ler pelo comportamento funciona em 60%, mas a síntese direta faz isso sem rede.
- **A distância existe no estado final** (pós-hoc, SP ≥ 0,93 contra WP ≤ 0,65), mas **o algoritmo, como sequência de passos, não está lá** para ser lido.
- **A regra de parada funcionou:** 1 ciclo, veredito claro, sem negociar depois de ver os dados.

## Correções em registros antigos
- **E019:** a conclusão "o gargalo é escolher a regra" continua válida.
- A saída proposta ali (escolher pelo resíduo de fechamento) foi refutada aqui. Entra em `obsoletos.txt`.
