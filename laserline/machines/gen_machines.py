"""Схематичные изометрические станки Laserline: линейный стиль, группы для анимации.
Слои: base, cabinBack, sheet, cut, gantry(head), cabinFront, extra.
"""
import math, re, sys, json
C = math.cos(math.radians(30))
def P(x, y, z): return ((x - y) * C, (x + y) * .5 - z)

NAVY = '#072730'; PAPER = '#F8F9F9'; BLUE = '#5EA7BB'; LIME = '#E8FC5C'; GREY = '#798591'; ORANGE = '#FF860D'

class Layer:
    def __init__(s, sw=1.3): s.items = []; s.sw = sw
    def _f(s, pts): return " ".join("%.1f,%.1f" % P(*q) for q in pts)
    def box(s, x0, y0, z0, x1, y1, z1, stroke=NAVY, fill=PAPER, pleat=None, n=0, sw=None, name=None):
        sw = sw or s.sw; g = []
        def poly(p): return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="miter"/>' % (s._f(p), fill, stroke, sw)
        def ln(a, b): return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"/>' % (*P(*a), *P(*b), stroke, sw * .6)
        g.append(poly([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]))
        g.append(poly([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)]))
        g.append(poly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)]))
        for i in range(1, n):
            if pleat == 'x':
                x = x0 + (x1 - x0) * i / n; g += [ln((x, y0, z1), (x, y1, z1)), ln((x, y1, z0), (x, y1, z1))]
            if pleat == 'y':
                y = y0 + (y1 - y0) * i / n; g += [ln((x0, y, z1), (x1, y, z1)), ln((x1, y, z0), (x1, y, z1))]
        s.items.append(((x0 + x1) / 2 + (y0 + y1) / 2 + (z0 + z1) / 2, "".join(g)))
    def line(s, pts, stroke=NAVY, sw=None, depth=0, dash=None, cls=None, close=False, name=None, fill='none'):
        sw = sw or s.sw
        d = 'M' + ' L'.join("%.1f %.1f" % P(*q) for q in pts) + (' Z' if close else '')
        extra = (' stroke-dasharray="%s"' % dash if dash else '') + (' pathLength="1"' if cls in ('cut','cut2') else '') + (' class="%s"' % cls if cls else '') + (' id="%s"' % name if name else '')
        s.items.append((depth, '<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="miter"%s/>' % (d, fill, stroke, sw, extra)))
    def svg(s):
        s.items.sort(key=lambda t: t[0]); return "".join(g for _, g in s.items)

def offs(dx, dy): return ((dx - dy) * C, (dx + dy) * .5)

