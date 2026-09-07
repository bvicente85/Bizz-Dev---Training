import os
import re
import json
import argparse
from pathlib import Path

def extract_metadata(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    
    metadata = {
        'filepath': str(filepath),
        'filename': filepath.name,
        'title': None,
        'duracao': None,
        'modalidade': None,
        'destinatarios': None,
        'tags': [],
        'areas': [], 
        'programa_resumo': None
    }

    # Extract Area from folder path
    parts = filepath.parts
    if '011_Biblioteca_Programas' in parts:
        idx = parts.index('011_Biblioteca_Programas')
        if idx + 1 < len(parts) - 1: # There is a subfolder
            metadata['areas'].append(parts[idx + 1])

    # 1. Extract Title (first H1)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        metadata['title'] = title_match.group(1).strip()
    else:
        # Fallback to filename
        metadata['title'] = filepath.stem.replace('Curso_', '').replace('_', ' ')

    # 2. Extract Duração
    duracao_match = re.search(r'(?i)\*\*Duração:?\*\*\s*(.+)', content)
    if not duracao_match:
        duracao_match = re.search(r'(?i)Duração:?\s*(.+)', content)
    if duracao_match:
        metadata['duracao'] = duracao_match.group(1).strip()

    # 3. Extract Modalidade
    mod_match = re.search(r'(?i)\*\*Modalidade:?\*\*\s*(.+)', content)
    if mod_match:
        metadata['modalidade'] = mod_match.group(1).strip()

    # 4. Extract Destinatários
    dest_match = re.search(r'(?i)##\s*(?:🎯\s*)?(A Quem se Dirige|Destinatários|Público-Alvo|Público)(.*?)(?=##|\Z)', content, re.DOTALL)
    if dest_match:
        text = dest_match.group(2).strip()
        if text and not text.lower() == 'indisponível':
            # Clean up newlines and extra spaces
            text = re.sub(r'\s+', ' ', text)
            metadata['destinatarios'] = text[:150] + ('...' if len(text) > 150 else '')

    # 5. Extract Tags
    tags_match = re.search(r'(?i)\*\*Tags:?\*\*\s*(.+)', content)
    if tags_match:
        tags_raw = tags_match.group(1)
        tags = [t.strip().strip('#') for t in tags_raw.split() if t.strip()]
        metadata['tags'] = tags

    return metadata


def analyze(base_path):
    target_dir = Path(base_path) / "01_Conhecimento_Base" / "011_Biblioteca_Programas"
    
    if not target_dir.exists():
        print(f"Error: Directory not found -> {target_dir}")
        return []

    all_courses = []
    
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if (file.endswith('.md') or file.endswith('.txt')) and not file.startswith('_Índice'):
                filepath = Path(root) / file
                meta = extract_metadata(filepath)
                all_courses.append(meta)

    return all_courses

def generate_reports(courses, base_path):
    out_dir = Path(base_path) / "01_Conhecimento_Base"
    
    total = len(courses)
    with_title = sum(1 for c in courses if c.get('title') and not c['title'].startswith('Curso'))
    with_duracao = sum(1 for c in courses if c.get('duracao') and c['duracao'].lower() not in ['não especificada', 'indisponível'])
    with_mod = sum(1 for c in courses if c.get('modalidade'))
    with_dest = sum(1 for c in courses if c.get('destinatarios'))
    with_tags = sum(1 for c in courses if len(c.get('tags', [])) > 0)

    # 1. Relatório de Qualidade
    relatorio = f"""# Relatório de Diagnóstico de Qualidade de Metadados (Cursos)

## 📊 Estatísticas Gerais
- **Total de ficheiros analisados:** {total}
- **Com Título explícito:** {with_title}/{total}
- **Com Duração preenchida:** {with_duracao}/{total}
- **Com Modalidade preenchida:** {with_mod}/{total}
- **Com Destinatários identificados:** {with_dest}/{total}
- **Com Tags/Competências mapeadas:** {with_tags}/{total}

## ⚠️ Principais Problemas Encontrados
- **Campo mais em falta:** Modalidade e Tags Estruturadas. A maioria dos cursos não tem este campo explicitado no texto de forma normalizada.
- **Duração inconsistente:** Muitos ficheiros têm texto livre ou "Não especificada".
- **Falta de standardização em Destinatários:** O campo varia entre "A quem se dirige", "Público", ou está diluído nos objetivos.
- **Estrutura não parseável:** Muitos cursos antigos usam listas não estruturadas sem headers claros. Alguns ainda estão em formato `.txt`.
"""
    with open(out_dir / "Relatorio_Qualidade_Metadata_Cursos.md", 'w', encoding='utf-8') as f:
        f.write(relatorio)

    # 2. Catálogo Global
    catalogo = """# Catálogo Global de Cursos SKOLAE
> **Nota para Agentes IA:** Utilize este catálogo para descobrir cursos relevantes com base nas necessidades do cliente.

| Área | Título do Curso | Duração | Destinatários | Tags | Caminho do Ficheiro |
|---|---|---|---|---|---|
"""
    courses_sorted = sorted(courses, key=lambda x: (x['areas'][0] if x['areas'] else 'Z', x['title'] or ''))
    
    for c in courses_sorted:
        area = c['areas'][0].split('_', 1)[-1].replace('_', ' ') if c['areas'] else 'Sem Área'
        title = c['title'] or c['filename']
        duracao = c['duracao'] or '-'
        dest = c['destinatarios'] or '-'
        tags = ", ".join(c['tags']) if c['tags'] else '-'
        
        try:
            rel_path = Path(c['filepath']).relative_to(out_dir).as_posix()
        except ValueError:
            rel_path = c['filepath']
            
        catalogo += f"| {area} | **{title}** | {duracao} | {dest} | {tags} | `{rel_path}` |\n"
        
    with open(out_dir / "Catalogo_Global_Cursos.md", 'w', encoding='utf-8') as f:
        f.write(catalogo)

    # Dump JSON
    with open(out_dir / "catalogo_raw_data.json", 'w', encoding='utf-8') as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)

    # 3. Índice por Competências
    indice = """# Índice por Competências e Áreas Observadas
> *Gerado automaticamente.*

"""
    grouped = {}
    for c in courses:
        area = c['areas'][0] if c['areas'] else 'Outros'
        area_clean = area.split('_', 1)[-1].replace('_', ' ').upper()
        if area_clean not in grouped:
            grouped[area_clean] = []
        grouped[area_clean].append(c)

    for area, curlist in sorted(grouped.items()):
        indice += f"## {area}\\n"
        for cur in sorted(curlist, key=lambda x: x['title'] or ''):
            title = cur['title'] or cur['filename']
            tags_str = f" [Tags: {', '.join(cur['tags'])}]" if cur['tags'] else ""
            indice += f"- {title}{tags_str}\\n"
        indice += "\\n"

    with open(out_dir / "Indice_por_Competencias.md", 'w', encoding='utf-8') as f:
        f.write(indice)

    # 4. Taxonomia Atual vs Proposta
    taxonomia = """# Taxonomia de Cursos (Diagnóstico e Proposta)

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
"""
    with open(out_dir / "Taxonomia_Cursos.md", 'w', encoding='utf-8') as f:
        f.write(taxonomia)

    print(f"Analysis complete. Processed {total} courses.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['analyze', 'apply'], required=True)
    parser.add_argument('--path', required=True)
    args = parser.parse_args()

    if args.mode == 'analyze':
        courses = analyze(args.path)
        generate_reports(courses, args.path)
    elif args.mode == 'apply':
        print("APPLY mode is not enabled yet.")
