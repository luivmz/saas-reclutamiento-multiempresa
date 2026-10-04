"""F33 — Diagramas reproducibles del diseño funcional del motor (Pillow, sin dependencias nuevas).

Genera en docs/academico/diseno-inteligente/diagramas/:
  F33-01_flujo_funcional.png      flujo vacante → evidencia → nivel humano → comparación → decisión RF-23
  F33-02_arquitectura_funcional.png  Laravel (registro) → cola → servicio futuro → resultado → auditoría → revisión

Son diagramas de DISEÑO: nada de lo dibujado como «propuesto» o «futuro» existe en el código.
Uso: python docs/academico/tools/f33/diagramas.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..', '..', 'diseno-inteligente', 'diagramas'))
FONT = 'C:/Windows/Fonts/arial.ttf'
FONT_B = 'C:/Windows/Fonts/arialbd.ttf'

# Paleta: humano, sistema determinista, existente, futuro (requiere G0 completa), bloqueado.
C = dict(humano='#DCEBFA', sistema='#DDF2E3', existente='#EFEFEF', futuro='#FFFFFF', bloqueado='#FADBD8',
         borde='#2F4F6F', texto='#111111', flecha='#2F4F6F', rojo='#B03A2E', gris='#7F7F7F')


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def wrap(d, text, f, width):
    lines = []
    for par in text.split('\n'):
        cur = ''
        for w in par.split(' '):
            t = (cur + ' ' + w).strip()
            if d.textlength(t, font=f) <= width:
                cur = t
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def dashed_rect(d, box, color, width=3, dash=14):
    x0, y0, x1, y1 = box
    for x in range(x0, x1, dash * 2):
        d.line([(x, y0), (min(x + dash, x1), y0)], fill=color, width=width)
        d.line([(x, y1), (min(x + dash, x1), y1)], fill=color, width=width)
    for y in range(y0, y1, dash * 2):
        d.line([(x0, y), (x0, min(y + dash, y1))], fill=color, width=width)
        d.line([(x1, y), (x1, min(y + dash, y1))], fill=color, width=width)


def box(d, xy, w, h, title, body='', kind='sistema', tag=None):
    x, y = xy
    fill = C[kind]
    d.rectangle([x, y, x + w, y + h], fill=fill)
    if kind == 'futuro':
        dashed_rect(d, (x, y, x + w, y + h), C['gris'])
    else:
        d.rectangle([x, y, x + w, y + h], outline=C['rojo'] if kind == 'bloqueado' else C['borde'], width=3)
    ft, fb = font(30, True), font(25)
    ty = y + 14
    for ln in wrap(d, title, ft, w - 30):
        d.text((x + 16, ty), ln, font=ft, fill=C['texto'])
        ty += 36
    for ln in wrap(d, body, fb, w - 30):
        d.text((x + 16, ty), ln, font=fb, fill=C['texto'])
        ty += 31
    if tag:
        tf = font(22, True)
        tw = d.textlength(tag, font=tf)
        d.rectangle([x + w - tw - 26, y - 16, x + w - 6, y + 14], fill='white',
                    outline=C['rojo'] if kind == 'bloqueado' else C['borde'], width=2)
        d.text((x + w - tw - 16, y - 13), tag, font=tf, fill=C['rojo'] if kind == 'bloqueado' else C['borde'])
    return (x, y, x + w, y + h)


def arrow(d, p0, p1, color=None, dashed=False, label=None, label_at=None):
    color = color or C['flecha']
    (x0, y0), (x1, y1) = p0, p1
    if dashed:
        n = max(1, int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 // 24))
        for i in range(0, n, 2):
            a, b = i / n, min(1, (i + 1) / n)
            d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)], fill=color,
                   width=4)
    else:
        d.line([p0, p1], fill=color, width=4)
    import math
    ang = math.atan2(y1 - y0, x1 - x0)
    for s in (0.45, -0.45):
        d.line([p1, (x1 - 26 * math.cos(ang - s), y1 - 26 * math.sin(ang - s))], fill=color, width=4)
    if label:
        f = font(23)
        d.text(label_at or ((x0 + x1) / 2 + 12, (y0 + y1) / 2 - 14), label, font=f, fill=color)


def legend(d, x, y):
    items = [('humano', 'Acción humana (RR. HH., evaluador, aprobador)'),
             ('sistema', 'Regla determinista propuesta (alcance B, requiere G0)'),
             ('existente', 'Existente en v1.1 (RF-21/RF-22, RF-23, RF-29)'),
             ('futuro', 'Futuro: solo con G0 completa y ADR adicional'),
             ('bloqueado', 'Bloqueado en este ciclo')]
    f = font(24)
    for i, (k, t) in enumerate(items):
        yy = y + i * 40
        d.rectangle([x, yy, x + 46, yy + 28], fill=C[k])
        if k == 'futuro':
            dashed_rect(d, (x, yy, x + 46, yy + 28), C['gris'], width=2, dash=6)
        else:
            d.rectangle([x, yy, x + 46, yy + 28], outline=C['rojo'] if k == 'bloqueado' else C['borde'], width=2)
        d.text((x + 60, yy), t, font=f, fill=C['texto'])


def title(d, text, sub, w):
    d.text((60, 40), text, font=font(40, True), fill=C['texto'])
    d.text((60, 96), sub, font=font(25), fill=C['gris'])
    d.line([(60, 140), (w - 60, 140)], fill=C['borde'], width=2)


def flujo():
    W, H = 2400, 2420
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)
    title(d, 'F33-01 — Flujo funcional del motor (diseño; nada implementado)',
          'Apoyo del sistema ≠ decisión final humana (RF-23). Ningún paso asigna niveles, puntúa ni recomienda personas.', W)
    X, BW = 120, 1250
    steps = [
        ('humano', 'P1 · Configurar la vacante', 'Perfil, competencias (catálogo versionado), criterios, pesos (A-06), '
         'preguntas estructuradas y rúbrica BARS. Se congela al publicar (A-07).', 'RF-05/06 · CU-04/05'),
        ('humano', 'P2 · Reunir evidencia del candidato', 'CV privado (C15), documentos, pruebas, formularios y notas '
         'del evaluador. Audio: por defecto no se graba.', 'RF-09/19'),
        ('humano', 'P3 · Registrar evidencia estructurada', 'El evaluador cita el fragmento y su fuente (documento, '
         'página, pregunta) y lo vincula a un criterio.', 'propuesto'),
        ('humano', 'P4 · Asignar nivel observado', 'Nivel BARS + justificación contrastiva + suficiencia de la '
         'evidencia (suficiente / parcial / insuficiente). Calificación independiente.', 'RF-19 extendido'),
        ('sistema', 'P5 · Verificar el proceso', 'Reglas deterministas: evidencia faltante, nivel sin justificación, '
         'discrepancia entre evaluadores (ICC), pregunta omitida, versión cambiada.', 'propuesto'),
        ('existente', 'P6 · Comparación estructurada', 'Ranking RF-21 por suma ponderada (A-24), sin desempate '
         'automático (A-26), con desglose por criterio y alertas del proceso.', 'RF-20/21/22'),
        ('humano', 'P7 · Decisión final humana', 'El Aprobador / Dirección decide con confirmación explícita y '
         'justificación; auditoría de solo inserción.', 'RF-23 · ADR-002'),
    ]
    y, H_BOX, GAP = 200, 205, 85
    boxes = []
    for kind, t, b, tag in steps:
        boxes.append(box(d, (X, y), BW, H_BOX, t, b, kind, tag))
        y += H_BOX + GAP
    for a, b in zip(boxes, boxes[1:]):
        arrow(d, ((a[0] + a[2]) // 2, a[3]), ((b[0] + b[2]) // 2, b[1] - 4))
    # Columna derecha. Arriba lo bloqueado (D). En medio, la cadena FUTURA de la alternativa C, enganchada DESPUÉS
    # de P4: localizador → revisión y confirmación humana → ayuda visible (solo fragmentos confirmados). Abajo, lo
    # prohibido sin excepción.
    RX, RW = 1560, 740
    box(d, (RX, boxes[1][1]), RW, 205, 'Scoring / recomendación (D)',
        'Nivel sugerido, puntaje o candidato recomendado por IA. Contradice ADR-001, contrato 4 y OUT-04/05.',
        'bloqueado', 'BLOQUEADA')
    loc = box(d, (RX, boxes[3][1]), RW, 170, 'C1 · Localizador documental',
              'Tras registrar el resultado (P4) sugiere fragmentos: quedan pendientes y no son visibles.',
              'futuro', 'FUTURA · G0 completa')
    conf = box(d, (RX, loc[3] + 50), RW, 150, 'C2 · Revisión y confirmación humana',
               'El evaluador confirma o rechaza cada fragmento.', 'futuro', 'FUTURA')
    vis = box(d, (RX, conf[3] + 50), RW, 170, 'C3 · Ayuda visible (solo confirmados)',
              'Anotaciones complementarias; no cambian nivel, puntaje ni resultado.', 'futuro', 'FUTURA')
    arrow(d, (boxes[3][2] + 4, (boxes[3][1] + boxes[3][3]) // 2), (loc[0] - 4, (loc[1] + loc[3]) // 2), C['gris'],
          True, 'después de P4', (boxes[3][2] + 20, boxes[3][1] + 28))
    cx = (loc[0] + loc[2]) // 2
    arrow(d, (cx, loc[3]), (cx, conf[1] - 4), C['gris'])
    arrow(d, (cx, conf[3]), (cx, vis[1] - 4), C['gris'])
    arrow(d, (vis[0] - 4, (vis[1] + vis[3]) // 2), (boxes[5][2] + 4, boxes[5][1] + 40), C['gris'], True,
          'comparación', (boxes[5][2] + 16, boxes[5][1] + 85))
    pro = box(d, (RX, vis[3] + 60), RW, 230, 'Inferencias prohibidas',
              'Emociones, personalidad, honestidad, inteligencia, estrés, liderazgo, salud mental o idoneidad desde '
              'rostro, voz o apariencia; prosodia, acento, biometría.', 'bloqueado', 'PROHIBIDA')
    legend(d, RX, pro[3] + 40)
    return im


def arquitectura():
    W, H = 2600, 1830
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)
    title(d, 'F33-02 — Arquitectura funcional (diseño; nada implementado)',
          'Laravel sigue siendo el sistema de registro. El servicio futuro es opcional, sin estado y sin acceso a la base '
          'de datos.', W)
    # Monolito Laravel
    d.rectangle([80, 190, 1500, 1500], outline=C['borde'], width=4)
    d.text((110, 205), 'Monolito Laravel (sistema de registro; organization_id, Policies, scope global)',
           font=font(28, True), fill=C['texto'])
    b1 = box(d, (130, 280), 620, 250, 'C05 · Vacante, criterios y rúbrica', 'Versiones congeladas: criteria_version, '
             'rubric_version.', 'existente', 'existente + propuesto')
    b2 = box(d, (830, 280), 620, 250, 'Módulo de evidencia (propuesto)', 'Evidencia por criterio, nivel humano, '
             'justificación, suficiencia, provenance y anotaciones complementarias. Futuro C: fragmentos pendientes '
             '→ confirmación humana → visibles.', 'sistema', 'alcance B')
    b3 = box(d, (130, 620), 620, 250, 'Reglas de proceso (propuesto)', 'Deterministas, en Laravel, síncronas; sin '
             'servicio externo ni ML.', 'sistema', 'alcance B')
    b4 = box(d, (830, 620), 620, 250, 'C09 · Ranking RF-21 y comparación', 'Suma ponderada de los puntajes que '
             'registran los evaluadores humanos; desglose y alertas.', 'existente', 'existente')
    b5 = box(d, (130, 960), 620, 250, 'C13 · Auditoría + analysis_run', 'analysis_run inmutable + '
             'analysis_run_events (solo inserción); hashes y versiones, sin texto de entrada ni PII.', 'existente',
             'existente + propuesto')
    b6 = box(d, (830, 960), 620, 250, 'C10 · Decisión final humana', 'RF-23: confirmación y justificación del '
             'Aprobador.', 'humano', 'RF-23')
    b7 = box(d, (130, 1290), 1320, 170, 'C16 · Cola (Redis existente): job idempotente', 'Solo para la alternativa C '
             'futura. Idempotency-Key = analysis_run_id; timeout, reintentos acotados, circuit breaker.', 'futuro',
             'FUTURA')
    arrow(d, (750, 405), (826, 405))
    arrow(d, (1140, 530), (1140, 616))
    arrow(d, (440, 530), (440, 616))
    arrow(d, (750, 745), (826, 745))
    arrow(d, (1140, 870), (1140, 956))
    arrow(d, (440, 870), (440, 956), label='eventos')
    # Servicio futuro
    s = box(d, (1680, 600), 820, 360, 'Servicio de asistencia documental', 'FUTURO y opcional. Sin estado, sin BD, '
            'sin conocimiento del dominio. Recibe un token técnico pseudónimo y texto minimizado (sin nombre, DNI, '
            'correo ni foto). Devuelve referencias a fragmentos y su versión; nunca niveles, puntajes ni candidatos.',
            'futuro', 'FUTURA · G0 completa + ADR')
    arrow(d, (1450, 1375), (1675, 900), C['gris'], True, 'petición REST', (1700, 1060))
    arrow(d, (1675, 700), (1455, 450), C['gris'], True, 'pendiente', (1505, 395))
    r = box(d, (1680, 1150), 820, 230, 'C17 · Riesgo operacional RF-29 (existente)', 'Solo el proceso: 15 contadores '
            'enteros, sin IDs ni PII; lejos del ranking y de la decisión.', 'existente', 'EXPERIMENTAL')
    blo = box(d, (1680, 230), 820, 250, 'Scoring / recomendación de personas', 'No existe ni se diseña en este ciclo '
              '(ADR-001, ADR-005).', 'bloqueado', 'BLOQUEADA')
    legend(d, 120, 1590)
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (('F33-01_flujo_funcional.png', flujo), ('F33-02_arquitectura_funcional.png', arquitectura)):
        fn().save(os.path.join(OUT, name), optimize=True)
        print('escrito', name)


if __name__ == '__main__':
    main()
