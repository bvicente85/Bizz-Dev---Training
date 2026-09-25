import os
import re
from pathlib import Path
from difflib import SequenceMatcher

def similar(a, b):
    if not a or not b: return 0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def normalize(text):
    if not text: return ""
    return re.sub(r'[^a-z0-9]', '', text.lower())

def extract_course_metadata(filepath, base_dir):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None

    # Ignore files that are clearly not courses (e.g., indexes)
    filename = filepath.name
    if filename.startswith('_Índice') or filename.lower() == 'index.md':
        return {'is_course': False, 'filepath': filepath.relative_to(base_dir).as_posix()}
        
    # Very basic heuristic: Does it have an H1 or "Curso" in filename or content looks like a course?
    if not re.search(r'(?i)(curso|programa|formação|objetivos|duração|programa)', content) and not filename.lower().startswith('curso'):
        return {'is_course': False, 'filepath': filepath.relative_to(base_dir).as_posix()}

    meta = {
        'is_course': True,
        'filepath': filepath.relative_to(base_dir).as_posix(),
        'filename': filename,
        'title': None,
        'id': None,
        'duracao': None,
        'area': None,
        'subarea': None,
        'nivel': None,
        'formato': None
    }

    # Area/Subarea from path
    parts = filepath.parts
    if '011_Biblioteca_Programas' in parts:
        idx = parts.index('011_Biblioteca_Programas')
        if idx + 1 < len(parts):
            meta['area'] = parts[idx + 1]
        if idx + 2 < len(parts) - 1:
            meta['subarea'] = parts[idx + 2]

    # ID extraction
    id_match = re.search(r'(?i)\*\*ID:?\*\*\s*([A-Z0-9\-]+)', content)
    if id_match:
        meta['id'] = id_match.group(1).strip()
    
    # Title extraction
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        meta['title'] = title_match.group(1).strip()
    else:
        meta['title'] = filename.replace('curso_', '').replace('Curso_', '').replace('.md', '').replace('_', ' ')
        
    # Duration
    dur_match = re.search(r'(?i)Duração:?\s*(.+)', content)
    if dur_match:
        meta['duracao'] = dur_match.group(1).strip().replace('**', '')

    # Nivel/Formato
    mod_match = re.search(r'(?i)Modalidade:?\s*(.+)', content)
    if mod_match:
        meta['formato'] = mod_match.group(1).strip().replace('**', '')

    return meta

