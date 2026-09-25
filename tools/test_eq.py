import unicodedata
import re
import os

def normalize_text(text):
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

cat_p = '01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/Curso_Percurso_-_Rising_leaders_-_modulos_transversais_e_de_negocio.md'

lib_p = ''
for root, dirs, files in os.walk(r'C:\Users\brunn\OneDrive - GIE IFE\Desktop\Bruno\PESSOAL\Business Development Formação\01_Conhecimento_Base\011_Biblioteca_Programas\15_Gestao_Projetos_e_Inovacao'):
    for f in files:
        if 'Rising_leaders_-_modulos' in f:
            lib_p = '01_Conhecimento_Base/011_Biblioteca_Programas/15_Gestao_Projetos_e_Inovacao/' + f

cat_norm = normalize_path(cat_p)
lib_norm = normalize_path(lib_p)

print('CAT_NORM:', repr(cat_norm))
print('LIB_NORM:', repr(lib_norm))
print('EQ?', cat_norm == lib_norm)
