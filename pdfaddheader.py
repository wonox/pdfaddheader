# https://achiwa912.github.io/pdfpagenum.html
from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import sys
import os
import argparse

# outline --help
parser = argparse.ArgumentParser(
    description='PDFファイルにヘッダーとフッターを加える\npdfaddheader.py -f report.pdf -u "aaa" -b "bottombottombottom"')

parser.add_argument(
    '-f',
    '--file',
    type=str,
    help='path\\filename.docx',
    required=True)

parser.add_argument(
    '-u',
    '--upper',
    type=str,
    help='header部分のテキスト',
    required=True)

parser.add_argument(
    '-b',
    '--bottom',
    type=str,
    help='footer部分のテキスト',
    required=True)


def pdfaddheader(path, header_text, footer_text):
    # フォントの設定
    font_name = "HeiseiKakuGo-W5"
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
    output_file = os.path.basename(path).split('.', 1)[0] + "_pgn.pdf"
    reader = PdfReader(path)
    pages = [pagexobj(p) for p in reader.pages]

    canvas = Canvas(output_file)

    for page_num, page in enumerate(pages, start=1):
        canvas.doForm(makerl(canvas, page))
        # footer_nombre = f"{page_num}/{len(pages)}"
        # header_text = r"ヘッダーのテスト"
        # footer_text = r"フッターのテスト"
        canvas.saveState()
        canvas.setStrokeColorRGB(0, 0, 0)
        canvas.setFont(font_name, 14)
        # PDFの高さ-10
        pdf_size = get_mediabox(page)[3] - 11
        # canvas.drawString(1, 830, header_text)
        canvas.drawString(1, pdf_size, header_text)
        # canvas.drawString(290, 10, footer_nombre)
        canvas.drawString(1, 1, footer_text)
        canvas.restoreState()
        canvas.showPage()

    canvas.save()


def get_mediabox(page):
    fs = []
    # pages2 = PdfReader(input_file).pages だと、MediaBox
    # mbox = page.MediaBox or page.inheritable.MediaBox
    # pages = [pagexobj(p) for p in reader.pages] だと BBox
    mbox = page.BBox or page.inheritable.BBox
    for m in mbox:
        fs.append(float(m))
    return fs


# コマンドライン引数を処理する
if __name__ == '__main__':
    cmd_args = parser.parse_args()
    file_path = cmd_args.file
    header_text = cmd_args.upper
    footer_text = cmd_args.bottom
    print(cmd_args.file)
    if not file_path:
        sys.exit('Arguments are too short')
    else:
        # 絶対パスへ変換
        path = os.path.abspath(file_path)
        # ファイルの存在有無
        if not os.path.isfile(path):
            sys.exit("I don't have that file.")
        pdfaddheader(path, header_text, footer_text)
