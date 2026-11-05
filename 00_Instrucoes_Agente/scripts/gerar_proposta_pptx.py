#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Motor de Geração de Propostas em PowerPoint (SKOLAE Formação)
Adapta o 'Template Proposta - 1 curso.pptx' preservando a identidade visual,
cores institucionais, fontes tipográficas oficiais e estrutura de grupos.
"""

import os
import sys
import json
import argparse
import pptx
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Cores Oficiais da SKOLAE
ORANGE_MAIN = RGBColor(0xFF, 0x9B, 0x23)    # #FF9B23 (Títulos e destaques principais)
ORANGE_ACCENT = RGBColor(0xFF, 0x91, 0x2B)  # #FF912B (Títulos de módulos e destaques em texto)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

# Tipografia Oficial da SKOLAE
F_TITLE_COND = 'GT Walsheim Pro Condensed Black'
F_TITLE_BOLD = 'GT Walsheim Pro Bold'
F_TITLE_SBD = 'GT Walsheim Pro Bold SBd'
F_TITLE_REG = 'GT Walsheim Pro'
F_BODY = 'Basier Circle'
F_BODY_BOLD = 'Basier BOLD'
F_BODY_SQ = 'Basier Circle'

def set_run(run, text, font_name, size_pt, bold=False, color_rgb=None):
    run.text = text
    run.font.name = font_name
    if size_pt is not None:
        run.font.size = Pt(size_pt)
    run.font.bold = bold
    if color_rgb:
        run.font.color.rgb = color_rgb

def gerar_proposta(data, template_path=r'Template Proposta - 1 curso.pptx', output_path=None):
    """
    Gera a proposta em PowerPoint baseada no dicionário de dados 'data'.
    """
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template base não encontrado em: {template_path}")
    
    prs = pptx.Presentation(template_path)
    
    # Extração de campos com valores por omissão seguros
    cliente = data.get('cliente', 'CLIENTE')
    cliente_completo = data.get('cliente_completo', cliente)
    area = data.get('area', 'FORMAÇÃO EXECUTIVA').upper()
    titulo_curso = data.get('titulo_curso', 'PROGRAMA DE FORMAÇÃO').upper()
    subtitulo = data.get('subtitulo', 'Desenvolver competências críticas para a excelência organizacional')
    duracao = data.get('duracao', '14 horas')
    duracao_detalhe = data.get('duracao_detalhe', 'As sessões poderão decorrer em 2 dias seguidos ou interpolados ou em 4 meios-dias')
    destinatarios = data.get('destinatarios', f'Colaboradores e quadros da {cliente}')
    formandos_num = str(data.get('formandos_num', '12'))
    modalidade = data.get('modalidade', 'Presencial ou Live training')
    
    # Enquadramento e Porquê (Slide 6)
    enquadramento_p1 = data.get('enquadramento_p1', f'Os responsáveis da {cliente} tomaram a decisão de investir no desenvolvimento de competências das suas equipas.')
    enquadramento_p2 = data.get('enquadramento_p2', 'Desde sempre a SKOLAE Formação dispõe no seu portefólio de soluções de aprendizagem específicas orientadas ao desenvolvimento de competências críticas e impacto no negócio.')
    enquadramento_p3 = data.get('enquadramento_p3', 'Uma sólida aposta na capacitação contínua nas organizações tem impacto direto no clima organizacional, na produtividade e na entrega de valor.')
    enquadramento_p4 = data.get('enquadramento_p4', 'Contextualizamos que abordar este tema é integrar abordagens práticas, ferramentas aplicadas e metodologias ativas orientadas a resultados mensuráveis.')
    subtitulo_enquadramento = data.get('subtitulo_enquadramento', 'Capacitação Estratégica e Excelência Operacional')
    proposito = data.get('proposito', f'Dotar os participantes de ferramentas e competências práticas com aplicação direta no contexto profissional da {cliente}.')
    
    # Metodologias e Competências (Slide 12)
    competencias = data.get('competencias', [
        'Planeamento e Estratégia',
        'Comunicação e Eficácia Operacional',
        'Inovação e Resolução de Problemas',
        'Métricas e Avaliação de Resultados'
    ])
    metodologia_p1 = data.get('metodologia_p1', 'Formação prática e participativa baseada em metodologias ativas de Action Learning, estudos de caso reais e exercícios aplicados ao contexto da organização.')
    metodologia_p2 = data.get('metodologia_p2', f'Será fomentada a aplicação direta ao contexto real da {cliente} através de dinâmicas práticas, reflexão e definição de planos de ação individuais.')
    metodologia_foco = data.get('metodologia_foco', 'Construção orientada à consolidação de competências e medição de impacto.')
    metodologia_cenarizacao = data.get('metodologia_cenarizacao', 'Simulação de cenários reais; análise crítica de desafios; exercícios aplicados e ferramentas práticas')
    metodologia_casos = data.get('metodologia_casos', f'Utilização de casos reais do setor da {cliente}, benchmarking de boas práticas e análise de ferramentas')

    # Conteúdos Programáticos (Slide 13)
    objetivos_especificos = data.get('objetivos_especificos', [])
    modulos = data.get('modulos', []) # Lista de dicts: [{'titulo': '...', 'topicos': [...]}]

    # ==============================================================================
    # SLIDE 1 (Capa 1)
    # ==============================================================================
    s1 = prs.slides[0]
    for sh in s1.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                if 'DESENVOLVIMENTO PESSOAL' in p.text:
                    p.text = ''
                    set_run(p.add_run(), area, F_BODY, 14, bold=False, color_rgb=ORANGE_MAIN)
                elif 'COMUNICAÇÃO INTERPESSOAL 360º' in p.text:
                    p.text = ''
                    set_run(p.add_run(), titulo_curso, F_TITLE_COND, 48, bold=True, color_rgb=WHITE)
                elif 'Desenvolva as suas competências de comunicação' in p.text:
                    p.text = ''
                    set_run(p.add_run(), subtitulo, F_BODY_BOLD, 16, bold=True, color_rgb=ORANGE_MAIN)

    # ==============================================================================
    # SLIDE 3 (Capa com Logo do Cliente)
    # ==============================================================================
    s3 = prs.slides[2]
    for sh in s3.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                if 'DESENVOLVIMENTO PESSOAL' in p.text:
                    p.text = ''
                    set_run(p.add_run(), area, F_BODY, 14, bold=False, color_rgb=ORANGE_MAIN)
                elif 'COMUNICAÇÃO INTERPESSOAL 360º' in p.text:
                    p.text = ''
                    set_run(p.add_run(), titulo_curso, F_TITLE_COND, 48, bold=True, color_rgb=WHITE)
                elif 'Desenvolva as suas competências de comunicação' in p.text:
                    p.text = ''
                    set_run(p.add_run(), subtitulo, F_BODY_BOLD, 16, bold=True, color_rgb=ORANGE_MAIN)
                elif 'Logo do cliente' in p.text:
                    p.text = ''
                    p.alignment = PP_ALIGN.CENTER
                    set_run(p.add_run(), cliente_completo, F_BODY, 13, bold=True, color_rgb=ORANGE_MAIN)

    # ==============================================================================
    # SLIDE 4 & 5 (Capas Alternativas)
    # ==============================================================================
    for s_idx in [3, 4]:
        s = prs.slides[s_idx]
        for sh in s.shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    if 'DESENVOLVIMENTO PESSOAL' in p.text:
                        p.text = ''
                        set_run(p.add_run(), area, F_BODY, 14, bold=False, color_rgb=ORANGE_MAIN)
                    elif 'COMUNICAÇÃO INTERPESSOAL 360º' in p.text:
                        p.text = ''
                        set_run(p.add_run(), titulo_curso, F_TITLE_COND, 48, bold=True, color_rgb=WHITE)
                    elif 'Desenvolva as suas competências de comunicação' in p.text:
                        p.text = ''
                        set_run(p.add_run(), subtitulo, F_BODY_BOLD, 16, bold=True, color_rgb=ORANGE_MAIN)

    # ==============================================================================
    # SLIDE 6 (Contexto & Enquadramento)
    # ==============================================================================
    s6 = prs.slides[5]
    for sh in s6.shapes:
        if sh.has_text_frame:
            tf = sh.text_frame
            if 'Os responsáveis da X' in tf.text or 'Os responsáveis da' in tf.text:
                for p in tf.paragraphs:
                    if 'Os responsáveis da' in p.text:
                        p.text = ''
                        set_run(p.add_run(), 'Os responsáveis da ', F_BODY_SQ, 12, bold=False)
                        set_run(p.add_run(), cliente, F_BODY_SQ, 12, bold=True, color_rgb=ORANGE_ACCENT)
                        resto = enquadramento_p1.replace('Os responsáveis da ' + cliente, '').replace('Os responsáveis da ' + cliente_completo, '').strip()
                        if not resto.startswith('tomaram'):
                            resto = 'tomaram a decisão de ' + resto
                        set_run(p.add_run(), f' {resto}', F_BODY_SQ, 12, bold=False)
                    elif 'Desde sempre a SKOLAE Formação' in p.text:
                        p.text = ''
                        set_run(p.add_run(), enquadramento_p2, F_BODY_SQ, 12, bold=False)
                    elif 'Uma boa comunicação interpessoal' in p.text or 'Uma sólida estratégia' in p.text:
                        p.text = ''
                        set_run(p.add_run(), enquadramento_p3, F_BODY_SQ, 12, bold=False)
                    elif 'Contextualizamos que abordar' in p.text:
                        p.text = ''
                        set_run(p.add_run(), enquadramento_p4, F_BODY_SQ, 12, bold=False)
            
            elif sh.name == 'CaixaDeTexto 5':
                p = tf.paragraphs[0]
                p.text = ''
                set_run(p.add_run(), subtitulo_enquadramento, F_BODY, 26, bold=False)

            elif sh.name == 'CaixaDeTexto 11':
                p = tf.paragraphs[0]
                p.text = ''
                p.alignment = PP_ALIGN.RIGHT
                set_run(p.add_run(), f'Sugerimos que cada turma não ultrapasse os {formandos_num} participantes, de forma a garantir a realização de simulações, gravação e feedback individualizado.', F_BODY, 12, bold=False)

            elif sh.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.GROUP and sh.name == 'Agrupar 17':
                for c in sh.shapes:
                    if c.name == 'CaixaDeTexto 22' and c.has_text_frame:
                        p = c.text_frame.paragraphs[0]
                        p.text = ''
                        set_run(p.add_run(), 'PROPÓSITO', 'Arial Nova', 14, bold=True)
                    elif c.name == 'CaixaDeTexto 13' and c.has_text_frame:
                        c.text_frame.clear()
                        p = c.text_frame.paragraphs[0]
                        set_run(p.add_run(), proposito, F_BODY, 13.5, bold=True)

            elif sh.name == 'Retângulo: Canto Arredondado 15':
                p = tf.paragraphs[0]
                p.text = ''
                p.alignment = PP_ALIGN.CENTER
                set_run(p.add_run(), destinatarios, F_TITLE_REG, 14, bold=True, color_rgb=ORANGE_MAIN)

            elif sh.name == 'Retângulo: Canto Arredondado 16':
                p0 = tf.paragraphs[0]
                p0.text = ''
                p0.alignment = PP_ALIGN.CENTER
                set_run(p0.add_run(), formandos_num, F_TITLE_REG, 32, bold=True, color_rgb=ORANGE_MAIN)
                p1 = tf.paragraphs[1]
                p1.text = ''
                p1.alignment = PP_ALIGN.CENTER
                set_run(p1.add_run(), 'formandos', F_TITLE_REG, 16, bold=True, color_rgb=ORANGE_MAIN)

    # ==============================================================================
    # SLIDE 12 (Abertura Itinerário Pedagógico)
    # ==============================================================================
    s12 = prs.slides[11]
    for sh in s12.shapes:
        if sh.name == 'CaixaDeTexto 30':
            p = sh.text_frame.paragraphs[0]
            p.text = ''
            set_run(p.add_run(), titulo_curso, F_TITLE_BOLD, 28, bold=True, color_rgb=ORANGE_MAIN)
        elif sh.name == 'CaixaDeTexto 81':
            p = sh.text_frame.paragraphs[0]
            p.text = ''
            set_run(p.add_run(), subtitulo, F_BODY, 14, bold=False)
        # Nota: CaixaDeTexto 83, 84 e 85 (bloco "ESTIMULAR A APRENDIZAGEM / TREINO")
        # são estritamente standard da SKOLAE e não devem ser modificadas.
        elif sh.name == 'CaixaDeTexto 3':
            tf = sh.text_frame
            p1 = tf.paragraphs[1]
            p1.text = ''
            set_run(p1.add_run(), duracao, F_BODY, 11, bold=False)
            p2 = tf.paragraphs[2]
            p2.text = ''
            set_run(p2.add_run(), duracao_detalhe, F_BODY, 11, bold=False, color_rgb=ORANGE_ACCENT)

    # Grupos Dedicados no Slide 12
    for sh in s12.shapes:
        if sh.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.GROUP:
            for child in sh.shapes:
                if child.has_text_frame:
                    if child.name == 'CaixaDeTexto 28': # Destinatários
                        tf = child.text_frame
                        tf.clear()
                        p0 = tf.paragraphs[0]
                        set_run(p0.add_run(), 'Destinatários', F_BODY, 14, bold=True)
                        p1 = tf.add_paragraph()
                        set_run(p1.add_run(), destinatarios, F_BODY, 11, bold=False)

                    elif child.name == 'CaixaDeTexto 27': # Competências
                        tf = child.text_frame
                        tf.clear()
                        p0 = tf.paragraphs[0]
                        set_run(p0.add_run(), 'Competências ', F_BODY, 14, bold=True)
                        p1 = tf.add_paragraph()
                        set_run(p1.add_run(), 'a desenvolver', F_BODY, 14, bold=True)
                        for comp in competencias:
                            p = tf.add_paragraph()
                            set_run(p.add_run(), comp, F_BODY, 11, bold=False)

                    elif child.name == 'CaixaDeTexto 26': # Metodologias
                        tf = child.text_frame
                        tf.clear()
                        p0 = tf.paragraphs[0]
                        set_run(p0.add_run(), 'Metodologias', F_BODY, 14, bold=True)
                        p1 = tf.add_paragraph()
                        set_run(p1.add_run(), metodologia_p1, F_BODY, 11, bold=False)
                        p2 = tf.add_paragraph()
                        set_run(p2.add_run(), metodologia_p2, F_BODY, 11, bold=False)
                        p_sp = tf.add_paragraph()
                        p_sp.text = ''
                        p_sp.font.size = Pt(3)
                        p3 = tf.add_paragraph()
                        set_run(p3.add_run(), 'FOCO PRÁTICO: ', F_BODY, 11, bold=True, color_rgb=ORANGE_ACCENT)
                        set_run(p3.add_run(), metodologia_foco, F_BODY, 11, bold=False)

    # ==============================================================================
    # SLIDE 13 (Itinerário e Conteúdos Programáticos)
    # ==============================================================================
    s13 = prs.slides[12]
    for sh in s13.shapes:
        if sh.has_text_frame:
            tf = sh.text_frame
            if sh.name == 'CaixaDeTexto 7':
                p = tf.paragraphs[0]
                p.text = ''
                set_run(p.add_run(), titulo_curso, F_TITLE_BOLD, 28, bold=True, color_rgb=ORANGE_MAIN)
            
            elif sh.name == 'CaixaDeTexto 9':
                p = tf.paragraphs[0]
                p.text = ''
                set_run(p.add_run(), subtitulo, F_BODY, 14, bold=False)

            elif sh.name == 'CaixaDeTexto 11': # Objetivos Específicos (Sem bullets)
                tf.clear()
                p0 = tf.paragraphs[0]
                set_run(p0.add_run(), 'Objetivos ESPECÍFICOS', F_BODY, 14, bold=True)
                for obj in objetivos_especificos:
                    p_sp = tf.add_paragraph()
                    p_sp.text = ''
                    p_sp.font.size = Pt(4)
                    p_item = tf.add_paragraph()
                    set_run(p_item.add_run(), obj, F_BODY, 11, bold=False)

            elif sh.name == 'CaixaDeTexto 12': # Módulos 1 e 2 (Títulos em Laranja FF912B, sem bullets)
                tf.clear()
                if len(modulos) >= 1:
                    m1 = modulos[0]
                    p_m1 = tf.paragraphs[0]
                    set_run(p_m1.add_run(), m1.get('titulo', 'MÓDULO 1').upper(), F_BODY, 12, bold=True, color_rgb=ORANGE_ACCENT)
                    for top in m1.get('topicos', []):
                        p = tf.add_paragraph()
                        set_run(p.add_run(), top, F_BODY, 10.5, bold=False)
                
                if len(modulos) >= 2:
                    m2 = modulos[1]
                    p_sp = tf.add_paragraph()
                    p_sp.text = ''
                    p_sp.font.size = Pt(6)
                    p_m2 = tf.add_paragraph()
                    set_run(p_m2.add_run(), m2.get('titulo', 'MÓDULO 2').upper(), F_BODY, 12, bold=True, color_rgb=ORANGE_ACCENT)
                    for top in m2.get('topicos', []):
                        p = tf.add_paragraph()
                        set_run(p.add_run(), top, F_BODY, 10.5, bold=False)

            elif sh.name == 'CaixaDeTexto 10': # Módulos 3 e 4 (Títulos em Laranja FF912B, sem bullets)
                tf.clear()
                if len(modulos) >= 3:
                    m3 = modulos[2]
                    p_m3 = tf.paragraphs[0]
                    set_run(p_m3.add_run(), m3.get('titulo', 'MÓDULO 3').upper(), F_BODY, 12, bold=True, color_rgb=ORANGE_ACCENT)
                    for top in m3.get('topicos', []):
                        p = tf.add_paragraph()
                        set_run(p.add_run(), top, F_BODY, 10.5, bold=False)
                
                if len(modulos) >= 4:
                    m4 = modulos[3]
                    p_sp = tf.add_paragraph()
                    p_sp.text = ''
                    p_sp.font.size = Pt(6)
                    p_m4 = tf.add_paragraph()
                    set_run(p_m4.add_run(), m4.get('titulo', 'MÓDULO 4').upper(), F_BODY, 12, bold=True, color_rgb=ORANGE_ACCENT)
                    for top in m4.get('topicos', []):
                        p = tf.add_paragraph()
                        set_run(p.add_run(), top, F_BODY, 10.5, bold=False)

    # ==============================================================================
    # CORREÇÃO GLOBAL: Substituir 'SKOALE' por 'SKOLAE'
    # ==============================================================================
    for s in prs.slides:
        for sh in s.shapes:
            if sh.has_text_frame and 'SKOALE' in sh.text_frame.text:
                for p in sh.text_frame.paragraphs:
                    if 'SKOALE' in p.text:
                        for r in p.runs:
                            if 'SKOALE' in r.text:
                                r.text = r.text.replace('SKOALE', 'SKOLAE')
                        if 'SKOALE' in p.text:
                            p.text = p.text.replace('SKOALE', 'SKOLAE')

    # ==============================================================================
    # SLIDE FINAL (Contactos Oficiais da Equipa Comercial e Pedagógica)
    # ==============================================================================
    s_last = prs.slides[-1]
    for sh in s_last.shapes:
        if sh.name == 'Retângulo 2':
            tf = sh.text_frame
            tf.clear()
            contacts = [
                ('Bruno Vicente', 'Business Developer', 'bvicente@abilways.com', 'Tlm.: (+35 1) 91 411 26 29'),
                ('Nuno Jorge', 'Head of Sales', 'njorge@abilways.com', 'Tlm.: (+351) 910 457 434'),
                ('Telma Lopes', 'Pedagogica Coordinator', 'tlopes@abilways.com', 'Tlm.: (+351) 914 165 110')
            ]
            for idx, (name, role, email, phone) in enumerate(contacts):
                p0 = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                if idx > 0:
                    p_sp = tf.add_paragraph()
                    p_sp.text = ''
                    p_sp.font.size = Pt(6)
                    p0 = tf.add_paragraph()
                
                r0 = p0.add_run()
                r0.text = name
                r0.font.name = F_BODY
                r0.font.size = Pt(13)
                r0.font.bold = True
                
                p1 = tf.add_paragraph()
                r1 = p1.add_run()
                r1.text = role
                r1.font.name = F_BODY
                r1.font.size = Pt(11)
                r1.font.bold = False
                
                p2 = tf.add_paragraph()
                r2 = p2.add_run()
                r2.text = email
                r2.font.name = F_BODY
                r2.font.size = Pt(11)
                r2.font.bold = False
                r2.font.underline = True
                r2.font.color.rgb = ORANGE_ACCENT
                
                p3 = tf.add_paragraph()
                r3 = p3.add_run()
                r3.text = phone
                r3.font.name = F_BODY
                r3.font.size = Pt(11)
                r3.font.bold = False

    # Determinar caminho de saída
    if not output_path:
        pasta_cliente = os.path.join(r'03_Carteira_Clientes\032_Clientes', cliente)
        os.makedirs(pasta_cliente, exist_ok=True)
        safe_course = "".join([c for c in titulo_curso if c.isalnum() or c in (' ', '_')]).strip().replace(' ', '_')
        output_path = os.path.join(pasta_cliente, f'Proposta_{cliente}_{safe_course}.pptx')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    return output_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Gerador de Propostas em PowerPoint da SKOLAE")
    parser.add_argument('--json', required=True, help="Caminho para o ficheiro JSON de dados da proposta")
    parser.add_argument('--output', required=False, help="Caminho de saída opcional do ficheiro PPTX")
    parser.add_argument('--template', default=r'Template Proposta - 1 curso.pptx', help="Caminho para o template base")
    
    args = parser.parse_args()
    with open(args.json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    res = gerar_proposta(data, template_path=args.template, output_path=args.output)
    print(f"SUCESSO: Proposta gerada em: {res}")
