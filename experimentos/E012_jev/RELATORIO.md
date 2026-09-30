# E012 — Relatório: o JEV como S1 externo real, sozinho e iterado pelo S2

**Veredito: PROMOVER.** Habilidade **H26 desbloqueada**; primeiro nó do tema **S1 com um S1 externo real** (S1 → D01).
Nível: **N2** (pré-registrado, 10 sementes × 3 instâncias por célula, sementes derivadas do commit `3d70ea0`, respostas brutas gravadas, reprodução IDÊNTICA a partir delas, guarda OK).
Validade da coleta: 3.298 chamadas, **0 erros**, 0 registros faltando, um único modelo servido (`jev-1.13.0`); 2,63 M tokens de entrada e 0,93 M de saída.
**Novidade: baixa** (caracterização de um S1 comercial novo + replicação do princípio "decompor em passos de uma passada").

## Previsões
| # | Previsto | Prob. | Obtido | Status |
|---|---|---|---|---|
| P1 | UMA T2 k=1 ≥ 0,80 em todo N | 0,45 | 0,90 · 0,83 · **0,63** (N=64) | 🟥 |
| P2 | UMA T2 k≥2 ≤ 0,25 em N=32,64 | 0,75 | máx. 0,10 | ✅ |
| P3 | ≥ 40% dos erros de UMA (k≥2) = atalho π(s) | 0,25 | 46/243 = 0,19 | 🟥 |
| P4 | ITER > UMA em k=4, p < 0,01 | 0,85 | 48/90 vs 7/90, p = 1,6e-11 | ✅ |
| P5 | acc_ITER(k) ≈ q^k (±0,15) em ≥ 7/9 células | 0,45 | 8/9 | ✅ |
| P6 | T1: ITER_PF > UMA, p < 0,01 | 0,80 | 149/270 vs 16/270, p = 1,3e-38 | ✅ |
| P7 | p(escolha) maior nos acertos | 0,70 | 0,65 vs 0,22, p = 0,0002; ECE 0,074 | ✅ |
| P8 | erros confiantes (p ≥ 0,9) ≤ 5% dos erros | 0,60 | **0/516** | ✅ |
| P9 | UMA × REPETIR concordam ≥ 80% (k=1) | 0,60 | 83/90 = 0,92 | ✅ |

**Brier: 0,12.** H1, H2 e H3 sobrevivem.

## O que foi mostrado
1. **O JEV é um S1 de um salto (H1).** Em uma passada: um salto 0,90 / 0,83 / 0,63 (N = 8/32/64); dois ou mais saltos ≈ acaso (≤ 0,10 em N ≥ 32). T1 em uma passada falha até com d = 1 (0,10 / 0,00 / 0,00): o JEV responde o nó de início ou **outra** raiz, em vez de seguir o ponteiro.
2. **O próprio salto se dissolve com N.** Acerto por chamada de um salto: 0,94 (N=8), 0,84 (N=32), 0,71 (N=64) em T2; 0,90 / 0,81 / 0,71 em T1. Uma única consulta de ponteiro piora com o tamanho: é a mesma forma da lei de nitidez do nosso S2 (A11) e de Veličković et al. (2025), agora num S1 comercial.
3. **A união S2∘S1 funciona e é previsível (H2).** Chamar o JEV um salto por vez recupera o que a passada única perde (k=4: 0,53 contra 0,08), e o acerto segue a lei multiplicativa acc(k) ≈ q^k em 8/9 células. Com q medido, o custo de confiabilidade de um problema de k saltos é calculável **antes** de rodar.
4. **O S3 por ponto fixo funciona sobre o JEV (H3).** T1 iterado com parada quando a resposta não se move: 0,55 contra 0,06.
5. **O JEV sabe quando não sabe.** p(escolha) média de 0,65 nos acertos e 0,22 nos erros, ECE 0,074 e **zero erros com p ≥ 0,9 em 516 erros**. É o insumo que faltava para um S3 seletivo sobre o S1 (G2).
6. Não determinismo baixo: 92% de concordância na mesma pergunta repetida (k=1).

## Atalhos triviais achados (regra 7)
- **Atalho de zero saltos:** em T2 N=8 k=8, UMA acerta 0,40 porque responde o nó de início em 24/30; 11 dos 12 acertos são casos em que π⁸(s) = s (ciclos curtos numa permutação de 8). Não é composição.
- **Atalho de um salto (P3):** só 19% dos erros de UMA são π(s). Em N = 8, k = 2, porém, 11/29 são. O JEV não segue um atalho único: em N grande, erra "para qualquer lado".

## Anatomia das falhas do ITER_PF em T1 (121 falhas em 270)
- 49 saltos errados;
- 32 **falsos pontos fixos** (o JEV diz que um nó não-raiz aponta para si, e o controlador para cedo);
- 26 raízes não reconhecidas (na raiz, o JEV responde outro nó, e o controlador segue andando);
- 14 orçamentos esgotados.

As duas classes do meio são falhas do **reconhecimento de auto-ponteiro**, não do salto: alvo direto para o S3.

## Revisor hostil
1. *"É só o prompt."* Possível. A medida vale para esta interface (JSON + instrução em português, `Choice` com N rótulos). Declarado no PREREG. Outra codificação é um experimento novo.
2. *"O ITER não é mérito do JEV, é do controlador."* Exatamente: é a tese da união (S2 compila o procedimento, S1 executa passos). O mérito medido é a previsibilidade (lei q^k), que permite ao S2 planejar.
3. *"30 por célula é pouco."* Para as perguntas pré-registradas as diferenças são enormes (p ≤ 1e-11); as curvas por célula têm IC largo e estão reportadas.

## Hipóteses semeadas
- **H-JEV-seletivo (→ H24/H08):** usar p(escolha) por salto como S3: repetir ou abster quando p < limiar. Previsão: zero erros confiantes com cobertura útil, e a lei q^k vira q_efetivo^k com q_efetivo > q.
- **H-JEV-autoponteiro:** perguntar "o nó x aponta para si?" como `Noul` separado, para corrigir os 58 falsos/omitidos pontos fixos.
- **H-JEV-nitidez:** o acerto por salto cai com N como na lei de nitidez; ajustar q(N) = f(N) e ver se ε_c tem análogo no JEV (ponte S1 ↔ S2).
