---
type: Cliente Context
title: Contexto do Cliente - GPFA
description: Perfil de contexto, setor e interlocutores do cliente GPFA.
tags: [cliente, engenharia, arquitetura, automacao_ia]
timestamp: 2026-10-20T11:30:00Z
---
# GPFA - Contexto e Perfil

*Links:* [Progresso Comercial](./GPFA_progress.md) | [Notas de Reunião](./GPFA_meeting_notes.md)


## Perfil da Empresa
- **Nome:** GPFA (GPFA / EPFR)
- **Sector:** Arquitetura, Engenharia, Fiscalização e Gestão de Obras
- **Especialização:** Forte especialização e volume de trabalho em projetos de **postos de abastecimento de combustível e redes de mobilidade elétrica** (onde cerca de 80% do trabalho técnico/documental é altamente repetitivo e padronizado).
- **Dimensão:** ~20 a 34 colaboradores. Pioneiros em BIM (desde 2007) em Portugal.
- **Ambiente de TI:** Em processo de migração para **Microsoft 365 / Outlook**. IT gerido em regime de outsourcing focado apenas em gestão de rede e resposta a emergências.

## Stakeholders
- **Miguel Freitas** (Sócio-Gerente / Proprietário e Decisor Principal)
  - Email: miguelfreitas@gpfa.pt
  - *Nota:* Deve estar obrigatoriamente em cópia em todas as propostas formais e comunicações de seguimento.
- **Hugo Freitas** (Área Administrativa, Processos & Automação / Champion Técnico de IA)
  - Visão transversal completa de todos os fluxos e processos do gabinete (do início ao fim da obra).
  - Background autodidata em programação (bases em C++ e PHP; noções básicas de Python).
  - Lidera internamente a exploração de IA: adquiriu licenças do Claude (Claude Pro / Team Premium) e desenvolveu os primeiros protótipos de agentes para leitura de projetos e geração de memórias descritivas.
- **Raquel Santos** (Administrativa / Interlocutor Operacional CRM)
  - Email: raquelsantos@gpfa.pt
  - Telemóvel: 915728099
- **André** (Desenho e Modelação BIM)
- **Fernando** (Polivalente / Operacional)

## Parceiro Técnico Estratégico SKOLAE
- **People Change AI:**
  - **Samuel Mourato** e **Marco Almas** (Especialistas em IA prática, agentes autónomos e automação corporativa).
  - Responsáveis pela arquitetura pedagógica do acompanhamento técnico, desenho da mentoria hands-on e suporte à integração de agentes no ecossistema da GPFA.

## Dores e Oportunidades de Automação
1. **Redução Drástica do Trabalho Repetitivo Documental:**
   - 80% dos projetos (postos de combustível e carregadores elétricos) seguem matrizes idênticas.
   - Elaboração morosa de memórias descritivas (processo tradicional demorava várias horas; com automação pode cair para 1 a 2 horas).
   - Termos de responsabilidade repetitivos (até 9 termos por projeto) e mapas comparativos de orçamentos de subempreiteiros.
2. **Mitigação do Risco Técnico ("Peças Soltas"):**
   - O Hugo já iniciou a construção autónoma de agentes no Claude, mas existe o risco de construir fluxos frágeis sem boas práticas de arquitetura de dados, prompting profissional e controlo de versões.
   - A GPFA quer capacitá-lo com mentoria técnica dedicada para garantir robustez, autonomia interna e escalabilidade.
3. **Fronteira com CAD e Revit:**
   - *AutoCAD:* Potencial de abordagem genérica / automação de ficheiros, mas sem integração profunda por agora.
   - *Revit:* Fora de âmbito no imediato (proprietário e dados sensíveis).
4. **Infraestrutura e Hardware:**
   - Portátil atual (32 GB RAM) insuficiente para computação paralela CAD + IA local/cloud.
   - A definir após piloto técnico: aquisição de workstation desktop de topo vs. servidor dedicado local (Xeon).