def machine(p, state='idle'):
    """p: dict L,W,kind,roof,pult,doors ; state: idle|hover (для Figma-вариантов)"""
    L, W, kind = p['L'], p['W'], p['kind']
    GX0 = int(L * .38); GX1 = GX0 + 26
    travel_x = (-int(L * .30), int(L * .40))
    hx = (-52, 52)
    CAB_X0, CAB_X1 = -14, L + 14
    CAB_Y0, CAB_Y1 = -40, W + 40
    CAB_Z = 122
    base = Layer(); sheet = Layer(1.1); cabB = Layer(1); gan = Layer(); cabF = Layer(1); extra = Layer()
    # основание + рельсы + стол
    base.box(0, 0, 0, L, W, 34); base.box(8, 8, 34, L - 8, W - 8, 38); base.box(14, 14, 38, L - 14, W - 14, 41)
    base.box(0, -14, 34, L, 0, 44); base.box(0, W, 34, L, W + 14, 44)
    nb = max(7, int(L / 33))
    half = L / 2
    for a, b in [(2, half - 2), (half + 2, L - 2)]:
        base.box(a, -14, 44, b, 0, 60, stroke=BLUE, fill='#E3EFF3', pleat='x', n=nb // 2 + 1)
        base.box(a, W, 44, b, W + 14, 60, stroke=BLUE, fill='#E3EFF3', pleat='x', n=nb // 2 + 1)
    # лист на столе
    sheet.box(18, 18, 41, L - 18, W - 18, 46, stroke=GREY, fill=PAPER, sw=1.1)
    # контур реза (оранжевый) на листе
    cx0, cy0 = L * .22, W * .24; cx1, cy1 = L * .62, W * .72
    cut = [(cx0, cy0, 46), (cx1, cy0, 46), (cx1, cy1, 46), (cx0 + 40, cy1, 46), (cx0, cy1 - 30, 46)]
    sheet.line(cut, stroke=ORANGE, sw=1.6, depth=1e6, close=True, cls='cut', name='cut')
    sheet.line([(cx1 + 30, W * .5, 46), (cx1 + 60, W * .5 + 10, 46), (cx1 + 60, W * .5 - 10, 46)], stroke=ORANGE, sw=1.6, depth=1e6, close=True, cls='cut2', name='cut2')
    # кабина: задние рёбра
    z0, z1 = 34, CAB_Z
    def post(x, y): return [(x, y, z0), (x, y, z1)]
    cabB.line(post(CAB_X0, CAB_Y0), stroke=GREY, sw=1); cabB.line(post(CAB_X1, CAB_Y0), stroke=GREY, sw=1); cabB.line(post(CAB_X0, CAB_Y1), stroke=GREY, sw=1)
    cabB.line([(CAB_X0, CAB_Y0, z1), (CAB_X1, CAB_Y0, z1)], stroke=GREY, sw=1)
    cabB.line([(CAB_X0, CAB_Y0, z1), (CAB_X0, CAB_Y1, z1)], stroke=GREY, sw=1)
    # портал: подвижная группа (двигается по X); голова — вложенная (по Y)
    gan.box(GX0 - 2, -24, 34, GX1 + 2, -2, 66); gan.box(GX0 - 2, W + 2, 34, GX1 + 2, W + 26, 66)
    gan.box(GX0, -24, 66, GX1, W + 26, 96)
    gan.box(GX1, -20, 70, GX1 + 14, W * .4, 92, stroke=NAVY, fill=LIME, pleat='y', n=8)
    gan.box(GX1, W * .6, 70, GX1 + 14, W + 22, 92, stroke=NAVY, fill=LIME, pleat='y', n=8)
    head = Layer()
    hy0 = W * .5 - 16
    head.box(GX1, hy0, 66, GX1 + 22, hy0 + 32, 100); head.box(GX1 + 6, hy0 + 10, 44, GX1 + 16, hy0 + 22, 66)
    head.line([(GX1 + 11, hy0 + 16, 44), (GX1 + 11, hy0 + 16, 36)], stroke=ORANGE, sw=1.8, depth=1e6, name='beam')
    # кабина: передние рёбра (прозрачное стекло, без заливки)
    brand = p.get('brand', '')
    ACC = {'Bystronic': LIME, 'Trumpf': BLUE, 'Bodor': ORANGE, 'HSG Laser': NAVY, "Han's Laser": GREY}.get(brand, LIME)
    cabF.line([(CAB_X1, CAB_Y0, z0), (CAB_X1, CAB_Y1, z0), (CAB_X0, CAB_Y1, z0)], stroke=GREY, sw=1)
    cabF.line(post(CAB_X1, CAB_Y1), stroke=GREY, sw=1.2); cabF.line(post(CAB_X1, CAB_Y0), stroke=GREY, sw=1.2); cabF.line(post(CAB_X0, CAB_Y1), stroke=GREY, sw=1.2)
    def quad(pts, fill, stroke=NAVY, sw=.9, op=1):
        d = 'M' + ' L'.join("%.1f %.1f" % P(*q) for q in pts) + ' Z'
        cabF.items.append((1e5, '<path d="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"/>' % (d, fill, op, stroke, sw)))
    roof = p.get('roof', 'flat')
    rf = [(CAB_X0, CAB_Y0, z1), (CAB_X1, CAB_Y0, z1), (CAB_X1, CAB_Y1, z1), (CAB_X0, CAB_Y1, z1)]
    if roof == 'slant':   # Trumpf: резкий скос крыши к оператору
        cabF.line([(CAB_X0, CAB_Y0, z1), (CAB_X1, CAB_Y0, z1), (CAB_X1, CAB_Y1, z1 - 38), (CAB_X0, CAB_Y1, z1 - 38)], stroke=NAVY, sw=1.3, close=True, depth=5)
        cabF.line([(CAB_X1, CAB_Y0, z1), (CAB_X1, CAB_Y1, z1 - 38)], stroke=NAVY, sw=1.3, depth=5)
        cabF.line([(CAB_X0, CAB_Y1, z1 - 38), (CAB_X0, CAB_Y1, z1 - 38)], stroke=NAVY, sw=1)
        cabF.line([(CAB_X1, CAB_Y1, z1 - 38), (CAB_X1, CAB_Y1, z1 - 56)], stroke=GREY, sw=1)
    elif roof == 'bevel':  # Bystronic: срезанная передняя кромка
        cabF.line(rf, stroke=NAVY, sw=1.3, close=True, depth=5)
        cabF.line([(CAB_X0, CAB_Y1 - 22, z1), (CAB_X1, CAB_Y1 - 22, z1)], stroke=NAVY, sw=1.1, depth=5)
        cabF.line([(CAB_X0, CAB_Y1, z1 - 22), (CAB_X1, CAB_Y1, z1 - 22)], stroke=NAVY, sw=1.1, depth=5)
        cabF.line([(CAB_X1, CAB_Y1 - 22, z1), (CAB_X1, CAB_Y1, z1 - 22)], stroke=NAVY, sw=1.1, depth=5)
    elif roof == 'barrel':  # Han's: арочная крыша
        cabF.line(rf, stroke=NAVY, sw=1.3, close=True, depth=5)
        mid = (CAB_Y0 + CAB_Y1) / 2
        cabF.line([(CAB_X1, CAB_Y0, z1), (CAB_X1, mid, z1 + 20), (CAB_X1, CAB_Y1, z1)], stroke=NAVY, sw=1.3, depth=5)
        cabF.line([(CAB_X0, mid, z1 + 20), (CAB_X1, mid, z1 + 20)], stroke=NAVY, sw=1.1, depth=5)
        cabF.line([(CAB_X0, CAB_Y0, z1), (CAB_X0, mid, z1 + 20), (CAB_X0, CAB_Y1, z1)], stroke=GREY, sw=1, depth=5)
    else:
        cabF.line(rf, stroke=NAVY, sw=1.3, close=True, depth=5)
    zt = z1 - (38 if roof == 'slant' else 0)  # верх лицевой грани
    # двери на лицевой (y=max) грани + блики
    n_doors = p.get('doors', 2)
    dw = (CAB_X1 - CAB_X0) / (n_doors + 1)
    for i in range(1, n_doors + 1):
        x = CAB_X0 + dw * i
        cabF.line([(x, CAB_Y1, z0), (x, CAB_Y1, zt)], stroke=GREY, sw=1, dash='3 3')
    cabF.line([(CAB_X0 + 14, CAB_Y1, z0 + 24), (CAB_X0 + 44, CAB_Y1, zt - 10)], stroke=BLUE, sw=1)
    cabF.line([(CAB_X0 + 28, CAB_Y1, z0 + 24), (CAB_X0 + 58, CAB_Y1, zt - 10)], stroke=BLUE, sw=1)
    # фирменная полоса цвета по низу лицевой грани
    quad([(CAB_X0, CAB_Y1, z0 + 2), (CAB_X1, CAB_Y1, z0 + 2), (CAB_X1, CAB_Y1, z0 + 14), (CAB_X0, CAB_Y1, z0 + 14)], ACC)
    # тёмный козырёк (GWEIKE)
    if brand == 'HSG Laser':
        quad([(CAB_X0, CAB_Y1, zt - 28), (CAB_X1, CAB_Y1, zt - 28), (CAB_X1, CAB_Y1, zt), (CAB_X0, CAB_Y1, zt)], NAVY, op=.85)
    # серая панель (Han's)
    if brand == "Han's Laser":
        quad([(CAB_X0, CAB_Y1, zt - 28), (CAB_X1, CAB_Y1, zt - 28), (CAB_X1, CAB_Y1, zt), (CAB_X0, CAB_Y1, zt)], GREY, op=.35)
    # табличка с названием бренда
    nm = {'Bystronic': 'BYSTRONIC', 'Trumpf': 'TRUMPF', 'Bodor': 'BODOR', 'HSG Laser': 'HSG LASER', "Han's Laser": "HAN'S LASER"}.get(brand, '')
    if nm:
        u0 = CAB_X0 + 8; tx = (0 - CAB_Y1) * C; ty = CAB_Y1 / 2 - (z0 + 44)
        cabF.items.append((2e5, '<g transform="matrix(%.3f .5 0 1 %.1f %.1f)"><text x="%d" y="0" font-family="IBM Plex Mono, monospace" font-weight="700" font-size="15" letter-spacing="1.2" fill="%s">%s</text></g>' % (C, tx, ty, u0, NAVY, nm)))
    # допы по типам
    if kind in ('A', 'C') and brand != 'Trumpf':
        # сменный стол: выезжает по +X за кабину
        ex = int(L * (.46 if kind == 'A' else .38))
        extra.box(CAB_X1 + 4, 10, 18, CAB_X1 + 4 + ex, W - 10, 30, stroke=NAVY)
        extra.box(CAB_X1 + 10, 18, 30, CAB_X1 + 4 + ex - 6, W - 18, 36, stroke=GREY, sw=1.1)
        extra.box(CAB_X1 + 4, 8, 0, CAB_X1 + 12, 16, 18); extra.box(CAB_X1 + 4 + ex - 8, W - 16, 0, CAB_X1 + 4 + ex, W - 8, 18)
    if brand == 'Trumpf' and kind != 'B':
        # Trumpf: загрузка листа спереди, стол выезжает к оператору (по +Y)
        ey = int(W * .55)
        extra.box(30, CAB_Y1 + 4, 18, L - 30, CAB_Y1 + 4 + ey, 30, stroke=NAVY)
        extra.box(38, CAB_Y1 + 10, 30, L - 38, CAB_Y1 + 4 + ey - 6, 36, stroke=GREY, sw=1.1)
    if brand == 'Bodor':
        # шкаф источника лазера: выше кабины, слева
        extra.box(CAB_X0 - 60, CAB_Y0 + 8, 34, CAB_X0 - 4, CAB_Y0 + 92, 150, stroke=NAVY)
        for k in (1, 2, 3):
            extra.box(CAB_X0 - 56, CAB_Y0 + 92 - 1, 34 + k * 26, CAB_X0 - 8, CAB_Y0 + 93, 34 + k * 26 + 2, stroke=GREY, sw=.8)
    if brand == 'Bystronic' and kind != 'B':
        # боковая стойка с экраном на качающемся кронштейне уже ниже; здесь шкаф управления у стола
        extra.box(CAB_X1 - 6, CAB_Y0 - 20, 0, CAB_X1 + 30, CAB_Y0 + 4, 70, stroke=NAVY)
    # пульт управления
    pult = p.get('pult', 'swing')
    if pult == 'swing':   # экран на кронштейне справа от кабины
        px, py = CAB_X1 - 10, CAB_Y1 + 22
        extra.box(px - 12, py, 0, px, py + 12, 78)
        extra.box(px - 40, py - 6, 78, px, py + 22, 100)
    elif pult == 'tall':  # высокая стойка слева (Han's)
        px, py = CAB_X0 + 40, CAB_Y1 + 24
        extra.box(px, py, 0, px + 16, py + 16, 100)
        extra.box(px - 14, py - 4, 100, px + 30, py + 22, 126)
    else:                  # низкий пульт-тумба слева
        px, py = CAB_X0 + 70, CAB_Y1 + 26
        extra.box(px, py, 0, px + 30, py + 24, 70); extra.box(px + 4, py + 2, 70, px + 26, py + 22, 94)
    # лампа статуса
    extra.box(CAB_X0 + 10, CAB_Y0 + 10, CAB_Z, CAB_X0 + 22, CAB_Y0 + 22, CAB_Z + 12, stroke=NAVY, fill=ACC)
    # сборка слоёв
    if state == 'hover':
        dx = travel_x[1] * .55; dy = hx[1] * .7
    else: dx = dy = 0
    gx, gy = offs(dx, 0); hdx, hdy = offs(0, dy)
    # зачем: группы. extra рисуем после кабины, но «сзади» (расширение) — перед base
    parts = []
    ext_items = extra.items
    # разделяем: расширение и пульт идут отдельно в порядке глубины
    g0=offs(travel_x[0],0); g1=offs(travel_x[1],0); h0=offs(0,hx[0]); h1=offs(0,hx[1])
    body = ('<g id="base">%s</g><g id="sheet">%s</g><g id="cabinBack">%s</g>'
            '<g id="gantry" style="--gx0:%.1fpx,%.1fpx;--gx1:%.1fpx,%.1fpx" transform="translate(%.1f %.1f)">%s<g id="head" style="--hy0:%.1fpx,%.1fpx;--hy1:%.1fpx,%.1fpx" transform="translate(%.1f %.1f)">%s</g></g>'
            '<g id="cabinFront">%s</g><g id="extra">%s</g>') % (base.svg(), sheet.svg(), cabB.svg(), *g0, *g1, gx, gy, gan.svg(), *h0, *h1, hdx, hdy, head.svg(), cabF.svg(), extra.svg())
    return body

def bbox(body_svg_paths):
    pass

def wrap(body, pad=14):
    # bbox по всем числам координат polygon/line/path
    xs, ys = [], []
    for m in re.finditer(r'points="([^"]+)"', body):
        for pt in m.group(1).split():
            a, b = pt.split(','); xs.append(float(a)); ys.append(float(b))
    for m in re.finditer(r'x1="(-?[\d.]+)" y1="(-?[\d.]+)" x2="(-?[\d.]+)" y2="(-?[\d.]+)"', body):
        xs += [float(m.group(1)), float(m.group(3))]; ys += [float(m.group(2)), float(m.group(4))]
    for m in re.finditer(r' d="([^"]+)"', body):
        for a, b in re.findall(r'(-?[\d.]+) (-?[\d.]+)', m.group(1)): xs.append(float(a)); ys.append(float(b))
    # учесть возможные смещения групп (диапазон хода портала) — расширим bbox по X запасом
    x0, y0 = min(xs) - pad, min(ys) - pad - 10
    return x0, y0, max(xs) - x0 + pad, max(ys) - y0 + pad

MODELS = [
    # бренд, модель, поле, L, W, тип, крыша, пульт, двери, лампа
    ('Bystronic', 'ByStar Fiber 3015', '3000×1500', 300, 150, 'A', 'bevel', 'swing', 2, 'lime'),
    ('Bystronic', 'ByStar Fiber 4020', '4000×2000', 360, 180, 'A', 'bevel', 'swing', 3, 'lime'),
    ('Bystronic', 'BySprint Fiber 3015', '3000×1500', 300, 150, 'B', 'bevel', 'swing', 2, 'lime'),
    ('Trumpf', 'TruLaser 3030', '3000×1500', 300, 150, 'B', 'slant', 'stand', 2, 'blue'),
    ('Trumpf', 'TruLaser 5030', '3000×1500', 300, 150, 'A', 'slant', 'stand', 2, 'blue'),
    ('Trumpf', 'TruLaser 3060', '6000×2000', 440, 160, 'A', 'slant', 'stand', 3, 'blue'),
    ('Bodor', 'Bodor i5 3015', '3000×1500', 300, 150, 'B', 'flat', 'stand', 2, 'lime'),
    ('Bodor', 'Bodor P 3015', '3000×1500', 300, 150, 'C', 'flat', 'stand', 2, 'lime'),
    ('Bodor', 'Bodor C 3015', '3000×1500', 300, 150, 'C', 'flat', 'stand', 1, 'blue'),
    ('HSG Laser', 'GWEIKE LF3015', '3000×1500', 300, 150, 'C', 'flat', 'swing', 2, 'lime'),
    ('HSG Laser', 'GWEIKE LF4020', '4000×2000', 360, 180, 'C', 'flat', 'swing', 3, 'lime'),
    ('HSG Laser', 'GWEIKE LF6025', '6000×2500', 440, 190, 'C', 'flat', 'swing', 3, 'lime'),
    ("Han's Laser", 'G3015', '3000×1500', 300, 150, 'C', 'barrel', 'tall', 2, 'blue'),
    ("Han's Laser", 'G4020', '4000×2000', 360, 180, 'C', 'barrel', 'tall', 3, 'blue'),
    ("Han's Laser", 'G6025', '6000×2500', 440, 190, 'C', 'barrel', 'tall', 3, 'blue'),
]

def params(m): return dict(brand=m[0], L=m[3], W=m[4], kind=m[5], roof=m[6], pult=m[7], doors=m[8], lamp=m[9])

def svg_of(m, state='idle', anim=False):
    body = machine(params(m), state)
    x0, y0, w, h = wrap(body, 20)
    # запас по ширине под ход портала не нужен: портал движется внутри кабины
    return '<svg class="mach" viewBox="%.0f %.0f %.0f %.0f" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">%s</svg>' % (x0, y0, w, h, body)

if __name__ == '__main__':
    out = sys.argv[1]
    import os; os.makedirs(out, exist_ok=True)
    css = '''
.card{background:#F8F9F9;border:1px solid #D7DCDC;padding:14px;position:relative}
.card h4{margin:0;font:700 15px 'Exo 2',sans-serif;color:#072730}
.card p{margin:2px 0 6px;font:12px 'IBM Plex Mono',monospace;color:#798591}
.mach{width:100%;height:auto;display:block}
.mach .cut,.mach .cut2{stroke-dasharray:1;stroke-dashoffset:1;opacity:0}
.card:hover .mach #gantry{animation:gx 3.2s ease-in-out infinite alternate}
.card:hover .mach #head{animation:hy 1.3s ease-in-out infinite alternate}
.card:hover .mach .cut{opacity:1;animation:draw 3.2s linear infinite}
.card:hover .mach .cut2{opacity:1;stroke-dashoffset:0}
.card:hover .mach #beam{animation:blink .18s steps(2) infinite}
@keyframes gx{from{transform:translate(var(--gx0))}to{transform:translate(var(--gx1))}}
@keyframes hy{from{transform:translate(var(--hy0))}to{transform:translate(var(--hy1))}}
@keyframes draw{0%{stroke-dashoffset:1}70%,100%{stroke-dashoffset:0}}
@keyframes blink{50%{opacity:.2}}
'''
    cards = []
    for m in MODELS:
        s = svg_of(m)
        open(f'{out}/{m[1].replace(" ","_")}_idle.svg', 'w').write(s)
        open(f'{out}/{m[1].replace(" ","_")}_hover.svg', 'w').write(svg_of(m, 'hover'))
        cards.append('<div class="card"><h4>%s</h4><p>%s · %s</p>%s</div>' % (m[1], m[0], m[2], s))
    open(f'{out}/grid.html', 'w').write('<!doctype html><meta charset=utf-8><style>body{margin:0;padding:20px;background:#EFEFEF;font-family:sans-serif}.g{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}%s</style><div class=g>%s</div>' % (css, ''.join(cards)))
    print('ok', len(MODELS))
