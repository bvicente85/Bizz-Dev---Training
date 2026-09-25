# Análise dos 9 Casos Não Correspondidos

## 1. Resumo Executivo

| Categoria | Nº de casos |
|---|---:|
| Ausência real | 0 |
| Falso negativo do matching | 9 |
| Possível duplicado | 0 |
| Não é curso | 0 |
| Informação insuficiente | 0 |
| Outro | 0 |

## 2. Análise Individual

### Curso_Ciclo_de_formação_em_Recursos_Humanos_para_não_especialistas.md
- Caminho: `01_Conhecimento_Base/011_Biblioteca_Programas/02_Recursos_Humanos/Curso_Ciclo_de_formação_em_Recursos_Humanos_para_não_especialistas.md`
- É um curso/programa?: Sim
- Nome: Curso: Ciclo de formação em Recursos Humanos para não especialistas
- ID: Não tem
- Duração: 14h
- Área: 02_Recursos_Humanos
- Encontrado no catálogo?: Sim
- Correspondência encontrada: Linha 32 do Catálogo
- Classificação: Falso negativo do matching
- Evidência: A string exata do nome do ficheiro consta na Tabela Markdown do Catálogo.
- Causa provável: Falha no algoritmo de comparação do script devido a diferenças na codificação de caracteres especiais (ç, ã) entre a leitura do caminho do sistema de ficheiros (Windows/NTFS) e a string lida do ficheiro de texto (UTF-8).

### Curso_Liderança_situacional_-_Jogo_dos_Exploradores_-_3_dias.md
- Caminho: `01_Conhecimento_Base/011_Biblioteca_Programas/10_Lideranca_e_Gestao_Equipas/Curso_Liderança_situacional_-_Jogo_dos_Exploradores_-_3_dias.md`
- É um curso/programa?: Sim
- Nome: Curso: Liderança situacional - Jogo dos Exploradores - 3 dias
- ID: Não tem
- Duração: 21h
- Área: 10_Lideranca_e_Gestao_Equipas
- Encontrado no catálogo?: Sim
- Correspondência encontrada: Linha 291 do Catálogo
- Classificação: Falso negativo do matching
- Evidência: A string exata do nome do ficheiro consta no Catálogo.
- Causa provável: Divergência de codificação Unicode nos caracteres (ç, ã).

### Curso_Storytelling_para_Lideres.md
- Caminho: `01_Conhecimento_Base/011_Biblioteca_Programas/10_Lideranca_e_Gestao_Equipas/Curso_Storytelling_para_Lideres.md`
- É um curso/programa?: Sim
- Nome: Storytelling para Líderes
- ID: Não tem
- Duração: 7 horas (1 dia)
- Área: 10_Lideranca_e_Gestao_Equipas
- Encontrado no catálogo?: Sim
- Correspondência encontrada: Linha 343 do Catálogo
- Classificação: Falso negativo do matching
- Evidência: Ficheiro consta na Tabela Markdown.
- Causa provável: Diferença minúscula na normalização das strings pelo algoritmo de matching em Python.

### Curso_5_Ferramentas_para_uma_comunicação_com_impacto.md
- Caminho: `01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_5_Ferramentas_para_uma_comunicação_com_impacto.md`
- É um curso/programa?: Sim
- Nome: Curso: 5 Ferramentas para uma comunicação com impacto
- ID: Não tem
- Duração: 14h
- Área: 15_Gestao_Projetos_e_Inovacao
- Encontrado no catálogo?: Sim
- Correspondência encontrada: Linha 434 do Catálogo
- Classificação: Falso negativo do matching
- Evidência: Ficheiro consta no Catálogo.
- Causa provável: Diferença de *encoding* devido aos acentos ("ç", "ã").

### Curso_Acompanhamento_de_KPIS_e_performance.md
- Caminho: `01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Acompanhamento_de_KPIS_e_performance.md`
- É um curso/programa?: Sim
- Nome: Curso: Acompanhamento de KPIS e performance
- ID: Não tem
- Duração: 7h
- Área: 15_Gestao_Projetos_e_Inovacao
- Encontrado no catálogo?: Sim
- Correspondência encontrada: Linha 438 do Catálogo
- Classificação: Falso negativo do matching
- Evidência: Ficheiro consta perfeitamente no Catálogo.
- Causa provável: Diferença de case-sensitivity ou normalização no script original.

