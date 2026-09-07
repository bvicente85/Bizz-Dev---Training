import os
import re
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRAMS_DIR = os.path.join(BASE_DIR, "011_Biblioteca_Programas")
CASES_FILE = os.path.join(BASE_DIR, "bd_casos_sucesso.md")
COMPETITIVE_FILE = os.path.join(BASE_DIR, "bd_posicionamento_competitivo.md")
OUTPUT_FILE = os.path.join(BASE_DIR, "..", "catalogo-interativo", "src", "data", "db.json")

def parse_cases():
    """Fazer o parsing de bd_casos_sucesso.md e agrupar por área formativa."""
    if not os.path.exists(CASES_FILE):
        print(f"Ficheiro de casos não encontrado: {CASES_FILE}")
        return {}

    with open(CASES_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Dividir por áreas (começam com ## [N]. Área: [Nome])
    area_sections = re.split(r'\n##\s+\d+\.\s+Área:\s*', content)
    cases_by_area = {}

    for section in area_sections[1:]: # Ignorar cabeçalho inicial
        lines = section.split('\n')
        area_name = lines[0].strip()
        
        # Encontrar os casos dentro desta secção (começam com ### Caso: [Nome])
        cases_text = '\n'.join(lines[1:])
        case_blocks = re.split(r'\n###\s+Caso:\s*', cases_text)
        
        cases_list = []
        for block in case_blocks[1:]:
            block_lines = block.split('\n')
            case_title = block_lines[0].strip()
            
            case_details = {
                "titulo": case_title,
                "setor": "",
                "foco": "",
                "contexto": "",
                "solucao": "",
                "metodologia": "",
                "impacto": ""
            }
            
            # Parsing dos campos bullet points
            current_field = None
            field_map = {
                "Setor": "setor",
                "Foco": "foco",
                "Contexto": "contexto",
                "Solução": "solucao",
                "Metodologia": "metodologia",
                "Impacto Obtido": "impacto"
            }
            
            for line in block_lines[1:]:
                line = line.strip()
                if not line:
                    continue
                # Procurar padrões como * **Campo:** Conteúdo
                match = re.match(r'^\*\s+\*\*(.*?)\*\*:\s*(.*)$', line)
                if match:
                    field_name, field_val = match.groups()
                    if field_name in field_map:
                        current_field = field_map[field_name]
                        case_details[current_field] = field_val
                elif line.startswith('*') or line.startswith('-'):
                    # Continuação ou lista simples se não der match completo
                    if current_field:
                        case_details[current_field] += "\n" + line
                else:
                    # Linha sem bullet, adiciona ao campo atual se existir
                    if current_field:
                        case_details[current_field] += " " + line

            cases_list.append(case_details)
        
        # Normalizar nome da área para mapeamento posterior
        cases_by_area[area_name] = cases_list

    return cases_by_area

def parse_competitive():
    """Fazer o parsing de bd_posicionamento_competitivo.md."""
    if not os.path.exists(COMPETITIVE_FILE):
        print(f"Ficheiro competitivo não encontrado: {COMPETITIVE_FILE}")
        return {"usps": [], "concorrencia": [], "objecoes": []}

    with open(COMPETITIVE_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Extrair Diferenciais (USPs)
    usps = []
    usp_section = re.search(r'## 1\. Proposta de Valor Central da SKOLAE(.*?)(?=## 2\.)', content, re.DOTALL)
    if usp_section:
        usp_text = usp_section.group(1).strip()
        # Encontrar os pontos principais (começam com *)
        usp_matches = re.finditer(r'\*\s+\*\*(.*?)\*\*:\s*(.*?)(?=\n\*|\Z)', usp_text, re.DOTALL)
        for m in usp_matches:
            title, desc = m.groups()
            usps.append({
                "titulo": title.strip(),
                "descricao": desc.strip().replace('\n', ' ')
            })

    # Extrair Concorrência
    concorrencia = []
    comp_section = re.search(r'## 2\. SKOLAE vs\. Concorrência Direta(.*?)(?=## 3\.)', content, re.DOTALL)
    if comp_section:
        comp_text = comp_section.group(1).strip()
        blocks = re.split(r'\n###\s+', comp_text)
        for b in blocks[1:]:
            b_lines = b.split('\n')
            comp_name = b_lines[0].strip()
            rest = '\n'.join(b_lines[1:])
            
            abordagem = ""
            contra = ""
            estatistica = ""
            
            ab_match = re.search(r'\*\s+\*\*A abordagem deles:\*\*\s*(.*?)(?=\n\*|\Z)', rest, re.DOTALL)
            if ab_match:
                abordagem = ab_match.group(1).strip().replace('\n', ' ')
                
            contra_match = re.search(r'\*\s+\*\*A nossa contra-argumentação:\*\*\s*\n?\s*>\s*(.*?)(?=\n\*|\Z)', rest, re.DOTALL)
            if contra_match:
                contra = contra_match.group(1).strip().replace('\n >', ' ').replace('\n', ' ')
                
            est_match = re.search(r'\*\s+\*\*Estatística de Apoio:\*\*\s*(.*?)(?=\n\*|\Z)', rest, re.DOTALL)
            if est_match:
                estatistica = est_match.group(1).strip().replace('\n', ' ')
                
            concorrencia.append({
                "concorrente": comp_name,
                "abordagem": abordagem,
                "contra_argumento": contra,
                "estatistica": estatistica
            })

    # Extrair Matriz de Contra-Argumentos (Tabela)
    objecoes = []
    table_match = re.search(r'\|\s*Se o cliente disser\.\.\.\s*\|\s*A nossa resposta estratégica\.\.\.\s*\|.*?\n(.*)', content, re.DOTALL)
    if table_match:
        table_lines = table_match.group(1).strip().split('\n')
        for line in table_lines:
            if '|' in line and not re.match(r'^\s*\|?\s*:?-+:?\s*\|', line):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 2 and parts[0] and parts[1]:
                    # Remover aspas extras de formatação markdown
                    obj = parts[0].strip('*').strip('"').strip('`').strip('*').strip('"')
                    resp = parts[1].strip('*').strip('"').strip('`').strip('*').strip('"')
                    objecoes.append({
                        "se_cliente_disser": obj,
                        "resposta": resp
                    })

    return {
        "usps": usps,
        "concorrencia": concorrencia,
        "objecoes": objecoes
    }

def clean_markdown(text):
    """Limpa marcações básicas de markdown ou formata de forma limpa."""
    return text.strip()

def parse_course_file(filepath):
    """Fazer o parsing de um ficheiro de curso (.md ou .txt)."""
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1].lower()
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    course_data = {
        "titulo": "",
        "area": "",
        "duracao": "",
        "metodologia": "",
        "descricao": "",
        "objetivos": [],
        "programa": [],
        "notas_venda": "",
        "origem_ficheiro": filename,
        "is_signature": True
    }

    # Determinar a área pelo nome da diretoria mãe
    parent_dir = os.path.basename(os.path.dirname(filepath))
    # Ex: "01_Vendas_e_Negociacao" -> "Vendas e Negociação"
    area_clean = re.sub(r'^\d+_', '', parent_dir).replace('_', ' ')
    # Corrigir alguns nomes comuns
    area_clean = area_clean.replace("Tecnologias Informacao", "Tecnologias de Informação")
    area_clean = area_clean.replace("Recursos Humanos", "Recursos Humanos")
    area_clean = area_clean.replace("Area Financeira", "Área Financeira")
    area_clean = area_clean.replace("Area Juridica", "Área Jurídica")
    area_clean = area_clean.replace("Formacao de Formadores", "Formação de Formadores")
    area_clean = area_clean.replace("Lideranca e Gestao Equipas", "Liderança e Gestão de Equipas")
    area_clean = area_clean.replace("Eficacia Personal e Soft Skills", "Eficácia Pessoal e Soft Skills")
    area_clean = area_clean.replace("Atendimento e Relacao Cliente", "Atendimento e Relação com o Cliente")
    area_clean = area_clean.replace("Linguas Estrangeiras", "Línguas Estrangeiras")
    area_clean = area_clean.replace("Sustentabilidade ESG", "Sustentabilidade e ESG")
    area_clean = area_clean.replace("Gestao Projetos e Inovacao", "Gestão de Projetos e Inovação")
    area_clean = area_clean.replace("Team Buildings", "Team Buildings")
    
    course_data["area"] = area_clean

    if ext == ".md":
        # Título
        title_match = re.search(r'^#\s+Curso:\s*(.*)$', content, re.MULTILINE)
        if not title_match:
            title_match = re.search(r'^#\s*(.*)$', content, re.MULTILINE)
        
        if title_match:
            course_data["titulo"] = title_match.group(1).strip()
        else:
            course_data["titulo"] = filename.replace("Curso_", "").replace(".md", "").replace("_", " ")

        # Cabeçalho: Área | Duração | Metodologia
        header_match = re.search(r'\*\*Área:\*\*\s*(.*?)\s*\|\s*\*\*Duração:\*\*\s*(.*?)\s*\|\s*\*\*Metodologia:\*\*\s*(.*?)$', content, re.MULTILINE)
        if header_match:
            _, dur, met = header_match.groups()
            course_data["duracao"] = dur.strip()
            course_data["metodologia"] = met.strip()
        else:
            # Tentar regexes mais flexíveis
            dur_match = re.search(r'\*\*Duração:\*\*\s*([^|]*)', content)
            if dur_match:
                course_data["duracao"] = dur_match.group(1).strip()
            met_match = re.search(r'\*\*Metodologia:\*\*\s*([^|\n]*)', content)
            if met_match:
                course_data["metodologia"] = met_match.group(1).strip()

        # Secções principais
        # 1. Descrição e Objetivos
        desc_section = re.search(r'##\s+Descrição\s+e\s+Objetivos(.*?)(?=##\s+Programa\s+Detalhado|##\s+Perfil\s+do\s+Formador|##\s+Notas\s+de\s+Venda|\Z)', content, re.DOTALL | re.IGNORECASE)
        if desc_section:
            desc_text = desc_section.group(1).strip()
            # Separar parágrafos de bullets (objetivos)
            paragraphs = []
            objectives = []
            for line in desc_text.split('\n'):
                line = line.strip()
                if line.startswith('*') or line.startswith('-'):
                    objectives.append(line.strip('*').strip('-').strip())
                elif line:
                    paragraphs.append(line)
            course_data["descricao"] = " ".join(paragraphs)
            course_data["objetivos"] = objectives
        else:
            # Caso não haja secção explícita, usar parágrafos iniciais
            body_without_title = re.sub(r'^#.*?\n', '', content)
            body_without_header = re.sub(r'^\*\*Área:\*\*.*?\n', '', body_without_title)
            course_data["descricao"] = body_without_header[:300].strip() + "..."

        # 2. Programa Detalhado
        prog_section = re.search(r'##\s+Programa\s+Detalhado(.*?)(?=##\s+Perfil\s+do\s+Formador|##\s+Notas\s+de\s+Venda|\Z)', content, re.DOTALL | re.IGNORECASE)
        if prog_section:
            prog_text = prog_section.group(1).strip()
            # Lendo módulos (ex: ### 1. Nome ou Módulos)
            modules = []
            current_module = None
            
            for line in prog_text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                # Novo Módulo (### Título ou **Título**)
                mod_match = re.match(r'^(?:###|\*\*)\s*(?:\d+\.|\-\s*)?\s*(.*?)(?:\*\*|\Z)$', line)
                if mod_match and (line.startswith('###') or line.startswith('**')):
                    if current_module:
                        modules.append(current_module)
                    current_module = {
                        "nome": mod_match.group(1).strip(),
                        "subtemas": []
                    }
                elif line.startswith('*') or line.startswith('-'):
                    # Subtema do módulo atual
                    subtema = line.strip('*').strip('-').strip()
                    if current_module:
                        current_module["subtemas"].append(subtema)
                    else:
                        # Se ainda não houver módulo, criar um genérico
                        current_module = {
                            "nome": "Conteúdos Gerais",
                            "subtemas": [subtema]
                        }
                else:
                    if current_module:
                        current_module["subtemas"].append(line)
            
            if current_module:
                modules.append(current_module)
            course_data["programa"] = modules

        # 3. Notas de Venda / Perfil do Formador
        notes_section = re.search(r'##\s+(?:Perfil\s+do\s+Formador\s*/\s*Notas\s+de\s+Venda|Notas\s+de\s+Venda|Perfil\s+do\s+Formador)(.*)$', content, re.DOTALL | re.IGNORECASE)
        if notes_section:
            course_data["notas_venda"] = notes_section.group(1).strip()

    elif ext == ".txt":
        # Formato de texto simples
        lines = content.split('\n')
        course_data["titulo"] = lines[0].replace("Curso:", "").strip() if lines[0].startswith("Curso:") else filename.replace(".txt", "")
        
        # Procurar carga horária
        for line in lines[1:4]:
            if "carga horária" in line.lower() or "duração" in line.lower():
                course_data["duracao"] = re.sub(r'^(?:Carga horária|Duração):\s*', '', line, flags=re.IGNORECASE).strip()
                break
        
        course_data["metodologia"] = "Presencial / Live Training"
        course_data["descricao"] = "Programa de formação focado no desenvolvimento de competências práticas para a área de " + course_data["area"] + "."
        
        # Procurar Módulos
        modules = []
        current_module = None
        in_modules = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if "módulos" in line.lower() or "programa" in line.lower() or "conteúdo" in line.lower():
                in_modules = True
                continue
            
            if in_modules:
                # Verificar se é um módulo numerado
                mod_match = re.match(r'^(\d+)\.\s*(.*)$', line)
                if mod_match:
                    if current_module:
                        modules.append(current_module)
                    current_module = {
                        "nome": mod_match.group(2).strip(),
                        "subtemas": []
                    }
                elif line.startswith('*') or line.startswith('-'):
                    sub = line.strip('*').strip('-').strip()
                    if current_module:
                        current_module["subtemas"].append(sub)
                    else:
                        current_module = {"nome": "Módulo Único", "subtemas": [sub]}
                else:
                    if current_module:
                        current_module["subtemas"].append(line)
                    else:
                        current_module = {"nome": "Módulo Único", "subtemas": [line]}
                        
        if current_module:
            modules.append(current_module)
        
        course_data["programa"] = modules
        course_data["is_signature"] = False # Cursos TXT tendem a ser mais simples / auxiliares

    return course_data

def build_database():
    """Varrer pastas e montar o JSON final."""
    print("A iniciar compilação da base de dados SKOLAE...")
    
    # 1. Parse de Casos de Sucesso e Competitivo
    cases = parse_cases()
    competitive = parse_competitive()
    
    # 2. Varrer programas de formação
    courses = []
    
    if os.path.exists(PROGRAMS_DIR):
        for root, dirs, files in os.walk(PROGRAMS_DIR):
            for file in files:
                if file.endswith((".md", ".txt")) and not file.startswith("index"):
                    filepath = os.path.join(root, file)
                    try:
                        course_info = parse_course_file(filepath)
                        courses.append(course_info)
                    except Exception as e:
                        print(f"Erro ao processar ficheiro {file}: {e}")
    else:
        print(f"Diretoria de programas não encontrada: {PROGRAMS_DIR}")

    # Montar JSON final
    db = {
        "metadados": {
            "total_cursos": len(courses),
            "total_areas": len(set(c["area"] for c in courses)),
            "versao": "1.0",
            "autor": "Antigravity SKOLAE Intelligence"
        },
        "cursos": courses,
        "casos_sucesso": cases,
        "posicionamento": competitive
    }
    
    # Garantir que a diretoria de output existe
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # Gravar JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        
    print(f"Base de dados gravada com sucesso em: {OUTPUT_FILE}")
    print(f"Total de cursos importados: {len(courses)}")

if __name__ == "__main__":
    build_database()
