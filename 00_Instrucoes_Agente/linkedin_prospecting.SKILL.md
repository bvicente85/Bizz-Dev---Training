---
type: Agent Skill
title: Prospeção LinkedIn
name: linkedin-prospector
version: 1.0.0
description: |
  Encontra perfis de profissionais e decisores no LinkedIn usando técnicas 
  de X-Ray Search (Google Dorking). Evita bloqueios de scraping.
compatibility: antigravity
allowed-tools:
  - search_web
tags: [skill, linkedin, decisores]
timestamp: 2026-06-18T10:23:00Z
---

# Skill de Prospeção de Contactos no LinkedIn (X-Ray Search)

A tua tarefa é encontrar os nomes e cargos exatos das pessoas que correspondem às personas de decisão de uma determinada organização.

## Fluxo de Pesquisa (Queries de X-Ray)

Para encontrar os contactos, deves adaptar as seguintes pesquisas no Google para a empresa/organização alvo:

1. **Para Persona A (Recursos Humanos / L&D):**
   `site:linkedin.com/in/ "[Nome da Empresa]" AND ("Recursos Humanos" OR "L&D" OR "Talento" OR "Formação" OR "Recursos Humanos")`

2. **Para Persona B (Diretores Técnicos / TI / Vendas / Negócio):**
   `site:linkedin.com/in/ "[Nome da Empresa]" AND ("Diretor" OR "Chefe" OR "Responsável" OR "Sistemas" OR "Auditoria" OR "VP")`

3. **Para Persona C (Líderes de Equipa e Champions):**
   `site:linkedin.com/in/ "[Nome da Empresa]" AND ("Coordenador" OR "Supervisor" OR "Manager" OR "Auditor")`

## Regras de Execução

1. Analisa os resultados da pesquisa do Google.
2. Extrai:
   * **Nome Completo**
   * **Cargo Atual** na organização alvo.
   * **Link do perfil do LinkedIn**
3. Valida se a pessoa trabalha na instituição (verifica se o cargo atual na descrição coincide).
4. Remove duplicados.
5. Se não encontrares nomes específicos, sugere os cargos e os departamentos a procurar manualmente.

## Template de Output

# Decisores Mapeados no LinkedIn: [Nome da Empresa]

### Persona A: Recursos Humanos & L&D
* **Nome:** [Nome do Profissional]
* **Cargo:** [Cargo exato no LinkedIn]
* **Perfil:** [URL do perfil do LinkedIn]
* **Relevância para a Venda:** [Porque é que esta pessoa deve ser contactada]

### Persona B: Diretores & Decisores de Negócio (Problem Owners)
* **Nome:** [Nome do Profissional]
* **Cargo:** [Cargo exato no LinkedIn]
* **Perfil:** [URL do perfil do LinkedIn]
* **Relevância para a Venda:** [Porque é que esta pessoa deve ser contactada]

### Persona C: Champions & Líderes de Equipa
* **Nome:** [Nome do Profissional]
* **Cargo:** [Cargo exato no LinkedIn]
* **Perfil:** [URL do perfil do LinkedIn]
* **Relevância para a Venda:** [Porque é que esta pessoa deve ser contactada]
