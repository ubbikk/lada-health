from pathlib import Path
from datetime import date,timedelta
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader
import shutil
root=Path.cwd()
fonts=Path('/Users/dmytropetrovskyi/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype')
pdfmetrics.registerFont(TTFont('DejaVu',str(fonts/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVu-Bold',str(fonts/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold',italic='DejaVu',boldItalic='DejaVu-Bold')
styles={
 'title':ParagraphStyle('title',fontName='DejaVu-Bold',fontSize=19,leading=23,spaceAfter=10),
 'h':ParagraphStyle('h',fontName='DejaVu-Bold',fontSize=13,leading=18,spaceBefore=7,spaceAfter=5),
 'p':ParagraphStyle('p',fontName='DejaVu',fontSize=9.5,leading=13,spaceAfter=7),
 'small':ParagraphStyle('small',fontName='DejaVu',fontSize=9,leading=12,spaceAfter=5),
 'cell':ParagraphStyle('cell',fontName='DejaVu',fontSize=9.5,leading=13),
}
def P(t,s='p'):return Paragraph(t,styles[s])
def T(rows,widths):
    table=Table([[P(v,'cell') for v in row] for row in rows],colWidths=widths,hAlign='LEFT')
    table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5,colors.black),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EEEEEE')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    return table
out=root/'docs/2026-09-14-lada-medication-plan-uk.pdf'
story=[]
story += [P('Ліки Лади','title'),P('<b>Щоденний розклад • Початок 14 вересня 2026 року</b>'),P('Розклад для спрощеної схеми. Час можна змістити під сон і прийоми їжі, зберігаючи інтервали. Підйом о 12:00; сніданок о 13:00, вечеря о 23:00. Останній прийом - о 01:00 наступної календарної доби.'),P('<b>Оновлено 21 вересня 2026 року:</b> Ніксар 20 мг вранці; Гленцет Едванс увечері.')]
story += [T([
['<b>Коли</b>','<b>Що і скільки</b>'],
['<b>12:00</b><br/>За 1 годину до їжі','<b>Ніксар 20 мг вранці.</b><br/>З водою. Їжа та соки: не раніше ніж через 1 годину після таблетки; якщо вже поїла - зачекати 2 години до прийому.'],
['<b>12:30</b><br/>За 30 хв до сніданку','<b>Омепразол / Омез 20 мг - 1 капсула.</b>'],
['<b>13:00</b><br/>Після сніданку','<b>Медрол 16 мг (курс до 20.09).</b><br/><b>NOW B-1 100 мг - 2 таблетки (разом 200 мг).</b> Один раз на день, 10 днів від першого прийому.<br/><b>Серетид Евохалер 25/125 мкг - «1 доза».</b> Кількість натискань уточнити; після прийому прополоскати рот і виплюнути воду.<br/><b>Ріалтріс - «1 доза».</b> Кількість розпилень у кожну ніздрю уточнити.<br/><b>Опатанол 1 мг/мл - по 1 краплі</b> в кожне уражене око.'],
['<b>21:00</b>','<b>Опатанол - по 1 краплі</b> в кожне уражене око; приблизно через 8 годин після ранкового прийому.'],
['<b>23:00</b><br/>Після вечері','<b>Гленцет Едванс - 1 таблетка.</b><br/><b>Медрол 8 мг (курс до 20.09).</b> Разом із ранковими 16 мг це <b>24 мг на добу</b>.'],
['<b>01:00</b><br/>Наступної доби','<b>Серетид і Ріалтріс - повторити призначені дози.</b> Після Серетиду прополоскати рот.']
],[125,394]),Spacer(1,10),P('<b>Ніксар за потреби:</b> лікар дозволив збільшення до <b>40 мг загалом за добу</b> (ще 20 мг до ранкових 20 мг). Час додаткової дози не уточнено. Для неї також дотримуватися інтервалу з їжею та соками: за 1 годину до або через 2 години після.'),P('<b>У цій спрощеній схемі не приймаємо:</b> Домрид SR і фамотидин / Квамател. Для шлунка залишено омепразол. Дексаметазон не додаємо до Медролу.'),P('<b>Не надолужувати пропуски подвійними дозами.</b> Позначати прийом одразу після нього. Не відмовлятися від їжі заради часу Ніксару - краще змістити таблетку.')]
story += [PageBreak(),P('Строки та важливі примітки','title'),P('Курси старої схеми відраховано від <b>14.09.2026</b>; Гленцет Едванс - за призначенням від 18.09; для <b>NOW B-1</b> - від першого прийому. Останній зазначений день входить у курс. Прийом о 01:00 належить до попереднього дня розкладу; остання нічна доза - у ніч після зазначеної дати. Після завершення курсу прибрати відповідний рядок зі щоденного розкладу, враховуючи винятки нижче.')]
start=date(2026,9,14)
ends={n:(start+timedelta(days=n-1)).strftime('%d.%m.%Y') for n in [7,14,30,90]}
story += [T([
['<b>Препарат</b>','<b>Початок</b>','<b>Тривалість і останній день</b>'],
['NOW B-1 100 мг','Перший прийом','<b>2 таблетки на добу (200 мг).</b><br/>10 днів від першого прийому.'],
['Медрол','14.09.2026',f'7 днів: <b>{ends[7]}</b><br/><b>До цієї дати потрібен план завершення.</b>'],
['Омепразол / Омез','14.09.2026',f'14 днів: <b>{ends[14]}</b>'],
['Ніксар','14.09.2026',f'30 днів: <b>{ends[30]}</b>'],
['Гленцет Едванс','За призначенням:<br/>18.09.2026','14 днів: <b>01.10.2026</b><br/>1 таблетка ввечері.'],
['Ріалтріс','14.09.2026',f'30 днів: <b>{ends[30]}</b>'],
['Опатанол','14.09.2026',f'30 днів: <b>{ends[30]}</b>'],
['Серетид Евохалер','14.09.2026',f'90 днів: <b>{ends[90]}</b><br/>Подальше лікування астми визначити до завершення.']
],[155,105,259])]
story += [P('Що найважливіше','h'),P('<b>ЕпіПен має бути доступний завжди.</b> Мати при собі 2 справні автоін’єктори по 0,3 мг. Це засіб для анафілаксії, не щоденна доза. Якщо тяжкі прояви зберігаються після першого введення, повторна доза через 5 хвилин; не чекати надруковані у призначенні 30 хвилин.'),P('<b>Серетид приймати регулярно</b> для контролю астми. Він не є інгалятором швидкої допомоги. <b>Ніксар</b> залишено для щоденних алергічних симптомів; Ріалтріс та Опатанол - для носа й очей.'),P('Два уточнення щодо доз','h'),P('<b>Серетид і Ріалтріс:</b> у призначенні написано «1 доза двічі на день», але не визначено кількість натискань та розпилень у кожну ніздрю. Ці числа потрібно уточнити перед використанням таблиці як точного дозатора. Не збільшувати дозу за здогадкою.'),P('<b>Медрол:</b> 20 вересня - кінець записаного 7-денного курсу, а не автоматична вказівка різко припинити стероїд. Через попередній дексаметазон до цієї дати потрібна конкретна схема: припинення чи зниження. Самостійно не збільшувати дозу і не продовжувати курс.'),P('Аналіз на Helicobacter pylori','h'),P('Омепразол може зробити аналіз калу хибнонегативним. Якщо остання доза буде <b>27.09</b>, три повні тижні без нього завершаться <b>18.10</b>; практична дата здачі - <b>з 19.10.2026</b> за умови виконання правил лабораторії. Недавні антибіотики або препарати вісмуту можуть змінити дату. Цей інтервал відповідає трьом тижням у направленні.'),P('Ця пам’ятка стосується перелічених ліків. Вона не змінює окрему схему Жастінди чи інших постійних препаратів.','small')]
def footer(c,d):
    c.setFont('DejaVu',8);c.drawString(38,22,'Лада • Оновлено 21.09.2026');c.drawRightString(A4[0]-38,22,str(d.page))
doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=38,rightMargin=38,topMargin=32,bottomMargin=36,title='Ліки Лади та щоденний розклад',author='')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
reader=PdfReader(out)
assert len(reader.pages)==2,len(reader.pages)
text='\n'.join(p.extract_text() for p in reader.pages)
for end in ends.values():assert end in text,end
(root/'output/medication-review-2026-09-21/simplified-pdf-text.txt').write_text(text)
print('Verified 2 pages; course end dates:',ends)
