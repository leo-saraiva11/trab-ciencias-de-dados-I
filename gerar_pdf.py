#!/usr/bin/env python3
"""
Gera o PDF do relatório final a partir de `relatorio_final.md`.
Fluxo: Markdown -> HTML (com CSS de relatório) -> PDF (via Google Chrome headless).

Uso:
  python3 gerar_pdf.py
"""
import os
import sys
import subprocess

import markdown

PROJECT = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(PROJECT, "relatorio_final.md")
HTML = os.path.join(PROJECT, "relatorio_final.html")
PDF = os.path.join(PROJECT, "relatorio_final.pdf")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
@page { size: A4; margin: 2cm 1.7cm; }
* { box-sizing: border-box; }
body { font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif;
       font-size: 10.5pt; line-height: 1.5; color: #1a1a1a; }
.cabecalho { text-align: center; line-height: 1.4; margin: 2px 0; }
h1 { font-size: 19pt; text-align: center; margin: 6px 0 14px; }
h2 { font-size: 14pt; border-bottom: 2px solid #333; padding-bottom: 3px;
     margin: 22px 0 10px; page-break-after: avoid; }
h3 { font-size: 12pt; margin: 16px 0 6px; page-break-after: avoid; }
h4 { font-size: 11pt; margin: 12px 0 6px; }
p, li { text-align: justify; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9pt;
        page-break-inside: avoid; }
th, td { border: 1px solid #bbb; padding: 4px 7px; vertical-align: top; }
th { background: #eef1f4; font-weight: 600; text-align: left; }
tr:nth-child(even) td { background: #fafafa; }
code { background: #f3f3f3; padding: 1px 4px; border-radius: 3px;
       font-family: 'SF Mono', Menlo, monospace; font-size: 8.8pt; }
pre { background: #f6f8fa; padding: 10px; border-radius: 5px; overflow-x: auto; }
pre code { background: none; padding: 0; font-size: 8.5pt; }
blockquote { border-left: 3px solid #999; margin: 10px 0; padding: 4px 12px;
             background: #f8f8f8; color: #333; }
a { color: #0645ad; text-decoration: none; word-break: break-all; }
strong { color: #111; }
"""


def main():
    if not os.path.exists(CHROME):
        sys.exit("ERRO: Google Chrome não encontrado em " + CHROME)
    with open(MD, encoding="utf-8") as f:
        corpo = markdown.markdown(
            f.read(),
            extensions=["tables", "fenced_code", "sane_lists", "md_in_html"],
        )
    html = ("<!doctype html><html lang='pt-br'><head><meta charset='utf-8'>"
            f"<style>{CSS}</style></head><body>{corpo}</body></html>")
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)

    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={PDF}", "file://" + HTML],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print(f"PDF gerado: {os.path.relpath(PDF, PROJECT)} "
          f"({os.path.getsize(PDF) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