### Curso_Gestão_de_projetos_com_metodologias_ágeis.md
- Caminho: `01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Gestão_de_projetos_com_metodologias_ágeis.md`
- É um curso/programa?: Sim
- Nome: Curso: Gestão de projetos com metodologias ágeis
- ID: Não tem
- Duração: 21h
- Área: 15_Gestao_Projetos_e_Inovacao
- Encontrado no catálogo?: Sim
- Correspondência encontrada: Linha 482 do Catálogo
- Classificação: Falso negativo do matching
- Evidência: Presente no Catálogo.
- Causa provável: Acentos ("ã", "á").

### Curso_Percurso_-_Rising_Leaders.md
- Caminho: `01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Percurso_-_Rising_Leaders.md`
- É um curso/programa?: Sim
- Nome: Curso: Percurso - Rising Leaders
- ID: Não tem
- Duração: 7h
- Área: 15_Gestao_Projetos_e_Inovacao
- Encontrado no catálogo?: Sim
- Correspondência encontrada: Linha 496 do Catálogo
- Classificação: Falso negativo do matching
- Evidência: O ficheiro existe linha a linha.
- Causa provável: A normalização do título ignorou os hífens que são usados no título do ficheiro, e a pontuação pode ter causado um mismatch no score.

### Curso_Percurso_-_Rising_leaders_-_modulos_transversais_e_de_negocio.md
- Caminho: `01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Percurso_-_Rising_leaders_-_modulos_transversais_e_de_negocio.md`
- É um curso/programa?: Sim
- Nome: Curso: Percurso - Rising leaders - modulos transversais e de negocio
- ID: Não tem (a extração apanhou um ID residual falso "e")
- Duração: 7h
- Área: 15_Gestao_Projetos_e_Inovacao
- Encontrado no catálogo?: Sim
- Correspondência encontrada: Linha 497 do Catálogo
- Classificação: Falso negativo do matching
- Evidência: Está no Catálogo.
- Causa provável: Nome muito longo com vários hífens.

### Curso_Plano_de_Formação_Manpower_-_vários_cursos_desenvolvimento_pessoal.md
- Caminho: `01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Plano_de_Formação_Manpower_-_vários_cursos_desenvolvimento_pessoal.md`
- É um curso/programa?: Sim
- Nome: Curso: Plano de Formação Manpower - vários cursos desenvolvimento pessoal
- ID: Não tem (a extração apanhou um ID residual falso "e")
- Duração: 14h
- Área: 15_Gestao_Projetos_e_Inovacao
- Encontrado no catálogo?: Sim
- Correspondência encontrada: Linha 501 do Catálogo
- Classificação: Falso negativo do matching
- Evidência: Está no Catálogo.
- Causa provável: Codificação de acentos ("ç", "ã", "á").

## 3. Conclusões

1. **Quantos dos 9 estão realmente em falta?**
   **Zero (0).** Nenhum curso está fisicamente ausente da Tabela do Catálogo Global. O script gerador (da fase 1) apanhou e listou todos com sucesso na tabela.

2. **Quantos são falsos negativos do algoritmo?**
   **Nove (9).** Todos os casos assinalados no relatório anterior foram falhas do algoritmo de *matching* (o segundo script criado para comparar). O script não conseguiu reconhecer que a string gerada por `os.walk` no Windows era idêntica à string extraída do ficheiro Markdown (devido essencialmente a questões de encoding Unicode e formatação de texto em Python).

3. **Quantos não deveriam estar no catálogo?**
   **Zero (0).** Os 9 ficheiros são todos guiões/manuais de cursos perfeitamente válidos e estruturados.

4. **Existem problemas sistemáticos na estrutura dos ficheiros?**
   **Sim.** 
   - A dependência de "nomes de ficheiros" e "títulos H1" para identificar unicamente um curso é um processo altamente suscetível a erros de codificação de texto (acentos, hífens, maiúsculas).
   - Não existe um `ID` oficial na maior parte destes ficheiros (alguns têm extrações falsas como "ID: e" vindas de palavras no texto).

## 4. Recomendação

**Próximo Passo Técnico Recomendado:**
Uma vez validado que o Catálogo gerado está **100% completo** (os 9 ficheiros supostamente ausentes estavam de facto lá), a infraestrutura está livre de bugs de exclusão. 
A única falha é a robustez do cruzamento de dados posterior. 

Para resolver isto, o sistema deve avançar para a **Fase 2 da normalização**: executar o *script* no Modo "Apply" para injetar um cabeçalho **YAML estrito** em todos os ficheiros da Biblioteca, dotando cada um de um `id` oficial e normalizado. Isto garantirá que futuras pesquisas de máquina usem identificadores absolutos e ignorem variações sintáticas de Títulos ou Caminhos.
