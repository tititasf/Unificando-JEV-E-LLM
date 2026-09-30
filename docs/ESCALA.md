# Protocolo Scalata: a escada de 30 degraus por tema

Protocolo de autorreflexão evolutiva, executado **no fim de todo ciclo**.
Dois eixos simultâneos:

- **Rigor** (`docs/VALIDACAO.md`): o que está provado, e com que peso (N0–N5).
- **Imaginação vertical** (este documento): o que o tema ainda *não é*, mas tem caminho lógico para se tornar, degrau por degrau (D01–D30).

Os dois não se misturam. A escada diz **para onde** ir; a régua diz **onde estamos**.

## Regras de ligação entre os eixos

1. **Um degrau só conta como atingido** se um experimento com evidência ≥ N1 o sustentar. O degrau atual sempre cita esse experimento.
2. Degraus acima do atual são **projeção**: servem para gerar hipóteses, nunca como afirmação.
3. **Disciplina N+1:** o ciclo seguinte só escreve código que implementa os requisitos do degrau imediatamente acima do atual. Nada de pular para N+3 antes de consolidar o piso.
4. Se um experimento mostrar que um degrau "atingido" não se sustenta, o tema **desce** na escada e o log registra a queda (como o E002 derrubou a leitura do E001).
5. A escada de um tema pode ser **reescrita** quando um resultado mostrar que a ordem dos degraus estava errada. A versão antiga fica no log.

## Formato obrigatório (em `EVOLUTION_LOG.md`, uma entrada por ciclo)

```
## Ciclo N — Tema: <componente exato>
- Degrau atual: DXX — sustentado por: <experimento, nível>  (ou: sem subir)
- O que o ciclo mostrou (com números):
- Barreira para DXX+1:
- Próximo teste (→ ENNN):
- Escada: inalterada | reescrita (se reescrita, colar a nova D01–D30 inteira)
```

**Mudança do ciclo 18 (decisão do usuário: "corte o ritual poético, mantenha só o rigor"):**
- As antigas seções 4 e 5 (visão vertical em 10 níveis e deep insight, com a visão maçônica) foram **removidas**. Elas custavam tempo e criavam uma sensação de profundidade que os dados não sustentavam.
- A escada completa só é copiada quando muda.
- As entradas antigas ficam no log como histórico.

## Como a escada se liga ao laço

```
... DECIDIR → ESCALAR (diagnóstico + escada + transição no EVOLUTION_LOG)
           → SEMEAR (a hipótese do degrau N+1 vai para o topo da fila do tema)
           → REGISTRAR → commit
```

No início de cada ciclo, leia a última entrada do `EVOLUTION_LOG.md` do tema
escolhido: o alvo do ciclo é o degrau N+1 que ela definiu.
