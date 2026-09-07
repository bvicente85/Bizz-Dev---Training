# Taxonomia de Cursos (Diagnóstico e Proposta)

## 1. Taxonomia Observada (Atual)
A organização baseia-se em diretórios físicos do Windows, com numerações rígidas (ex: `06_Area_Financeira`, `10_Lideranca_e_Gestao_Equipas`).
- **Problema Estrutural:** Um curso cruza áreas, mas fica bloqueado pela estrutura de pastas única.
- **Tags Existentes:** Poucas e não controladas.

## 2. Proposta de Normalização (YAML Frontmatter para Fase 2)
Todos os ficheiros `.md` e `.txt` na pasta `011_Biblioteca_Programas` devem ser convertidos num standard uniforme, sem alterar as pastas, adicionando ao topo o seguinte bloco:

```yaml
---
title: "Título Oficial do Curso"
area: "Grande Área (ex: Liderança, Comunicação, Vendas)"
subarea: "Tópico Específico (ex: Conflitos, Protocolo)"
duracao_horas: 14 
modalidade: [Presencial, Live Training, E-learning, Híbrido]
publico: [Líderes, Técnicos, Operacionais, Todos]
competencias: [Escuta Ativa, Resiliência, Delegação]
tags: [conflitos, feedback, equipas]
---
```
