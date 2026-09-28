"""Borradores visuales (PNG) de flujo, BPMN y casos de uso, dibujados con Pillow.

Son borradores de revisión para la auditoría F27C. No son modelos de PowerDesigner ni los
sustituyen: cada imagen lleva la marca «BORRADOR» y la formalización queda en
POWERDESIGNER_WORKLIST.md.
"""
import math
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = 'C:/Windows/Fonts/'


def font(size, bold=False, italic=False):
    name = 'arialbd.ttf' if bold else ('ariali.ttf' if italic else 'arial.ttf')
    return ImageFont.truetype(FONT_DIR + name, size)


INK = (33, 37, 41)
MUTED = (110, 117, 125)
LANE_BG = [(247, 249, 252), (238, 243, 250)]
TASK_FILL = (255, 255, 255)
TASK_LINE = (31, 78, 121)
SYS_FILL = (232, 244, 236)
SYS_LINE = (46, 125, 50)
FUT = (150, 150, 150)
GATE_FILL = (255, 248, 220)
WARN = (176, 0, 32)


def wrap(draw, text, fnt, width):
    out = []
    for para in text.split('\n'):
        words, line = para.split(' '), ''
        for w in words:
            t = (line + ' ' + w).strip()
            if draw.textlength(t, font=fnt) <= width:
                line = t
            else:
                if line:
                    out.append(line)
                line = w
        out.append(line)
    return out


def text_block(draw, cx, cy, text, fnt, width, fill=INK, spacing=4):
    lines = wrap(draw, text, fnt, width)
    lh = fnt.size + spacing
    y = cy - lh * len(lines) / 2 + spacing / 2
    for ln in lines:
        w = draw.textlength(ln, font=fnt)
        draw.text((cx - w / 2, y), ln, font=fnt, fill=fill)
        y += lh


def arrowhead(draw, p0, p1, color, size=12, open_=False):
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    a = (p1[0] - size * math.cos(ang - 0.4), p1[1] - size * math.sin(ang - 0.4))
    b = (p1[0] - size * math.cos(ang + 0.4), p1[1] - size * math.sin(ang + 0.4))
    if open_:
        draw.line([a, p1, b], fill=color, width=2)
    else:
        draw.polygon([p1, a, b], fill=color)


def dashed(draw, pts, color, width=2, dash=10, gap=7):
    for p0, p1 in zip(pts, pts[1:]):
        L = math.dist(p0, p1)
        if L == 0:
            continue
        dx, dy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        d = 0
        while d < L:
            e = min(d + dash, L)
            draw.line([(p0[0] + dx * d, p0[1] + dy * d), (p0[0] + dx * e, p0[1] + dy * e)], fill=color, width=width)
            d = e + gap


