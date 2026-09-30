# E019 — Pré-registro: a rede treinada só com o ponteiro inventa a distância? Leitura não supervisionada da variável oculta

**Escrito antes de rodar. Não editar depois da primeira execução completa.**
Trilha: B (T3). Foco G1 (CRITICA ciclo 19: APROFUNDAR). Nível de partida: N0.
Habilidade-alvo: **H19**. Nó pai: **E018** · Operador: **MELHORAR**. Degrau-alvo: S2 D18.

## Previsões: commitadas ANTES de qualquer piloto (`PREVISOES.md`, commit c412a7f)
Nenhum piloto da rota nova rodou antes das previsões. O smoke (300 passos, 2 sementes) rodou depois delas e não as mudou. Ele só validou o código:

| | |
|---|---|
| rede SP em n = 64 | 0,146 (subtreinada) |
| síntese SP | 2/2 |
| leitura SP | \|r\| ≈ 0,5 |

| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1 | rede SP só com ponteiro, n = 64: IQM ≥ 0,75 | 0,60 | < 0,5 → a rede sem valor não extrapola; a leitura perde sentido fora da distribuição |
| P2 | SP mecanística reconhecida (regra min-plus [1,1,0], início +∞, ponteiro argmin x_u + w) em ≥ 4/5 | 0,35 | — |
| P3 | SP: \|r(leitura escolhida, distância verdadeira)\| ≥ 0,9 em ≥ 4/5 | 0,45 | < 0,5 em todas → a rede não guarda a distância numa direção linear |
| P4 | WP (controle): \|r(leitura, largura)\| < 0,5 em ≥ 4/5 | 0,50 | — |
| P5 | SP: síntese direta a partir dos ponteiros verdadeiros reconhecida em ≥ 4/5 | 0,85 | — |
| P6 | todo programa reconhecido: 1,000 em n = 256 | 0,95 | < 1 → furo no reconhecimento |

- **Leitura central:** P1 e P3 juntas dizem se a rede **inventa** a distância; P2, se a regra dela é exatamente o min-plus.
- **Se P2 falhar e P5 passar:** a síntese continua suficiente e a rede, supérflua, como no E018.
- **Se P2 passar:** é um resultado com candidatura a novo. Uma rede genérica, só com o ponteiro, tem variável e regra identificadas sem supervisão.
  - Ainda assim não bate a síntese em recuperação. O ganho é o custo de busca (candidatos avaliados: 72 contra 10.800) e a identificação da variável.

## Relação com a literatura
- **Rodionov & Prokhorenkova 2023** (*NAR without intermediate supervision*, NeurIPS): sem dicas, com regularização autossupervisionada. Não extraem variável nem regra.
- **MINAR** (2025/26): circuitos, não variáveis simbólicas.
- **Cranmer et al. 2020:** regressão simbólica das mensagens, supervisionada.
- **MIPS (2024):** extração de programa em RNN, com variáveis inteiras por agrupamento.
- **O que é novo aqui:** a leitura escalar é achada por **fechamento dinâmico** (z^{t+1} ≈ R(z^t), sem alvo) numa GNN sem dicas, e o resultado é conferido contra a variável oculta verdadeira.
  - Busca de novidade: 2 buscas no ciclo 19, sem trabalho idêntico.
  - Novidade esperada: média, se P2 e P3 passarem; baixa, caso contrário.

## Montagem
- **Rede:** a do E018 (importada, hash guardado), treinada **só** com a perda de ponteiro por pais válidos. 4000 passos, n = 16, T ~ U{8..24}.
- **Mecanística:**
  - trajetórias h^t em 8 grafos de n = 16 e 8 de n = 32, 16 passos;
  - para cada forma R (18): leitura linear z = h·a + b₀ e coeficientes, 300 passos de Adam, pelo resíduo de fechamento normalizado pela variância de z;
  - normalização: z' = (z − z_fonte) / escala (coeficiente do peso), reajuste e arredondamento a ½;
  - programa com fonte 0 e início em {−∞, +∞, 0, 1};
  - escolha pela concordância com os ponteiros da rede, em n = 32 (8 grafos).
- **Síntese direta (atalho não neural, pergunta 9 da crítica):** enumeração conjunta de 18 formas × 75 coeficientes × 4 inícios × fonte {0, 1} × 18 ponteiros, escolha pela validade contra os ponteiros verdadeiros.
- **Diagnóstico pós-escolha:** Pearson entre a leitura escolhida (passo 32) e a variável verdadeira, nos nós não-fonte; também o máximo das 18.
- **Rede:** acurácia de ponteiro em n = 16, 32 e 64 (64 grafos). **Programas:** Python puro em n = 16, 64 e 256 (20 grafos).
- **Linha de base publicada:** o protocolo difere do CLRS oficial (o amostrador ER tem p = 0,5 fixo). A comparação numérica externa fica para o H-G1-externo, então este nó **não** é `externo`.

## Sementes e poder
- **Treino:** 1900–1904 (N1, 5 por família). **Teste:** `lab.sementes.derivar(base_teste(__file__), 5)`.
- `n_para_diferenca(0,2; 0,9; alfa = 0,05)` = 7: com 5 sementes por família só se separam efeitos grandes. Está declarado.
- **Custo:** ~15 min de CPU por (semente, família) × 10 ≈ 150 min de CPU, ~40 min de parede. Acima do teto de 60 min, pela mesma razão do E018.

## Guarda do avaliador
```
experimentos/E019_variavel_oculta/e019.py : c11fd0cfccd5c536
experimentos/E018_extracao/e018.py        : f6bb6bab1251c388
lab/tarefas_clrs.py                       : fd2b3258eb55e4f4
lab/sementes.py                           : 4a5e4da1269f9b77
lab/estat.py                              : 40af21b3e5c3d582
```

## Ameaças conhecidas
- **A linguagem de regras contém o min-plus.** A leitura só acha o que a linguagem pode dizer.
- **Leitura linear:** a rede pode guardar a distância de forma não linear (monótona). Nesse caso P3 falha mesmo com a variável presente. O diagnóstico "máximo das 18" dá uma cota.
- **A escolha da mecanística usa os ponteiros da rede.** Se a rede erra, a escolha herda o erro, como no E018.
- **Invariância a deslocamento do min-plus:** a fonte é fixada em 0 por construção, o que não perde generalidade no SP. No WP o controle é só a correlação.
