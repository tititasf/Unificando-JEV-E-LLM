# BÚSSOLA — árvore de habilidades e goals

*Gerado por `python3 -m lab.bussola` a partir de `registro/habilidades.json` e da árvore de experimentos. Não editar à mão.*
Narrativa e critérios dos goals: [`GOALS.md`](GOALS.md).

🟩 desbloqueada (com evidência) · 🟨 na fronteira (pode ser atacada agora) · ⬜ trancada

## Goals (estrelas-guia)

| goal | progresso | faltam | nível exigido |
|---|---|---|---|
| **G1** Pensador de tamanho livre, com prova | ██████░░ 6/8 | H11, H19 | N4 |
| **G2** Saber exatamente quando nao sabe | ████░░░ 4/7 | H08, H12, H24 | N3 |
| **G3** Uma lingua que nasce, ensina e pensa | ████░░ 4/6 | H14, H15 | N4 |
| **G4** Descobrir regras de um mundo desconhecido | ███████░░░ 7/10 | H08, H17, H20 | N4 |
| **G5** Pensar com o custo certo | ████░░░ 4/7 | H12, H18, H24 | N3 |
| **G6** Auto-aperfeicoamento recursivo demonstrado | █░ 1/2 | H21 | N3 |

## Fronteira: o que atacar agora (maior prioridade primeiro)

Prioridade = (1 + habilidades que dependem desta + 3 × goals que ela abre) ÷ custo.

| # | habilidade | prioridade | abre | goals | hipóteses na fila |
|---|---|---|---|---|---|
| 1 | 🟨 **H24** S2 compila S1 sob a corte do S3 (amortizacao verificada) (S1+S2+S3) | 4.5 | 2 | G2, G5 | H-compilar |
| 2 | 🟨 **H08** Metacognicao calibrada com garantia (S3) | 4.0 | 1 | G2, G4 | H-S3-fronteira |
| 3 | 🟨 **H17** Planejar a partir da meta (S6) | 2.5 | 1 | G4 | H-Sigma4 |
| 4 | 🟨 **H21** Laboratorio que se aperfeicoa (RSI medido) (LAB) | 2.0 | 0 | G6 | — |
| 5 | 🟨 **H11** Algoritmos classicos extrapolam (T3) (S2) | 1.7 | 1 | G1 | — |
| 6 | 🟨 **H14** Lingua emergente composicional (S5) | 1.7 | 1 | G3 | H-Sigma6 |
| 7 | 🟨 **H09** Latente vetorial livre (S2) | 0.5 | 0 | — | H-latente-livre |
| 8 | 🟨 **H25** Coexistencia: regra cooperativa emergente (S4) (S4+S5) | 0.5 | 0 | — | H-comuns |

## Linha do tempo de desbloqueios (meta-métrica do G6)

- ciclo 3: **H02** Mensagem simbolica robusta
- ciclo 4: **H03** Laboratorio com regua, laco e arvore
- ciclo 5: **H01** Passo latente que extrapola
- ciclo 7: **H04** Lei de nitidez validada
- ciclo 8: **H22** Linhas de base publicadas validadas
- ciclo 9: **H07** Metacognicao legivel em qualquer escala
- ciclo 10: **H06** Memoria de trabalho latente
- ciclo 11: **H16** Modelo de mundo com o mesmo passo
- ciclo 12: **H26** JEV medido como S1 externo real
- ciclo 13: **H05** Nitidez em qualquer escala
- ciclo 14: **H10** Varias hipoteses vivas (busca latente)
- ciclo 15: **H13** Codigo minimo corretor
- ciclo 16: **H23** Protocolo CLRS reimplementado com linha de base
- taxa: 13 habilidades em 16 ciclos = 0.81 por ciclo

## Árvore (pré-requisitos → habilidade)

- 🟩 **H01** Passo latente que extrapola · S2 · S2 D05 · requer: raiz — por E005  
  critério: Passo iterado treinado em N<=12, k<=4 acerta >=95% em k>=16x e N>=10x, numa tarefa sem atrator, 10 sementes (≥ N2)
- 🟩 **H02** Mensagem simbolica robusta · S5 · S5 D04 · requer: raiz — por E003  
  critério: Mensagem discreta vence a analogica sob ruido por >=20 pontos, p<0,01, conhecimento fragmentado entre agentes (≥ N2)
- 🟩 **H03** Laboratorio com regua, laco e arvore · LAB · - · requer: raiz — por M001, M003  
  critério: Pre-registro, guarda por hash, arvore de experimentos, meta-metricas funcionando (≥ N0)
- 🟩 **H22** Linhas de base publicadas validadas · LAB · - · requer: H01 — por E008  
  critério: PonderNet reimplementada reproduz o efeito publicado (passos aprendidos crescem com a dificuldade, Spearman >= 0,8, com acuracia mantida). Deep Thinking (progressive loss) implementado e testado; overthinking AUSENTE no motor estruturado (piloto M006: 100% com T=200 com e sem progressive loss), efeito a reavaliar quando o latente for livre (H09). (≥ N1)
