# JEV no laboratório: estado real e plano de integração

## Estado real (30/09/2026, após o ciclo 11)

- **Acesso confirmado:** a rede passou a liberar `api.typesafe.ai`; `python3 -m lab.jev` → JEV ACESSIVEL. Modelos listados: `jev-latest` e `jev-preview` (ambos de 10/09/2026).
  - SDK oficial: `typesafe-sdk` 0.7.2 (`TypeSafeClient.system_one(state, questions)`).
  - Credencial **persistente**: variável `TYPESAFE` nas configurações do ambiente de nuvem (o `lab/jev.py` a copia para `TYPESAFE_API_KEY`, que é o nome que o SDK lê). Setup do ambiente: `pip install typesafe-sdk`. Testado sem o arquivo local: JEV ACESSIVEL.
- **Primeira fumaça (não é resultado; 2 perguntas, sem pré-registro):** Noul "o nó 3 aponta para si?" com pai = {1:3, 2:3, 3:3} → 0,53 (resposta certa: sim); Choice "raiz a partir do nó 1" com pai = {1:2, 2:3, 3:3} → "2" (certa: "3"). Repetindo a fumaça minutos depois: Noul 0,51 e Choice "3" (certa). **As respostas variam entre chamadas iguais**: o E-JEV precisa gravar cada resposta bruta e medir a variação (várias chamadas por instância). Só mostra que o protocolo funciona; o desempenho se mede no E-JEV pré-registrado (H26).
- Nenhum resultado dos ciclos 1–11 usou o JEV. **Ciclo 12 (E012):** primeira medida pré-registrada. O JEV é um S1 de um salto; iterado pelo S2 segue q^k; sabe quando não sabe (0/516 erros com p ≥ 0,9). Ver `experimentos/E012_jev/RELATORIO.md`.
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
