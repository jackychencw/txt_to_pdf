
import locale
import re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, PageBreak

pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))
pdfmetrics.registerFont(TTFont('msyhBd', 'msyh.ttf'))
pdfmetrics.registerFont(TTFont('msyhIt', 'msyh.ttf'))
pdfmetrics.registerFont(TTFont('msyhBI', 'msyh.ttf'))

style = ParagraphStyle('test')
style.fontName = 'msyh'
style.fontSize = 10
style.firstLineIndent=2*style.fontSize
style.leading = 1.4*style.fontSize
spaceBefore = 0.5*style.fontSize

def guess_notepad_encoding(filepath, default_ansi_encoding=None):
    with open(filepath, 'rb') as f:
        data = f.read(3)
    if data[:2] in ('\xff\xfe', '\xfe\xff'):
        return 'utf-16'
    if data == u''.encode('utf-8-sig'):
        return 'utf-8-sig'
    # presumably "ANSI"
    return default_ansi_encoding or locale.getpreferredencoding()

def txtToPdf(filename):
    fpath = filename
    enc = guess_notepad_encoding(fpath)
    f = open(fpath, encoding=enc)
    try:
        story = []
        pdf_name = filename[:-3] + 'pdf'
        print(pdf_name)
        for line in f.readlines():
            line = re.sub(r"</?[a-zA-z]>?", "", line)

            p = Paragraph(line, style)
            p.spaceBefore = spaceBefore
            story.append(p)

        doc = SimpleDocTemplate(pdf_name)
        doc.build(story)
    finally:
        f.close()