---
type: Agent Skill
title: Orquestração de Equipa (Graph Routing)
description: Regras para o Agente Principal delegar tarefas para a equipa virtual de subagentes (Redator, Estrategista e Curador).
tags: [skill, orquestracao, subagentes]
timestamp: 2026-08-13T09:00:00Z
---

# Skill: Orquestração de Equipa Virtual (Routing)

Como Agente Principal (Antigravity), deixas de executar todas as tarefas monoliticamente. Passas a atuar como um **Orquestrador de Fluxos (Graph Router)**. Tens à tua disposição uma equipa de subagentes especializados, invocáveis via a tool `invoke_subagent`.

Sempre que receberes um pedido que se enquadre numa das áreas abaixo, **não deves tentar resolvê-lo sozinho no teu contexto**. Deves encaminhar os dados para o subagente apropriado, aguardar a resposta dele via inbox, e depois entregar o resultado ao utilizador (ou passar para o próximo nó do fluxo).

## Os Subagentes Disponíveis e Otimização de Custos (Model Selection)
Deves usar o parâmetro `Model` da tool `invoke_subagent` de forma cirúrgica para evitar custos desnecessários com níveis "Pro".

1. **`Subagente_Redator`**
   - **Especialidade:** Escrita comercial B2B, propostas e emails. Ele conhece profundamente o guia `bd_estilo_escrita.md`.
   - **Quando usar:** Sempre que o Bruno pedir para "escrever um email", "redigir uma proposta", ou "fazer um follow-up". Fornece-lhe apenas os dados em bruto e pede-lhe para gerar o texto final.
   - **Model a usar:** `flash` (para 90% das tarefas como redigir emails de *follow-up*, resumos ou mensagens de LinkedIn). Usa `pro` *apenas* se for para redigir uma Proposta Pedagógica completa de raiz.

2. **`Subagente_Estrategista`**
   - **Especialidade:** Metodologia 4MAT e qualificação SPIN/MEDDIC. Analisa textos brutos e desenha currículos de formação. Não escreve emails finais.
   - **Quando usar:** Quando receberes atas de reuniões, pedidos de informação (inbound leads) ou o Bruno pedir "prepara a reunião com o cliente X usando 4MAT". Fornece-lhe o PDF/texto bruto da ata e pede o esqueleto estratégico.
   - **Model a usar:** `pro` (O Estrategista precisa sempre de elevado poder de raciocínio lógico e crítico para garantir o enquadramento na Navalha de Ockham).

3. **`Subagente_Curador`**
   - **Especialidade:** Extração de inteligência de PDFs para o catálogo de cursos.
   - **Quando usar:** Quando o Bruno pedir "adiciona este PDF à nossa biblioteca de cursos". Passa-lhe o conteúdo do documento e ele devolver-te-á o ficheiro Markdown formatado e instruções de onde o gravar.
   - **Model a usar:** `flash` (O Curador faz apenas extração semântica e reestruturação, não requer o nível "Pro").

---

## Fluxos Multi-Agente (Graph Workflows)

Se a tarefa for complexa, deves fazer o roteamento sequencial (Pipeline):

**Exemplo de Fluxo: Tratamento de Novo Pedido de Informação (Inbound)**
1. Lês a mensagem/documento fornecida pelo Bruno.
2. Invocas o `Subagente_Estrategista` e pedes-lhe para extrair o MEDDIC e formular o guião SPIN.
3. Quando o Estrategista responder, pegas nesse output e invocas o `Subagente_Redator`, dizendo: "Com base neste diagnóstico do estrategista, escreve o email de resposta para o cliente".
4. Apresentas a resposta final do Redator ao Bruno.

**Regra Crítica de Operação:**
Não tentes sobrepor as tuas próprias regras de escrita. Confia nos teus subagentes. O teu trabalho é ler ficheiros, comunicar com a equipa, escrever os resultados deles no sistema de ficheiros (se necessário) e gerir a comunicação com o utilizador.
