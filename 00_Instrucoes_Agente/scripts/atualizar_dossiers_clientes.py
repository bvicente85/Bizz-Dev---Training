import os

# --- 1. Joaquim Chaves Saúde ---
jcs_notes_path = r"03_Carteira_Clientes/032_Clientes/Joaquim Chaves Saúde/Joaquim Chaves Saúde_meeting_notes.md"
jcs_progress_path = r"03_Carteira_Clientes/032_Clientes/Joaquim Chaves Saúde/Joaquim Chaves Saúde_progress.md"

jcs_notes_update = """
## 14 de Outubro de 2026 - Reunião de Preparação: Beer Game (Armazém e Logística)
*Ata Completa:* [[meeting-report-JCS-beer-game-2026-10-14]] | [Ver Ficheiro Markdown](../../034_Reunioes_Clientes/2026-10/meeting-report-JCS-beer-game-2026-10-14.md)
* **Participantes:** Bruno Vicente (SKOLAE), João Diniz (Formador Especialista), Paulo Mestre (Armazém), Rafaela Gouveia, Cristiana Batista, Joana Caparica (Formação).
* **Resumo:** Alinhamento técnico da simulação *Beer Game* agendada para **23 de outubro de 2026**.
  - O armazém irá fechar totalmente no dia da ação para garantir foco pleno da equipa.
  - Objetivo: Dotar a equipa de visão holística de toda a cadeia de abastecimento (receção à expedição), combatendo a atuação em silos no SAP e melhorando a articulação com a área de compras.
  - Participantes confirmados: Márcia, Ana Beatriz, Rafaela (+ Fábio das Compras a convidar).
  - João Diniz conclui planeamento fino durante o fim de semana.

## 14 de Outubro de 2026 - Ponto de Situação Operacional (Cristiana Schneider)
*Ata Completa:* [[meeting-report-JCS-chamada-outubro-2026-10-14]] | [Ver Ficheiro Markdown](../../034_Reunioes_Clientes/2026-10/meeting-report-JCS-chamada-outubro-2026-10-14.md)
* **Participantes:** Bruno Vicente (SKOLAE), Cristiana (Schneider / RH JCS).
* **Resumo:**
  - **Turma de Outubro («Motivação e Orientação para Objetivos»):** Cancelada a sessão de outubro devido a falha interna de comunicação da JCS (agendas bloqueadas em datas desfasadas, apenas 2 presenças em 12).
  - **Decisão:** Não avançar para proteger a qualidade; turma reagendada para **janeiro de 2027** (follow-up em meados de dezembro).
  - **Turmas de Novembro:** As **duas turmas de novembro mantêm-se firmes** nas datas acordadas.
  - **Faturação:** Projeto global de 2.800€ a faturar aos poucos; necessária submissão da lista de presenças para emissão de POs por centro de custo.
"""

with open(jcs_notes_path, "r", encoding="utf-8") as f:
    jcs_notes_content = f.read()

if "14 de Outubro de 2026" not in jcs_notes_content:
    with open(jcs_notes_path, "a", encoding="utf-8") as f:
        f.write(jcs_notes_update)
    print("Updated JCS notes")

# Update JCS progress
with open(jcs_progress_path, "r", encoding="utf-8") as f:
    jcs_prog_content = f.read()

jcs_prog_add = """
* **14/10/2026 (Preparação Beer Game):** Reunião com Paulo Mestre e João Diniz. Ação presencial confirmada para 23 de outubro (armazém fecha).
* **14/10/2026 (Gestão de Turmas):** Turma de outubro de Motivação adiada para janeiro de 2027 (falha interna JCS na convocatória). As 2 turmas de novembro mantêm-se. Lista de presenças a submeter para POs por centro de custo (2.800€).
"""
if "14/10/2026" not in jcs_prog_content:
    target_marker = "## Histórico de Interações"
    if target_marker in jcs_prog_content:
        jcs_prog_content = jcs_prog_content.replace(target_marker, target_marker + "\n" + jcs_prog_add)
    else:
        jcs_prog_content += "\n## Histórico Recente\n" + jcs_prog_add
    with open(jcs_progress_path, "w", encoding="utf-8") as f:
        f.write(jcs_prog_content)
    print("Updated JCS progress")


# --- 2. Pecol ---
pecol_notes_path = r"03_Carteira_Clientes/032_Clientes/Pecol_Sistemas_de_Fixacao/Pecol_Sistemas_de_Fixacao_meeting_notes.md"
pecol_progress_path = r"03_Carteira_Clientes/032_Clientes/Pecol_Sistemas_de_Fixacao/Pecol_Sistemas_de_Fixacao_progress.md"

pecol_notes_update = """
## 14 de Outubro de 2026 - Contacto Telefónico (Call Center - Carla)
*Ata Completa:* [[meeting-report-pecol-2026-10-14]] | [Ver Ficheiro Markdown](../../034_Reunioes_Clientes/2026-10/meeting-report-pecol-2026-10-14.md)
* **Participantes:** Bruno Vicente (SKOLAE), Carla (Gestora de Call Center Pecol).
* **Resumo:** Carla esclareceu que a formação da sua equipa já foi realizada com outra entidade externa e que a equipa de vendas (>100 comerciais no terreno) tem fornecedor estabelecido.
* **Encaminhamento:** Indicou que o caminho é ligar para o número geral da Pecol no final de outubro, pedir para falar com os Recursos Humanos e referir o Dr. Frederico (ausente até ao fim do mês).
"""

