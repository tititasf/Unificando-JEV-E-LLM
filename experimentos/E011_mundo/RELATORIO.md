# E011 — Relatório: modelo de mundo com o mesmo passo (S6)

**Veredito: PROMOVER.** Habilidade **H16 desbloqueada**; **primeiro nó de S6** (S6 → D01).
Nível: **N2** (pré-registrado, 10 sementes, sementes de teste derivadas do commit `078a745`, reprodução limpa, guarda OK).
**Novidade: baixa**, e com uma ressalva forte (ver "Atalho trivial"): é o princípio das Interaction Networks / Graph Network Simulators em miniatura, com o mesmo passo do S2.

## Previsões
| # | Previsto | Prob. | Obtido | Status |
|---|---|---|---|---|
| P1 | MUNDO: erro por passo < 1% em L = 8, 32, 64 | 0,80 | 0,0000 nos três | ✅ |
| P2 | MUNDO: trajetórias 100% certas em L=64, IQM ≥ 0,95 | 0,80 | 1,00 | ✅ |
| P3 | SEM_PAREDE erro por passo em L=64 > 5% e MUNDO melhor com p < 0,01 | 0,80 | 0,129; p = 0,0002 | ✅ |
| P4 | SEM_REBOTE erro por passo em L=8 > 30% | 0,90 | 0,813 | ✅ |

**Brier: 0,03.**

## O que foi mostrado
1. Um passo relacional (a mesma forma do S2) sobre o estado-produto (posição × velocidade) aprende a física da caixa (movimento e rebote) com trajetórias de 8 passos em L=8, e prevê 16 passos **sem nenhum erro** em caixas 8× maiores (L=64, 256 estados), 10/10 sementes.
2. **O rebote precisa do atributo local "distância à parede à frente":** sem ele, 13–15% de erro por passo, concentrado nos choques (o erro cai com L porque os choques ficam mais raros).
3. A tarefa exige o rebote: física sem rebote erra 81% em L=8.
4. A lei de nitidez se manteve: 256 estados em 16 passos compostos, sem dissolução.

## Atalho trivial (regra 7), dito sem rodeio
Com os atributos dados (dx, relação de velocidade, velocidade atual, distância à parede truncada em 2),
a física inteira é uma **tabela local de 12 casos** (4 velocidades × 3 distâncias). Qualquer
tabela que acerte esses casos generaliza para qualquer L, porque os atributos não dependem de L.
Logo, **a extrapolação em L é garantida pelo desenho dos atributos, não descoberta pelo modelo.**
O que o experimento testa de fato: (a) o passo aprende a tabela a partir de trajetórias; (b) a
softmax fica nítida o bastante em 256 estados para compor 16 passos sem acumular erro; (c) a
peça de parede é necessária. H16 pede exatamente isso, mas o degrau seguinte (atributos
aprendidos, várias partículas, mundo 2D, ruído) é onde está o risco real.

## Revisor hostil
1. *"Os atributos entregam a resposta."* Sim, em grande parte (acima). Declarado no PREREG. Não conta como avanço em G4 além do primeiro degrau.
2. *"PERSISTÊNCIA 0,92 em L=8, não 1,0?"* A comparação usa o estado completo (x, v). Em L=8 a órbita é periódica com período 2(L−1)/|v| = 7 ou 14 passos, então dentro de 16 passos o estado volta exatamente ao inicial em t = 7, 14 (|v|=2) ou t = 14 (|v|=1); "nada muda" acerta nesses instantes (~8%). Em L ≥ 32 o período passa de 16 e o acerto vai a zero. Coerente.
3. *"Sem linha de base publicada."* Correto: não reimplementamos um GNS; a pergunta aqui era só se o mesmo passo serve. Uma comparação com um GNS mínimo fica para H20.

## Hipóteses semeadas
- **H-mundo-cru:** atributos aprendidos a partir da posição crua (sem "distância à parede" dada); é o teste que faltou.
- **H-mundo-2p:** duas partículas que colidem (interação, o caso das Interaction Networks).
- **H-imaginar:** usar o modelo de mundo para planejar (alcançar uma posição-alvo) → ponte para H17.
