# E012 — Pré-registro: o JEV como S1 externo real, sozinho e iterado pelo S2

**Escrito antes de rodar. Não editar depois da primeira execução completa.**
Trilha: E (união S1+S2+S3). Átomos/sínteses: 1.1, 1.5, Σ (S2 compila/itera S1; S3 para por ponto fixo). Nível de partida: N0 (nenhum dado do JEV).
Habilidade-alvo: **H26** (JEV medido como S1 externo real). Nó pai: **E005** (T2) · Operador: **RASCUNHO**. Degrau-alvo: S1 D01 (primeiro S1 externo medido).
Escolha: a bússola põe H05 no topo; sobreposição justificada pela política "infra que desbloqueia" (PLANO §3): o JEV é o S1 real do laboratório (pedido central do usuário), recém-acessível, e este experimento é pré-requisito de fato para a H24 com S1 externo. Critério da H26 revisto **antes** deste pré-registro (versão antiga guardada em `criterio_antigo`).

## Hipóteses
- **H1 (o JEV é um S1 de um salto):** em uma passada, o JEV resolve T2 com k = 1 e cai para perto do acaso com k ≥ 2.
- **H2 (a união S2∘S1):** um controlador que chama o JEV um salto por vez (S2 iterando S1) recupera o acerto com k ≥ 2, e o acerto segue a lei multiplicativa acc(k) ≈ q^k, com q = acerto por salto.
- **H3 (S3 por ponto fixo):** em T1, iterar o JEV um salto por vez e parar quando a resposta não se move supera a pergunta em uma passada.

## Relação com a literatura
- Transformers em uma passada não compõem k saltos arbitrários: limite tipo Fano para raciocínio multi-salto em uma passada (arXiv 2509.21199); "Hopping Too Late" (2406.12775).
- Decompor em subtarefas de uma passada e encadear (chain-of-thought) resolve a composição, com o erro amplificado como (1−ε)^k (mesmas fontes; teoria de CoT).
- **Novidade: baixa.** É a caracterização de um S1 comercial novo (JEV, set/2026) e uma replicação do princípio. Não há reimplementação de linha de base publicada (não se aplica: o JEV não é treinado aqui).

## Piloto (declarado)
- Piloto (sementes 1290, 4 instâncias por célula): T2 k=1: 4/4 (N=8), 3/4 (N=32); k ≥ 2: 1/16; T1 uma passada: 2/16. Primeira pergunta de k=2 respondida com o atalho de um salto π(s).
- Smoke do avaliador (sementes 1290–1291, 1 instância por célula; não vale): 96 registros, 0 erros de API, acerto por salto ≈ 0,93 (N=8), 0,90 (N=32), 0,67 (N=64); erros de UMA com k ≥ 2 raramente iguais a π(s) (1/14). O smoke fez a métrica da P5 trocar de p1 (uma célula) para q (todos os saltos), antes deste commit.

## Montagem
- Tarefas: T2 (permutação, k saltos; `E005/tarefa_t2.exemplo`), N ∈ {8, 32, 64}, k ∈ {1, 2, 4, 8}. T1 (floresta com raízes distratoras; `E001/mlu.make_example`), N ∈ {8, 32, 64}, d ∈ {1, 3, 5}.
- Codificação: estado JSON (`ponteiros`/`pai`, `inicio`, `k`) + pergunta `Choice` com os N rótulos. Modelo `jev-latest` (o modelo servido é gravado em cada chamada).
- Braços:
  - **UMA** (JEV em uma passada).
  - **REPETIR** (a mesma pergunta de novo; T2, k ∈ {1, 2}).
  - **ITER** (T2: k chamadas de um salto, encadeadas pelo controlador).
  - **ITER_PF** (T1: chamadas de um salto até a resposta não se mover; orçamento de 12 chamadas; sem ponto fixo = errado).
  - **ACASO** (1/N).
  - **UM_SALTO** (responde π(s) / pai(s), exato).
