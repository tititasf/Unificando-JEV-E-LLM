# JEV no laboratório: estado real e plano de integração

## Estado real (ciclo 11)

- **O JEV ainda não respondeu a nenhuma chamada deste laboratório.** Nenhum ciclo até agora usou o JEV.
  - SDK oficial instalado: `typesafe-sdk` 0.7.2 (`TypeSafeClient.system_one(state, questions)`; API em `https://api.typesafe.ai`, modelo padrão `jev-latest`).
  - Credencial: o usuário forneceu uma chave (ciclo 11). Ela **não** vai para o git; nesta sessão fica em `~/.config/typesafe/env`. Para durar entre sessões, deve ser cadastrada como variável `TYPESAFE_API_KEY` nas configurações do ambiente de nuvem.
  - **Bloqueio atual:** a política de rede do ambiente nega `api.typesafe.ai` (proxy responde 403). Falta liberar esse domínio em *Network access*.
- Wrapper: `lab/jev.py` (`estado`, `escolher`, `sim_nao`); skill: `.claude/skills/jev/SKILL.md`.
- O "S1" dos experimentos (E001 em diante) é **um modelo nosso**, pequeno, de uma passada, *inspirado* no conceito de modelo de decisão tipada. Onde a documentação diz "estilo JEV", leia "inspirado no conceito do JEV".
- O S2 do laboratório é o Claude (o pesquisador que orquestra os ciclos).

## O que o JEV é (fontes públicas, set/2026)

TypeSafe lançou o JEV em 15/09/2026 como o primeiro modelo "System One": responde a tipos
fixos de pergunta com valores tipados em vez de texto (sim/não com probabilidade; escolha
entre até 255 opções com probabilidade por opção e confiança; nota numa rubrica ordenada).
Acesso pela API da TypeSafe ou pelo OpenRouter (`typesafe/jev-latest`, versões fixas como
`jev-1.13`). O formato das requisições vem do SDK oficial (`typesafe-sdk`): `state` (texto ou
JSON) + `questions` nomeadas (`Noul`, `Choice`, `Score`); respostas em `.nouls[n].noul`,
`.choices[n].choice`, `.scores[n]`, com `usage` de tokens.

## Como conectar (o que o usuário precisa fazer)

1. Nas configurações do ambiente de nuvem (menu do ambiente na barra de título da sessão → Edit):
   - **Credencial:** criar a variável de ambiente `TYPESAFE_API_KEY` (API direta) **ou** `OPENROUTER_API_KEY` (via OpenRouter). Nunca colar a chave no chat.
   - **Rede:** liberar o domínio correspondente (`openrouter.ai` e/ou o domínio da API da TypeSafe) em *Network access*.
2. Abrir uma sessão nova (ela carrega as variáveis).
3. O laboratório detecta sozinho: `python3 -m lab.jev` diz se há credencial e rede.

## Como o JEV entra nos ciclos (quando houver acesso)

Papel: **S1 externo real**, ao lado do S1 compilado internamente (H24).

| Uso | Onde | Regra |
|---|---|---|
| **Sistema sob teste** | E-JEV: as tarefas T1/T2 codificadas em texto (grafo pequeno + pergunta tipo *Choice* "qual nó é a raiz/destino?"), medindo acerto, confiança, latência e custo contra o S2 iterado, em vários tamanhos | É um experimento como qualquer outro: pré-registro, sementes do commit, régua |
| **S1 da arquitetura S1+S2+S3** | H24/H12: JEV chuta (O(1)), o S3 verifica por invariante, o S2 só entra quando o JEV não é confiável | Mede-se o custo total e os erros confiantes |
| **S1 do próprio laboratório** | triagem rápida (ex.: classificar hipóteses da fila por tipo, detectar duplicatas na árvore) | Só como **sugestão**; a decisão passa pela bússola e pelo pesquisador |

**Proibido (regra 12):** usar o JEV como avaliador ou métrica de resultado. Toda métrica
continua vindo de verificadores exatos. O JEV é peça sob teste ou ferramenta de triagem, nunca juiz.

## Primeiro experimento planejado (E-JEV)

- Pergunta: um S1 externo real, de uma passada, resolve "achar a raiz" (T1) e "k saltos" (T2) em que tamanhos, com que calibração, e a que custo, comparado ao S2 iterado do laboratório?
- Previsão a pré-registrar: acerto alto em d pequeno e queda com a profundidade (como o S1-MLP do E001), confiança útil para o S3 rotear. O ganho da união S1+S2 se mede pela fronteira de Pareto acerto × custo com zero erros confiantes (G2, G5).
