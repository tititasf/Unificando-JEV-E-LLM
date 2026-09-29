# E004 — Relatório: metacognição invariante à escala

**Veredito: MATAR** (P2 falhou). O S3 continua no degrau **D03**.
**Achado maior, não previsto: o S2 contínuo muda de regime com a escala** (sequencial → difusivo).
Nível: N2 para o negativo (pré-registrado, 10 sementes); N1 para o achado de regime (diagnóstico, 4 sementes).

## Previsões

| # | Previsto | Obtido (N=128) | Status |
|---|---|---|---|
| P1 | ABS cobertura DENTRO ≤ 10% | 30% (abaixo de 50%: A4 se replica em parte) | 🟥 previsão errada, sem morte |
| P2 | **ESTAVEL ≥ 99% cobertura, ≥ 99% abstenção FORA, ≥ 99,5% acc seletiva, em todo N** | cobertura 100%, **abstenção FORA 30%**, acc seletiva 90,3%, 39 erros | 🟥 **H morta** |
| P3 | ENT cobertura < 50% | 30% | ✅ |
| P4 | UNIF passa em todo N | abstenção FORA 41,5%, 30 erros | 🟥 |
| P5 | ESTAVEL_PURO ≈ ESTAVEL | idênticos em todas as células | ✅ |
| P6 | CONV abstenção FORA < 90% em algum N | 30% em N=128 | ✅ |
| P7 | ESTAVEL > ABS, p < 0,01 | P(A>B)=0,26, p=0,63 | 🟥 |

Com N ≤ 32, todos os braços com S3 foram perfeitos. Em N=64 e N=128,
**nenhum** braço funcionou nas duas direções: os de nitidez (ABS, ENT)
nunca respondem; os de convergência (CONV, ESTAVEL) respondem cedo e erram.
**ESTAVEL = CONV em todas as células:** a "estabilidade do argmax" não
acrescenta nada ao critério publicado de ponto fixo. Tabela completa: `resultados.md`.

## Diagnóstico pós-hoc: por que falhou (`diagnostico.md`)

Acurácia do argmax após t passos, com d = N−5 (4 sementes × 10 casos):

| N | modo | t=12 | t=24 | t=48 | passos até fixar na raiz ÷ d |
|---|---|---|---|---|---|
| 12 | contínuo | 1,00 | 1,00 | 1,00 | 1,00 |
| 32 | contínuo | 0,00 | 0,00 | 1,00 | 1,00 |
| 64 | contínuo | 0,00 | 0,00 | 0,03 | 1,00 |
| **128** | **contínuo** | **0,57** | **0,75** | **1,00** | **0,08** |
| 128 | cristalizado | 0,00 | 0,00 | 0,00 | 1,00 |

- Até N=64 o S2 contínuo anda **um salto por passo**, como o cristalizado.
- Em N=128 o vazamento por passo ((N−1)·e^(−margem)) passa de um limiar: em ~6 passos o estado se dissolve pelo caminho inteiro (máx z ≈ 0,02) e em ~12 entra num **equilíbrio** em que a raiz certa tem a maior massa por margem mínima (0,012 contra ~0,008). A resposta aparece **12× antes** do que andar permitiria.
- Por isso a condição FORA não era "impossível" em N=128, e por isso a convergência para cedo: no regime difusivo, "terminei" = "cheguei ao equilíbrio", e o equilíbrio às vezes está errado (90% de acerto).

## Consequências e correções

1. **S3:** um sinal de parada só pode ser invariante à escala se o *pensamento* que ele lê tiver um regime estável. A escada do S3 foi reordenada (EVOLUTION_LOG, ciclo 4): a legibilidade do pensamento vem antes.
2. **S2:** a afirmação "extrapola 32× iterando" (E001/E002) vale **até N=64**. Em N=128 a resposta vem de outro mecanismo (difusão até o equilíbrio), não da iteração salto a salto. Anotado em `docs/SISTEMAS.md` e no log do S2.
3. **Alerta de literatura confirmado em miniatura:** o latente pode resolver a tarefa por um caminho diferente do pretendido (cf. *Do Latent Tokens Think?*). Aqui o caminho alternativo é identificável e mensurável.

## Revisor hostil

1. *"O regime difusivo pode ser só o atrator de novo."* Provável: com d = N−5 o caminho tem quase todos os nós, e a difusão fica presa nele. Teste: d ≪ N (várias árvores grandes). → H-regime.
2. *"Os limiares a priori foram azarados."* ESTAVEL = CONV em todas as células, e o diagnóstico mostra um motivo estrutural (equilíbrio precoce), não de limiar.
3. *"10 casos por célula no diagnóstico."* Por isso ele é N1 e não muda o veredito.

## Hipóteses semeadas

- **H-S3-legível (D04 novo do S3):** com o S2 cristalizado (um salto por passo), CONV/ESTAVEL cumprem os critérios da P2 em todo N. Custo: perde o atalho difusivo.
- **H-regime (S2):** o regime difusivo é uma capacidade (resolve em ~O(1) passos) ou um artefato do atrator? Prever onde fica o limiar de N a partir da margem aprendida e testar com d ≪ N.
- **H-híbrido (Σ1 revisitada):** um S3 que *detecta o regime* (nitidez caindo abaixo de ~3× o uniforme) e alterna entre ler a convergência e cristalizar.
