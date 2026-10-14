import sys
import pptx
from pptx.util import Pt
from pptx.dml.color import RGBColor

ORANGE_MAIN = RGBColor(0xFF, 0x9B, 0x23)
ORANGE_ACCENT = RGBColor(0xFF, 0x91, 0x2B)

input_path = r'c:\Users\brunn\OneDrive - GIE IFE\Desktop\Bruno\PESSOAL\Business Development Formação\03_Carteira_Clientes\032_Clientes\Devoteam\SKOLAE - Comunicar com Impacto da Apresentação Pessoal ao Pitch Profissional.pptx'
output_path = r'c:\Users\brunn\OneDrive - GIE IFE\Desktop\Bruno\PESSOAL\Business Development Formação\03_Carteira_Clientes\032_Clientes\Devoteam\Proposta_Devoteam_Comunicar_com_Impacto_Pitch.pptx'

prs = pptx.Presentation(input_path)

# ==============================================================================
# SLIDE 2 (Contexto, Desafio, Why, Proposito)
# ==============================================================================
s2 = prs.slides[1]

for sh in s2.shapes:
    if sh.name == 'Retângulo 2':
        tf = sh.text_frame
        tf.clear()
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = 'A '
        r0.font.name = 'Basier Circle'
        r0.font.size = Pt(13)

        r1 = p0.add_run()
        r1.text = 'Devoteam'
        r1.font.name = 'Basier Circle'
        r1.font.size = Pt(13)
        r1.font.bold = True
        r1.font.color.rgb = ORANGE_ACCENT

        r2 = p0.add_run()
        r2.text = ' procurou a SKOLAE para o desenvolvimento de um programa prático de Elevator Pitch e Técnicas de Apresentação em língua inglesa, desenhado especificamente para os seus consultores e perfis técnicos.'
        r2.font.name = 'Basier Circle'
        r2.font.size = Pt(13)

        p1 = tf.add_paragraph()
        p1.text = ''

        p2 = tf.add_paragraph()
        r3 = p2.add_run()
        r3.text = 'A SKOLAE Formação dispõe de soluções pedagógicas orientadas à transposição do know-how técnico em valor de negócio, dotando os profissionais de ferramentas para comunicar com assertividade, clareza e autoridade perante clientes e stakeholders internacionais.'
        r3.font.name = 'Basier Circle'
        r3.font.size = Pt(13)

    elif sh.name == 'CaixaDeTexto 5':
        tf = sh.text_frame
        tf.clear()
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = 'Comunicar com impacto,'
        r0.font.name = 'Basier Circle'
        r0.font.size = Pt(20)

        p1 = tf.add_paragraph()
        r1 = p1.add_run()
        r1.text = 'Clareza executiva e'
        r1.font.name = 'Basier Circle'
        r1.font.size = Pt(20)

        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = 'Presença profissional.'
        r2.font.name = 'Basier Circle'
        r2.font.size = Pt(20)

    elif sh.name == 'CaixaDeTexto 11':
        tf = sh.text_frame
        tf.clear()
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = 'Sugerimos que cada turma não ultrapasse os 8 a 10 participantes, de forma a garantir a realização de simulações, gravação e feedback individualizado. '
        r0.font.name = 'Basier Circle'
        r0.font.size = Pt(12)

        r1 = p0.add_run()
        r1.text = 'O propósito desta proposta'
        r1.font.name = 'Basier Circle'
        r1.font.size = Pt(12)
        r1.font.color.rgb = ORANGE_ACCENT

        r2 = p0.add_run()
        r2.text = ' será: dotar os consultores da Devoteam de técnicas práticas para estruturar e apresentar um pitch convincente e com impacto em inglês.'
        r2.font.name = 'Basier Circle'
        r2.font.size = Pt(12)

    elif sh.name == 'CaixaDeTexto 3':
        tf = sh.text_frame
        tf.clear()
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = '“A clareza e a segurança na apresentação pessoal e de soluções são determinantes para transformar competência técnica em confiança e autoridade comercial.”'
        r0.font.name = 'Basier Circle'
        r0.font.size = Pt(12)

    elif sh.name == 'Retângulo: Canto Arredondado 15':
        tf = sh.text_frame
        tf.clear()
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = 'Consultores e Perfis Técnicos (TI / Cloud)'
        r0.font.name = 'GT Walsheim Pro'
        r0.font.size = Pt(13)
        r0.font.bold = True
        r0.font.color.rgb = ORANGE_MAIN

    elif sh.name == 'Retângulo: Canto Arredondado 16':
        tf = sh.text_frame
        tf.clear()
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = '8 a 10'
        r0.font.name = 'GT Walsheim Pro'
        r0.font.size = Pt(26)
        r0.font.bold = True
        r0.font.color.rgb = ORANGE_MAIN

        p1 = tf.add_paragraph()
        r1 = p1.add_run()
        r1.text = 'formandos / turma'
        r1.font.name = 'GT Walsheim Pro'
        r1.font.size = Pt(13)
        r1.font.bold = True
        r1.font.color.rgb = ORANGE_MAIN

# ==============================================================================
# SLIDE 6 (Itinerário Pedagógico - Destinatários e Metodologias)
# ==============================================================================
s6 = prs.slides[5]
for sh in s6.shapes:
    if sh.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.GROUP:
        for c in sh.shapes:
            if c.name == 'CaixaDeTexto 28' and c.has_text_frame:
                tf = c.text_frame
                tf.clear()
                p0 = tf.paragraphs[0]
                r0 = p0.add_run()
                r0.text = 'Destinatários'
                r0.font.name = 'Basier Circle'
                r0.font.size = Pt(14)
                r0.font.bold = True

                p1 = tf.add_paragraph()
                r1 = p1.add_run()
                r1.text = 'Consultores, engenheiros e equipas técnicas da Devoteam que pretendam reforçar o impacto da sua comunicação pessoal e estruturar apresentações de valor em inglês perante clientes e stakeholders.'
                r1.font.name = 'Basier Circle'
                r1.font.size = Pt(11)

prs.save(output_path)
print('Proposta Devoteam gerada com sucesso em:', output_path)
