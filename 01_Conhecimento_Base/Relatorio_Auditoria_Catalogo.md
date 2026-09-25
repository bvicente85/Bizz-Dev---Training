# Auditoria de Cobertura do Catálogo Global de Cursos

## 1. Objetivo
Validar se o ficheiro `Catalogo_Global_Cursos.md` é um inventário completo e fiel dos ficheiros de cursos existentes em `011_Biblioteca_Programas`.

## 2. Metodologia
Script de análise exaustiva (`audit_catalog.py`) que percorre todos os ficheiros `.md`, isola os que são cursos, extrai os metadados (Título, Caminho, Duração), faz o parse da tabela markdown do Catálogo Global e realiza matching (por Caminho e Título Normalizado).

## 3. Resultados Globais

| Métrica | Resultado |
|---|---:|
| Ficheiros analisados | 543 |
| Cursos/programas identificados | 501 |
| Cursos no Catálogo Global | 540 |
| Cursos presentes em ambos | 492 |
| Cursos na Biblioteca mas ausentes do Catálogo | 9 |
| Cursos no Catálogo sem ficheiro correspondente | 48 |
| Cobertura do Catálogo | 98.20% |

## 4. Cursos na Biblioteca e no Catálogo
*(Amostra de 10 cursos para validação de formato)*
| ID | Curso (Biblioteca) | Ficheiro | Correspondência |
|---|---|---|---|
| - | Catálogo Geral de Cursos | 01_Conhecimento_Base/011_Biblioteca_Programas/_Catálogo_Geral_Cursos.md | Confirmado (Caminho/Título Exato) |
| - | Atitude Comercial e Espírito d | 01_Conhecimento_Base/011_Biblioteca_Programas/01_Vendas_e_Negociacao/Curso_Atitude_Comercial_Espirito_Servico.md | Confirmado (Caminho/Título Exato) |
| - | Curso: A lente da colaboração  | 01_Conhecimento_Base/011_Biblioteca_Programas/01_Vendas_e_Negociacao/Curso_A_lente_da_colaboração_e_da_performance.md | Confirmado (Caminho/Título Exato) |
| - | Curso: Business Developer | 01_Conhecimento_Base/011_Biblioteca_Programas/01_Vendas_e_Negociacao/Curso_Business_Developer.md | Confirmado (Caminho/Título Exato) |
| - | Como Fazer um Pitch | 01_Conhecimento_Base/011_Biblioteca_Programas/01_Vendas_e_Negociacao/Curso_Como_Fazer_um_Pitch.md | Confirmado (Caminho/Título Exato) |
| - | Curso: Gestão de clientes na p | 01_Conhecimento_Base/011_Biblioteca_Programas/01_Vendas_e_Negociacao/Curso_Gestão_de_clientes_na_prática.md | Confirmado (Caminho/Título Exato) |
| - | Curso: IP - Técnicas de Negoci | 01_Conhecimento_Base/011_Biblioteca_Programas/01_Vendas_e_Negociacao/Curso_IP_-_Técnicas_de_Negociação_Inglês.md | Confirmado (Caminho/Título Exato) |
| - | Curso: IP PNL aplicado à negoc | 01_Conhecimento_Base/011_Biblioteca_Programas/01_Vendas_e_Negociacao/Curso_IP_PNL_aplicado_à_negociação_Inglês.md | Confirmado (Caminho/Título Exato) |
| - | KAM – Key Account Management | 01_Conhecimento_Base/011_Biblioteca_Programas/01_Vendas_e_Negociacao/Curso_KAM_Key_Account_Management.md | Confirmado (Caminho/Título Exato) |
| - | Negociação Comercial | 01_Conhecimento_Base/011_Biblioteca_Programas/01_Vendas_e_Negociacao/Curso_Negociacao_Comercial.md | Confirmado (Caminho/Título Exato) |

