---
type: Cliente Context
title: Contexto do Cliente - GPFA
description: Perfil de contexto, setor e interlocutores do cliente GPFA.
tags: [cliente, engenharia, arquitetura, automacao_ia]
timestamp: 2026-11-10T15:50:00Z
---
# GPFA - Contexto e Perfil

*Links:* [Progresso Comercial](./GPFA_progress.md) | [Notas de Reunião](./GPFA_meeting_notes.md) | [Índice Dossier](./_Índice_GPFA.md)


## Perfil da Empresa
- **Nome:** GPFA (GPFA / EPFR)
- **Sector:** Arquitetura, Engenharia, Fiscalização e Gestão de Obras
- **Especialização:** Forte especialização e volume de trabalho em projetos de **postos de abastecimento de combustível e redes de mobilidade elétrica** (onde cerca de 80% do trabalho técnico/documental é altamente repetitivo e padronizado).
- **Dimensão:** ~20 a 34 colaboradores. Pioneiros em BIM (desde 2007) em Portugal.
- **Ambiente de TI:** Em processo de migração para **Microsoft 365 / Outlook**. IT gerido em regime de outsourcing focado em gestão de rede e infraestrutura básica.

## Stakeholders
- **Miguel Freitas** (Sócio-Gerente / Proprietário e Decisor Principal)
  - Email: `miguelfreitas@gpfa.pt`
  - *Nota de Protocolo:* Deve estar obrigatoriamente em cópia em todas as propostas formais e comunicações de seguimento comercial.
- **Hugo Freitas** (Área Administrativa, Processos & Automação / Champion Técnico de IA)
  - Visão transversal completa de todos os fluxos e processos do gabinete (do início ao fecho da obra).
  - Background autodidata em programação (bases em C++ e PHP; noções de Python e PowerShell).
  - Lidera internamente a exploração de IA: subscreveu Claude (Claude Pro / Team Premium) e desenvolveu os primeiros protótipos de agentes e scripts para leitura de projetos e geração de memórias descritivas.
  - Alvo da capacitação técnica 1:1.
- **Raquel Santos** (Administrativa / Interlocutora Operacional CRM)
  - Email: `raquelsantos@gpfa.pt`
  - Telemóvel: 915728099
- **André** (Desenho e Modelação BIM)
- **Fernando** (Polivalente / Operacional)

## Parceiro Técnico Estratégico SKOLAE & Equipa Docente
- **People Change AI:**
  - **Samuel Mourato** e **Marco Almas:** Coordenação pedagógica, desenho da arquitetura de mentoria e suporte à integração no ecossistema da GPFA.
- **Formador Responsável:**
  - **José Martins:** Especialista em Automação de Processos & Liderança Tecnológica. Mais de 20 anos de experiência em engenharia de software (Blip/FanDuel, Talkdesk, Vodafone, Altice), CCP (Certificado de Competências Pedagógicas) e PSM I (Professional Scrum Master).

## Dores e Oportunidades de Automação
1. **Redução Drástica do Trabalho Repetitivo Documental:**
   - 80% dos projetos (postos de combustível e carregadores elétricos) seguem matrizes padronizadas.
   - Elaboração morosa de memórias descritivas (30 a 60 memórias/mês, cerca de 4h cada; com automação estruturada cai para metade ou 1h a 2h).
   - Termos de responsabilidade repetitivos (até 9 termos por projeto) e mapas comparativos de orçamentos de subempreiteiros.
2. **Mitigação do Risco Técnico ("Peças Soltas"):**
   - O Hugo já iniciou a construção autónoma de agentes no Claude e scripts em PowerShell/Python, mas existe o risco de criar fluxos frágeis sem boas práticas de arquitetura, controlo de versões (Git/Markdown), gestão de custos de tokens e segurança de chaves/dados.
   - A GPFA quer capacitá-lo com mentoria técnica dedicada para garantir robustez, autonomia interna e governança sólida.
3. **Fronteira com CAD e Revit:**
   - *AutoCAD:* Potencial de abordagem genérica / automação de ficheiros a médio prazo.
   - *Revit:* Fora de âmbito no imediato (proprietário e dados sensíveis).
4. **Infraestrutura e Hardware:**
   - Portátil atual (32 GB RAM) é limitado para computação paralela de engenharia + agentes locais.
   - Transição planeada: migração dos scripts em produção para um **desktop local dedicado encomendado pela GPFA**, com agendamento automático de tarefas e observabilidade (logs e alertas via Microsoft Teams).
