# E003 — Pré-registro: o "Cristal Comum" (sincronia S2 ↔ S4/S5)

**Escrito antes de rodar.** Trilhas A + D. Sínteses: Σ1 (ver `docs/SISTEMAS.md`).

## Pergunta

A discretização que estabiliza o raciocínio de um agente também torna
robusta a **comunicação** entre agentes? Se sim, "pensamento" e "símbolo"
são a mesma operação (colapso num ponto discreto), e um protocolo único
serve aos dois.

## Montagem

- O conhecimento é **fragmentado**: dois agentes (A e B) conhecem cada um
  metade dos ponteiros do grafo (partição aleatória dos nós). Nenhum resolve sozinho.
- Os dois usam o mesmo passo latente S2 já treinado (treino idêntico ao E001,
  sementes 300…309, **10 sementes**). Nenhum re-treino para comunicar.
- A cada passo, cada agente calcula a sua contribuição parcial m_X (logits
  vindos dos nós que conhece) e a envia por um **canal com ruído gaussiano σ**
  por componente. O receptor soma as mensagens e atualiza o estado.
- Mesma potência nos dois canais:
  - **CONT** (analógico): envia m_X; o estado = softmax(soma recebida).
  - **SIMB** (cristal): envia ‖m_X‖·onehot(argmax m_X), só se o agente
    detém a maior parte da massa; o estado = onehot(argmax da soma recebida).
- Teste congelado: sementes 40000+s; d ∈ {8, 32}; N = d+5; 20 exemplos;
  σ ∈ {0; 0,5; 1; 2; 4}; T = d+8.

## Previsões e critérios

| # | Previsão | Morte |
|---|---|---|
| Q1 | σ=0: CONT e SIMB ≈ 100% | Se SIMB < 95% com σ=0: a fragmentação quebrou o método. |
| Q2 | Existe σ em que SIMB ≥ CONT + 20 pontos em d=32, com Fisher agregado p<0,01 | Se em nenhum σ SIMB vence por isso: Σ1 morta para comunicação. |
| Q3 | A vantagem do SIMB **cresce com d** (erro analógico acumula por salto) | Se a vantagem em d=32 ≤ a de d=8: não há acúmulo; o mecanismo é outro. |
| Q4 | Em σ muito alto (4), ambos falham | Se SIMB ainda ~100% em σ=4: o ruído está mal calibrado → refazer a escala (não é vitória). |

## Honestidade prévia

É o princípio da regeneração digital de Shannon/von Neumann aplicado a um
raciocínio aprendido. A novidade não está no princípio; está em verificar
que **o mesmo operador** (cristalização) cumpre as duas funções sem re-treino.
Nível máximo possível aqui: N1–N2 numa tarefa.
