---
type: Agent Skill
title: Adicionar Novo Curso / Serviço
description: Protocolo de extração, estruturação e catalogação de novos cursos e serviços na biblioteca central.
tags: [skill, cursos, biblioteca]
timestamp: 2026-06-18T10:23:00Z
---

# Skill: Adicionar Novo Curso / Serviço
Este protocolo define como o Antigravity deve processar novas informações de cursos (via PDF, Site ou Manual) para manter o ecossistema de BD atualizado de forma rápida e autónoma.

## Gatilho (Trigger)
"Usa a skill de adicionar curso para [FONTE]" ou pedidos similares de atualização de biblioteca.

---

## Fase 1: Extração de Inteligência
O Agente deve analisar a fonte e extrair obrigatoriamente:
1. **Verificação de Ficheiro Existente:** Antes de iniciar, validar se já existe um ficheiro para este curso na pasta da área core. 
   * Se o ficheiro NÃO existir: Avançar para a extração normal.
   * Se o ficheiro JÁ existir: Inspecionar o seu conteúdo. Caso seja um rascunho corrompido, com erros de OCR ou um marcador de ficheiro vazio (ex: `=== FILE: ... ===`), o agente DEVE propor ao utilizador a sua atualização com o conteúdo real do PDF, em vez de saltar a tarefa.
2. **Título Oficial do Curso**
3. **Área Core da SKOLAE:** (Cruzar com as 15 áreas na bd_biblioteca_cursos.md)
4. **Carga Horária Sugerida**
5. **Metodologia:** (Ex: Presencial, Live Training, VOD, Action Learning)
6. **Público-alvo:** (Ex: Middle Management, Operacionais, RH)
7. **Objetivos Pedagógicos:** (Mínimo 3 pontos)
8. **Programa Detalhado:** (Estrutura de módulos ou tópicos)
9. **Formador/Expert Sugerido:** (Se mencionado)

---

## Fase 2: Criação do Ficheiro de Detalhe
Criar um ficheiro Markdown em: `01_Conhecimento_Base/01_biblioteca de programas/[Subpasta_da_Area]/Curso_[NOME_CURSO].md`
**Template do Ficheiro:**
```markdown
# Curso: [Nome]
**Área:** [Área Core] | **Duração:** [X]h | **Metodologia:** [Tipo]

## Descrição e Objetivos
[Breve resumo do propósito do curso]
* Objetivo 1...
* Objetivo 2...

## Programa Detalhado
### 1. [Módulo 1]
* Tópico...
### 2. [Módulo 2]
* Tópico...

## Perfil do Formador / Notas de Venda
[Informação sobre o facilitador ou argumentos de venda extraídos]
```

---

## Fase 3: Sincronização da Biblioteca (Indexação)
1. Abrir: `01_Conhecimento_Base/bd_biblioteca_cursos.md`
2. Localizar a **Área Core** correspondente.
3. Inserir o novo curso na secção `*Programas Detalhados:*`, criando o link para o ficheiro gerado na Fase 2 (usando o caminho completo com a subpasta correta).
   * Exemplo: `[Nome do Curso](file:///path/to/01_biblioteca%20de%20programas/XX_Area/file.md)`

---

## Fase 4: Otimização de Proposta (Opcional)
Se o curso for de um tema radicalmente novo ou de consultoria:
1. Abrir: `02_Metodologias/bd_biblioteca_enquadramentos.md`
2. Criar um novo **Template de Enquadramento** seguindo a estrutura lógica (Contexto -> Autoridade -> Impacto).

---

## Checklist de Conclusão para o Usuário
O Agente deve responder confirmando:
- [ ] Leitura completa da fonte efetuada.
- [ ] Ficheiro de detalhe criado em /01_biblioteca de programas/[Area]/.
- [ ] Biblioteca de cursos atualizada com o link direto no índice central.
- [ ] (Se aplicável) Novo template de enquadramento adicionado.
- [ ] Próximo passo sugerido (ex: gerar proposta para cliente X).