class Swimlanes:
    """Diagrama con carriles verticales (columnas) y flujo de arriba abajo.

    lanes: lista de (pool, nombre del carril). nodes: id -> dict(kind, lane, row, label, style).
    kinds: start, end, task, gateway, terminator, link. edges: dict(src, dst, label, kind, via).
    """

    TOP, LEFT = 176, 30

    def __init__(self, title, lanes, subtitle='', show_lanes=True, CW=300, RH=125, TW=252, TH=92, FS=19):
        self.title, self.subtitle, self.lanes, self.show_lanes = title, subtitle, lanes, show_lanes
        self.CW, self.RH, self.TW, self.TH, self.FS = CW, RH, TW, TH, FS
        if not show_lanes:
            self.TOP = 112
        self.nodes, self.edges = {}, []
        self.badges = {}
        self.groups = []

    def group(self, lane0, lane1, row0, row1, label, style='subprocess'):
        """Contenedor de subproceso expandido (o grupo transversal) detrás de los nodos."""
        self.groups.append((lane0, lane1, row0, row1, label, style))

    def node(self, nid, kind, lane, row, label='', style='normal', off=0):
        self.nodes[nid] = dict(kind=kind, lane=lane, row=row, label=label, style=style, off=off)

    def edge(self, src, dst, label='', kind='seq', side=None, lpos=None):
        self.edges.append(dict(src=src, dst=dst, label=label, kind=kind, side=side, lpos=lpos))

    def _center(self, n):
        return (self.LEFT + n['lane'] * self.CW + self.CW / 2 + n['off'], self.TOP + n['row'] * self.RH + self.RH / 2)

    def _bbox(self, n):
        cx, cy = self._center(n)
        k = n['kind']
        if k in ('task', 'terminator'):
            return cx - self.TW / 2, cy - self.TH / 2, cx + self.TW / 2, cy + self.TH / 2
        if k == 'gateway':
            return cx - 38, cy - 38, cx + 38, cy + 38
        if k == 'bnd':
            return cx, cy, cx, cy
        return cx - 24, cy - 24, cx + 24, cy + 24

    def render(self, path, note=''):
        rows = max([n['row'] for n in self.nodes.values()] + [g[3] for g in self.groups]) + 1
        W = self.LEFT * 2 + self.CW * len(self.lanes) + 40
        H = self.TOP + rows * self.RH + 90
        img = Image.new('RGB', (int(W), int(H)), 'white')
        d = ImageDraw.Draw(img)
        d.text((self.LEFT, 14), self.title, font=font(26, bold=True), fill=INK)
        d.text((self.LEFT, 48), self.subtitle, font=font(17, italic=True), fill=MUTED)
        # Marca de borrador
        mark = 'BORRADOR DE REVISIÓN — no es el modelo formal de PowerDesigner'
        d.text((self.LEFT, 72), mark, font=font(16, bold=True), fill=WARN)
        if self.show_lanes:
            # Pools
            pools = []
            for i, (pool, _) in enumerate(self.lanes):
                if pools and pools[-1][0] == pool:
                    pools[-1][2] = i
                else:
                    pools.append([pool, i, i])
            for pool, a, b in pools:
                x0, x1 = self.LEFT + a * self.CW, self.LEFT + (b + 1) * self.CW
                d.rectangle([x0, 104, x1, 134], fill=(214, 226, 243), outline=TASK_LINE, width=2)
                text_block(d, (x0 + x1) / 2, 119, pool, font(17, bold=True), x1 - x0 - 10)
            for i, (_, lane) in enumerate(self.lanes):
                x0 = self.LEFT + i * self.CW
                d.rectangle([x0, 134, x0 + self.CW, H - 60], fill=LANE_BG[i % 2], outline=(180, 190, 205), width=1)
                d.rectangle([x0, 134, x0 + self.CW, self.TOP - 4], fill=(230, 236, 245), outline=(180, 190, 205))
                text_block(d, x0 + self.CW / 2, (134 + self.TOP - 4) / 2, lane, font(16, bold=True), self.CW - 12)
            for pool, a, b in pools:
                x0, x1 = self.LEFT + a * self.CW, self.LEFT + (b + 1) * self.CW
                d.rectangle([x0, 104, x1, H - 60], outline=TASK_LINE, width=3)
        # Aristas primero
        for l0, l1, r0, r1, label, style in self.groups:
            x0 = self.LEFT + l0 * self.CW + 8
            x1 = self.LEFT + (l1 + 1) * self.CW - 8
            y0 = self.TOP + r0 * self.RH + 4
            y1 = self.TOP + (r1 + 1) * self.RH - 4
            col = {'transversal': (46, 125, 50), 'future': (130, 130, 130)}.get(style, (120, 80, 160))
            fill = {'transversal': (244, 250, 244), 'future': (246, 246, 246)}.get(style, (250, 246, 255))
            d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=fill)
            dashed(d, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], col, width=3, dash=14, gap=6)
            fl = font(self.FS - 2, bold=True)
            yy = y0 + 6
            for ln in wrap(d, label, fl, x1 - x0 - 24):
                d.text((x0 + 12, yy), ln, font=fl, fill=col)
                yy += self.FS
            if style == 'subprocess':
                mx = (x0 + x1) / 2
                for dx in (-8, 0, 8):
                    d.line([(mx + dx, y1 - 26), (mx + dx, y1 - 8)], fill=col, width=3)
        gutter_used = {}
        self._labels = []
        for e in self.edges:
            self._draw_edge(d, e, gutter_used)
        for nid, n in self.nodes.items():
            self._draw_node(d, n)
        for lx, ly, text, fut in self._labels:
            fx = font(14, bold=True)
            w = d.textlength(text, font=fx)
            d.rectangle([lx - 2, ly, lx + w + 2, ly + 17], fill='white')
            d.text((lx, ly), text, font=fx, fill=WARN if fut else INK)
        for nid, text in self.badges.items():
            x0, y0, x1, y1 = self._bbox(self.nodes[nid])
            fb = font(self.FS - 2, bold=True)
            w = d.textlength(text, font=fb)
            d.rounded_rectangle([x1 - w - 14, y0 - 14, x1 + 2, y0 + self.FS - 6], radius=8, fill=WARN)
            d.text((x1 - w - 6, y0 - 13), text, font=fb, fill='white')
        if note:
            d.text((self.LEFT, H - 48), note, font=font(15, italic=True), fill=MUTED)
        img.save(path, optimize=True)
        return img.size

    def _draw_node(self, d, n):
        x0, y0, x1, y1 = self._bbox(n)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        fut = n['style'] == 'future'
        sysn = n['style'] == 'system'
        line = FUT if fut else (SYS_LINE if sysn else TASK_LINE)
        k = n['kind']
        if k == 'bnd':
            return
        if k == 'task':
            d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=(245, 245, 245) if fut else (SYS_FILL if sysn else TASK_FILL),
                                outline=line, width=3)
            if fut:
                dashed(d, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], FUT, width=3)
            text_block(d, cx, cy, n['label'], font(self.FS), self.TW - 16, fill=FUT if fut else INK)
        elif k == 'terminator':
            d.rounded_rectangle([x0, y0 + 12, x1, y1 - 12], radius=28, fill=(240, 244, 250), outline=line, width=3)
            text_block(d, cx, cy, n['label'], font(self.FS, bold=True), self.TW - 20)
        elif k == 'gateway':
            pts = [(cx, y0), (x1, cy), (cx, y1), (x0, cy)]
            d.polygon(pts, fill=GATE_FILL, outline=FUT if fut else (168, 120, 0))
            d.line(pts + [pts[0]], fill=FUT if fut else (168, 120, 0), width=3)
            d.text((cx - 9, cy - 16), 'X', font=font(26, bold=True), fill=(168, 120, 0))
            lab = wrap(d, n['label'], font(self.FS - 3, bold=True), 190)
            yy = y0 + 4 - self.FS * len(lab)
            for ln in lab:
                w = d.textlength(ln, font=font(self.FS - 3, bold=True))
                d.rectangle([x1 + 4, yy, x1 + 8 + w, yy + self.FS], fill='white')
                d.text((x1 + 6, yy), ln, font=font(self.FS - 3, bold=True), fill=INK)
                yy += self.FS
        elif k in ('start', 'end', 'link', 'inter'):
            w = 3 if k in ('start', 'inter', 'link') else 7
            fill = {'start': (220, 245, 225), 'end': (250, 225, 225)}.get(k, (235, 235, 250))
            d.ellipse([x0, y0, x1, y1], fill=fill, outline=INK, width=w)
            if k in ('inter', 'link'):
                d.ellipse([x0 + 6, y0 + 6, x1 - 6, y1 - 6], outline=INK, width=2)
            if k == 'link':
                d.polygon([(cx - 7, cy - 9), (cx + 9, cy), (cx - 7, cy + 9)], fill=INK)
            if k == 'inter':
                d.rectangle([cx - 10, cy - 7, cx + 10, cy + 7], outline=INK, width=2)
                d.line([(cx - 10, cy - 7), (cx, cy + 1), (cx + 10, cy - 7)], fill=INK, width=2)
            f3 = font(self.FS - 3)
            if k in ('inter', 'end'):
                lab = wrap(d, n['label'], f3, self.CW - 30)
                yy = y1 + 4
                for ln in lab:
                    d.text((cx - d.textlength(ln, font=f3) / 2, yy), ln, font=f3, fill=INK)
                    yy += self.FS - 1
            else:
                lab = wrap(d, n['label'], f3, self.CW / 2 + 40 - n['off'])
                yy = cy - (self.FS - 1) * len(lab) / 2
                for ln in lab:
                    d.text((x1 + 8, yy), ln, font=f3, fill=INK)
                    yy += self.FS - 1

    def _anchor(self, n, side):
        x0, y0, x1, y1 = self._bbox(n)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        return {'top': (cx, y0), 'bottom': (cx, y1), 'left': (x0, cy), 'right': (x1, cy)}[side]

    def _draw_edge(self, d, e, gutter_used):
        s, t = self.nodes[e['src']], self.nodes[e['dst']]
        color = FUT if (e['kind'] == 'future') else (MUTED if e['kind'] == 'msg' else INK)
        if e['side'] == 'lr':
            p0, p1 = self._anchor(s, 'left'), self._anchor(t, 'right')
            gx = p1[0] + 40
            pts = [p0, (gx, p0[1]), (gx, p1[1]), p1]
        elif e['side'] == 'lgutter':
            lane = min(s['lane'], t['lane'])
            k = gutter_used.get(('l', lane), 0)
            gutter_used[('l', lane)] = k + 1
            gx = self.LEFT + lane * self.CW + 10 + 9 * k
            p0, p1 = self._anchor(s, 'left'), self._anchor(t, 'left')
            pts = [p0, (gx, p0[1]), (gx, p1[1]), p1]
        elif e['side'] == 'gutter':
            lane = max(s['lane'], t['lane'])
            k = gutter_used.get(lane, 0)
            gutter_used[lane] = k + 1
            gx = self.LEFT + (lane + 1) * self.CW - 10 - 9 * k
            p0, p1 = self._anchor(s, 'right'), self._anchor(t, 'right')
            pts = [p0, (gx, p0[1]), (gx, p1[1]), p1]
        elif t['row'] > s['row']:
            if s['lane'] == t['lane'] and e['side'] is None:
                p0, p1 = self._anchor(s, 'bottom'), self._anchor(t, 'top')
                if abs(p0[0] - p1[0]) < 2:
                    pts = [p0, p1]
                else:
                    ym = p1[1] - 18
                    pts = [p0, (p0[0], ym), (p1[0], ym), p1]
            elif s['kind'] == 'gateway' or e['side']:
                side = e['side'] or ('right' if t['lane'] > s['lane'] else 'left')
                p0 = self._anchor(s, side)
                p1 = self._anchor(t, 'top')
                pts = [p0, (p1[0], p0[1]), p1]
            else:
                p0 = self._anchor(s, 'bottom')
                p1 = self._anchor(t, 'top')
                ym = p1[1] - 22
                pts = [p0, (p0[0], ym), (p1[0], ym), p1]
        elif t['row'] == s['row']:
            side = 'right' if t['lane'] > s['lane'] else 'left'
            other = 'left' if side == 'right' else 'right'
            pts = [self._anchor(s, side), self._anchor(t, other)]
        else:
            lane = max(s['lane'], t['lane'])
            key = lane
            k = gutter_used.get(key, 0)
            gutter_used[key] = k + 1
            gx = self.LEFT + (lane + 1) * self.CW - 14 - 10 * k
            p0 = self._anchor(s, 'right')
            p1 = self._anchor(t, 'right')
            pts = [p0, (gx, p0[1]), (gx, p1[1]), p1]
        if e['kind'] in ('msg', 'future'):
            dashed(d, pts, color, width=2)
            if e['kind'] == 'msg':
                d.ellipse([pts[0][0] - 5, pts[0][1] - 5, pts[0][0] + 5, pts[0][1] + 5], outline=color, width=2, fill='white')
            arrowhead(d, pts[-2], pts[-1], color, open_=e['kind'] == 'msg')
        else:
            d.line(pts, fill=color, width=3, joint='curve')
            arrowhead(d, pts[-2], pts[-1], color)
        if e['label']:
            fx = font(14, bold=True)
            if e['side'] in ('gutter', 'lgutter'):
                p0, p1 = pts[1], pts[2]
                w = d.textlength(e['label'], font=fx)
                pos = e['lpos'] or ('vr' if e['side'] == 'lgutter' else 'vl')
                lx = p0[0] + 6 if pos == 'vr' else p0[0] - w - 6
                ly = (p0[1] + p1[1]) / 2 - 8
            else:
                p0, p1 = pts[0], pts[1]
                lx = (p0[0] + p1[0]) / 2 + 6
                ly = (p0[1] + p1[1]) / 2 - 20
            self._labels.append((lx, ly, e['label'], e['kind'] == 'future'))


