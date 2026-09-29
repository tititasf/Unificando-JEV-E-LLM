# E009 — Relatório: S3 em dois tempos

**Veredito: PROMOVER.** Habilidade **H07 desbloqueada**; o **S3 sobe de D03 para D04** (parado desde o ciclo 1).
Nível: **N2** (pré-registrado, 10 sementes, sementes de teste derivadas do commit `b1804f8`, reproduzido de checkout limpo, guarda OK). **Novidade: baixa a média.**

## Previsões
| # | Previsto | Prob. | Obtido | Status |
|---|---|---|---|---|
| P1 | DOIS_TEMPOS cobertura DENTRO ≥ 0,99, acc seletiva ≥ 0,995 | 0,55 | 1,000 [0,995; 1] e 1,0000 | ✅ |
| P2 | abstenção FORA_ORC ≥ 0,99 | 0,85 | 1,000 [0,995; 1] | ✅ |
| P3 | erros FORA_REG ≤ 1% | 0,80 | **0/600** [0; 0,006] | ✅ |
| P4 | CONV erros FORA_REG ≥ 20% | 0,80 | 50,8% (305/600) | ✅ |
| P5 | PONDER erros FORA_REG ≥ 20% | 0,80 | 51,0% (306/600) | ✅ |
| P6 | SO_ANTES abstenção FORA_ORC < 0,50 | 0,90 | 0,001 | ✅ |
| P7 | ABS também cumpre P1–P3 | 0,60 | sim (0/600 erros) | ✅ |
| P8 | passos FORA_REG DOIS_TEMPOS ≤ 0,10 × ABS | 0,85 | **0,053** (1,1 contra 20,1) | ✅ |

**Brier: 0,07.**

## O que foi mostrado
1. **Uma metacognição que funciona de N=12 a N=1024 sem nenhum ajuste por escala:** responde 100% onde o pensamento é legível e o orçamento basta; se abstém 100% quando o orçamento não basta; **zero** respostas erradas quando o pensamento está dissolvido.
2. **Sem essa metacognição, os métodos publicados erram com confiança:** a parada por ponto fixo (estilo FPRM) e a PonderNet respondem ~51% errado no regime dissolvido. É o tipo de erro que o G2 quer eliminar.
3. **O que resolve é tratar a dissolução como "não sei"** (P7: o limiar absoluto do E001 também passa). O tempo 1 ("antes de pensar", pela lei de nitidez) acrescenta **economia de 19×** no regime dissolvido: decide no primeiro passo em vez de pensar ~20 passos para depois desistir.
4. **Os dois tempos são necessários juntos:** só o tempo 1 não percebe falta de orçamento (P6); só o tempo 2 (CONV) erra no regime dissolvido (P4).

## Correção de registros anteriores
- **A4 (E002) e A8 (E004) reinterpretados.** Dizia-se "o limiar absoluto não escala: se abstém embora o S2 acerte". No regime dissolvido o S2 acerta por sorte de atrator (~50%); abster-se ali era **correto**. O que não escalava era a **métrica** (acurácia do S2 como verdade), não o limiar. O problema real era a falta de uma definição de "pensamento legível", que a lei de nitidez deu.

## Revisor hostil
1. *"A zona de transição foi excluída."* Sim, declarado. O próximo degrau (D05, calibração com garantia) precisa cobri-la.
2. *"ABS passa também; qual é a contribuição?"* A metacognição que previne erro confiante em qualquer escala é o resultado; o tempo 1 é uma economia de 19×; a definição operacional de legibilidade (ε_c(m) da teoria) é o que torna o tempo 1 possível sem ajuste.
3. *"T1 é uma tarefa-atrator."* Por isso a métrica do regime dissolvido é erro, não abstenção. Repetir em T2 é o próximo passo natural (H-campo-médio-T2).

## Hipóteses semeadas
- **H-S3-fronteira (→ H08):** na zona de transição (N̂/1,5 a 1,5N̂), um S3 calibrado com garantia conformal mantém o risco seletivo ≤ α.
- **H-S3-T2:** o S3 em dois tempos transfere para T2 (sem atrator) sem re-ajuste.