## 5. Cursos na Biblioteca mas ausentes do Catálogo
| ID | Curso | Ficheiro | Área | Duração |
|---|---|---|---|---|
| - | Curso: Ciclo de formação em Recursos Humanos para não especialistas | 01_Conhecimento_Base/011_Biblioteca_Programas/02_Recursos_Humanos/Curso_Ciclo_de_formação_em_Recursos_Humanos_para_não_especialistas.md | 02_Recursos_Humanos |  14h | Metodologia: --- Slide slide7 --- FORM-AÇÃO Promover o envolvimento Propomos que os participantes iniciem o seu p... |
| - | Curso: Liderança situacional - Jogo dos Exploradores - 3 dias | 01_Conhecimento_Base/011_Biblioteca_Programas/10_Lideranca_e_Gestao_Equipas/Curso_Liderança_situacional_-_Jogo_dos_Exploradores_-_3_dias.md | 10_Lideranca_e_Gestao_Equipas |  21h | Metodologia: --- Slide slide2 --- As competências essenciais para liderar e gerir em diferentes situações |
| - | Storytelling para Líderes | 01_Conhecimento_Base/011_Biblioteca_Programas/10_Lideranca_e_Gestao_Equipas/Curso_Storytelling_para_Lideres.md | 10_Lideranca_e_Gestao_Equipas |  7 horas (1 dia) | Metodologia: Action Learning, simulações gravadas (autoscopia) e debriefing executivo |
| - | Curso: 5 Ferramentas para uma comunicação com impacto | 01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_5_Ferramentas_para_uma_comunicação_com_impacto.md | 15_Gestao_Projetos_e_Inovacao |  14h | Metodologia: essencialmente exemplificativas, práticas, que fomentem a partilha e o treino. --- Slide slide3 --- ... |
| - | Curso: Acompanhamento de KPIS e performance | 01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Acompanhamento_de_KPIS_e_performance.md | 15_Gestao_Projetos_e_Inovacao |  7h | Metodologia: --- Slide slide7 --- Clarificação de conceitos Feedback; Sínteses; Debriefings Utilização de exemplo... |
| - | Curso: Gestão de projetos com metodologias ágeis | 01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Gestão_de_projetos_com_metodologias_ágeis.md | 15_Gestao_Projetos_e_Inovacao |  21h | Metodologia: ágeis.pptx (PPTX) === --- Slide slide1 --- |
| - | Curso: Percurso - Rising Leaders | 01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Percurso_-_Rising_Leaders.md | 15_Gestao_Projetos_e_Inovacao |  7h | Metodologia: --- Slide slide14 --- Desenvolva a sua self leadership para alinhar as equipas com o negócio e a sat... |
| - | Curso: Percurso - Rising leaders - modulos transversais e de negocio | 01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Percurso_-_Rising_leaders_-_modulos_transversais_e_de_negocio.md | 15_Gestao_Projetos_e_Inovacao |  7h | Metodologia: --- Slide slide14 --- Desenvolva a sua self leadership para apoiar o crescimento da sua equipa |
| - | Curso: Plano de Formação Manpower - vários cursos desenvolvimento pessoal | 01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Plano_de_Formação_Manpower_-_vários_cursos_desenvolvimento_pessoal.md | 15_Gestao_Projetos_e_Inovacao |  14h | Metodologia: --- Slide slide8 --- FORM-AÇÃO Promover o envolvimento Propomos que os participantes iniciem o seu p... |