with open(pecol_notes_path, "r", encoding="utf-8") as f:
    pecol_notes_content = f.read()

if "14 de Outubro de 2026" not in pecol_notes_content:
    with open(pecol_notes_path, "a", encoding="utf-8") as f:
        f.write(pecol_notes_update)
    print("Updated Pecol notes")

with open(pecol_progress_path, "r", encoding="utf-8") as f:
    pecol_prog_content = f.read()

pecol_prog_add = "* **[14-10-2026]:** Contacto com Carla (Call Center). Formação já realizada com concorrente. Ligar no final de outubro para o número geral da Pecol e contactar RH referenciando o Dr. Frederico."
if "14-10-2026" not in pecol_prog_content:
    pecol_prog_content = pecol_prog_content.replace("## Histórico de Interações", "## Histórico de Interações\n" + pecol_prog_add)
    with open(pecol_progress_path, "w", encoding="utf-8") as f:
        f.write(pecol_prog_content)
    print("Updated Pecol progress")


# --- 3. Lyzer ---
lyzer_notes_path = r"03_Carteira_Clientes/032_Clientes/Lyzer/Lyzer_meeting_notes.md"
lyzer_progress_path = r"03_Carteira_Clientes/032_Clientes/Lyzer/Lyzer_progress.md"

lyzer_notes_update = """
## 14 de Outubro de 2026 | Alinhamento de Calendário (Design Thinking & Gestão de Projetos)
*Ata Completa:* [[meeting-report-alinhamento-projetos-novembro-2026-10-14]] | [Ver Ficheiro Markdown](../../034_Reunioes_Clientes/2026-10/meeting-report-alinhamento-projetos-novembro-2026-10-14.md)
* **Participantes:** Bruno Vicente e Coordenação de Projetos.
* **Design Thinking (21h):** Cliente solicitou maior número de sessões no período da tarde. Acordado propor o acréscimo do **dia 26 de novembro à tarde** mantendo a totalidade das 21 horas para não comprometer os exercícios práticos.
* **Gestão de Projetos (António Bento):** Curso reagendado para novembro com reunião de preparação já marcada. Forte alinhamento com a nova dinâmica comercial pretendida pelo novo administrador francês.
"""

with open(lyzer_notes_path, "r", encoding="utf-8") as f:
    lyzer_notes_content = f.read()

if "14 de Outubro de 2026" not in lyzer_notes_content:
    with open(lyzer_notes_path, "a", encoding="utf-8") as f:
        f.write(lyzer_notes_update)
    print("Updated Lyzer notes")

with open(lyzer_progress_path, "r", encoding="utf-8") as f:
    lyzer_prog_content = f.read()

lyzer_prog_add = "*   **2026-10-14:** Definição de proposta para Francisca Galante: propor o dia 26 de novembro à tarde para completar as 21h de Design Thinking; Gestão de Projetos reagendada para novembro com António Bento."
if "2026-10-14" not in lyzer_prog_content:
    lyzer_prog_content = lyzer_prog_content.replace("## Histórico de Interações", "## Histórico de Interações\n" + lyzer_prog_add)
    with open(lyzer_progress_path, "w", encoding="utf-8") as f:
        f.write(lyzer_prog_content)
    print("Updated Lyzer progress")


# --- 4. Hydra ---
hydra_notes_path = r"03_Carteira_Clientes/032_Clientes/Hydra/Hydra_meeting_notes.md"
hydra_progress_path = r"03_Carteira_Clientes/032_Clientes/Hydra/Hydra_progress.md"

hydra_notes_update = """
## 14 de Outubro de 2026 - Ponto de Situação de Calendário e Faturação
*Ata Completa:* [[meeting-report-alinhamento-projetos-novembro-2026-10-14]] | [Ver Ficheiro Markdown](../../034_Reunioes_Clientes/2026-10/meeting-report-alinhamento-projetos-novembro-2026-10-14.md)
* **Participantes:** Bruno Vicente e Coordenação de Projetos.
* **Calendário:** Sessões de formação reagendadas para **27 e 28 de outubro de 2026**.
* **Cobranças/Financeiro:** Existem cobranças pendentes a acompanhar.
* **Próximos Passos:** Enviar e-mail à Hydra a confirmar as novas datas das sessões e contactar Margarida (Topskillers) para aferir novidades de equipa e contratações.
"""

with open(hydra_notes_path, "r", encoding="utf-8") as f:
    hydra_notes_content = f.read()

if "14 de Outubro de 2026" not in hydra_notes_content:
    with open(hydra_notes_path, "a", encoding="utf-8") as f:
        f.write(hydra_notes_update)
    print("Updated Hydra notes")

with open(hydra_progress_path, "r", encoding="utf-8") as f:
    hydra_prog_content = f.read()

hydra_prog_add = "* **14/10/2026:** Sessões reagendadas para 27 e 28 de outubro. Verificar cobranças pendentes e enviar email de confirmação à cliente."
if "14/10/2026" not in hydra_prog_content:
    hydra_prog_content = hydra_prog_content.replace("## 🚦 Estado Atual do Funil de Vendas", "## 🚦 Estado Atual do Funil de Vendas\n" + hydra_prog_add)
    with open(hydra_progress_path, "w", encoding="utf-8") as f:
        f.write(hydra_prog_content)
    print("Updated Hydra progress")

print("All client files updated successfully!")
