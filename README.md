# pdfaddheader

既存の PDF ファイルに、ヘッダーテキストと、フッターテキストを追加するコマンドラインツールです。
例：

- python pdfaddheader.py -f report.pdf -u "aaa" -b "bottombottombottom"
- pyinstaller pdfaddheader.py --onefile で、Windows 実行ファイル化したので、pdfaddheader.exe -f report.pdf -u "aaa" -b "bottombottombottom" も利用できます。