- 🟩 **H23** Protocolo CLRS reimplementado com linha de base · LAB · T3 · requer: H22 + H06 — por E016  
  critério: Geradores e resolvedores exatos (BFS, Bellman-Ford) testados; um motor aprendido e a linha de base Deep Thinking avaliados no protocolo n=16 -> n=64 com acuracia de ponteiros e IC (≥ N1)
- 🟩 **H04** Lei de nitidez validada · S2 · fronteira S2 D04 · requer: H01 — por E007  
  critério: Limiar de vazamento eps_c congelado preve N_c de >=30 sementes novas dentro de 1,5x, e o papel de d (por passo x acumulado) decidido (≥ N2)
- 🟩 **H05** Nitidez em qualquer escala · S2 · S2 D05+ · requer: H04 — por E013  
  critério: Um mecanismo (temperatura adaptativa, treino de precisao ou cristal) mantem eps < eps_c ate N=4096 sem re-treino, em T1 e T2 (≥ N2)
- 🟩 **H06** Memoria de trabalho latente · S2 · S2 D06 · requer: H01 — por E010  
  critério: O proprio estado carrega um contador/pilha: resolve T2 com k na entrada (sem controlador contando) e extrapola k 16x (≥ N2)
- 🟩 **H07** Metacognicao legivel em qualquer escala · S3 · S3 D04 · requer: H04 — por E009  
  critério: Mesmo sinal de parada, fixado em N=12, responde >=99% quando da e se abstem >=99% quando nao da, de N=12 a N=1024 (≥ N2)
- 🟨 **H08** Metacognicao calibrada com garantia · S3 · S3 D05-D06 · requer: H07 + H22  
  critério: Risco seletivo <= alfa garantido (conformal) sob mudanca de escala e de tarefa; E-AURC ~0 em 2 familias (≥ N2)
- 🟨 **H09** Latente vetorial livre · S2 · S2 D09 · requer: H04 + H06  
  critério: Estado = vetor livre (nao distribuicao sobre nos); mede-se acumulo de ruido e o ganho da quantizacao em T2 (≥ N2)
- 🟩 **H10** Varias hipoteses vivas (busca latente) · S2 · S2 D07 · requer: H06 — por E014  
  critério: Tarefa com ramificacao (ex.: alcancabilidade com varios caminhos): o estado mantem >1 candidato e acerta onde o cristal falha (≥ N2)
- 🟨 **H11** Algoritmos classicos extrapolam (T3) · S2 · S2 D11 · requer: H05 + H06 + H22 + H23  
  critério: BFS e caminho minimo: >=95% em 10x o tamanho do treino, batendo a linha de base Deep Thinking com IC (≥ N2)
- ⬜ **H12** Chutar e verificar · S1+S3 · S3 D09 · requer: H07 + H24  
  critério: S1 chuta, S3 verifica com invariante barato, S2 so quando falha: domina a fronteira de Pareto acc x custo do S2 sozinho (≥ N2)
- 🟩 **H13** Codigo minimo corretor · S5 · S5 D05 · requer: H02 — por E015  
  critério: Codigo com menos bits por passo que o one-hot e >= robustez sob ruido; curva bits x acc medida (≥ N2)
- 🟨 **H14** Lingua emergente composicional · S5 · S5 D11-D12 · requer: H13  
  critério: Agentes inventam do zero um codigo discreto que generaliza a combinacoes nunca vistas (>=90% zero-shot) (≥ N2)
- ⬜ **H15** Ensinar um passo por mensagens · S5+S2 · S5 D16 / S2 D21 · requer: H14 + H06  
  critério: Agente A transmite seu passo latente a B so por mensagens discretas; B atinge >=95% com 10x menos exemplos que aprendendo sozinho (≥ N2)
- 🟩 **H16** Modelo de mundo com o mesmo passo · S6 · S6.1 / S2 D24 · requer: H06 — por E011  
  critério: O passo aprendido preve o proximo estado de um ambiente simples com erro < 1% por 16 passos (≥ N2)
- 🟨 **H17** Planejar a partir da meta · S6 · S6.2-6.3 · requer: H16 + H10  
  critério: Busca bidirecional/rollouts latentes: passos ~d/2 e >=95% em tarefas de planejamento com efeito atrasado (≥ N2)
- ⬜ **H18** Orcamento como sentido · S0+S3 · S3 D11 · requer: H12 + H22  
  critério: Energia restante como entrada do S3 domina o limiar fixo na fronteira de Pareto acc x custo (≥ N2)
- ⬜ **H19** Programa extraido e provado · S2 · S2 D18-D19 · requer: H05 + H11  
  critério: Extracao automatica do automato equivalente ao passo aprendido + prova (verificador exaustivo/indutivo) de correcao para todo N (≥ N3)
