# Stack: até onde o Python puro vai (e quando pedir mais)

Medido em 2026-09-29 neste contêiner (4 núcleos):

| Operação | Vazão |
|---|---|
| multiplica-soma (1 núcleo) | ~2,9·10⁷ /s |
| passo S2 genérico O(N²), N=64 / 256 | ~4.000 / ~300 por s |
| passo S2 estruturado O(N), N=64 / 256 | ~35.000 / ~9.000 por s |
| BPTT de 16 passos, N=16, 1 exemplo | ~1.000 /s |

## Estimativa de custo antes de pré-registrar

```
CPU (s) ≈ operações por exemplo × exemplos × (1 + 2 se houver treino) ÷ (2,9·10⁷ × 4 núcleos)
```

| Habilidade | Estimativa | Cabe? |
|---|---|---|
| H04, H07, H12, H22 (motor de 33 parâmetros) | minutos | ✅ |
| H06 memória de trabalho (estado × registro pequeno) | minutos a 1 h | ✅ com passo estruturado |
| H23 protocolo CLRS com motor pequeno (n=16 → 64) | ~1 h | ⚠️ limite |
| H09 latente livre (vetor d=32 por nó, n=64) | ~14 s por exemplo de treino → dezenas de horas | ❌ |
| H11 algoritmos com processador de mensagens (h=32) | idem | ❌ |

## Gatilho

Quando a estimativa de um experimento pré-registrável passar de **30 min de
CPU com 4 núcleos** mesmo com passo estruturado e amostras mínimas (pelo
cálculo de `lab.estat.n_para_diferenca`), **parar e pedir ao usuário** a
decisão de stack (numpy puro ou PyTorch CPU). Até lá, Python puro. Pela
tabela acima, o gatilho deve disparar em **H09 ou H11**.

## Decisão do ciclo 18
O usuário liberou o PyTorch (CPU; sem GPU nesta sessão). Instalado: torch 2.14.0+cpu. Pedir ao usuário antes de GPU ou de outras bibliotecas pesadas.
