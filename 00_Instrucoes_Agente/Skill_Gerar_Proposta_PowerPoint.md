---
type: Agent Skill
title: Gerar Proposta em PowerPoint (SKOLAE Standard)
description: Automatização da criação de propostas comerciais em PowerPoint a partir do template oficial da SKOLAE, preservando rigorosamente a identidade visual, tipografias GT Walsheim/Basier e grelha de cartões.
tags: [skill, propostas, pptx, powerpoint, automacao]
timestamp: 2026-09-17T13:35:00Z
---

# Skill: Gerar Proposta em PowerPoint (SKOLAE Standard)

Esta skill permite gerar automaticamente apresentações oficiais de propostas comerciais em PowerPoint (`.pptx`) para clientes corporativos, utilizando como base o molde mestre `Template Proposta - 1 curso.pptx`.

---

## 1. Gatilhos de Ativação (Triggers)
A skill deve ser ativada sempre que o utilizador pedir:
* *"Cria a proposta em PowerPoint para o cliente [Cliente] com o curso [Curso]"*
* *"Gera a proposta PPTX para a empresa [Empresa] com a formação [Formação]"*
* *"Prepara o PowerPoint da proposta de [Curso] para [Cliente]"*

---

## 2. Regras de Design e Identidade Visual (Invariáveis)

1. **Preservação Mestre do Template:**
   * O ficheiro base `Template Proposta - 1 curso.pptx` **nunca é sobrescrito**. O ficheiro resultante é gravado na pasta do cliente em `03_Carteira_Clientes/032_Clientes/[Cliente]/Proposta_[Cliente]_[Curso].pptx`.
   * Todos os slides institucionais (Slides 7 a 11 e 14 a 22) mantêm-se 100% inalterados.
2. **Tipografia Oficial Obrigatória:**
   * **Títulos de Capa (Slides 1, 3, 4, 5):** `GT Walsheim Pro Condensed Black` a 48pt em **Branco Puro** (`#FFFFFF`).
   * **Títulos no Itinerário (Slides 12, 13):** `GT Walsheim Pro Bold` a 28pt em **Laranja SKOLAE** (`#FF9B23`).
   * **Subtítulos e Etapas:** `GT Walsheim Pro Bold SBd`.
   * **Títulos de Módulos (Slide 13):** `Basier Circle` em caixa alta a 12pt com cor **Laranja Destaque** (`#FF912B`).
   * **Corpo de Texto, Tópicos e Objetivos:** `Basier Circle` a 10.5pt ou 11pt.
   * **Texto do Enquadramento (Slide 6):** `Basier Square` a 12pt.
3. **Regra Anti-Bullets no Slide 13:**
   * É **estritamente proibido** inserir caracteres literais de lista (`•`, `-`, etc.) no Slide 13. Todos os tópicos e objetivos devem ser gerados como linhas limpas de texto simples para facilitar a edição pelo utilizador.
4. **Alocação Exata de Grupos no Slide 12:**
   * O subtítulo superior (`CaixaDeTexto 81`) contém apenas a promessa curta em 1 linha.
   * Os **Destinatários** são inseridos no cartão dedicado `Agrupar 9` (`CaixaDeTexto 28`).
   * As **Competências a Desenvolver** são inseridas no cartão dedicado `Agrupar 1` (`CaixaDeTexto 27`).
   * As **Metodologias** são inseridas no cartão dedicado `Agrupar 5` (`CaixaDeTexto 26`).
5. **Preservação do Bloco Metodológico Gráfico Standard (TREINO / ESTIMULAR A APRENDIZAGEM):**
   * No slide de abertura do itinerário (Slide 12 no template base de 22 slides / Slide 8 após eliminação das capas excedentes), o bloco gráfico à direita (`CaixaDeTexto 83`, `CaixaDeTexto 84` e `CaixaDeTexto 85`: *"TREINO / ESTIMULAR A APRENDIZAGEM"*, *"Cenarização; role playing..."*, *"Utilização de exemplos, estudos de caso..."* e *"Clarificação de conceitos / Feedback / Sínteses / Debriefings"*) é **estritamente standard e invariável**. **Nunca deve ser adaptado ou alterado**, mantendo-se 100% fiel ao template de origem.

---

## 3. Fluxo de Execução Automatizado

Ao receber um pedido de criação de proposta PPTX:

1. **Recuperação de Dados Factual:**
   * Consultar o ficheiro do curso em `01_Conhecimento_Base/011_Biblioteca_Programas/` para extrair: Título, Carga Horária, Destinatários, Metodologias e os 4 Módulos com os respetivos tópicos.
   * Consultar o histórico ou contexto do cliente em `03_Carteira_Clientes/032_Clientes/[Cliente]/` (se existente) para afinar o enquadramento.
2. **Construção do Payload Estruturado (JSON):**
   * Estruturar os dados no formato esperado pelo motor:
     * `cliente`: Nome curto do cliente (ex: ERSE, TIBA);
     * `cliente_completo`: Designação oficial (ex: ERSE — Entidade Reguladora dos Serviços Energéticos);
     * `area`: Área oficial da SKOLAE (ex: MARKETING E COMUNICAÇÃO, VENDAS E NEGOCIAÇÃO);
     * `titulo_curso`: Título em caixa alta (ex: MARKETING DIGITAL CORPORATIVO);
     * `subtitulo`: Promessa de impacto em 1 linha;
     * `duracao`: Ex.: 14 horas;
     * `destinatarios`: Público-alvo específico do cliente;
     * `enquadramento_p1` a `p4`: Narrativa institucional SKOLAE (com destaque do cliente);
     * `proposito`: Frase clara e direta no bloco WHY;
     * `competencias`: Lista de 4 a 6 competências chave;
     * `objetivos_especificos`: Lista de 5 a 6 objetivos em texto limpo;
     * `modulos`: Lista dos 4 módulos com os tópicos correspondentes.
3. **Execução do Script Motor:**
   * Executar o script `00_Instrucoes_Agente/scripts/gerar_proposta_pptx.py` passando o JSON.
4. **Validação e Entrega:**
   * Confirmar a integridade do ficheiro gerado e fornecer ao utilizador o link local clicável no formato `[Abrir Proposta](file:///...)`.
