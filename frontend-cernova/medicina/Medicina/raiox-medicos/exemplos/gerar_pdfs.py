# -*- coding: utf-8 -*-
"""Gera os PDFs de exemplo (relatório + entrevista) do Raio-X — identidade azul sóbria."""
import os, math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Flowable, KeepTogether)

OUT = os.path.dirname(os.path.abspath(__file__))

NAVY   = colors.HexColor('#15304c')
NAVY2  = colors.HexColor('#1d3f63')
BLUE   = colors.HexColor('#2f5d8a')
MUTED  = colors.HexColor('#5b6b7c')
INK    = colors.HexColor('#1f2a36')
LINE   = colors.HexColor('#e3e9ef')
BG     = colors.HexColor('#f2f5f8')
SEV    = {'alto': NAVY, 'medio': colors.HexColor('#3f6390'), 'baixo': colors.HexColor('#8aa0b8')}
GA     = {'verde':'#5a8f6e','amarelo':'#bb9a44','vermelho':'#a8543f'}
GA_L   = {'verde':'#bcd2c5','amarelo':'#e6d6ad','vermelho':'#ddb6ab'}

ss = getSampleStyleSheet()
def st(name, **kw):
    base = dict(fontName='Helvetica', fontSize=10.5, leading=15, textColor=INK)
    base.update(kw); return ParagraphStyle(name, **base)

H1   = st('H1', fontName='Helvetica-Bold', fontSize=19, leading=23, textColor=NAVY)
SUB  = st('SUB', fontSize=11, textColor=MUTED)
SEC  = st('SEC', fontName='Helvetica-Bold', fontSize=10, textColor=BLUE, leading=14, spaceBefore=6, spaceAfter=4)
ATIT = st('ATIT', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=NAVY)
IMP  = st('IMP', fontSize=10.5, leading=15)
FUND = st('FUND', fontName='Helvetica-Oblique', fontSize=9.5, textColor=MUTED)
LEAD = st('LEAD', fontSize=12, leading=17, textColor=INK)
WHITE= st('WHITE', fontSize=11.5, leading=16, textColor=colors.white)
TAGW = st('TAGW', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)
SMALL= st('SMALL', fontSize=8.5, textColor=MUTED, leading=12)
BANDS= st('BANDS', fontName='Helvetica-Bold', fontSize=15, textColor=colors.HexColor('#a8543f'), alignment=TA_CENTER)

class Logo(Flowable):
    def __init__(self): self.width=460; self.height=42
    def draw(self):
        c=self.canv
        c.setFillColor(NAVY); c.roundRect(0,2,38,38,9,fill=1,stroke=0)
        c.setFillColor(colors.white); c.setFont('Helvetica-Bold',15); c.drawCentredString(19,14,'JC')
        c.setFillColor(NAVY); c.setFont('Helvetica-Bold',14); c.drawString(50,24,'Junior Contabilidade')
        c.setFillColor(MUTED); c.setFont('Helvetica',10); c.drawString(50,9,'Assessoria para médicos e clínicas')

class Gauge(Flowable):
    def __init__(self, faixa, score, w=260, h=120):
        self.faixa=faixa; self.score=score; self.width=w; self.height=h
    def draw(self):
        c=self.canv; cx=self.width/2; cy=26; r=92
        x1,y1,x2,y2=cx-r,cy-r,cx+r,cy+r
        c.setLineCap(1); c.setLineWidth(15)
        for name,start in (('vermelho',2),('amarelo',62),('verde',122)):
            ext=56
            c.setStrokeColor(colors.HexColor(GA[name] if self.faixa==name else GA_L[name]))
            p=c.beginPath(); p.arc(x1,y1,x2,y2,start,ext); c.drawPath(p)
        ang=180-(min(self.score,16)/16.0)*180
        rr=r-12; nx=cx+rr*math.cos(math.radians(ang)); ny=cy+rr*math.sin(math.radians(ang))
        c.setStrokeColor(NAVY); c.setLineWidth(3.5); c.line(cx,cy,nx,ny)
        c.setFillColor(NAVY); c.circle(cx,cy,6,fill=1,stroke=0)

def alerta(a):
    sev=a['severidade']
    tag=Table([[Paragraph(sev.upper(), TAGW)]], colWidths=[14*mm])
    tag.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),SEV[sev]),('TOPPADDING',(0,0),(-1,-1),2),
        ('BOTTOMPADDING',(0,0),(-1,-1),2),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    head=Table([[Paragraph(a['titulo'],ATIT), tag]], colWidths=[None,16*mm])
    head.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]))
    inner=[head, Spacer(1,5), Paragraph(a['impacto'],IMP), Spacer(1,5), Paragraph(a['fundamento'],FUND)]
    box=Table([[inner]], colWidths=[165*mm])
    box.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
        ('TOPPADDING',(0,0),(-1,-1),11),('BOTTOMPADDING',(0,0),(-1,-1),11),
        ('LINEBEFORE',(0,0),(0,-1),4,SEV[sev]),('BOX',(0,0),(-1,-1),0.6,LINE),
        ('BACKGROUND',(0,0),(-1,-1),colors.white)]))
    return KeepTogether([box, Spacer(1,9)])

