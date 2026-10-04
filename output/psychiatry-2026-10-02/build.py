from pathlib import Path
import re, shutil
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from pypdf import PdfReader
D=Path('docs'); fonts=Path('/Users/dmytropetrovskyi/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype')
for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,str(fonts/file)))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB')
styles={k:ParagraphStyle(k,fontName='DVB' if k in ['title','h'] else 'DV',fontSize=sz,leading=lead,spaceAfter=gap,keepWithNext=k in ['title','h']) for k,sz,lead,gap in [('title',17,22,9),('h',11.5,15,7),('p',10,14,8),('small',8.5,12,6),('cell',9.2,12.5,0)]}
def fmt(s):return re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',escape(s))
def P(s,k='p'):return Paragraph(fmt(s),styles[k])
def footer(c,d):
 c.setFont('DV',8);c.setFillColor(colors.HexColor('#666666'));c.drawString(42,25,'Лада | Оновлено 02.10.2026');c.drawRightString(A4[0]-42,25,str(d.page))
def build(path,flow):
 SimpleDocTemplate(str(path),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=36,bottomMargin=46,title='Лада: нотатки та ліки',author='Дмитро').build(flow,onFirstPage=footer,onLaterPages=footer)
 print(path,len(PdfReader(path).pages))

psych=Path('docs/2026-10-02-psychiatrist-uk.md').read_text()
flow=[]
for block in psych.strip().split('\n\n'):
 if block=='---':flow.append(PageBreak());continue
 if block.startswith('# '):
  lines=block.splitlines();flow.append(P(lines[0][2:],'title'))
  if len(lines)>1:flow.append(P(' '.join(lines[1:]),'small'))
 elif block.startswith('## '):
  lines=block.splitlines();flow.append(P(lines[0][3:],'h'))
  if len(lines)>1:flow.append(P(' '.join(lines[1:])))
 else:flow.append(P(block))
build(D/'2026-10-02-psychiatrist-uk.pdf',flow)
assert len(PdfReader(D/'2026-10-02-psychiatrist-uk.pdf').pages)==2
