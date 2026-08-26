---
type: Agent Skill
title: Tratamento e Triagem de Pedidos de Informação
description: Lógica de qualificação SPIN/MEDDIC e protocolo para resposta rápida a pedidos de orçamentos e convites de propostas.
tags: [skill, inbound, orcamento]
timestamp: 2026-06-18T10:23:00Z
---

# Skill: Tratamento e Triagem de Pedidos de Informação

## Objetivo e Contexto
Esta skill define o protocolo para processar pedidos de informação comercial inbound (pedidos de orçamento, convites para apresentar proposta ou emails de contacto de potenciais clientes) que são colocados na pasta [033_Pedidos_Informacao](file:///c:/Users/brunn/OneDrive%20-%20GIE%20IFE/Desktop/Bruno/PESSOAL/Business%20Development%20Formação/03_Carteira_Clientes/033_Pedidos_Informacao) ou indicados pelo Bruno no chat. O objetivo é automatizar a triagem inicial, organizar os ficheiros do cliente e gerar um draft de resposta imediata com o mínimo esforço administrativo para o Bruno.

---

## Fluxo de Trabalho (Passo a Passo)

Sempre que o Bruno pedir para analisar um pedido de informação (ex: "analisa o pedido X"), deves executar os seguintes passos pela ordem exata:

### Passo 1: Triagem do Pedido (Mapeamento MEDDIC)
Lê o ficheiro bruto do pedido de informação e extrai os seguintes dados estruturados com base no framework **MEDDIC**:
*   **Empresa/Entidade:** Nome oficial do cliente.
*   **Interlocutor (Economic Buyer / Champion):** Nome, cargo e nível de influência na decisão.
*   **Tema da Formação:** Assunto principal solicitado.
*   **Dor de Negócio (Pain):** Problemas, dificuldades, gargalos ou necessidades operacionais específicas que motivaram o pedido.
*   **Métricas de Impacto (Metrics):** Indicadores ou resultados que o cliente quer melhorar (ex: ROI, produtividade, retenção, margens, etc.).
*   **Processo de Decisão (Decision Process/Criteria):** Prazos, procedimentos internos ou requisitos regulatórios para adjudicação (ex: consulta ao mercado, data de fecho do plano).
*   **Prazo Limite:** Data limite para resposta ou entrega de proposta (se mencionada).

### Passo 2: Verificação do Registo e Setup do Cliente
1. Pesquisa no diretório [03_Carteira_Clientes](file:///c:/Users/brunn/OneDrive%20-%20GIE%20IFE/Desktop/Bruno/PESSOAL/Business%20Development%20Formação/03_Carteira_Clientes) para verificar se já existe uma pasta dedicada a este cliente.
2. **Caso seja Cliente Novo:** Executa o **Protocolo de Setup de Cliente Novo** conforme definido no Capítulo 3 do manual de operação [bd_instrucoes_operacao.md](file:///c:/Users/brunn/OneDrive%20-%20GIE%20IFE/Desktop/Bruno/PESSOAL/Business%20Development%20Formação/00_Instrucoes_Agente/bd_instrucoes_operacao.md). Preenche os ficheiros iniciais com os dados extraídos no Passo 1.
3. **Caso seja Cliente Existente:** Atualiza o ficheiro `[nome_cliente]_context.md` e acrescenta o novo registo e próxima ação a `[nome_cliente]_progress.md`.

#### Desvio de Fluxo: Pedidos Incompletos, Vagos ou Downloads (Qualificação SPIN)
Se a informação recolhida no Passo 1 for insuficiente para estruturar uma proposta comercial séria (faltando dados de dores reais, destinatários ou métricas):
1. **Pula o Passo 3:** Não forces o mapeamento de um curso nem sugiras soluções padrão sem contexto fidedigno.
2. **No Passo 4:** Redige o email de resposta utilizando estritamente o modelo de qualificação rápida de leads (**Secção F do Guia de Estilo de Escrita [bd_estilo_escrita.md](file:///c:/Users/brunn/OneDrive%20-%20GIE%20IFE/Desktop/Bruno/PESSOAL/Business%20Development%20Formação/00_Instrucoes_Agente/bd_estilo_escrita.md)**). As 3 perguntas devem ser ajustadas sob a lógica **SPIN** (Situação, Problema, Implicação e Necessidade de Retorno) para preencher os dados de MEDDIC em falta, incentivando o agendamento de uma conversa curta através da agenda online.

#### Desvio de Fluxo: Pedidos Históricos (Ações já Ocorridas)
Se a triagem do Passo 1 revelar que a data de realização do projeto ou evento já passou em relação à data atual do sistema (local time):
1. **Setup Histórico e Ficheiro de Progresso:** Executa o setup normal do cliente novo, mas no ficheiro `[nome]_progress.md` define o estado no funil como "Concluído (Histórico)" e marca todas as tarefas operacionais como executadas `[x]`.
2. **Cancelamento do Fluxo Ativo (Passos 3 e 4):** Ignora o mapeamento pedagógico prospectivo e a elaboração de rascunhos de e-mail comercial. 
3. **Foco no Arquivo e Resumo:** Move os ficheiros brutos/atas para a pasta de reuniões do respetivo mês histórico em `034_Reunioes_Clientes`, limpa a pasta de triagem e apresenta ao Bruno apenas o sumário do projeto realizado, confirmando que os ficheiros foram arquivados.

### Passo 3: Análise de Solução Formativa (Fit Pedagógico)
1. Invoca a lógica da [Skill_Mapeamento_Solucoes.md](file:///c:/Users/brunn/OneDrive%20-%20GIE%20IFE/Desktop/Bruno/PESSOAL/Business%20Development%20Formação/00_Instrucoes_Agente/Skill_Mapeamento_Solucoes.md) cruzando as dores identificadas no Passo 1 com o catálogo central [bd_biblioteca_cursos.md](file:///c:/Users/brunn/OneDrive%20-%20GIE%20IFE/Desktop/Bruno/PESSOAL/Business%20Development%20Formação/01_Conhecimento_Base/bd_biblioteca_cursos.md).

2. Define o Curso Sugerido, o Racional e a Taxa de Compatibilidade (Fit).
3. Desenha ou adapta a solução formativa (Fit 100%, Fit Parcial ou Fit Incompleto com proposta à medida) e anexa este sumário técnico na tua resposta ao Bruno.

### Passo 4: Elaboração da Resposta e Próximo Passo
1. Redige um rascunho de email de resposta ao interlocutor seguindo rigorosamente as diretrizes em [bd_estilo_escrita.md](file:///c:/Users/brunn/OneDrive%20-%20GIE%20IFE/Desktop/Bruno/PESSOAL/Business%20Development%20Formação/00_Instrucoes_Agente/bd_estilo_escrita.md) (para português ou inglês, consoante o idioma do contacto):
   *   Utiliza as regras gerais de escrita humana e evita jargões de IA.
   *   Garante um tom informal-profissional e direto.
   *   Propõe um próximo passo simples (ex: agendar chamada rápida de 10 minutos).
2. Atualiza o ficheiro `[nome_cliente]_progress.md` com a tarefa pendente (ex: `[ ] Enviar email de resposta ao pedido`).

---

## Formato do Output no Chat
Ao finalizar a análise, responde ao Bruno com o seguinte formato estruturado:

```markdown
### 1. Triagem do Pedido: [Nome do Cliente]
*   **Interlocutor:** [Nome e Cargo, ou "Não especificado"]
*   **Tema da Formação:** [Tema]
*   **Dores Principais:** [Resumo das dores]
*   **Prazo:** [Data limite ou "Não especificado"]
*   **Estado da Organização:** [Indicar se foi criada pasta de raiz ou se é cliente existente]

### 2. Mapeamento Pedagógico
*   **Curso Sugerido:** [Nome do Curso no Catálogo]
*   **Taxa de Compatibilidade:** [X%]
*   **Racional e Módulos:** [Breve explicação de fit e módulos a incluir ou ajustar]

### 3. Rascunho de Email de Resposta
**Assunto:** [Assunto curto e descritivo]

[Rascunho de Email conforme o bd_estilo_escrita.md]

---
*Nota: A pasta do cliente foi criada/atualizada em `[link para a pasta do cliente]` e a tarefa de resposta foi adicionada ao progresso.*
```
