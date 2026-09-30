# E019 — Relatório: a rede treinada só com o ponteiro inventa a distância?

**Veredito: INFORMATIVO (N1, 5 sementes por família).** 3/6 previsões acertaram. Elas foram commitadas **antes de qualquer piloto**, a primeira vez no foco G1.

A resposta curta:
- **Sim, a rede inventa a distância.** No SP, a melhor leitura linear das 18 correlaciona |r| ≥ 0,95 com a distância verdadeira em 5/5 sementes (diagnóstico pós-hoc).
- **A leitura sem supervisão recupera o programa exato em 3/5 sementes.** Regra min-plus, início +∞ e ponteiro argmin x_u + w, sem nenhuma verdade no laço. É abaixo do critério pré-registrado de 4/5.
- **A síntese direta a partir dos ponteiros verdadeiros continua em 5/5.**

## Números
- **Rede treinada só com o ponteiro** (IQM [IC95%]):

  | família | n = 16 | n = 32 | n = 64 |
  |---|---|---|---|
  | SP | 0,940 | 0,868 | **0,758** [0,545; 0,768] |
  | WP | 0,990 | 0,964 | 0,713 [0,294; 0,925] |

  Com o valor supervisionado (E018), a rede SP fazia 0,799 em n = 64. Sem o valor, perde pouco.
- **SP mecanística (nenhuma verdade na escolha):**

  | semente | regra escolhida | reconhecida? | r(leitura, distância) | máx \|r\| nas 18 |
  |---|---|---|---|---|
  | 1900 | min(x_v, min_u x_u + w) | ✅ | 0,942 | 0,953 |
  | 1901 | min / maxf | ✗ | −0,980 | 0,983 |
  | 1902 | min-plus sem manter | ✅ | −0,751 | 0,986 |
  | 1903 | min(x_v, min_u w + ½) | ✗ | 0,870 | 0,979 |
  | 1904 | min-plus sem manter | ✅ | 0,949 | 0,954 |

  - Nas sementes 1901 e 1903 a leitura **é** a distância (|r| ≥ 0,87), mas a regra arredondada saiu errada: a escolha pelo ponteiro da rede teve concordância baixa (0,59 e 0,53).
  - Os programas reconhecidos acertam 1,000 em n = 256; a rede, 0,76 em n = 64.
- **Custo de busca:** a mecanística avaliou 72 programas; a síntese, 10.800 (150× mais). O treino da rede (≈ 570 s) custa mais que a enumeração inteira (≈ 200 s).
- **WP (controle):**
  - a leitura escolhida tem \|r\| < 0,5 em 3/5; máx \|r\| de 0,30 a 0,78;
  - a rede WP guarda algo correlacionado com a largura, mas bem mais fraco que no SP (0,95–0,99);
  - o controle separa as famílias no máximo das 18 (SP ≥ 0,95 em 5/5, WP ≤ 0,78 em 5/5), mas não passou o critério pré-registrado.
- **CPU:** 8104 s (~135 min).

## Previsões (commitadas antes de qualquer piloto, c412a7f)
| # | prob. | resultado |
|---|---|---|
| P1 rede SP n = 64 ≥ 0,75 | 0,60 | ✅ 0,758 (no limite) |
| P2 SP mecanística ≥ 4/5 | 0,35 | 🟥 3/5 |
| P3 SP \|r\| ≥ 0,9 em ≥ 4/5 | 0,45 | 🟥 3/5 (0,751 e 0,870 ficaram abaixo) |
| P4 WP \|r\| < 0,5 em ≥ 4/5 | 0,50 | 🟥 3/5 |
| P5 síntese SP ≥ 4/5 | 0,85 | ✅ 5/5 |
| P6 reconhecidos = 1,000 em n = 256 | 0,95 | ✅ 8/8 |

Brier deste ciclo, só com previsões pré-piloto: 0,127. É pior que os ciclos pós-piloto (~0,05–0,11), o que confirma que aquela calibração estava inflada.

## Ataque
1. **"O máximo das 18 usa a verdade."** Sim, é diagnóstico, não resultado. O que vale como resultado é a leitura escolhida sem verdade: \|r\| ≥ 0,87 em 4/5 sementes, abaixo de 0,9 em duas.
2. **"A escolha pela concordância com o ponteiro da rede é o elo fraco."** Nas duas falhas, a variável estava certa e a regra errada. Duas hipóteses concorrem:
   - o resíduo de fechamento, que já é calculado, escolheria melhor;
   - mais reinícios da leitura ajudariam.

   Não testo agora: seria escolher a regra depois de ver o dado. Vai pré-registrado no E020.
3. **"A síntese direta acha 5/5 e a rede não é necessária."** Continua verdade para a recuperação do programa. O que a rede acrescenta aqui é **científico, não de engenharia**:
   - uma GNN genérica, sem dicas e só com o ponteiro, inventa a distância numa direção linear (5/5, pós-hoc);
   - a regra dela pode ser lida por fechamento dinâmico sem supervisão (3/5).

   Não achei esse fato publicado (Rodionov 2023 e MINAR não extraem variáveis), mas 3/5 com 5 sementes não sustenta anúncio.

## O que aprendemos
- **Sem alvo de valor, a rede inventa a variável oculta que o algoritmo precisa.** No SP ela é a distância, linear no estado. No WP, onde o ponteiro é trivial, a variável é fraca: o controle funciona na direção prevista, mas não no limiar pré-registrado.
- **O gargalo da extração não supervisionada é escolher a regra, não achar a variável.**
- **Calibração honesta (primeira vez só pré-piloto):** Brier 0,127. As previsões pós-piloto eram fáceis demais.

## Próximo (E020, pré-registrado antes de qualquer piloto)
- **H-mec-robusta:** escolha pelo resíduo de fechamento em vez do ponteiro da rede; 3 reinícios por forma; 10 sementes (N2).
- Critério para candidato a novo: reconhecimento ≥ 8/10 no SP e controle WP separado.

> **Correção (E020, ciclo 20).** A saída proposta acima, escolher a regra pelo resíduo de fechamento, foi **refutada**: 0/10, contra 6/10 da escolha pelo ponteiro, nas mesmas redes.
> A rede chega ao ponto fixo do Bellman-Ford por outra dinâmica. Pela regra de parada, a linha de leitura não supervisionada está encerrada.