# ---------------- RELATÓRIO ----------------
REPORT = {
 'faixa':'vermelho','score':17,'rotulo':'Exposição alta','perfil':'Clínica de convênio (Lucro Presumido)',
 'leitura':'O Raio-X acendeu o vermelho: a clínica tem múltiplos pontos de exposição abertos ao mesmo tempo — fiscal, contratual e de dados — e pelo menos três deles podem gerar cobrança retroativa ou perda de receita imediata.',
 'alertas':[
   {'severidade':'alto','titulo':'A clínica aplica a tributação reduzida de serviços hospitalares sem cumprir os requisitos formais — o benefício pode ser revertido com cobrança retroativa',
    'impacto':'Usar a presunção de 8% de IRPJ e 12% de CSLL sem ser sociedade empresária e sem licença Anvisa em dia é exatamente o cenário em que o Fisco reverte o benefício e cobra a diferença dos últimos 5 anos, com multa e juros. O STJ já negou o benefício a uma clínica nessa situação por ausência de forma societária adequada e de conformidade com a Anvisa. O risco não é teórico.',
    'fundamento':'base: STJ Tema 217 (REsp 1.116.399/BA) + STJ REsp 1.877.568 + CARF Súmula 142'},
   {'severidade':'alto','titulo':'Sem contrato escrito com todas as operadoras, a clínica perde o direito de contestar glosas',
    'impacto':'Sem contrato escrito e sem faturar no padrão TISS vigente, a operadora pode glosar (deixar de pagar) procedimentos e o prestador perde o direito de acessar a justificativa e de contestar. É perda direta de caixa e fragiliza a posição da clínica em reajustes e na cobrança do que é devido.',
    'fundamento':'base: Lei 9.656/1998 + Lei 13.003/2014 + RN ANS 503/2022 + RN ANS 489/2022'},
   {'severidade':'alto','titulo':'A clínica trata dados sensíveis de pacientes sem base legal definida e sem plano de incidente',
    'impacto':'Dados de saúde são dados sensíveis. Tratar sem base legal, sem controle de acesso e sem plano de resposta a incidente expõe a clínica a multa de até 2% do faturamento (limitada a R$ 50 milhões por infração), além de indenização ao paciente e dano de reputação. O médico costuma ignorar que é o controlador e que responde pelo fornecedor de TI.',
    'fundamento':'base: LGPD (Lei 13.709/2018) + Resolução ANPD 15/2024'},
   {'severidade':'medio','titulo':'A receita de consulta simples não está separada das demais — e isso fragiliza toda a tese tributária',
    'impacto':'O benefício da base reduzida de IRPJ/CSLL nunca se aplica a consultas médicas simples — essa exclusão é expressa no STJ Tema 217 e na Súmula CARF 142. Sem separar a receita de consulta das receitas de procedimentos, exames e terapias, a clínica não consegue demonstrar qual parcela do faturamento tem direito ao tratamento diferenciado. Em uma autuação, a falta de segregação tende a contaminar tudo.',
    'fundamento':'base: STJ REsp 1.877.568 + STJ Tema 217 (REsp 1.116.399/BA)'},
   {'severidade':'medio','titulo':'Licença Anvisa desatualizada ou inexistente bloqueia o benefício fiscal e expõe a clínica a interdição',
    'impacto':'O cumprimento das normas da Anvisa — boas práticas de funcionamento (RDC 63/2011) e infraestrutura física (RDC 50/2002) — é requisito legal para sustentar a tese de serviços hospitalares no IRPJ/CSLL. Sem licença sanitária em dia, o Fisco afasta o benefício. Além disso, falhas nas boas práticas ou projeto físico fora da norma podem gerar auto de infração, multa e interdição em inspeção da vigilância sanitária.',
    'fundamento':'base: Anvisa RDC 63/2011 + Anvisa RDC 50/2002'},
 ],
 'naoAvaliado':'Este Raio-X é uma triagem — ele mostra onde há fumaça, mas só o Diagnóstico quantifica o tamanho real de cada exposição, confirma os períodos em aberto e indica o que precisa ser resolvido primeiro.',
 'cta':'Sua exposição está alta. No Diagnóstico Executivo a gente quantifica cada um desses alertas e monta o plano de blindagem. Quer que o nosso time entre em contato?',
 'disclaimer':'Triagem preliminar automatizada, com base em normas e jurisprudência vigentes (validadas em 06/2026). Não constitui parecer jurídico-contábil; a confirmação ocorre no diagnóstico. — Junior Contabilidade & Assessoria',
}