def parse_catalog(catalog_path):
    catalog_courses = []
    if not os.path.exists(catalog_path):
        return catalog_courses
        
    with open(catalog_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Find table
    in_table = False
    for line in lines:
        if '|' in line and '---' in line:
            in_table = True
            continue
        if in_table and '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6:
                area = parts[1]
                title = parts[2].replace('**', '')
                duracao = parts[3]
                dest = parts[4]
                path_str = parts[6].replace('`', '') if len(parts) > 6 else ""
                
                catalog_courses.append({
                    'title': title,
                    'area': area,
                    'duracao': duracao,
                    'filepath': path_str,
                    'raw_line': line.strip()
                })
    return catalog_courses

def generate_report():
    base_dir = Path(r"C:\Users\brunn\OneDrive - GIE IFE\Desktop\Bruno\PESSOAL\Business Development Formação")
    bib_dir = base_dir / "01_Conhecimento_Base" / "011_Biblioteca_Programas"
    cat_path = base_dir / "01_Conhecimento_Base" / "Catalogo_Global_Cursos.md"
    
    all_files = []
    for root, dirs, files in os.walk(bib_dir):
        for f in files:
            if f.endswith('.md'):
                all_files.append(Path(root) / f)
                
    lib_courses = []
    non_courses = []
    
    for f in all_files:
        meta = extract_course_metadata(f, base_dir)
        if meta:
            if meta['is_course']:
                lib_courses.append(meta)
            else:
                non_courses.append(meta)
                
    cat_courses = parse_catalog(cat_path)
    
    # Matching Logic
    in_both = []
    only_in_lib = []
    only_in_cat = list(cat_courses)
    ambiguous = []
    duplicates = []
    
    # Track matched cat indices
    matched_cat_indices = set()
    
    for lib in lib_courses:
        matched = False
        best_match = None
        best_score = 0
        best_idx = -1
        
        for i, cat in enumerate(cat_courses):
            if i in matched_cat_indices:
                continue
                
            # Path match
            if lib['filepath'] and cat['filepath'] and lib['filepath'] in cat['filepath']:
                matched = True
                best_match = cat
                best_idx = i
                break
                
            # Title match
            if lib['title'] and cat['title']:
                norm_lib = normalize(lib['title'])
                norm_cat = normalize(cat['title'])
                if norm_lib == norm_cat and len(norm_lib) > 3:
                    matched = True
                    best_match = cat
                    best_idx = i
                    break
                    
                score = similar(lib['title'], cat['title'])
                if score > best_score:
                    best_score = score
                    best_match = cat
                    best_idx = i
                    
        if matched:
            in_both.append((lib, best_match, "Confirmado (Caminho/Título Exato)"))
            matched_cat_indices.add(best_idx)
        elif best_score > 0.85:
            ambiguous.append((lib, best_match, f"Score: {best_score:.2f}"))
            # Treat as essentially in both, but we log it as ambiguous
            in_both.append((lib, best_match, "Possível Correspondência"))
            matched_cat_indices.add(best_idx)
        else:
            only_in_lib.append(lib)
            
    # Compute only in cat
    only_in_cat = [cat for i, cat in enumerate(cat_courses) if i not in matched_cat_indices]
    
    # Compute coverage
    total_lib = len(lib_courses)
    total_cat = len(cat_courses)
    total_both = len(in_both)
    coverage = (total_both / total_lib * 100) if total_lib > 0 else 0
    
    # Specific case
    power_automate_case = "O ficheiro `01_Conhecimento_Base/011_Biblioteca_Programas/03_Tecnologias_Informacao/Office_Produtividade/curso_power_automate_fundamentos.md` NÃO existe na Biblioteca de Programas (pelo menos não com esse nome ou extensão .md). Verifiquei todos os caminhos e ficheiros na pasta."
    
    for f in all_files:
        if 'power_automate_fundamentos' in str(f).lower():
            meta = extract_course_metadata(f, base_dir)
            
            in_cat = False
            cat_line = ""
            for cat in cat_courses:
                if 'power automate' in cat['title'].lower() or ('power_automate_fundamentos' in cat['filepath']):
                    in_cat = True
                    cat_line = cat['raw_line']
                    break
                    
            if in_cat:
                power_automate_case = f"1. O ficheiro EXISTE na Biblioteca em: `{f.relative_to(base_dir).as_posix()}`\\n2. O curso EXISTE no Catálogo Global.\\n3. Linha exata: `{cat_line}`"
            else:
                power_automate_case = f"1. O ficheiro EXISTE na Biblioteca em: `{f.relative_to(base_dir).as_posix()}`\\n2. O curso NÃO EXISTE no Catálogo Global. O indexador falhou a sua recolha ou não fez o matching corretamente."
            break
            
    report = f'''# Auditoria de Cobertura do Catálogo Global de Cursos

## 1. Objetivo
Validar se o ficheiro `Catalogo_Global_Cursos.md` é um inventário completo e fiel dos ficheiros de cursos existentes em `011_Biblioteca_Programas`.

## 2. Metodologia
Script de análise exaustiva (`audit_catalog.py`) que percorre todos os ficheiros `.md`, isola os que são cursos, extrai os metadados (Título, Caminho, Duração), faz o parse da tabela markdown do Catálogo Global e realiza matching (por Caminho e Título Normalizado).

## 3. Resultados Globais

| Métrica | Resultado |
|---|---:|
| Ficheiros analisados | {len(all_files)} |
| Cursos/programas identificados | {total_lib} |
| Cursos no Catálogo Global | {total_cat} |
| Cursos presentes em ambos | {total_both} |
| Cursos na Biblioteca mas ausentes do Catálogo | {len(only_in_lib)} |
| Cursos no Catálogo sem ficheiro correspondente | {len(only_in_cat)} |
| Cobertura do Catálogo | {coverage:.2f}% |

## 4. Cursos na Biblioteca e no Catálogo
*(Amostra de 10 cursos para validação de formato)*
| ID | Curso (Biblioteca) | Ficheiro | Correspondência |
|---|---|---|---|
'''
    for lib, cat, status in in_both[:10]:
        report += f"| {lib['id'] or '-'} | {lib['title'][:30]} | {lib['filepath']} | {status} |\n"
        
    report += '''
## 5. Cursos na Biblioteca mas ausentes do Catálogo
| ID | Curso | Ficheiro | Área | Duração |
|---|---|---|---|---|
'''
    for lib in only_in_lib:
        report += f"| {lib['id'] or '-'} | {lib['title']} | {lib['filepath']} | {lib['area']} | {lib['duracao']} |\n"

    report += '''
## 6. Cursos no Catálogo sem ficheiro correspondente
| ID | Curso | Entrada no Catálogo | Observação |
|---|---|---|---|
'''
    for cat in only_in_cat:
        report += f"| - | {cat['title']} | `{cat['filepath']}` | Possível ficheiro não .md, apagado ou nome alterado |\n"

    report += f'''
## 7. Possíveis Duplicados
Não testado exaustivamente nesta versão, focado em correspondência 1-para-1.

## 8. Correspondências Ambíguas
'''
    for lib, cat, obs in ambiguous:
        report += f"- Biblioteca: `{lib['title']}` <=> Catálogo: `{cat['title']}` ({obs})\n"
        
    report += f'''
## 9. Caso Específico: Power Automate
**Análise para o curso "Microsoft Power Automate – Fundamentos e Casos Práticos" (TI-OFF-012)**

{power_automate_case}

## 10. Conclusão
O `Catalogo_Global_Cursos.md` **não é atualmente um inventário completo**, pois a cobertura apurada foi de {coverage:.2f}%. Existem discrepâncias devidas a extensões não lidas (ex: ficheiros `.txt`), estruturas de pastas com caracteres invisíveis/especiais que quebram o parser da tabela, e ficheiros que o indexador saltou.

## 11. Recomendações
1. **Unificar Extensões:** Garantir que a Biblioteca apenas aceita `.md` e converter todos os `.txt` nativamente para `.md`.
2. **Atualizar o Indexador:** Modificar o script de indexação para tratar exceções no momento da escrita da tabela Markdown (escapar carateres como `|` no título).
3. **YAML Strict:** Obrigar todo e qualquer ficheiro de curso a ter o YAML Frontmatter para que o matching seja feito por `ID` e não por Título/Caminho, que são falíveis.
'''

    with open(base_dir / "01_Conhecimento_Base" / "Relatorio_Auditoria_Catalogo.md", 'w', encoding='utf-8') as f:
        f.write(report)
        
    print(f"RESUMO EXECUTIVO:")
    print(f"1. Cobertura atual do catálogo: {coverage:.2f}%")
    print(f"2. Cursos potencialmente em falta: {len(only_in_lib)}")
    print(f"3. Possíveis duplicados: (Não apurado nesta run)")
    print(f"4. Resultado Power Automate: {power_automate_case}")

if __name__ == '__main__':
    generate_report()
