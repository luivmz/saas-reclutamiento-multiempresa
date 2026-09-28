"""Rasteriza un SVG exportado por PowerDesigner con Edge sin interfaz (headless).

PowerDesigner 16.6 omite en su PNG nativo el contenido de los subprocesos expandidos
(vista compuesta); su SVG sí lo incluye. Este script produce el PNG desde ese SVG, sin
retoques: copia el SVG junto al original (para que resuelva la carpeta *_svg_Files con
los iconos), fija su ancho y alto en píxeles según el viewBox y toma la captura.

Uso: python svg2png.py entrada.svg salida.png [escala]
"""
import re
import subprocess
import sys
from pathlib import Path

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'


def render(svg, png, scale=2):
    svg, png = Path(svg).resolve(), Path(png).resolve()
    text = svg.read_text(encoding='utf-8')
    vb = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', text)
    width, height = int(float(vb.group(1)) + 0.999), int(float(vb.group(2)) + 0.999)
    head_end = text.index('>', text.index('<svg')) + 1
    head = text[:head_end]
    head = re.sub(r'\swidth="[^"]*"', f' width="{width}px"', head, count=1)
    head = re.sub(r'\sheight="[^"]*"', f' height="{height}px"', head, count=1)
    tmp = svg.with_name(svg.stem + '.render.svg')
    tmp.write_text(head + text[head_end:], encoding='utf-8')
    try:
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        '--default-background-color=FFFFFFFF', f'--force-device-scale-factor={scale}',
                        f'--window-size={width},{height}', f'--screenshot={png}', tmp.as_uri()],
                       check=True, capture_output=True)
    finally:
        tmp.unlink()
    return width, height


if __name__ == '__main__':
    print(render(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 2))
