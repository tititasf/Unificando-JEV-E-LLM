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

### 1. Diagnóstico (onde estamos?)
- Tema:
- Degrau atual: DXX — sustentado por: <experimento, nível de evidência>
- O que já funciona:
- Barreira para DXX+1:

### 2. Escada de 30 degraus
- D01: <o estado mais primitivo>
- ...
- DXX: ← ESTAMOS AQUI
- DXX+1: ← PRÓXIMO ALVO
- ...
- D30: <o ponto ômega do tema>

### 3. Transição DXX → DXX+1
1. Sacada / premissa a quebrar:
2. O que subtrair:
3. O que construir e testar (→ experimento ENNN):

### 4. Visão vertical (10 níveis de leitura do ciclo)
### 5. Deep insight (conceito · metanoia · aplicação · hack · visão maçônica)
```

As seções 4 e 5 são o espaço de reflexão livre. Elas podem inspirar
hipóteses, mas uma hipótese só entra na fila do `ESTADO.md` se for testável
por um experimento no degrau N+1.

## Como a escada se liga ao laço

```
... DECIDIR → ESCALAR (diagnóstico + escada + transição no EVOLUTION_LOG)
           → SEMEAR (a hipótese do degrau N+1 vai para o topo da fila do tema)
           → REGISTRAR → commit
```

No início de cada ciclo, leia a última entrada do `EVOLUTION_LOG.md` do tema
escolhido: o alvo do ciclo é o degrau N+1 que ela definiu.