def build_report(path):
    doc=SimpleDocTemplate(path, pagesize=A4, leftMargin=22*mm, rightMargin=22*mm, topMargin=18*mm, bottomMargin=16*mm,
                          title='Relatório — Raio-X de Exposição')
    e=[Logo(), Spacer(1,14), Paragraph('Relatório — Raio-X de Exposição', H1),
       Paragraph('Perfil: '+REPORT['perfil'], SUB), Spacer(1,12)]
    box=Table([[ [Gauge(REPORT['faixa'],REPORT['score']), Spacer(1,2), Paragraph(REPORT['rotulo'],BANDS),
                  Spacer(1,4), Paragraph('Pontuação de exposição: <b>%d</b>'%REPORT['score'], st('c',alignment=TA_CENTER,textColor=MUTED,fontSize=10))] ]], colWidths=[165*mm])
    box.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.6,LINE),('BACKGROUND',(0,0),(-1,-1),colors.white),
        ('TOPPADDING',(0,0),(-1,-1),14),('BOTTOMPADDING',(0,0),(-1,-1),14)]))
    e+=[box, Spacer(1,12), Paragraph(REPORT['leitura'], LEAD), Spacer(1,14),
        Paragraph('Seus principais alertas', st('h',fontName='Helvetica-Bold',fontSize=14,textColor=NAVY)), Spacer(1,8)]
    for a in REPORT['alertas']: e.append(alerta(a))
    na=Table([[Paragraph(REPORT['naoAvaliado'], st('na',fontSize=10,textColor=colors.HexColor('#41566c'),leading=14))]], colWidths=[165*mm])
    na.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#eef3f8')),('BOX',(0,0),(-1,-1),0.6,colors.HexColor('#dce5ee')),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    cta=Table([[Paragraph(REPORT['cta'], WHITE)]], colWidths=[165*mm])
    cta.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),('LEFTPADDING',(0,0),(-1,-1),16),('RIGHTPADDING',(0,0),(-1,-1),16),
        ('TOPPADDING',(0,0),(-1,-1),14),('BOTTOMPADDING',(0,0),(-1,-1),14),('ROUNDEDCORNERS',[8,8,8,8])]))
    e+=[Spacer(1,6), na, Spacer(1,12), cta, Spacer(1,14), Paragraph(REPORT['disclaimer'], SMALL)]
    doc.build(e)

# ---------------- ENTREVISTA (transcrição) ----------------
TURNS = [
 ('sec','Boas-vindas e consentimento (LGPD)'),
 ('a','Oi! Sou a Alice, especialista em estrutura fiscal, patrimonial e de governança para médicos. Em poucos minutos eu mostro os riscos que o seu consultório ou clínica pode estar correndo. Não pergunto nada sobre pacientes — só sobre a estrutura do negócio. Antes de começar, preciso do seu OK para usar suas respostas no resultado e para o nosso time entrar em contato (consentimento — art. 7º, I, da LGPD).'),
 ('c','Li e concordo. Pode começar.'),
 ('sec','Identificação e segmentação'),
 ('a','Vamos começar entendendo sua estrutura. Como você atua hoje?'),('c','Tenho 1 PJ / clínica.'),
 ('a','De onde vem a maior parte da sua receita?'),('c','Convênios / planos de saúde.'),
 ('a','Faixa de faturamento anual, somando tudo?'),('c','R$ 1 – 4,8 milhões.'),
 ('a','E o regime tributário atual?'),('c','Lucro Presumido.'),
 ('sec','Tributação da clínica'),
 ('a','Vamos olhar a parte tributária da clínica. Vocês usam (ou querem usar) a tributação reduzida de serviços hospitalares — a presunção de 8% de IRPJ e 12% de CSLL?'),('c','Sim, e não cumprimos sociedade empresária / sem licença Anvisa.'),
 ('a','Vocês separam a receita de consulta simples das demais (procedimentos, exames, terapias)?'),('c','Não / não sei.'),
 ('a','A clínica está registrada/licenciada na Anvisa/vigilância sanitária e em dia?'),('c','Não / não sei.'),
 ('a','Se fazem análises clínicas/laboratório (inclusive testes rápidos), conhecem a norma vigente (RDC 978/2025)?'),('c','Não fazemos análises clínicas.'),
 ('sec','Relação com os convênios'),
 ('a','Sobre a sua relação com os convênios. Há contrato escrito com todas as operadoras com quem vocês trabalham?'),('c','Não / só com algumas.'),
 ('a','Vocês têm uma rotina formal de recurso de glosa (faturamento em TISS, prazos, contestação)?'),('c','Não / não sei.'),
 ('sec','Dados de pacientes e governança'),
 ('a','Quase lá. Vocês tratam dados de pacientes com base legal definida, controle de acesso e plano de incidente?'),('c','Não / não sei.'),
 ('a','Sabem que um incidente relevante (vazamento) precisa ser comunicado à ANPD em 3 dias úteis?'),('c','Sim, sabíamos.'),
 ('a','Atendem por telemedicina com registro em prontuário?'),('c','Não fazemos telemedicina.'),
 ('a','A publicidade e as redes sociais seguem a Resolução CFM 2.336/2023 (CRM/RQE, regras de imagem e preço)?'),('c','Sim, seguem as regras.'),
 ('sec','Transição tributária 2026'),
 ('a','Por fim, a transição de 2026. Se a clínica fosse do Simples, já estaria pronta para a NFS-e nacional (obrigatória desde set/2026)?'),('c','Não somos do Simples.'),
 ('a','E o sistema de vocês já emite documento com destaque de CBS/IBS (vigente desde jan/2026)?'),('c','Não / não sei.'),
 ('a','Perfeito, terminei a leitura. Vou te mostrar o resultado.'),
]

