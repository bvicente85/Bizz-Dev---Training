import os
import re

cases = [
    r"01_Conhecimento_Base/011_Biblioteca_Programas/02_Recursos_Humanos/Curso_Ciclo_de_formação_em_Recursos_Humanos_para_não_especialistas.md",
    r"01_Conhecimento_Base/011_Biblioteca_Programas/10_Lideranca_e_Gestao_Equipas/Curso_Liderança_situacional_-_Jogo_dos_Exploradores_-_3_dias.md",
    r"01_Conhecimento_Base/011_Biblioteca_Programas/10_Lideranca_e_Gestao_Equipas/Curso_Storytelling_para_Lideres.md",
    r"01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_5_Ferramentas_para_uma_comunicação_com_impacto.md",
    r"01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Acompanhamento_de_KPIS_e_performance.md",
    r"01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Gestão_de_projetos_com_metodologias_ágeis.md",
    r"01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Percurso_-_Rising_Leaders.md",
    r"01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Percurso_-_Rising_leaders_-_modulos_transversais_e_de_negocio.md",
    r"01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Plano_de_Formação_Manpower_-_vários_cursos_desenvolvimento_pessoal.md"
]

catalog_path = r"01_Conhecimento_Base/Catalogo_Global_Cursos.md"
with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog_lines = f.readlines()

print("--- ANALYZING 9 CASES ---")
for path in cases:
    print(f"\nFILE: {path}")
    if not os.path.exists(path):
        print("  -> ERROR: File not found locally!")
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "NO H1 TITLE"
    
    id_match = re.search(r'(?i)ID:?\s*([A-Z0-9\-]+)', content)
    course_id = id_match.group(1).strip() if id_match else "NO ID"
    
    is_course = "curso" in content.lower() or "objetivo" in content.lower() or "formação" in content.lower()
    
    print(f"  -> Title: {title}")
    print(f"  -> ID: {course_id}")
    print(f"  -> Looks like course: {is_course}")
    
    # Search in catalog
    print("  -> Searching catalog for filename...")
    filename = os.path.basename(path)
    found_in_catalog = False
    for i, line in enumerate(catalog_lines):
        if filename in line:
            print(f"     [MATCH EXACT FILENAME] Line {i}: {line.strip()}")
            found_in_catalog = True
        elif title != "NO H1 TITLE" and title[:15] in line:
             print(f"     [MATCH TITLE PARTIAL] Line {i}: {line.strip()}")
             found_in_catalog = True
             
    if not found_in_catalog:
        print("     [NO MATCH FOUND IN CATALOG]")