## 6. Cursos no Catálogo sem ficheiro correspondente
| ID | Curso | Entrada no Catálogo | Observação |
|---|---|---|---|
| - | A Jornada da Visao | `01_Conhecimento_Base/011_Biblioteca_Programas/01_Vendas_e_Negociacao/Curso_A_Jornada_da_Visao.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Inteligencia Emocional Comercial | `01_Conhecimento_Base/011_Biblioteca_Programas/01_Vendas_e_Negociacao/Curso_Inteligencia_Emocional_Comercial.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | ZEISS Elite Partners | `01_Conhecimento_Base/011_Biblioteca_Programas/01_Vendas_e_Negociacao/Curso_ZEISS_Elite_Partners.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Power BI | `01_Conhecimento_Base/011_Biblioteca_Programas/03_Tecnologias_Informacao/Office_Produtividade/Curso_Power_BI.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Marketing Digital | `01_Conhecimento_Base/011_Biblioteca_Programas/05_Marketing_e_Comunicacao/Curso_Marketing_Digital.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | A Lente da Colaboracao | `01_Conhecimento_Base/011_Biblioteca_Programas/10_Lideranca_e_Gestao_Equipas/Curso_A_Lente_da_Colaboracao.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Confianca Ativo Execucao | `01_Conhecimento_Base/011_Biblioteca_Programas/10_Lideranca_e_Gestao_Equipas/Curso_Confianca_Ativo_Execucao.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Curso: Gestão de Conflitos (Versão 7h - Metodologia Tradicional/Prática) | `01_Conhecimento_Base/011_Biblioteca_Programas/10_Lideranca_e_Gestao_Equipas/Curso_Gestao_Conflitos_7h.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Derrubar Paredes e Muros | `01_Conhecimento_Base/011_Biblioteca_Programas/10_Lideranca_e_Gestao_Equipas/Curso_Derrubar_Paredes_e_Muros.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Gold Mine Lideranca | `01_Conhecimento_Base/011_Biblioteca_Programas/10_Lideranca_e_Gestao_Equipas/Curso_Gold_Mine_Lideranca.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Lideranca Gestao Mudanca | `01_Conhecimento_Base/011_Biblioteca_Programas/10_Lideranca_e_Gestao_Equipas/Curso_Lideranca_Gestao_Mudanca.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Comunicacao Interna | `01_Conhecimento_Base/011_Biblioteca_Programas/11_Eficacia_Pessoal_e_Soft_Skills/Curso_Comunicacao_Interna.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Comunicacao com PNL | `01_Conhecimento_Base/011_Biblioteca_Programas/11_Eficacia_Pessoal_e_Soft_Skills/Curso_Comunicacao_com_PNL.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Cook and Learn Team Building | `01_Conhecimento_Base/011_Biblioteca_Programas/11_Eficacia_Pessoal_e_Soft_Skills/Curso_Cook_and_Learn_Team_Building.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Focar e Priorizar | `01_Conhecimento_Base/011_Biblioteca_Programas/11_Eficacia_Pessoal_e_Soft_Skills/Curso_Focar_e_Priorizar.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Gestao Energia e Workflow | `01_Conhecimento_Base/011_Biblioteca_Programas/11_Eficacia_Pessoal_e_Soft_Skills/Curso_Gestao_Energia_e_Workflow.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Mandamentos da Agilidade | `01_Conhecimento_Base/011_Biblioteca_Programas/11_Eficacia_Pessoal_e_Soft_Skills/Curso_Mandamentos_da_Agilidade.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Programa: A Lente do Orgulho: Inteligência Emocional e Naturalidade na Excelência | `01_Conhecimento_Base/011_Biblioteca_Programas/11_Eficacia_Pessoal_e_Soft_Skills/Curso_A_Lente_do_Orgulho.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Curso: Atitude Comercial e Espírito de Serviço | `01_Conhecimento_Base/011_Biblioteca_Programas/12_Atendimento_e_Relacao_Cliente/Curso_atitude_comercial_servico.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Curso: Imagem e Protocolo Empresarial | `01_Conhecimento_Base/011_Biblioteca_Programas/12_Atendimento_e_Relacao_Cliente/Curso_Imagem_Protocolo_Premium.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Curso: Redes sociais aplicadas à venda de automóveis premium | `01_Conhecimento_Base/011_Biblioteca_Programas/12_Atendimento_e_Relacao_Cliente/Curso_Redes_Sociais_Automovel_Premium.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Excelencia Servico ao Cliente | `01_Conhecimento_Base/011_Biblioteca_Programas/12_Atendimento_e_Relacao_Cliente/Curso_Excelencia_Servico_ao_Cliente.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Gestao de Conflitos | `01_Conhecimento_Base/011_Biblioteca_Programas/12_Atendimento_e_Relacao_Cliente/Curso_Gestao_de_Conflitos.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Programa: Atendimento e Serviço ao Cidadão | `01_Conhecimento_Base/011_Biblioteca_Programas/12_Atendimento_e_Relacao_Cliente/Curso_Atendimento_Servico_Cidadao.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Programa: Atitude Comercial e Espírito de Serviço | `01_Conhecimento_Base/011_Biblioteca_Programas/12_Atendimento_e_Relacao_Cliente/Curso_Atitude_Comercial.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Programa: CALL ME – Excelência no Atendimento Telefónico | `01_Conhecimento_Base/011_Biblioteca_Programas/12_Atendimento_e_Relacao_Cliente/Curso_Call_Me.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Programa: Customer Experience Management | `01_Conhecimento_Base/011_Biblioteca_Programas/12_Atendimento_e_Relacao_Cliente/Curso_Customer_Experience_Management.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Programa: Excelência no Atendimento | `01_Conhecimento_Base/011_Biblioteca_Programas/12_Atendimento_e_Relacao_Cliente/Curso_Excelencia_No_Atendimento.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Programa: Gerir a Relação com o Cliente 2.0 | `01_Conhecimento_Base/011_Biblioteca_Programas/12_Atendimento_e_Relacao_Cliente/Curso_Gerir_Relacao_Cliente_2_0.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Programa: Gestão de Cobranças e Recuperação de Créditos | `01_Conhecimento_Base/011_Biblioteca_Programas/12_Atendimento_e_Relacao_Cliente/Curso_Gestao_Cobrancas.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Programa: PLEASE COMPLAIN – Gestão de Reclamações | `01_Conhecimento_Base/011_Biblioteca_Programas/12_Atendimento_e_Relacao_Cliente/Curso_Please_Complain.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Programa: Reinventar a Experiência Cliente com a IA | `01_Conhecimento_Base/011_Biblioteca_Programas/12_Atendimento_e_Relacao_Cliente/Curso_Experiencia_Cliente_IA.txt` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Preçário YES'N'YOU 2026 | `01_Conhecimento_Base/011_Biblioteca_Programas/13_Linguas_Estrangeiras/Idiomas/YESNYOU_Preçário_2026.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Course: AI Applied to HR | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/course_ai_applied_hr.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Course: AI Mastery in Finance | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/course_ai_mastery_finance.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Course: AI for Content Creation in Marketing | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/course_ai_content_creation_marketing.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Course: AI-Powered Software Testing: Fundamentals and Best Practices | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/course_ai_powered_software_testing.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Course: Collaboration & Cross-functional Alignment | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/course_collaboration_cross_functional_alignment.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Course: Communication & Influence | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/course_communication_influence.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Course: Compliance and Governance of Artificial Intelligence (AI) | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/course_compliance_governance_ai.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Course: Performance Management & Goal Setting (OKRs) | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/course_performance_management_goal_setting_okrs.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Course: Product AI | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/course_product_ai.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Course: Public Speaking & Presenting with Impact | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/course_public_speaking_presenting_impact.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Course: Reinventing the Customer Experience with AI | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/course_reinventing_customer_experience_ai.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Course: Security of AI in Production | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/course_security_ai_production.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Course: Time Management & Prioritisation | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/course_time_management_prioritisation.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Course: Understanding Product and Tech Roadmaps | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/course_understanding_product_tech_roadmaps.md` | Possível ficheiro não .md, apagado ou nome alterado |
| - | Training Programme: Security & Risk Management and GDPR / Data Protection | `01_Conhecimento_Base/011_Biblioteca_Programas/16_Oferta_em_Ingles/programa_ciberseguranca_gdpr_cegid_en.md` | Possível ficheiro não .md, apagado ou nome alterado |

## 7. Possíveis Duplicados
Não testado exaustivamente nesta versão, focado em correspondência 1-para-1.

## 8. Correspondências Ambíguas

## 9. Caso Específico: Power Automate
**Análise para o curso "Microsoft Power Automate – Fundamentos e Casos Práticos" (TI-OFF-012)**

1. O ficheiro EXISTE na Biblioteca em: `01_Conhecimento_Base/011_Biblioteca_Programas/03_Tecnologias_Informacao/Office_Produtividade/curso_power_automate_fundamentos.md`\n2. O curso EXISTE no Catálogo Global.\n3. Linha exata: `| Tecnologias Informacao | **Microsoft Power Automate – Fundamentos e Casos Práticos** | 14 horas (2 dias) | - | - | `01_Conhecimento_Base/011_Biblioteca_Programas/03_Tecnologias_Informacao/Office_Produtividade/curso_power_automate_fundamentos.md` |`

## 10. Conclusão
O `Catalogo_Global_Cursos.md` **não é atualmente um inventário completo**, pois a cobertura apurada foi de 98.20%. Existem discrepâncias devidas a extensões não lidas (ex: ficheiros `.txt`), estruturas de pastas com caracteres invisíveis/especiais que quebram o parser da tabela, e ficheiros que o indexador saltou.

## 11. Recomendações
1. **Unificar Extensões:** Garantir que a Biblioteca apenas aceita `.md` e converter todos os `.txt` nativamente para `.md`.
2. **Atualizar o Indexador:** Modificar o script de indexação para tratar exceções no momento da escrita da tabela Markdown (escapar carateres como `|` no título).
3. **YAML Strict:** Obrigar todo e qualquer ficheiro de curso a ter o YAML Frontmatter para que o matching seja feito por `ID` e não por Título/Caminho, que são falíveis.