def bubble(role, text):
    if role=='a':
        body=[Paragraph('Alice', SMALL), Spacer(1,2), Paragraph(text, st('ab',fontSize=10.5,leading=15,textColor=INK))]
        t=Table([[body]], colWidths=[120*mm], hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#eef4f9')),('BOX',(0,0),(-1,-1),0.5,LINE),
            ('LEFTPADDING',(0,0),(-1,-1),11),('RIGHTPADDING',(0,0),(-1,-1),11),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    else:
        body=[Paragraph('Cliente', st('cw',fontSize=8.5,textColor=colors.HexColor('#cfe0ee'),alignment=TA_RIGHT)), Spacer(1,2),
              Paragraph(text, st('cb',fontSize=10.5,leading=15,textColor=colors.white,fontName='Helvetica-Bold'))]
        t=Table([[body]], colWidths=[120*mm], hAlign='RIGHT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLUE),
            ('LEFTPADDING',(0,0),(-1,-1),11),('RIGHTPADDING',(0,0),(-1,-1),11),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    return KeepTogether([t, Spacer(1,7)])

def build_transcript(path):
    doc=SimpleDocTemplate(path, pagesize=A4, leftMargin=22*mm, rightMargin=22*mm, topMargin=18*mm, bottomMargin=16*mm,
                          title='Transcrição — Raio-X de Exposição')
    e=[Logo(), Spacer(1,14), Paragraph('Transcrição da conversa — Raio-X de Exposição', H1),
       Paragraph('Agente Alice · perfil: Clínica de convênio (Lucro Presumido)', SUB), Spacer(1,8)]
    note=Table([[Paragraph('Cliente fictício, usado para demonstração. As respostas foram roteirizadas para ilustrar uma clínica com várias exposições abertas. Nenhum dado real.', st('n',fontSize=9.5,textColor=colors.HexColor('#7a5b16'),leading=13))]], colWidths=[165*mm])
    note.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#fff8ec')),('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#f3e3c0')),
        ('LEFTPADDING',(0,0),(-1,-1),11),('RIGHTPADDING',(0,0),(-1,-1),11),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)]))
    e+=[note, Spacer(1,12)]
    for role,text in TURNS:
        if role=='sec': e+=[Spacer(1,6), Paragraph(text.upper(), SEC), Spacer(1,2)]
        else: e.append(bubble(role,text))
    res=Table([[ [Paragraph('Resultado do Raio-X', st('rt',fontName='Helvetica-Bold',fontSize=11,textColor=colors.white,alignment=TA_CENTER)),
                  Spacer(1,3), Paragraph('Exposição alta — pontuação 17 — 5 alertas (3 de severidade alta)', st('rb',fontSize=11,textColor=colors.white,alignment=TA_CENTER)),
                  Spacer(1,3), Paragraph('O detalhamento de cada alerta está no Relatório do Raio-X.', st('rs',fontSize=9.5,textColor=colors.HexColor('#cfe0ee'),alignment=TA_CENTER))] ]], colWidths=[165*mm])
    res.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),('TOPPADDING',(0,0),(-1,-1),14),('BOTTOMPADDING',(0,0),(-1,-1),14)]))
    e+=[Spacer(1,10), res, Spacer(1,12),
        Paragraph('Triagem preliminar automatizada, com base em normas e jurisprudência vigentes (validadas em 06/2026). Não constitui parecer jurídico-contábil; a confirmação ocorre no diagnóstico. — Junior Contabilidade & Assessoria', SMALL)]
    doc.build(e)

build_report(os.path.join(OUT,'Relatorio-RaioX-exemplo-clinica-convenio.pdf'))
build_transcript(os.path.join(OUT,'Transcricao-RaioX-exemplo-clinica-convenio.pdf'))
print('PDFs gerados em', OUT)