def use_case_diagram(path, title, subtitle, actors_left, actors_right, cases, links, includes, note=''):
    """actors_*: [(id, nombre)]; cases: [(id, nombre, columna 0|1|2, fila)]; links: [(actor, cu)];
    includes: [(base, incluido, estereotipo)]. El actor se ubica a la altura media de sus casos."""
    RH, ew, eh = 108, 330, 76
    rows = max(c[3] for c in cases) + 1
    W, H = 1900, int(190 + RH * rows + 90)
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    d.text((40, 14), title, font=font(28, bold=True), fill=INK)
    d.text((40, 50), subtitle, font=font(17, italic=True), fill=MUTED)
    d.text((40, 76), 'BORRADOR DE REVISIÓN — no es el modelo formal de PowerDesigner', font=font(16, bold=True), fill=WARN)
    bx0, bx1, by0, by1 = 390, W - 390, 110, H - 60
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=18, outline=TASK_LINE, width=3, fill=(250, 252, 255))
    d.text((bx0 + 16, by0 + 10), 'Plataforma SaaS de reclutamiento, evaluación y selección — línea base RF-01 a RF-27',
           font=font(17, bold=True), fill=TASK_LINE)
    colx = {0: bx0 + 30 + ew / 2, 1: (bx0 + bx1) / 2 - 70, 2: bx1 - 30 - ew / 2}
    pos = {cid: (colx[col], by0 + 90 + row * RH) for cid, name, col, row in cases}
    apos = {}
    for side, lst in ((0, actors_left), (1, actors_right)):
        for aid, name in lst:
            ys = [pos[c][1] for a, c in links if a == aid]
            apos[aid] = (170 if side == 0 else W - 170, sum(ys) / len(ys), side, name)
    for a, c in links:
        ax, ay, side, _ = apos[a]
        cx, cy = pos[c]
        tx = cx - ew / 2 if ax < cx else cx + ew / 2
        d.line([(ax + (38 if side == 0 else -38), ay - 12), (tx, cy)], fill=(95, 105, 120), width=2)
    for base, inc, st in includes:
        (x0, y0), (x1, y1) = pos[base], pos[inc]
        p0 = (x0 + (ew / 2 if x1 > x0 else -ew / 2), y0)
        p1 = (x1 + (-ew / 2 + 40 if x1 > x0 else ew / 2 - 40), y1 + (-eh / 2 + 6 if y1 > y0 else eh / 2 - 6))
        dashed(d, [p0, p1], (150, 90, 0), width=2)
        arrowhead(d, p0, p1, (150, 90, 0), open_=True)
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        lab = f'«{st}»'
        w = d.textlength(lab, font=font(14, italic=True))
        d.rectangle([mx - w / 2 - 3, my - 10, mx + w / 2 + 3, my + 10], fill='white')
        d.text((mx - w / 2, my - 9), lab, font=font(14, italic=True), fill=(150, 90, 0))
    for cid, name, col, row in cases:
        cx, cy = pos[cid]
        d.ellipse([cx - ew / 2, cy - eh / 2, cx + ew / 2, cy + eh / 2], fill='white', outline=TASK_LINE, width=3)
        text_block(d, cx, cy, f'{cid}' + chr(10) + f'{name}', font(16), ew - 64)
    for aid, (ax, ay, side, name) in apos.items():
        d.ellipse([ax - 16, ay - 70, ax + 16, ay - 38], outline=INK, width=3, fill='white')
        d.line([(ax, ay - 38), (ax, ay + 5)], fill=INK, width=3)
        d.line([(ax - 30, ay - 22), (ax + 30, ay - 22)], fill=INK, width=3)
        d.line([(ax, ay + 5), (ax - 22, ay + 40)], fill=INK, width=3)
        d.line([(ax, ay + 5), (ax + 22, ay + 40)], fill=INK, width=3)
        text_block(d, ax, ay + 70, f'{aid}' + chr(10) + f'{name}', font(16, bold=True), 300)
    if note:
        d.text((40, H - 44), note, font=font(15, italic=True), fill=MUTED)
    img.save(path, optimize=True)
    return img.size