- Referência interna do S2 aprendido: A10/E005 (100% em T2 até k = 64, N = 128); não é re-rodada.
- Respostas brutas em `respostas_jev.jsonl`. O avaliador regenera instâncias e verdade a partir das sementes e só lê a escolha do JEV; confere o encadeamento dos passos. Reprodução: `python3 -m lab.reproduzir experimentos/E012_jev --dados=respostas_jev.jsonl`.

## Previsões e critérios de morte
| # | Previsão | Prob. | Morte se |
|---|---|---|---|
| P1 | UMA T2 k=1: acerto ≥ 0,80 em N = 8, 32 e 64 | 0,45 | — |
| P2 | UMA T2 k ∈ {2,4,8}: acerto ≤ 0,25 em N = 32 e 64 (as 6 células) | 0,75 | alguma célula ≥ 0,60 → **H1 morta** |
| P3 | ≥ 40% dos erros de UMA em T2 k ≥ 2 são o atalho π(s) | 0,25 | — |
| P4 | ITER > UMA em T2 k=4 (somando os N), Fisher p < 0,01 | 0,85 | ITER ≤ UMA ou p ≥ 0,05 → **H2 morta** |
| P5 | acc_ITER(k) dentro de ±0,15 de q(N)^k em ≥ 7 das 9 células (N × k ∈ {2,4,8}) | 0,45 | ≤ 3 de 9 → a lei multiplicativa não descreve o JEV |
| P6 | T1: ITER_PF > UMA (somando células), Fisher p < 0,01 | 0,80 | ITER_PF ≤ UMA → **H3 morta** |
| P7 | UMA T2: p(escolha) média maior nos acertos que nos erros, permutação p < 0,01 | 0,70 | — |
| P8 | Erros confiantes (p(escolha) ≥ 0,9) ≤ 5% dos erros de UMA (T1+T2) | 0,60 | — |
| P9 | UMA × REPETIR concordam em ≥ 80% em T2 k=1 | 0,60 | — |

**H26 desbloqueada** (N1) se a coleta for válida: 0 registros faltando, erros de API ≤ 2% das chamadas, um único modelo servido, reprodução IDÊNTICA a partir das respostas gravadas.

## Sementes e poder
- Sementes de teste: `lab.sementes.derivar(base_teste(__file__), 10)` (derivadas do commit deste PREREG); 3 instâncias por semente e célula → 30 por célula.
- `n_para_diferenca(0,1; 0,5) = 30`: 30 por célula distinguem acaso/atalho (≈ 0,1) de 0,5 com α = 0,01 e poder 0,8. As comparações das P4/P6 somam células (90–270 por braço).
- Custo: ~3.300 chamadas, ~0,2 s cada, 8 em paralelo → ~3 min de parede; ~2–3 M tokens de entrada. CPU local desprezível.

## Guarda do avaliador
```
experimentos/E012_jev/e012.py            : ebdee73c7f6fb45f
experimentos/E005_t2_salto/tarefa_t2.py  : b62e43a6a77ab648
experimentos/E001_mlu/mlu.py             : 601604873fae9691
lab/sementes.py                          : 4a5e4da1269f9b77
lab/estat.py                             : 40af21b3e5c3d582
lab/jev.py                               : 81e83eec18a89053
lab/reproduzir.py                        : beb29b62ffa35eac
```

## Ameaças conhecidas
- O JEV não é determinístico (medido na P9); `jev-latest` pode mudar de versão entre execuções (o modelo servido é gravado e checado).
- A codificação (JSON + instrução em português) afeta o desempenho; outra codificação pode dar outro número. É uma medida do JEV **nesta interface**, não um limite do modelo.
- O controlador ITER lê só a escolha do JEV, sem verificar o salto (verificar custaria o mesmo que resolver); o ITER_PF usa a checagem de ponto fixo, que é O(1) sobre a própria resposta.
