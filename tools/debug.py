import unicodedata
import re
import os
from pathlib import Path

def normalize_text(text):
    if not text: return ''
    text = unicodedata.normalize('NFKC', text).lower()
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

base_dir = Path(r"C:\Users\brunn\OneDrive - GIE IFE\Desktop\Bruno\PESSOAL\Business Development Formação")
cat_path = base_dir / "01_Conhecimento_Base" / "Catalogo_Global_Cursos.md"

with open(cat_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    if 'Rising_leaders' in line:
        parts = [p.strip() for p in line.split('|')]
        print(f"Parts length: {len(parts)}")
        print(f"Index -2: {repr(parts[-2])}")
        cat_p = parts[-2].replace('`', '')
        print(f"cat_p: {repr(cat_p)}")
        print(f"cat_norm: {repr(normalize_path(cat_p))}")

target = "01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Percurso_-_Rising_leaders_-_modulos_transversais_e_de_negocio.md"
print(f"target_norm: {repr(normalize_path(target))}")
