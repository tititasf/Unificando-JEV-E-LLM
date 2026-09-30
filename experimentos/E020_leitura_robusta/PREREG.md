# E020 — Pré-registro: leitura robusta da variável oculta (escolha pelo resíduo de fechamento, N2)

**Escrito antes de rodar. Não editar depois da primeira execução completa.**
Trilha: B (T3). Foco G1 (CRITICA ciclo 20: APROFUNDAR, com regra de parada). Nível de partida: N1 (E019).
Habilidade-alvo: **H19**. Nó pai: **E019** · Operador: **MELHORAR**. Degrau-alvo: S2 D18.

## Previsões: commitadas antes de qualquer piloto (`PREVISOES.md`, commit 3d45084)
O smoke (300 passos, 2 sementes, redes subtreinadas; SP n = 64 dá 0,148) só validou o código. As previsões não mudaram.

| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1 | SP, escolha nova: min-plus reconhecido em ≥ 8/10 | 0,35 | — |
| P2 | SP, escolha nova: \|r\| ≥ 0,9 em ≥ 8/10 | 0,45 | — |
| P3 | WP (controle): \|r\| < 0,5 em ≥ 8/10 | 0,35 | — |
| P4 | SP, escolha nova: reconhecido em ≥ 7/10 | 0,50 | < 7/10 → **a linha de leitura não supervisionada é encerrada** (regra de parada) |
| P5 | escolha nova ≥ antiga + 2, nas mesmas redes | 0,45 | — |
| P6 | reconhecidos: 1,000 em n = 256 | 0,95 | < 1 → furo no reconhecimento |
| P7 | rede SP n = 64 ≥ 0,75 | 0,55 | — |

**Candidato a novo** (regra 20, no nível N2): P1 e P3 passam.

## Hipótese
No E019, a leitura escolhida pela concordância com o ponteiro da rede errou a regra em 2/5 sementes em que a variável estava certa. A escolha pelo **resíduo de fechamento da regra arredondada**, que é o próprio critério que definiu a leitura, recupera o min-plus em ≥ 8/10.

## Relação com a literatura
Como no E019: Rodionov & Prokhorenkova 2023 (sem dicas, sem extração), MINAR (circuitos), Cranmer 2020 (regressão simbólica supervisionada), MIPS (RNN). Novidade esperada: média, se P1 e P3 passarem; baixa, caso contrário.

## Montagem
- **Redes:** as do E019 (importadas, com hash guardado), só com o ponteiro, 4000 passos, n = 16.
- **Leitura:**
  - por forma: 3 reinícios (`e019.ajusta_leitura`, 300 passos), fica o de menor resíduo;
  - normalização e arredondamento (`e019.normaliza`).
- **Escolha nova:**
  - forma: menor resíduo de fechamento normalizado da regra arredondada na leitura normalizada;
  - início: o programa mais próximo da leitura final da rede (n = 32, 64 passos);
  - ponteiro: concordância com a rede.
- **Escolha antiga:** `e019.melhor_programa` (concordância de ponteiro), como ablação pareada.
- **Sem verdade em nenhuma escolha.** O diagnóstico pós-escolha é o Pearson com a variável verdadeira.
- A síntese direta não roda (5/5 em E018 e E019), por custo; está declarado.

## Sementes e poder
- **Treino:** 2000–2009 (N2, 10 por família). **Teste:** `lab.sementes.derivar(base_teste(__file__), 10)`.
- Com k = 10, `ic_proporcao(8, 10)` ≈ [0,49; 0,94]. Separa 0,8 de 0,3 (`n_para_diferenca(0,3; 0,8; 0,05)` ≈ 15, no limite). As 10 sementes são o N2 mínimo.
- **Custo:** ~16 min de CPU por (semente, família) × 20 ≈ 320 min de CPU, ~80 min de parede. Acima do teto, pela mesma razão do E018 e do E019.

## Guarda do avaliador
```
{
 "experimentos/E020_leitura_robusta/e020.py": "42f5c325232100d4",
 "experimentos/E019_variavel_oculta/e019.py": "c11fd0cfccd5c536",
 "experimentos/E018_extracao/e018.py": "f6bb6bab1251c388",
 "lab/tarefas_clrs.py": "fd2b3258eb55e4f4",
 "lab/sementes.py": "4a5e4da1269f9b77",
 "lab/estat.py": "40af21b3e5c3d582"
}
```

## Ameaças conhecidas
- **A escolha nova nasceu da análise das falhas do E019** (desenho pós-hoc). As sementes são novas e as previsões vieram antes de qualquer piloto.
- A linguagem de regras contém o min-plus.
- **O resíduo de fechamento pode favorecer formas quase constantes.** A normalização pela variância mitiga isso, sem garantia.