def block_diagram(path, title, subtitle, groups, boxes, arrows, notes=(), size=(1900, 1700), anchors=None):
    """Diagrama conceptual de bloques.
    groups: [(x, y, w, h, etiqueta, estilo)]; boxes: {id: (x, y, w, h, texto, estilo)};
    arrows: [(origen, destino, etiqueta, estilo)] con estilo 'solid' | 'dashed'; notes: [(x, y, w, texto)]."""
    W, H = size
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    d.text((40, 14), title, font=font(28, bold=True), fill=INK)
    d.text((40, 50), subtitle, font=font(17, italic=True), fill=MUTED)
    d.text((40, 76), 'BORRADOR DE REVISIÓN — no es el modelo formal de PowerDesigner', font=font(16, bold=True), fill=WARN)
    palette = {
        'layer': ((244, 247, 252), (31, 78, 121)),
        'business': ((238, 244, 251), (31, 78, 121)),
        'transversal': ((240, 248, 240), (46, 125, 50)),
        'infra': ((246, 246, 246), (90, 90, 90)),
        'experimental': ((250, 246, 255), (120, 80, 160)),
        'actors': ((255, 250, 235), (168, 120, 0)),
    }
    for x, y, w, h, label, style in groups:
        fill, line = palette.get(style, palette['layer'])
        d.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=fill, outline=line, width=2)
        if style == 'experimental':
            dashed(d, [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], line, width=3)
        d.text((x + 14, y + 8), label, font=font(17, bold=True), fill=line)
    box_fill = {'normal': ('white', (31, 78, 121)), 'human': ((255, 243, 224), (191, 96, 0)),
                'transversal': ('white', (46, 125, 50)), 'infra': ('white', (90, 90, 90)),
                'experimental': ('white', (120, 80, 160)), 'actor': ((255, 250, 235), (168, 120, 0))}

    def anchor(b, side):
        x, y, w, h = b[:4]
        return {'top': (x + w / 2, y), 'bottom': (x + w / 2, y + h), 'left': (x, y + h / 2), 'right': (x + w, y + h / 2)}[side]

    labels = []
    targets = dict(anchors or {})
    targets.update(boxes)
    for arr in arrows:
        src, dst, label, style = arr[:4]
        via = arr[4] if len(arr) > 4 else None
        a, b = targets[src], targets[dst]
        ax0, ay0, aw, ah = a[:4]
        bx0, by0, bw, bh = b[:4]
        if by0 >= ay0 + ah:            # destino debajo
            p0, p1 = anchor(a, 'bottom'), anchor(b, 'top')
            ox = max(ax0, bx0) + (min(ax0 + aw, bx0 + bw) - max(ax0, bx0)) / 2
            if min(ax0 + aw, bx0 + bw) - max(ax0, bx0) > 20:
                pts = [(ox, p0[1]), (ox, p1[1])]
            else:
                ym = (p0[1] + p1[1]) / 2
                pts = [p0, (p0[0], ym), (p1[0], ym), p1]
        elif ay0 >= by0 + bh:          # destino arriba
            p0, p1 = anchor(a, 'top'), anchor(b, 'bottom')
            ox = max(ax0, bx0) + (min(ax0 + aw, bx0 + bw) - max(ax0, bx0)) / 2
            if min(ax0 + aw, bx0 + bw) - max(ax0, bx0) > 20:
                pts = [(ox, p0[1]), (ox, p1[1])]
            else:
                ym = (p0[1] + p1[1]) / 2
                pts = [p0, (p0[0], ym), (p1[0], ym), p1]
        elif bx0 >= ax0 + aw:          # a la derecha
            p0, p1 = anchor(a, 'right'), anchor(b, 'left')
            xm = (p0[0] + p1[0]) / 2
            pts = [p0, (xm, p0[1]), (xm, p1[1]), p1]
        else:                          # a la izquierda
            p0, p1 = anchor(a, 'left'), anchor(b, 'right')
            xm = (p0[0] + p1[0]) / 2
            pts = [p0, (xm, p0[1]), (xm, p1[1]), p1]
        if via:
            pts = list(via)
        col = (120, 80, 160) if style == 'dashed' else (60, 70, 85)
        if style == 'dashed':
            dashed(d, pts, col, width=3)
            arrowhead(d, pts[-2], pts[-1], col, size=14, open_=True)
        else:
            d.line(pts, fill=col, width=3)
            arrowhead(d, pts[-2], pts[-1], col, size=14)
        if label:
            mx = (pts[len(pts) // 2 - 1][0] + pts[len(pts) // 2][0]) / 2 + 8
            my = (pts[len(pts) // 2 - 1][1] + pts[len(pts) // 2][1]) / 2 - 10
            labels.append((mx, my, label, col))
    for bid, (x, y, w, h, text, style) in boxes.items():
        fill, line = box_fill.get(style, box_fill['normal'])
        d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=fill, outline=line, width=3)
        if style == 'experimental':
            dashed(d, [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], line, width=3)
        text_block(d, x + w / 2, y + h / 2, text, font(17), w - 20)
    for mx, my, label, col in labels:
        f = font(14, bold=True)
        w = d.textlength(label, font=f)
        if mx + w > W - 8:
            mx = W - w - 16
        d.rectangle([mx - 3, my - 1, mx + w + 3, my + 17], fill='white')
        d.text((mx, my), label, font=f, fill=col)
    for x, y, w, text in notes:
        f = font(15, italic=True)
        lines = wrap(d, text, f, w - 20)
        h = 20 * len(lines) + 16
        d.rectangle([x, y, x + w, y + h], fill=(255, 252, 230), outline=(200, 170, 60))
        yy = y + 8
        for ln in lines:
            d.text((x + 10, yy), ln, font=f, fill=INK)
            yy += 20
    img.save(path, optimize=True)
    return img.size
