# Unificando Sistema 1 + 2 (+3): contexto, reflexão e plano de exploração

## 1. Contexto (o que foi conversado, sem enfeite)

| Termo | O que é, de fato |
|---|---|
| **Transformer** | Arquitetura de rede neural (atenção + camadas), 2017. |
| **LLM** | Transformer grande treinado para gerar o próximo token. Pensa "em voz alta" (texto). |
| **"JEV" / modelo de decisão tipada** | A ideia: um modelo que **não gera texto**, só devolve escolhas fechadas (enum, número, probabilidade) numa passada. *Nota de honestidade: não consegui verificar as afirmações específicas sobre o produto "JEV" citadas na conversa; o experimento abaixo não depende delas — usa só o conceito "classificador de uma passada".* |
| **Sistema 1 / 2** | Kahneman: rápido/intuitivo vs. lento/deliberativo. Na IA: classificador de uma passada vs. raciocínio iterativo. |
| **Sistema 3** | Metacognição (próximo à "mente reflexiva" de Stanovich): decidir *quanto* pensar e *reconhecer quando não sabe*. |
| **Sistemas 0, 4–7** | 0 (sobrevivência/orçamento) e 4 (enxame) têm contrapartes testáveis. 5–7 (ressonância, hipertempo, colapso quântico) são **metáfora/especulação**, não engenharia — abaixo eu os traduzo para versões testáveis. |

## 2. Reflexão

A intuição "unir S1 e S2 vai dar 100.000×" merece ser testada, não acreditada.
Há duas formas bem diferentes de "unir":

1. **Colar** (roteador): S1 responde se estiver confiante; senão chama S2.
   É o que a indústria faz hoje (modelo pequeno → modelo grande).
2. **Fundir no mesmo substrato**: S2 é um laço de pensamento num estado
   latente (sem texto); S1 vive **dentro** do laço, colapsando cada passo
   num estado discreto; S3 observa o laço e decide parar ou se abster.

Minha aposta antes de testar: a (2) ganha, e o ganho não aparece como
"velocidade", e sim como **generalização** — resolver problemas maiores que
os vistos no treino, só pensando mais tempo.

## 3. O que foi construído e testado (micro-escala, Python puro)

`experimento/mlu.py` — **MLU, Motor Latente Unificado**. Sem numpy/torch;
roda em ~30 s numa CPU. Detalhes e números em [`RESULTADOS.md`](RESULTADOS.md).

Tarefa: "ache a raiz" num grafo de ponteiros com várias raízes distratoras.
Profundidade *d* = número de saltos = dificuldade. Treino só com *d* ≤ 4 e 12 nós.

```
          entrada (grafo + nó inicial)
                    │
     ┌──────────────┴───────────────┐
     │   S1-MLP (8.124 parâmetros)  │  ← "modelo de decisão": 1 passada
     └──────────────┬───────────────┘
                    │ (só no MLU "colado")
                    ▼
   ┌───────────────────────────────────────────┐
   │ S2: passo latente com 33 parâmetros,      │
   │     os MESMOS pesos a cada passo          │◄──┐
   │ S1 interno: "cristaliza" o estado         │   │ pensa de novo
   │ S3: convergiu? → responde                 │───┘
   │     estourou orçamento? → "não sei"       │
   └───────────────────────────────────────────┘
```

### Resultados principais (4 sementes, consistentes)

1. **S1 sozinho** (8.124 parâmetros): 94–97 % em *d*=0, mas cai para ~50–70 % a partir de *d*=1. Não aplicável a grafos de outro tamanho.
2. **S2 latente** (33 parâmetros): 100 % em todas as profundidades, **inclusive *d*=5..9, nunca vistas**, e em grafos de 16 e 32 nós.
3. **S3 (parada metacognitiva)**: mesma acurácia com **54 % menos computação** (gasta exatamente *d*+1 passos), e quando o orçamento não basta ele **se abstém em vez de errar**: 1000 respostas, **0 erros**, 200 abstenções. O S2 de passos fixos errava calado nesses casos.
4. **Colar S1 + S2 (roteador) PIORA**: 92–99 % contra 100 % e **mais** computação. O S1 está confiante e errado em ~5 % dos casos fáceis. *Unir por colagem não multiplica; subtrai.*
5. **O achado mais interessante — cristalização**: com estado latente contínuo, o pensamento "vaza" um pouco a cada passo; em grafos de 64–128 nós, 2 de 4 sementes caem para 0 %. Colapsando o estado num ponto discreto a cada passo (o S1 atuando *dentro* do S2), o mesmo modelo de 33 parâmetros resolve **100 % em 128 nós / 100 saltos em todas as sementes** — 25× a profundidade do treino.

### Leitura honesta

- A tarefa é simples e os atributos das arestas dão ao S2 um viés forte (ele só precisa aprender "siga o ponteiro e fique parado na raiz"). O S1-MLP é uma linha de base sem essa estrutura. Então o resultado **não** prova "S2 > S1" em geral; mostra que **estrutura iterativa + parada metacognitiva + colapso discreto** generaliza onde força bruta de parâmetros não.
- O "100.000×" não apareceu como velocidade. Apareceu, em miniatura, como **modelo 250× menor que generaliza para problemas 25× mais profundos**, sabendo quando parar e quando não sabe.

## 4. Plano da exploração final (próximos micro-experimentos)

Cada um cabe em Python puro e em minutos, e testa uma "camada" do mapa:

| # | Sistema | Pergunta testável | Experimento |
|---|---|---|---|
| E1 ✅ | S1+S2+S3 | Fundir > colar? | Feito (`mlu.py`). |
| E2 | S1 útil de verdade | E quando a intuição é necessária? | Grafo entregue com **ruído** (ponteiros corrompidos): S1 precisa limpar a percepção antes do S2 raciocinar. |
| E3 | S3 aprendido | Parada/abstenção aprendidas batem a regra fixa? | Cabeça de "halt" treinada (estilo PonderNet) + roteador calibrado. |
| E4 | Cristalização adaptativa | Quando manter superposição e quando colapsar? | Tarefa com várias hipóteses vivas (ex.: grafo com ciclos/ambiguidade); cristalizar só com confiança alta. |
| E5 | S0 (orçamento) | Um agente com "energia" finita aprende a economizar pensamento? | Recompensa = acerto − λ·passos; medir a fronteira acurácia × custo. |
| E6 | S4 + S5 (enxame, comunicação latente) | Agentes que trocam **vetores** superam agentes que trocam **símbolos**? | Cada agente vê parte do grafo; comparar mensagens latentes vs. discretas. |
| E7 | S6 (hipertempo → planejamento) | Simular futuros ajuda a decidir? | Modelo de mundo pequeno + rollouts latentes antes de agir. |

Critério para todos: comparar contra linha de base, mais de uma semente,
reportar falhas, e só chamar de "descoberta" o que sobreviver a isso.

## 5. Como rodar

```bash
python3 experimento/mlu.py            # completo (~30 s)
python3 experimento/mlu.py --quick    # rápido
python3 experimento/mlu.py --seed=2   # outra semente
```
