---
type: Agent Skill
title: Extração de Sessões de Mentoria
description: Pipeline para processar logs de conversas com o Gem Mentor e extrair regras de Ockham para a doutrina base.
tags: [skill, aprendizagem, mentoria]
timestamp: 2026-08-18T12:00:00Z
---

# Skill: Extração de Sessões de Mentoria

Esta skill define o protocolo para transferir conhecimento das sessões móveis (Gem Mentor Pragmático) para o cérebro operacional local da SKOLAE.

## Gatilho (Trigger)
"Processa a sessão de mentoria [Nome do Ficheiro]" ou "Lê a nova sessão de mentoria".

---

## Fluxo de Execução Obrigatório

Sempre que ativado, o agente principal deve executar os seguintes passos na ordem indicada:

### Passo 1: Leitura do Log
Lê o ficheiro indicado que deverá estar localizado em `01_Conhecimento_Base/013_Sessoes_Mentoria/`.

### Passo 2: Extração de Princípios (A Regra do "E Depois?")
Analisa a conversa e extrai apenas os **Princípios Práticos**. Ignora toda a teoria académica que não tenha aplicação direta nas vendas B2B, escrita de emails ou negociação.
Para cada conceito útil, formula-o como uma Regra de Ockham (uma ação clara e simples).

### Passo 3: Injeção na Memória de Aprendizagem
Atualiza diretamente o ficheiro `bd_memoria_aprendizagem.md` (e/ou `bd_estilo_escrita.md` se for uma regra de comunicação).
* Insere o novo princípio numa secção apropriada.
* Adiciona uma linha de log na secção "Registo de Atualizações Recentes" mencionando que a aprendizagem foi extraída de uma sessão de mentoria.

### Passo 4: Debrief ao Utilizador
Responde ao Bruno no chat com o seguinte formato:
1. **O que aprendemos:** Um resumo curtíssimo (2 linhas) do conceito assimilado.
2. **Como vamos aplicar:** Como é que os Subagentes (Redator ou Estrategista) vão passar a comportar-se daqui para a frente por causa desta nova regra.
3. **Confirmação:** Confirmação de que os ficheiros mestre foram atualizados com sucesso.
