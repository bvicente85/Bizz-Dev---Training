---
type: Agent Skill
title: Manutenção de Contas e Otimização de Memória
description: Rotina para resumir histórico longo de reuniões (poupar tokens) e arquivar clientes inativos.
tags: [skill, manutencao, tokens, arquivo]
timestamp: 2026-08-20T09:00:00Z
---

# Skill: Manutenção de Contas e Otimização de Memória

Esta *skill* define a rotina que o Agente Principal deve executar para impedir que o sistema de ficheiros cresça indefinidamente e consuma recursos de contexto (tokens e latência) de forma desnecessária.

## Gatilho (Trigger)
"Faz a manutenção das contas", "Limpa a memória do cliente X", ou "Arquiva os clientes inativos".

---

## Fluxo de Execução Obrigatório

Sempre que ativado, o agente principal deve avaliar a carteira de clientes (`032_Clientes`) e executar as seguintes operações de otimização:

### Passo 1: Resumo Periódico de Notas de Reunião (Token Optimization)
Para clientes ativos cujo ficheiro `[Nome]_meeting_notes.md` tenha crescido significativamente (mais de 15/20 linhas de histórico antigo ou múltiplas interações):
1. O Agente deve ler o ficheiro na totalidade.
2. Deve condensar todas as interações e decisões com mais de 2 meses num único parágrafo denominado **"Resumo Executivo do Histórico Antigo"**.
3. Deve apagar os registos brutos e detalhados antigos.
4. Deve manter apenas o Resumo Executivo no topo, seguido do histórico integral apenas das **últimas duas (2) interações recentes**.
5. *Objetivo:* Garantir que a leitura deste ficheiro para responder a um email simples não consome tokens de processamento a ler atas irrelevantes de meses atrás.

### Passo 2: Arquivo de Clientes Inativos
Para clientes cujo ficheiro de progresso (`[Nome]_progress.md`) indique que a oportunidade está "Fechada/Perdida" ou inativa/suspensa há demasiados meses sem perspetiva de retoma:
1. O Agente deve mover a diretoria completa do cliente da pasta `032_Clientes/` para a pasta `032_Clientes_Arquivo/`.
2. O Agente deve atualizar os links nos índices se necessário.
3. *Objetivo:* Manter a pesquisa semântica focada apenas em clientes com potencial comercial ativo.

### Passo 3: Debriefing
O Agente deve responder ao Bruno com um log rápido das manutenções que efetuou:
* "Notas de reunião comprimidas para o(s) cliente(s): X, Y."
* "Pastas arquivadas para o(s) cliente(s): Z."
