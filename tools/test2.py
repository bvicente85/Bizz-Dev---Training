import os
import re
import unicodedata
from pathlib import Path
from difflib import SequenceMatcher

def normalize_text(text):
    if not text: return ""
    text = unicodedata.normalize('NFKC', text)
    text = text.lower()
    text = re.sub(r'[\u2010-\u2015\u2212]', '-', text)
    text = re.sub(r'[\u2018\u2019\u201A\u201B\u2039\u203A\u0027]', "'", text)
    text = re.sub(r'[\u201C\u201D\u201E\u201F\u0022\u00AB\u00BB]', '"', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_path(path_str):
    path_str = path_str.replace('\\\\', '/').replace('\\', '/')
    normalized = unicodedata.normalize('NFD', path_str)
    normalized = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    return normalize_text(normalized)

def similar(a, b):
    if not a or not b: return 0
    return SequenceMatcher(None, a, b).ratio()

base_dir = Path(r"C:\Users\brunn\OneDrive - GIE IFE\Desktop\Bruno\PESSOAL\Business Development Formação")
bib_dir = base_dir / "01_Conhecimento_Base" / "011_Biblioteca_Programas"
cat_path = base_dir / "01_Conhecimento_Base" / "Catalogo_Global_Cursos.md"

all_files = []
for root, dirs, files in os.walk(bib_dir):
    for f in files:
        if f.endswith('.md'):
            if not f.startswith('_') and not f.lower().startswith('index'):
                all_files.append(Path(root) / f)

lib_courses = []
for f in all_files:
    meta = {'filepath': f.relative_to(base_dir).as_posix(), 'filename': f.name}
    lib_courses.append(meta)

cat_courses = []
with open(cat_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip().startswith('|---'):
            continue
        if '|' in line and not 'Nota para Agentes' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) > 6:
                path_str = parts[-2].replace('`', '')
                cat_courses.append({'filepath_norm': normalize_path(path_str)})

matched_count = 0
only_in_lib = []

for lib in lib_courses:
    matched = False
    lib_path_norm = normalize_path(lib['filepath'])
    
    for cat in cat_courses:
        if lib_path_norm in cat['filepath_norm'] and len(lib_path_norm) > 10:
            matched = True
            break
            
    if matched:
        matched_count += 1
    else:
        only_in_lib.append(lib)

print(f"Total Lib: {len(lib_courses)}")
print(f"Total Cat: {len(cat_courses)}")
print(f"Matched: {matched_count}")
print(f"Missing: {len(only_in_lib)}")
for m in only_in_lib:
    print(m['filename'])

