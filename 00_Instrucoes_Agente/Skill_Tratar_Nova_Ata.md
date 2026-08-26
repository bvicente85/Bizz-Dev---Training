---
type: Agent Skill
title: Tratar Nova Ata de Reunião
description: Processamento estruturado de transcrições e notas de reuniões com clientes, arquivamento e extração de tarefas (Action Items).
tags: [skill, reunioes, atas]
timestamp: 2026-06-18T10:23:00Z
---

# Skill: Tratar Nova Ata de Reunião
Esta instrução automatiza o processamento de notas de reunião e a gestão da carteira de clientes na Sala 03.

## Objetivo
Transformar notas brutas ou transcrições numa estrutura organizada de cliente, garantindo a atualização do histórico, do contexto e dos próximos passos comerciais.

## Fluxo de Execução Obrigatório
Sempre que fores ativado com esta Skill (através da menção `@Skill_Tratar_Nova_Ata`), deves seguir rigorosamente estes passos:

### 1. Extração de Inteligência
- Identificar o **Nome da Empresa/Cliente** e a **Data** da interação.
- Listar **Stakeholders** mencionados (identificando quem decide e quem influencia).
- Isolar a **"Dor" ou Necessidade** central (o problema que a formação deve resolver).
- Mapear os **Action Items** (tarefas combinadas, identificando o responsável e o prazo acordado).

### 2. Organização do Ficheiro Original (Ata)
- Identificar a data em que a reunião foi realizada.
- Se a data não for evidente nas notas ou no nome do ficheiro, **deves perguntar e confirmar a data com o utilizador** antes de avançar.
- Mover o ficheiro original com as notas da reunião para a pasta correspondente ao mês na diretoria `03_Carteira_Clientes\034_Reunioes_Clientes\` (ex: `034_Reunioes_Clientes\2026-05\`). Se a pasta do mês não existir, deves criá-la.

### 3. Validação no Palácio da Memória (Sala 03)
- Pesquisar em `03_Carteira_Clientes\032_Clientes\` se o cliente já existe.

### 4. Cenário: Cliente Novo (Criação)
- Executa o **Protocolo de Setup de Cliente Novo** conforme definido no Capítulo 3 do manual de operação [bd_instrucoes_operacao.md](file:///c:/Users/brunn/OneDrive%20-%20GIE%20IFE/Desktop/Bruno/PESSOAL/Business%20Development%20Formação/00_Instrucoes_Agente/bd_instrucoes_operacao.md).
- Preenche os ficheiros iniciais com os dados extraídos no Passo 1 (Nome da Empresa, Stakeholders, Dor principal).
- Escreve as notas brutas da reunião no ficheiro `[Nome]_meeting_notes.md`.

### 5. Cenário: Cliente Existente (Atualização)
- **Notas de Reunião:** Fazer *append* das novas notas no topo de `[Nome]_meeting_notes.md`.
- **Contexto:** Adicionar novos stakeholders ou dados estratégicos a `[Nome]_context.md` (mantendo o histórico).
- **Progresso:** Atualizar o histórico de interações e redefinir o "Próximo Passo" em `[Nome]_progress.md`.

### 6. Padrões de Qualidade e Estilo
- **Idioma:** Português Europeu obrigatório (ex: "contacto", "equacionar").
- **Tom:** Informal-profissional, direto e sem frases feitas (consultar `bd_estilo_escrita.md`).
- **Rigor:** Basear todas as conclusões em factos extraídos da ata.

### 7. Relatório de Execução e Follow-Up (Debrief)
Ao terminar, deves apresentar ao Bruno:
- Confirmação das ações tomadas (ex: "Pasta criada e 3 ficheiros gerados").
- Uma breve análise do ROI potencial ou urgência da oportunidade.
- A tabela de **Action Items** extraídos (Quem | Ação | Prazo).
- Um **rascunho de e-mail de debrief/alinhamento pós-reunião** para enviar ao cliente (em PT-PT ou EN, conforme o idioma do cliente), agradecendo a conversa e confirmando de forma resumida os próximos passos e datas combinadas, seguindo as diretrizes de [bd_estilo_escrita.md](file:///c:/Users/brunn/OneDrive%20-%20GIE%20IFE/Desktop/Bruno/PESSOAL/Business%20Development%20Formação/00_Instrucoes_Agente/bd_estilo_escrita.md).