- ⬜ **H20** Aprendiz de regras desconhecidas · S2+S3+S6 · T6 · requer: H17 + H08 + H10  
  critério: Em ambientes interativos de brinquedo com regras ocultas (estilo ARC-AGI-3), descobre a regra e resolve >=80% com <=1M parametros (≥ N3)
- 🟨 **H21** Laboratorio que se aperfeicoa (RSI medido) · LAB · - · requer: H03  
  critério: Em >=10 ciclos, mudancas META causam queda mensuravel de ciclos-por-degrau e Brier < 0,15, avaliadas em ciclos posteriores (≥ N0)
- 🟨 **H24** S2 compila S1 sob a corte do S3 (amortizacao verificada) · S1+S2+S3 · S1 1.2 / S3 D08 · requer: H01 + H07  
  critério: Um S1 de uma passada destilado das respostas do S2 responde com latencia O(1); o S3 verifica/roteia e so aciona o S2 quando o S1 nao e confiavel. Custo medio >= 5x menor que o S2 sozinho, mantendo 0 erros confiantes (inclusive fora da distribuicao), em 2 familias de tarefas (≥ N2)
- 🟨 **H25** Coexistencia: regra cooperativa emergente (S4) · S4+S5 · S4 4.4 · requer: H02  
  critério: N agentes com recurso comum limitado e mensagens simbolicas convergem para uma regra de uso que atinge >= 90% do bem-estar social otimo, contra agentes egoistas (tragedia dos comuns), sem controle central (≥ N2)
- 🟩 **H26** JEV medido como S1 externo real · S1(JEV)+S2 · S1 1.x · requer: H01 — por E012  
  critério: JEV respondendo T1 (raiz) e T2 (k saltos) como Choice, respostas brutas gravadas e reprocessaveis, em >= 3 tamanhos e >= 10 sementes: curva acerto x tamanho x profundidade, ECE e erros confiantes por verificador exato, contra acaso, atalho de um salto e o JEV iterado por um controlador S2 (referencia interna do S2 aprendido: A10/E005) (≥ N1)

## Mapa de dependências

```
✔ H01 Passo latente que extrapola
  ✔ H22 Linhas de base publicadas validadas
    ✔ H23 Protocolo CLRS reimplementado com linha de base
      ◐ H11 Algoritmos classicos extrapolam (T3)
        · H19 Programa extraido e provado
    ◐ H08 Metacognicao calibrada com garantia
      · H20 Aprendiz de regras desconhecidas
    ◐ H11 Algoritmos classicos extrapolam (T3) (↑ já mostrado)
    · H18 Orcamento como sentido
  ✔ H04 Lei de nitidez validada
    ✔ H05 Nitidez em qualquer escala
      ◐ H11 Algoritmos classicos extrapolam (T3) (↑ já mostrado)
      · H19 Programa extraido e provado (↑ já mostrado)
    ✔ H07 Metacognicao legivel em qualquer escala
      ◐ H08 Metacognicao calibrada com garantia (↑ já mostrado)
      · H12 Chutar e verificar
        · H18 Orcamento como sentido (↑ já mostrado)
      ◐ H24 S2 compila S1 sob a corte do S3 (amortizacao verificada)
        · H12 Chutar e verificar (↑ já mostrado)
    ◐ H09 Latente vetorial livre
  ✔ H06 Memoria de trabalho latente
    ✔ H23 Protocolo CLRS reimplementado com linha de base (↑ já mostrado)
    ◐ H09 Latente vetorial livre (↑ já mostrado)
    ✔ H10 Varias hipoteses vivas (busca latente)
      ◐ H17 Planejar a partir da meta
        · H20 Aprendiz de regras desconhecidas (↑ já mostrado)
      · H20 Aprendiz de regras desconhecidas (↑ já mostrado)
    ◐ H11 Algoritmos classicos extrapolam (T3) (↑ já mostrado)
    · H15 Ensinar um passo por mensagens
    ✔ H16 Modelo de mundo com o mesmo passo
      ◐ H17 Planejar a partir da meta (↑ já mostrado)
  ◐ H24 S2 compila S1 sob a corte do S3 (amortizacao verificada) (↑ já mostrado)
  ✔ H26 JEV medido como S1 externo real
✔ H02 Mensagem simbolica robusta
  ✔ H13 Codigo minimo corretor
    ◐ H14 Lingua emergente composicional
      · H15 Ensinar um passo por mensagens (↑ já mostrado)
  ◐ H25 Coexistencia: regra cooperativa emergente (S4)
✔ H03 Laboratorio com regua, laco e arvore
  ◐ H21 Laboratorio que se aperfeicoa (RSI medido)
★ G1 Pensador de tamanho livre, com prova ⇐ H19
★ G2 Saber exatamente quando nao sabe ⇐ H08, H12
★ G3 Uma lingua que nasce, ensina e pensa ⇐ H15
★ G4 Descobrir regras de um mundo desconhecido ⇐ H20
★ G5 Pensar com o custo certo ⇐ H18, H24
★ G6 Auto-aperfeicoamento recursivo demonstrado ⇐ H21
```
