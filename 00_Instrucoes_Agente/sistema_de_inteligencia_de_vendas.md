---
type: Architecture
title: Sistema de Inteligência de Vendas - SKOLAE (AntiGravity)
description: Apresentação da arquitetura e estrutura de pastas do repositório local do cérebro comercial.
tags: [arquitetura, manual]
timestamp: 2026-06-18T10:23:00Z
---

# Sistema de Inteligência de Vendas - SKOLAE (AntiGravity)

Este repositório contém o "Cérebro" e o "Banco de Memória" para a gestão de Business Development na SKOLAE. O sistema utiliza o AntiGravity para processar ficheiros Markdown locais, garantindo privacidade, rapidez e personalização total.

## 📂 Estrutura do Sistema

A organização de pastas é crítica para que a IA consiga cruzar regras globais com dados específicos de clientes:

Raiz/
│
01_Conhecimento_Base/
│   ├── 01_biblioteca de programas/   # Cursos organizados por subpastas (01-16)
│   ├── 02_outras fontes de conhecimento/ # Ativos extra, PDFs e Consultoria
│   └── bd_biblioteca_cursos.md        # Índice central e links
│
02_Metodologias/                       # Templates e Metodologia SKOLAE
│
03_Carteira_Clientes/                  # Gestão de Contas e Pipeline
    ├── Clientes/
    │   ├── adnovum/
    │   │   ├── adnovum_context.md
    │   │   ├── adnovum_meeting_notes.md
    │   │   └── adnovum_progress.md
    └── 

## ⚙️ Como Operar

1. **Workspace:** Abre sempre a pasta Raiz no teu AntiGravity.
2. **Contexto Local:** Ao trabalhares um cliente, o agente lê os ficheiros dentro da pasta desse cliente.
3. **Inteligência Global:** O agente utiliza caminhos relativos (`../../`) para consultar as instruções de operação e o estilo de escrita que estão na raiz.
4. **Atualização:** Após cada reunião ou interação, os ficheiros `_meeting_notes.md` e `_progress.md` devem ser atualizados para manter a "memória fresca" da IA.

## 🚀 Portabilidade e Backup

* **Local First:** Todo o sistema vive na tua máquina. Não há dependência de bases de dados externas.
* **Migração:** Para levar este sistema para outro computador, basta copiar a pasta raiz.
* **Backup:** Recomenda-se a sincronização desta pasta com um serviço de cloud (OneDrive/Google Drive) para evitar perda de dados e permitir o trabalho em múltiplos dispositivos.

## 🧠 Regras de Ouro
* Nunca enviar propostas genéricas.
* Validar sempre a biblioteca de cursos antes de desenhar soluções novas.
* Manter o tom informal-profissional e o Português Europeu.