---
name: jev
description: Usar o JEV (TypeSafe System One) como S1 externo do laboratorio — diagnostico de acesso, perguntas Noul/Choice e regras de uso (sob teste ou triagem, nunca metrica).
---

# /jev — o S1 externo

1. **Diagnóstico:** `python3 -m lab.jev`. Mostra SDK (`typesafe-sdk`), credencial (`TYPESAFE_API_KEY`) e rede até `api.typesafe.ai`. Saída 1 = sem acesso: registre no DIARIO e siga o ciclo sem JEV (nunca finja uso).
2. **Fumaça:** `python3 -m lab.jev --teste` (uma pergunta Noul e uma Choice).
3. **No código:** `from lab import jev; jev.escolher(estado, instrucoes, opcoes)` → `(rotulo, bruto)`; `jev.sim_nao(estado, instrucoes)` → probabilidade. Estado pode ser texto ou JSON.

## Regras

- **Três papéis permitidos** (docs/JEV.md): sistema sob teste (experimento pré-registrado), S1 na arquitetura S1+S2+S3 (H24/H12/H26), triagem do laboratório (só sugestão).
- **Proibido (regra 12):** JEV como avaliador, juiz ou métrica. Métrica vem de verificador exato.
- **Credencial:** nunca no repositório. Vem do ambiente de nuvem (variável `TYPESAFE` ou `TYPESAFE_API_KEY`) ou de `~/.config/typesafe/env` (fora do git, só na sessão).
- **Reprodutibilidade:** chamadas ao JEV não são determinísticas nem gratuitas. Todo experimento com JEV guarda as respostas brutas em `respostas_jev.jsonl` e a análise roda sobre esse arquivo; o `lab.reproduzir` reprocessa as respostas gravadas. Fixe a versão do modelo (ex.: `jev-1.13`), não `jev-latest`.
- **Custo:** registre tokens (`usage`) e número de chamadas no resultados.json.
