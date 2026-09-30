# M010 — Pilotos do G1: rede genérica sem dicas, sonda e extração (ciclo 18)

Os scripts rodaram no rascunho da sessão e foram copiados para cá **sem mudança**. Os caminhos dentro deles apontam para o rascunho, e os pesos `.pt` não foram versionados. Servem de registro, não de reprodução exata. Nenhum deles vale como resultado: sementes 0, 3–11 e 1890–1896, fora das faixas de teste.

| script | o que fez | achado |
|---|---|---|
| `g1_piloto.py` | MPNN genérico (mensagem MLP, agregação max) em Bellman-Ford, n = 16 → 64 | Treino longo colapsou (0,316) até usar lr 5e-4 + corte de gradiente 1,0 + 100 lotes fixos. Depois disso: 0,957 / 0,926 / 0,826 em n = 16 / 32 / 64. A agregação soma explodiu fora da distribuição. |
| `g1_sonda.py` | Correlação do valor decodificado a cada passo com o BF de k saltos | O estado acompanha o BF de k saltos (alinhamento algorítmico emergente, como no MINAR). |
| `g1_extrair.py` | Ajuste das 18 regras nas transições da rede, em circuito aberto | Escolheu min(x_v, min_u x_u + w) com θ ≈ [0,975; 0,954; 0,019] → [1, 1, 0]. A margem sobre a 2ª regra foi pequena (MSE 0,00049 contra 0,00067). |
| `e018_dbg.py` | Rede do E018, 4000 passos, SP e WP, 1 fio | SP 0,943 / 0,887 / 0,815; WP 0,980 / 0,975 / 0,948. ~570 s de CPU por família. A extração v1, com início decodificado de h0, falhou nas duas famílias. |
| `ext2.py` | Três rotas (mecanística, comportamental, síntese direta) nas redes acima | SP: as três acham a regra do semianel; as da rede usam início 1,0. WP: a síntese acha o programa exato; as rotas da rede escolhem `media`/`minf`, que imita os erros da rede (erro 0,043 contra ela). |
| `ptrchk.py` | Checagem do ponteiro corrigido | WP: argmax_u w_uv (aresta mais pesada) acerta 1,000, empatado com o ponteiro do semianel. É o atalho da árvore geradora máxima. |

**Lição.** O teste que decide a rota vem antes da rota. Aqui, a síntese direta, sem rede, é a linha de base que qualquer revisor pediria. Ela ficou pré-registrada como braço do E018.
