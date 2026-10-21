#!/usr/bin/env python3
"""Сборка пакета для Тильды: python3 build.py  →  head.html, blocks/*.html, preview.html"""
import math, re, pathlib, html, os
ROOT = pathlib.Path(__file__).parent
DARK = os.environ.get('LL_THEME','light')=='dark'   # LL_THEME=dark python3 build.py → тёмная версия
BDIR = 'blocks-dark' if DARK else 'blocks'; SUF = '-dark' if DARK else ''
(ROOT/BDIR).mkdir(exist_ok=True)

# ---------- линейные изометрические иллюстрации ----------
C30 = math.cos(math.radians(30))
def P(x,y,z): return ((x-y)*C30,(x+y)*.5-z)
class Scene:
    def __init__(s,fill,stroke,sw=1.3): s.items=[]; s.fill=fill; s.stroke=stroke; s.sw=sw
    def box(s,x0,y0,z0,x1,y1,z1,stroke=None,pleat=None,n=0):
        st=stroke or s.stroke; g=[]
        def poly(p): return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="miter"/>'%(" ".join("%.1f,%.1f"%P(*q) for q in p),s.fill,st,s.sw)
        def ln(a,b): return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"/>'%(*P(*a),*P(*b),st,s.sw*.6)
        g.append(poly([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]))
        g.append(poly([(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)]))
        g.append(poly([(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)]))
        for i in range(1,n):
            if pleat=='y':
                y=y0+(y1-y0)*i/n; g+=[ln((x0,y,z1),(x1,y,z1)),ln((x1,y,z0),(x1,y,z1))]
            else:
                x=x0+(x1-x0)*i/n; g+=[ln((x,y0,z1),(x,y1,z1)),ln((x,y1,z0),(x,y1,z1))]
        s.items.append(((x0+x1)/2+(y0+y1)/2+(z0+z1)/2,"".join(g)))
    def svg(s,pad=6):
        s.items.sort(key=lambda t:t[0]); body="".join(g for _,g in s.items)
        pts=[tuple(map(float,m.split(','))) for m in re.findall(r'(-?[\d.]+,-?[\d.]+)',body)]
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        x0,y0=min(xs)-pad,min(ys)-pad; w,h=max(xs)-x0+pad,max(ys)-y0+pad
        return '<svg class="ll-wire" viewBox="%.0f %.0f %.0f %.0f" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">%s</svg>'%(x0,y0,w,h,body)
def machine(fill,stroke,up,low):
    s=Scene(fill,stroke,1.4); GX0,GX1=120,146
    s.box(0,0,0,300,150,34); s.box(8,8,34,292,142,38); s.box(14,14,38,286,136,41)
    s.box(0,-14,34,300,0,44); s.box(0,150,34,300,164,44)
    for a,b,c,d in [(2,-14,112,0),(152,-14,298,0),(2,150,112,164),(152,150,298,164)]: s.box(a,b,44,c,d,60,stroke=low,n=9)
    s.box(GX0-2,-24,34,GX1+2,-2,66); s.box(GX0-2,152,34,GX1+2,176,66); s.box(GX0,-24,66,GX1,176,96)
    s.box(GX1,-20,70,GX1+14,62,92,stroke=up,pleat='y',n=8); s.box(GX1,98,70,GX1+14,172,92,stroke=up,pleat='y',n=8)
    s.box(GX1,64,66,GX1+22,96,100); s.box(GX1+6,74,40,GX1+16,86,66)
    return s.svg()
def accordion(fill,stroke,acc,n=16):
    s=Scene(fill,stroke,1.2); s.box(0,0,0,260,70,50,stroke=acc,n=n); s.box(260,0,0,290,70,50); s.box(-30,0,0,0,70,50); return s.svg()
def photocards(front,back,bg,acc):
    """две фото-карточки (полароид), линейный стиль, без скруглений"""
    return (f'<svg class="ll-wire" viewBox="0 0 300 262" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false" fill="none" stroke-width="1.6">'
      f'<g transform="rotate(7 195 130)"><rect x="125" y="14" width="150" height="196" fill="{bg}" stroke="{back}"/><rect x="138" y="27" width="124" height="128" stroke="{back}"/><path d="M138 135 L168 100 L190 122 L214 88 L262 135" stroke="{back}"/><path d="M138 172 H210 M138 186 H186" stroke="{back}"/></g>'
      f'<g transform="rotate(-6 115 150)"><rect x="28" y="44" width="164" height="206" fill="{bg}" stroke="{front}"/><rect x="42" y="58" width="136" height="136" stroke="{front}"/>'
      f'<path d="M42 176 L78 130 L102 154 L128 112 L178 176" stroke="{front}"/><circle cx="148" cy="86" r="9" stroke="{acc}"/><path d="M42 214 H112 M42 228 H92" stroke="{front}"/></g></svg>')
def nameplate(fill,stroke,acc):
    """шильдик станка: табличка с строками текста и винтами"""
    s=Scene(fill,stroke,1.2); s.box(0,0,0,170,100,12); s.box(14,14,12,110,24,14); s.box(14,34,12,140,42,14); s.box(14,52,12,90,60,14,stroke=acc)
    for x,y in ((6,6),(156,6),(6,86),(156,86)): s.box(x,y,12,x+8,y+8,15)
    return s.svg()
def lifetime(fill,stroke,acc):
    """срок службы: столбики растут во времени, последний выделен"""
    s=Scene(fill,stroke,1.2)
    for i,h in enumerate((18,30,44,60,78)): s.box(i*34,0,0,i*34+26,70,h,stroke=(acc if i==4 else None))
    return s.svg()
PARCEL='A'   # вариант иллюстрации в блоке формы: A (раскладка), B (изометрия), C (карточки на петлях)
def _pats(g,bl,o):
    out='<defs>'
    for k,c in (('pc-g',g),('pc-b',bl),('pc-o',o)):
        out+='<pattern id="%s" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0H8" stroke="%s" stroke-width="1.4"/></pattern>'%(k,c)
    return out+'</defs>'
def parcel(fill,stroke,c1,c2,c3):
    """цифровой паспорт и три образца ткани 5x5 см; анимация идёт сама (CSS в ll.css)"""
    F,S,G,BL,OR=fill,stroke,c1,c2,c3
    if PARCEL=='A':
        return ('<svg class="ll-wire pc pc-A" viewBox="-10 -30 680 450" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false" fill="none" stroke-width="1.6">'+_pats(G,BL,OR)+
         '<g class="a-sheet"><g transform="rotate(-7 150 200)"><rect x="40" y="30" width="230" height="310" fill="%(F)s" stroke="%(S)s"/><path d="M62 62H190M62 82H150" stroke="%(S)s" stroke-width="2"/>'
         '<path d="M62 130H248M62 166H248M62 202H248M62 238H248M62 274H248M62 130V274M150 130V274M248 130V274" stroke="%(G)s" stroke-width="1.2"/>'
         '<rect x="206" y="52" width="42" height="42" stroke="%(OR)s"/><rect x="216" y="62" width="22" height="22" stroke="%(OR)s"/></g></g>'
         '<g class="a1"><g transform="rotate(-9 400 100)"><rect x="350" y="30" width="96" height="96" fill="url(#pc-g)" stroke="%(G)s"/></g></g>'
         '<g class="a2"><g transform="rotate(5 470 150)"><rect x="420" y="60" width="96" height="96" fill="url(#pc-b)" stroke="%(BL)s"/></g></g>'
         '<g class="a3"><g transform="rotate(14 500 230)"><rect x="452" y="116" width="96" height="96" fill="url(#pc-o)" stroke="%(OR)s"/></g></g>'
         '<g class="a-env"><g transform="rotate(3 330 270)"><rect x="170" y="190" width="300" height="190" fill="%(F)s" stroke="%(S)s"/><path d="M170 190L320 300L470 190M170 380L270 285M470 380L370 285" stroke="%(S)s"/></g></g></svg>')%dict(F=F,S=S,G=G,BL=BL,OR=OR)
    if PARCEL=='C':
        def card(x,y,col,pat,cls):
            return ('<g class="%s"><g transform="translate(%d %d)"><rect width="150" height="230" fill="%s" stroke="%s"/><circle cx="75" cy="22" r="7" stroke="%s"/>'
                    '<path d="M24 54H126M24 70H92" stroke="%s" stroke-width="1.5"/><rect x="24" y="92" width="102" height="102" fill="url(#%s)" stroke="%s"/><path d="M24 208H100" stroke="%s"/></g></g>')%(cls,x,y,F,S,col,S,pat,col,G)
        return ('<svg class="ll-wire pc pc-C" viewBox="0 0 560 330" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false" fill="none" stroke-width="1.6">'+_pats(G,BL,OR)+
           '<path d="M85 82L85 0M280 52L280 0M475 22L475 0" stroke="%s"/>'%G+card(10,60,G,'pc-g','c1')+card(205,30,BL,'pc-b','c2')+card(400,0,OR,'pc-o','c3')+'<path d="M0 316H560" stroke="%s"/></svg>'%G)
    # B: изометрия — паспорт и три образца, образцы и закладка выдвигаются
    s=Scene(F,S,1.4)
    s.box(0,0,0,150,205,16)
    def wrap(cls):
        d,t=s.items[-1]; s.items[-1]=(d,'<g class="%s">%s</g>'%(cls,t))
    s.box(150,24,2,162,64,14,stroke=OR); wrap('b-tab')
    def path(pts,col,sw=1.3):
        d='M'+' L'.join('%.1f %.1f'%P(*q) for q in pts)
        s.items.append((300,'<path d="%s" fill="none" stroke="%s" stroke-width="%s"/>'%(d,col,sw)))
    z=16
    path([(18,28,z),(112,28,z)],S,1.8); path([(18,44,z),(84,44,z)],S,1.3)
    for k in range(5): path([(18,84+k*24,z),(132,84+k*24,z)],G,1.1)
    path([(18,84,z),(18,180,z)],G,1.1); path([(75,84,z),(75,180,z)],G,1.1); path([(132,84,z),(132,180,z)],G,1.1)
    s.box(196,0,0,280,84,7,stroke=G,pleat='y',n=8); wrap('b1')
    s.box(196,100,0,280,184,7,stroke=BL,pleat='y',n=8); wrap('b2')
    s.box(196,200,0,280,284,7,stroke=OR,pleat='y',n=8); wrap('b3')
    out=s.svg(pad=14).replace('class="ll-wire"','class="ll-wire pc pc-B"')
    m=re.search(r'viewBox="(-?[\d.]+) (-?[\d.]+) ([\d.]+) ([\d.]+)"',out); x,y,w,h=map(float,m.groups())
    return out.replace(m.group(0),'viewBox="%.0f %.0f %.0f %.0f"'%(x-20,y-20,w+60,h+50))
def photos(fill,stroke,acc):
    s=Scene(fill,stroke,1.2); s.box(0,0,0,120,90,5); s.box(40,50,12,160,140,17,stroke=acc); s.box(60,70,17,70,80,40); return s.svg()
def layers(fill,stroke,acc):
    s=Scene(fill,stroke,1.2)
    for i,c in enumerate([None,None,acc]): s.box(0,0,i*34,160,110,i*34+14,stroke=c)
    return s.svg()
def analysis(fill,stroke,acc):
    s=Scene(fill,stroke,1.2); s.box(0,0,0,190,60,40,stroke=acc and stroke,n=12); s.box(190,0,0,215,60,40,stroke=acc); s.box(-25,0,0,0,60,40,stroke=acc); return s.svg()
def calc(fill,stroke,acc):
    s=Scene(fill,stroke,1.2); s.box(0,0,0,130,100,8,stroke='#072730'); s.box(15,15,8,115,25,10); s.box(15,35,8,95,45,10); s.box(15,55,8,75,65,10); s.box(15,75,8,45,85,10,stroke=acc); return s.svg()
NAVY,PAPER,BG,LIME,BLUE,ORANGE,GREY,NAVY2='#072730','#F8F9F9','#EFEFEF','#E8FC5C','#5EA7BB','#FF860D','#798591','#0D3744'

# ---------- логотипы ----------
LOGO=lambda p:(ROOT/'assets'/p).read_text().strip()
logo_dark=LOGO('logo-dark.svg'); logo_light=LOGO('logo-light.svg')
SOC={
 'tg':'<svg viewBox="0 0 16 13" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M0.754067 4.42912C0.754067 4.42912 6.19396 2.19656 8.08062 1.41045C8.80384 1.09601 11.2565 0.0897852 11.2565 0.0897852C11.2565 0.0897852 12.3885 -0.350437 12.2942 0.718674C12.2627 1.1589 12.0112 2.69967 11.7596 4.36623C11.3823 6.72456 10.9735 9.30301 10.9735 9.30301C10.9735 9.30301 10.9106 10.0262 10.3761 10.152C9.84151 10.2778 8.96107 9.71178 8.80384 9.58601C8.67807 9.49167 6.44551 8.07667 5.62796 7.3849C5.40785 7.19623 5.15629 6.8189 5.6594 6.37867C6.7914 5.34101 8.14351 4.05178 8.96107 3.23423C9.3384 2.8569 9.71573 1.97645 8.14351 3.04556C5.91096 4.58634 3.70984 6.03279 3.70984 6.03279C3.70984 6.03279 3.20673 6.34723 2.2634 6.06423C1.32007 5.78123 0.219512 5.4039 0.219512 5.4039C0.219512 5.4039 -0.535155 4.93223 0.754067 4.42912Z"/></svg>',
 'max':'<svg viewBox="0 0 13 13" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M6.32667 0.17338C2.56028 0.370185 0.0740293 3.32407 0.231113 7.04894C0.299724 8.67935 0.95514 10.0823 1.11042 11.6296C1.15014 12.0305 1.03458 12.5252 1.49681 12.7003C2.06556 12.9152 2.93764 12.5541 3.41431 12.2237C3.57681 12.1135 3.73208 11.9853 3.85125 11.8264C4.34417 12.1532 4.81181 12.4692 5.39861 12.61C7.98236 13.2294 10.8135 11.812 12.0719 9.53518C14.4372 5.25782 11.2396 -0.0830092 6.32667 0.17338ZM4.86417 9.10005C4.66014 9.25894 4.46334 9.4756 4.23764 9.60019C3.91083 9.77532 3.80972 9.59296 3.68695 9.30407C3.30056 8.38505 3.25361 6.81963 3.47931 5.85727C3.78264 4.54824 4.79556 3.3963 6.18764 3.27352C7.59597 3.14894 8.9032 3.86394 9.49361 5.15491C10.8008 8.02755 7.45514 10.8641 4.86417 9.10185V9.10005Z"/></svg>',
 'vk':'<svg viewBox="0 0 21 13" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M11.3473 13C4.22917 13 0.169169 8.12012 0 0H3.56557C3.68268 5.95996 6.31125 8.48448 8.39333 9.005V0H11.7508V5.14014C13.8069 4.91892 15.9668 2.57658 16.6955 0H20.0529C19.4934 3.17518 17.151 5.51752 15.4854 6.48048C17.151 7.26126 19.8188 9.30431 20.8338 13H17.138C16.3442 10.5275 14.3664 8.61461 11.7508 8.35435V13H11.3473Z"/></svg>'}
ARROW='<svg class="ll-arrow" viewBox="0 0 22 22" aria-hidden="true"><path d="M1 21L21 1M6 1h15v15"/></svg>'
TG_URL,MAX_URL,VK_URL='https://t.me/','https://max.ru/','https://vk.com/'   # ← подставьте ваши ссылки
def sec_head(num,label,title,lead=None,dark=False):
    eb=f'<div class="ll-eyebrow ll-label"><b>{num}</b>{label}</div>' if num else ''
    ld=f'<p class="ll-lead">{lead}</p>' if lead else ''
    return f'<div class="ll-head ll-reveal">{eb}<h2 class="ll-h2">{title}</h2>{ld}</div>'
def wrap(inner,cls='',id='',dark=False,tag='section'):
    i=f' id="{id}"' if id else ''
    return f'<{tag} class="ll ll-sec{" ll-sec--dark" if dark else ""} {cls}"{i}><div class="ll-wrap">{inner}</div></{tag}>'

blocks={}
# ---------- 01 шапка ----------
blocks['01-header']=f'''<header class="ll ll-header"><div class="ll-wrap">
<a class="ll-logo" href="#top" aria-label="Laserline — на главную">{logo_dark}</a>
<nav class="ll-nav" id="llNav" aria-label="Основное меню"><a href="#catalog">Каталог</a><a href="#series">Серии</a><a href="#consult">Консультация инженера</a><a href="#guarantees">Гарантии</a><a href="#delivery">Условия</a><a href="#video">Видео</a><a href="#contacts">Контакты</a></nav>
<a class="ll-btn" href="#request">Связаться с инженером</a>
<button class="ll-burger" id="llBurger" type="button" aria-label="Меню" aria-expanded="false" aria-controls="llNav"><i></i><i></i><i></i></button>
</div></header>'''
# ---------- 02 hero ----------
mach_dark=machine(NAVY,BG,LIME,BLUE)
# тёмный макет: в главной карточке рендер гофры (картинка, адрес вставляется в Тильде), станок-схема переехала в правую карточку
MAIN_ART = '<img class="ll-main-img" src="https://static.tildacdn.com/tild6363-3836-4336-b461-323530623436/image_1.png" alt="Гофрозащита для лазерных станков" width="425" height="381">' if DARK else f'<div class="ll-main-art">{mach_dark}</div>'
CA_ART = mach_dark if DARK else accordion(PAPER,GREY,NAVY)
blocks['02-hero']=f'''<section class="ll ll-sec ll-hero" id="top"><div class="ll-wrap"><div class="ll-bento">
<div class="ll-card ll-card--dark ll-main ll-reveal"><div>
<h1 class="ll-h1">Гофрозащита для лазерных станков раскроя металла</h1>
<p class="ll-body">Комплект под марку и модель станка. Три серии — под толщину металла, окалину и температуру в зоне резания.</p></div>
<a class="ll-btn ll-btn--lime" href="#catalog">Подобрать комплект</a>
{MAIN_ART}{ARROW}</div>
<a class="ll-card ll-ca ll-reveal" style="--d:.1s" href="#catalog"><h3>Подбор комплекта по модели станка</h3>{ARROW}
<div class="ll-art">{CA_ART}</div>
<div class="ll-tags"><span class="ll-tag">Bystronic</span><span class="ll-tag">Trumpf</span><span class="ll-tag">Bodor</span><span class="ll-tag">HSG Laser</span><span class="ll-tag">Han's Laser</span><span class="ll-tag">+5 марок</span></div></a>
<a class="ll-card ll-cb ll-reveal" style="--d:.15s" href="#consult"><h3>Консультация инженера: бесплатно, по фото шильдика и гофр</h3>{ARROW}
<div class="ll-art">{photocards(NAVY,GREY,PAPER,BLUE)}</div>
<span class="ll-only-d ll-cb-l">Инженер на связи:</span><div class="ll-tags"><span class="ll-tag">{SOC['tg'].replace('<svg','<svg fill="#072730"')}<i class="ll-sr">Telegram</i></span><span class="ll-tag">{SOC['max'].replace('<svg','<svg fill="#072730"')}<i class="ll-sr">MAX</i></span><span class="ll-tag">{SOC['vk'].replace('<svg','<svg fill="#072730"')}<i class="ll-sr">VK</i></span></div></a>
<a class="ll-card ll-cc ll-reveal" style="--d:.2s" href="#series"><h3>Серии Laserline под условия резки</h3>{ARROW}
<div class="ll-art">{layers(PAPER,GREY,NAVY)}</div>
<div class="ll-tags"><span class="ll-tag">Econom</span><span class="ll-tag">Optimal</span><span class="ll-tag">Pro</span></div></a>
<div class="ll-card ll-facts ll-reveal" style="--d:.25s">
<div class="ll-fact"><b>0 ₽</b><span>Образец для примерки</span></div><div class="ll-fact"><b>30 дней</b><span>Гарантия на брак</span></div>
<div class="ll-fact"><b>0 ₽</b><span>Доставка по всей России</span></div><div class="ll-fact"><b>2 часа</b><span>Расчёт по фото</span></div></div>
</div></div></section>'''
# ---------- 03 каталог + окно ----------
mach_light=machine(PAPER,NAVY,ORANGE,BLUE)
def chips(items,key,active):
    return '<div class="ll-chips" data-key="%s">'%key+''.join(f'<button type="button" class="ll-chip" aria-pressed="{"true" if i==active else "false"}">{html.escape(t)}</button>' for i,t in enumerate(items))+'</div>'
modal_art=accordion(NAVY2,BG,BLUE)
cat_inner=sec_head('01','Каталог','Комплект под вашу модель станка','Выберите марку и модель — покажем готовый комплект. Самостоятельные замеры не нужны.')+f'''
<div class="ll-cfg"><div class="ll-card ll-schema ll-reveal"><div class="ll-legend">
<div><i style="background:#E3EFF3;border:1px solid {BLUE}"></i><p><b>Нижние гофры — 4 шт.</b><span>вдоль направляющих</span></p></div>
<div><i style="background:{LIME};border:1px solid {NAVY}"></i><p><b>Верхние гофры — 2 шт.</b><span>по траверсе</span></p></div></div><div class="ll-mach" id="llMachine">{mach_light}</div><p class="ll-mach-cap" id="llMachCap"></p></div>
<div class="ll-steps ll-reveal" style="--d:.1s">
<div class="ll-card ll-step"><div class="ll-label">Шаг 1</div><h3>Марка станка</h3><div id="llBrands"></div></div>
<div class="ll-card ll-step"><div class="ll-label">Шаг 2</div><h3>Модель</h3><div id="llModels"></div></div>
<div class="ll-card ll-step"><div class="ll-label">Шаг 3</div><h3>Серия</h3><div id="llSeries"></div><p class="ll-hint">Серия зависит от толщины металла и характера резки. <a class="ll-link" href="#series">Как выбрать серию →</a> <a class="ll-link" href="#consult">Не уверены? Спросите инженера →</a></p></div>
<button type="button" class="ll-btn" id="llShow" style="justify-content:flex-start;text-align:left">Показать комплект</button>
</div></div><p class="ll-cfg-note">Нет вашей модели в списке? <a class="ll-link" href="#consult">Спросите инженера, это бесплатно →</a></p>
<div class="ll-modal" id="llModal" role="dialog" aria-modal="true" aria-labelledby="llMTitle"><div class="ll-modal-box">
<div><div class="ll-modal-img">{modal_art}</div><div class="ll-modal-draw">Чертежи здесь будут</div><p class="ll-modal-pdf">Скачать полную спецификацию (PDF)</p></div>
<div><div class="ll-modal-top"><span class="ll-label">Модель гофрозащиты</span><button class="ll-close" type="button" id="llClose" aria-label="Закрыть"></button></div>
<div class="ll-modal-title"><h3 class="ll-title" id="llMTitle">Optimal</h3><span class="ll-modal-tag" id="llMTag">Для регулярного раскроя</span></div>
<p class="ll-modal-desc" id="llMDesc"></p>
<dl class="ll-specs"><div><dt>Состав</dt><dd>4 нижние + 2 верхние гофры</dd></div><div><dt>Назначение</dt><dd id="llMUse"></dd></div><div><dt>Условия резки</dt><dd id="llMCut"></dd></div><div><dt>Толщина металла</dt><dd id="llMTh"></dd></div><div><dt>Цена и срок</dt><dd>по запросу — рассчитаем в КП</dd></div><div><dt>Совместимость</dt><dd id="llMFit"></dd></div></dl>
<button type="button" class="ll-btn ll-btn--lime ll-btn--block" id="llPick">Подобрать эту модель</button></div></div></div>'''
blocks['03-catalog']=wrap(cat_inner,id='catalog')
# ---------- 04 диагностика ----------
def dstep(time,title,txt,art,link=''):
    lk=f'<a class="ll-link ll-link--acc" href="#video">{link}</a>' if link else ''
    return f'<div class="ll-card ll-dstep ll-reveal"><div class="ll-dbody"><div class="ll-dtop"><div class="ll-art">{art}</div><span class="ll-time">{time}</span></div><h3 class="ll-h4">{title}</h3><p class="ll-body ll-muted">{txt}</p>{lk}</div></div>'
diag=sec_head('02','Консультация инженера','Экспертная консультация инженера — бесплатно','Нужна экспертная рекомендация инженеров по подбору наиболее экономически выгодной комплектации? Это бесплатно. Пришлите три вещи, и мы вернёмся с рекомендацией. Даём её на основании многолетнего опыта: исходим из состояния, характера износа и срока службы текущего комплекта ваших гофр.')
diag+='<div class="ll-steps3">'+dstep('1','Фото шильдика станка','Табличка на станке с маркой и моделью: по ней инженер определяет, какой у вас станок.',nameplate(PAPER,GREY,NAVY))+dstep('2','Фото или видео всех гофрозащит','Снимите каждую гофру, включая изношенные места и повреждения. По снимкам видны состояние и характер износа.',photocards(NAVY,GREY,PAPER,BLUE),'Как снять размеры гофры — видео 2 мин →')+dstep('3','Примерный срок службы гофр','Сколько работает текущий комплект. По сроку службы видно, насколько он выдерживает ваши условия.',lifetime(PAPER,GREY,NAVY))+'</div>'
diag+=f'''<div class="ll-cta"><div class="ll-cta-photo ll-reveal"><div><h3 class="ll-h3">Отправить данные инженеру</h3><p class="ll-body">Бесплатно и без обязательств</p></div>
<div class="ll-msg"><a href="{TG_URL}" target="_blank" rel="noopener">{SOC['tg']}<i class="ll-sr">Telegram</i></a><a href="{MAX_URL}" target="_blank" rel="noopener">{SOC['max']}<i class="ll-sr">MAX</i></a><a href="{VK_URL}" target="_blank" rel="noopener">{SOC['vk']}<i class="ll-sr">VK</i></a></div></div>
<div class="ll-urgent ll-reveal" style="--d:.1s"><b>24 ч</b><div><span class="ll-label">Аварийная остановка?</span><p>Напишите «срочно» — отгрузим в течение 24 часов после оплаты.</p></div></div></div>'''
blocks['04-diagnostics']=wrap(diag,id='consult')
# ---------- 05 серии ----------
def meters(vals,names=('Нагрузка','СОЖ и абразив','Окалина и капли')):
    return '<div class="ll-meters">'+''.join(f'<div class="ll-meter"><span>{n}</span><span class="ll-dots">'+''.join(f'<i class="{"on" if k<v else ""}"></i>' for k in range(5))+'</span></div>' for n,v in zip(names,vals))+'</div>'
def ser(name,tag,acc,seg,thick,m,txt,cls=''):
    return f'''<article class="ll-ser {cls} ll-reveal" style="--acc:{acc}"><div class="ll-ser-b"><p class="ll-label ll-ser-tag">{tag}</p><h3 class="ll-ser-name">{name}</h3>
<div class="ll-th"><div class="ll-th-row"><span class="ll-label">Толщина металла</span><b>{thick}</b></div><div class="ll-segs">{"".join(f'<i class="{"on" if k<seg else ""}"></i>' for k in range(6))}</div></div>
{meters(m)}<p>{txt}</p></div></article>'''
sr=sec_head('03','Серии Laserline','Серия определяется условиями резки','Толщина металла, объём расплава и температура в зоне резания определяют, какой материал выдержит нагрузку.')
sr+='<div class="ll-series">'+ser('Econom','Тонколистовой металл · сухая резка',GREY,2,'до __ мм',(1,0,0),'Минимальная пылевая нагрузка, без агрессивных сред и раскалённых капель. Материал: отечественный технический полимер европейского качества.')+ser('Optimal','Средние толщины · интенсивное производство',BLUE,4,'до __ мм',(3,3,1),'Работа с СОЖ и умеренной абразивной нагрузкой. Баланс ресурса материала и стоимости.')+ser('Laserline Pro','Толстолистовой металл · тяжёлая резка',ORANGE,6,'до 40 мм',(5,3,5),'Капли расплава и раскалённая окалина. Полная герметизация оптического тракта.','ll-ser--pro')+'</div>'
sr+='<p class="ll-cap ll-note">Шкалы условные: показывают сравнение серий между собой, а не измеренные значения.</p><div class="ll-samples ll-reveal"><div><h3>Сравните материалы в руках</h3><p>Бесплатно отправим 3 образца ткани 5×5 см — Econom, Optimal и Pro — Почтой России.</p></div><a class="ll-btn ll-btn--lime" href="#request" data-kind="samples">Получить образцы тканей</a></div>'
blocks['05-series']=wrap(sr,id='series',dark=True)
# ---------- 06 видео ----------
vd=sec_head('04','Видео','Краш-тест: пламя горелки против ткани Laserline Pro','Направляем пламя промышленной газовой горелки на ткань серии Pro. 30 секунд — и вы видите результат сами.')
vd+='''<div class="ll-player ll-reveal" id="llPlayer"><button class="ll-play" type="button" aria-label="Смотреть видео" id="llPlay"></button><span class="ll-cap">Видео краш-теста · 30 сек · встроенный плеер</span></div>
<div class="ll-vids"><div class="ll-card ll-vcard ll-reveal"><h3>Как снять размеры с порванной гофры</h3><p>Инженер показывает замер, 2 минуты.</p></div>
<div class="ll-card ll-vcard ll-reveal" style="--d:.1s"><h3>Монтаж комплекта на станок</h3><p>Хронометраж уточняется.</p></div>
<div class="ll-card ll-vcard ll-vcard--hl ll-reveal" style="--d:.2s"><h3>Цифровой паспорт материала</h3><p>Характеристики серии и ссылка на краш-тест — на ваш e-mail.</p><a class="ll-btn" href="#request" data-kind="passport">Запросить паспорт</a></div></div>'''
blocks['06-video']=wrap(vd,id='video')
# ---------- 07 гарантии ----------
def gcard(stage,stat,unit,title,txt,acc,link=None):
    lk=f'<a class="ll-link" href="#guarantees">{link}</a>' if link else ''
    return f'<div class="ll-reveal"><span class="ll-label ll-stage">{stage}</span><div class="ll-card ll-g" style="--acc:{acc}"><div class="ll-gb"><b class="ll-num">{stat}</b><span class="ll-label ll-muted">{unit}</span><hr><h3>{title}</h3><p>{txt}</p>{lk}</div></div></div>'
gr=sec_head('05','Гарантии','Гарантии производителя')
gr+='<div class="ll-gtrack">'+gcard('Перед заказом','0 ₽','образец для примерки','Гарантия совместимости','Изготовим бесплатный образец по размерам вашего станка и отправим для примерки. Если нужна корректировка — переделаем бесплатно.',LIME)+gcard('После отгрузки','30 дней','с даты отгрузки','Гарантия на брак','На производственный брак — по товарной накладной.',BLUE)+gcard('При преждевременном износе','Комиссия','по каждому случаю','Разбор случаев износа','Собираем техническую комиссию: устанавливаем причину и даём рекомендации по увеличению ресурса оборудования.',NAVY,'Рекомендации по сроку службы →')+'</div><p class="ll-foot">Права покупателя защищены законодательством РФ.</p>'
blocks['07-guarantees']=wrap(gr,id='guarantees')
# ---------- 08 заказчики ----------
cl=sec_head('06','Заказчики','Нам доверяют','Предприятия, которые уже защищают станки гофрами Laserline. Логотипы и отзывы — с согласия заказчиков.')
cl+='<div class="ll-logos">'+''.join(f'<div class="ll-slot ll-reveal" style="--d:{i*.05}s"><span class="ll-label">Логотип</span><b>{n}</b></div>' for i,n in enumerate(['КАМАЗ','им. Бериева','Заказчик 3','Заказчик 4','Заказчик 5','Заказчик 6']))+'</div>'
def rev(i,acc,dark):
    return f'''<figure class="ll-card ll-rev {"ll-rev--dark" if dark else ""} ll-reveal" style="--acc:{acc};--d:{i*.1}s"><div class="ll-rev-b"><span class="q" aria-hidden="true">“</span><blockquote>Здесь будет отзыв заказчика: что защищали, как гофра отработала смену, что изменилось в простоях.</blockquote><p class="ll-cap">Ресурс гофры: было __ → стало __ мес.</p>
<figcaption class="ll-author"><i></i><div><b>Имя Фамилия</b><span>Должность · Компания</span></div></figcaption><a class="ll-link" href="#">Письмо-благодарность →</a></div></figure>'''
cl+='<div class="ll-reviews">'+rev(0,LIME,True)+rev(1,BLUE,False)+rev(2,ORANGE,False)+'</div>'
blocks['08-clients']=wrap(cl,id='clients')
# ---------- 09 доставка ----------
dl=sec_head('07','Условия','Условия поставки')
dl+=f'''<div class="ll-del"><div class="ll-card ll-routes ll-reveal">
<div class="ll-route"><div class="ll-route-h"><span class="ll-chipx ll-label">Стандарт</span><b>0 ₽ · 3–5 дней</b></div><p>Бесплатная доставка СДЭК по европейской части России. В другие регионы — по срокам СДЭК.</p></div>
<hr style="border:0;border-top:1px solid var(--line);width:100%;margin:0">
<div class="ll-route"><div class="ll-route-h"><span class="ll-chipx ll-chipx--lime ll-label">Срочно</span><b>24 ч</b><a class="ll-btn ll-btn--lime" href="#request" data-kind="calc">Нужна срочная отгрузка</a></div><p>Для аварийных остановок: отгрузка в течение 24 часов после оплаты, кроме выходных и праздников.</p>
<div class="ll-fast"></div><div class="ll-fast-l ll-label"><span>Оплата</span><span>Отгрузка ≤ 24 часа</span></div></div></div>
<div class="ll-docs ll-reveal" style="--d:.1s"><span class="ll-label">В комплекте</span><h3>Документы</h3><ul><li>Счёт</li><li>Товарная накладная</li><li>Технический паспорт изделия</li></ul></div></div>'''
blocks['09-delivery']=wrap(dl,id='delivery')
# ---------- 10 форма ----------
fm=f'''<div class="ll-form-grid"><div><div class="ll-head" style="margin-bottom:0"><h2 class="ll-h2">Запросите паспорт материала или образцы тканей</h2><p class="ll-lead">Отправим на e-mail цифровой паспорт с характеристиками и ссылкой на краш-тест — или бесплатно пришлём три образца ткани Почтой России.</p></div>
<form class="ll-form" id="llForm" novalidate>
<fieldset class="ll-kinds full"><legend style="position:absolute;left:-9999px">Что вам нужно</legend>
<label><input type="radio" name="kind" value="passport" checked> Цифровой паспорт на e-mail</label><label><input type="radio" name="kind" value="samples"> Образцы тканей почтой</label><label><input type="radio" name="kind" value="calc"> Расчёт комплекта</label></fieldset>
<label class="f">Имя<input type="text" name="name" required autocomplete="name"></label>
<label class="f">Компания<input type="text" name="company" autocomplete="organization"></label>
<label class="f">Марка и модель станка<input type="text" name="machine" id="llMachine"></label>
<label class="f">E-mail<input type="email" name="email" required autocomplete="email"></label>
<label class="f full">Телефон или ник в Telegram / MAX / VK<input type="text" name="contact" autocomplete="tel"></label>
<button class="ll-btn ll-btn--lime full" type="submit">Отправить запрос</button>
<label class="ll-consent full"><input type="checkbox" name="agree" required><span>Согласен на обработку персональных данных в соответствии с <a class="ll-link" href="#" style="border-color:var(--lime)">политикой конфиденциальности</a></span></label>
<p class="ll-hint full">Ответит инженер-конструктор. Адрес для отправки образцов уточним в переписке.</p></form>
<div class="ll-ok" id="llOk" role="status">Спасибо! Заявка принята — инженер ответит в рабочее время.</div></div>
<div class="ll-parcel ll-reveal" style="--d:.1s">{parcel(PAPER,NAVY,GREY,BLUE,ORANGE)}</div></div>'''
blocks['10-request']=wrap(fm,id='request',dark=True)
# ---------- 11 футер ----------
logo_light_cls=logo_light.replace('<svg','<svg class="logo"',1)
blocks['11-footer']=f'''<footer class="ll ll-footer" id="contacts"><div class="ll-wrap"><div class="ll-fgrid">
<div>{logo_light_cls}<p>Гофрозащита для лазерных станков. Суб-бренд Станкозащиты.рф.</p></div>
<div><h4>Навигация</h4><ul><li><a href="#catalog">Каталог</a></li><li><a href="#series">Серии</a></li><li><a href="#consult">Консультация инженера</a></li><li><a href="#delivery">Условия</a></li></ul></div>
<div><h4>Информация</h4><ul><li><a href="#guarantees">Гарантии</a></li><li><a href="#video">Видео</a></li><li><a href="#guarantees">Рекомендации по сроку службы</a></li></ul></div>
<div><h4>Контакты</h4><p>Телефон: +7 (___) ___-__-__</p><p>E-mail: info@…</p><p>Производство: город уточняется</p>
<div class="ll-social"><a href="{TG_URL}" aria-label="Telegram" target="_blank" rel="noopener">{SOC['tg']}</a><a href="{MAX_URL}" aria-label="MAX" target="_blank" rel="noopener">{SOC['max']}</a><a href="{VK_URL}" aria-label="ВКонтакте" target="_blank" rel="noopener">{SOC['vk']}</a></div></div>
</div></div></footer>'''
# ---------- 99 скрипты ----------
JS=r'''<script>
(function(){
  var root=document;
  function $(s,c){return (c||root).querySelector(s)}
  function $$(s,c){return Array.prototype.slice.call((c||root).querySelectorAll(s))}
  /* меню на телефоне */
  var burger=$('#llBurger'),nav=$('#llNav');
  if(burger&&nav){burger.addEventListener('click',function(){var o=nav.classList.toggle('is-open');burger.setAttribute('aria-expanded',o)});
    $$('a',nav).forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('is-open');burger.setAttribute('aria-expanded','false')})})}
  /* появление блоков при скролле */
  document.documentElement.classList.add('ll-js');
  var rv=$$('.ll-reveal');
  /* страховка: если что-то пошло не так, через 4 с показываем всё */
  setTimeout(function(){rv.forEach(function(n){n.classList.add('is-in')})},4000);
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -40px 0px'});rv.forEach(function(n){io.observe(n)})}
  else{rv.forEach(function(n){n.classList.add('is-in')})}
  /* подбор комплекта */
  var DATA={'Bystronic':['ByStar Fiber 3015','ByStar Fiber 4020','BySprint Fiber 3015'],'Trumpf':['TruLaser 3030','TruLaser 5030','TruLaser 3060'],'Bodor':['Bodor i5 3015','Bodor P 3015','Bodor C 3015'],'HSG Laser':['GWEIKE LF3015','GWEIKE LF4020','GWEIKE LF6025'],"Han's Laser":['G3015','G4020','G6025']};
  var SER={
    'Econom':{tag:'Для тонколистового металла',desc:'Минимальная пылевая нагрузка, без агрессивных сред и раскалённых капель. Материал: отечественный технический полимер европейского качества.',use:'Тонколистовой металл, сухая резка',cut:'Сухая резка, без агрессивных сред',th:'до __ мм'},
    'Optimal':{tag:'Для регулярного раскроя',desc:'Работа с СОЖ и умеренной абразивной нагрузкой. Баланс ресурса материала и стоимости.',use:'Средние толщины, интенсивное производство',cut:'СОЖ, умеренная абразивная нагрузка',th:'до __ мм'},
    'Laserline Pro':{tag:'Для тяжёлой резки',desc:'Капли расплава и раскалённая окалина. Полная герметизация оптического тракта.',use:'Толстолистовой металл, тяжёлая резка',cut:'Капли расплава, раскалённая окалина',th:'до 40 мм'}};
  var st={brand:'Bystronic',model:'ByStar Fiber 3015',series:'Optimal'};
  function chips(el,items,key,pick){if(!el)return;el.className='ll-chips';el.innerHTML='';items.forEach(function(t){var b=document.createElement('button');b.type='button';b.className='ll-chip';b.textContent=t;b.setAttribute('aria-pressed',st[key]===t);b.addEventListener('click',function(){st[key]=t;if(pick)pick();render()});el.appendChild(b)})}
@@MACHINES@@
  function render(){
    chips($('#llBrands'),Object.keys(DATA),'brand',function(){st.model=DATA[st.brand][0]});
    chips($('#llModels'),DATA[st.brand],'model');
    chips($('#llSeries'),Object.keys(SER),'series');
    drawMachine();
    var s=$('#llShow');if(s)s.textContent='Показать комплект: '+st.brand+' '+st.model+' · '+st.series.replace('Laserline ','')}
  render();
  /* окно «Модель гофрозащиты» */
  var modal=$('#llModal'),lastFocus=null;
  function openM(){var d=SER[st.series];$('#llMTitle').textContent=st.series.replace('Laserline ','');$('#llMTag').textContent=d.tag;$('#llMDesc').textContent=d.desc;$('#llMUse').textContent=d.use;$('#llMCut').textContent=d.cut;$('#llMTh').textContent=d.th;$('#llMFit').textContent=st.brand+' '+st.model;lastFocus=document.activeElement;modal.classList.add('is-open');document.documentElement.style.overflow='hidden';$('#llClose').focus()}
  function closeM(){modal.classList.remove('is-open');document.documentElement.style.overflow='';if(lastFocus)lastFocus.focus()}
  var show=$('#llShow');if(show)show.addEventListener('click',openM);
  var cl=$('#llClose');if(cl)cl.addEventListener('click',closeM);
  if(modal){modal.addEventListener('click',function(e){if(e.target===modal)closeM()});document.addEventListener('keydown',function(e){if(e.key==='Escape'&&modal.classList.contains('is-open'))closeM()})}
  function setKind(k){var r=$('input[name="kind"][value="'+k+'"]');if(r)r.checked=true}
  var pick=$('#llPick');if(pick)pick.addEventListener('click',function(){closeM();setKind('calc');var m=$('#llMachine');if(m)m.value=st.brand+' '+st.model+' · '+st.series;var f=$('#request');if(f)f.scrollIntoView({behavior:'smooth'})});
  $$('[data-kind]').forEach(function(a){a.addEventListener('click',function(){setKind(a.getAttribute('data-kind'))})});
  /* видео: подставьте ссылку на Rutube/YouTube/VK в data-src плеера */
  var play=$('#llPlay'),pl=$('#llPlayer');
  if(play&&pl)play.addEventListener('click',function(){var src=pl.getAttribute('data-src');if(!src){return}var f=document.createElement('iframe');f.src=src;f.allow='autoplay; fullscreen';f.setAttribute('allowfullscreen','');pl.innerHTML='';pl.appendChild(f)});
  /* форма: если задан адрес приёма, отправляем JSON, иначе просто показываем подтверждение.
     Для приёма заявок в Тильду замените блок на штатную форму (см. README). */
  var form=$('#llForm'),ok=$('#llOk');
  if(form)form.addEventListener('submit',function(e){e.preventDefault();var d={};new FormData(form).forEach(function(v,k){d[k]=v});
    if(!form.elements.name.value||!form.elements.email.value||!form.elements.agree.checked){(form.elements.name.value?(form.elements.email.value?form.elements.agree:form.elements.email):form.elements.name).focus();return}
    var done=function(){form.style.display='none';ok.style.display='block'};
    if(window.LL_FORM_ENDPOINT){fetch(window.LL_FORM_ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(done).catch(done)}else{done()}});
})();
</script>'''
JS=JS.replace('@@MACHINES@@',(ROOT/'src'/'machines.js').read_text())
blocks['99-scripts']=JS

# ---------- выгрузка ----------
def to_dark(s):
    """светлые цвета иллюстраций → тёмная тема (CSS перекрашивается отдельно, ll-dark.css)"""
    s=s.replace('<svg fill="#072730"','<svg fill="#EFEFEF"')
    s=s.replace('fill="#072730"','fill="#0C3340"').replace('stroke="#072730"','stroke="#EFEFEF"')
    s=s.replace('fill="#F8F9F9"','fill="#0A2A34"').replace('stroke="#798591"','stroke="#9FB6BE"')
    s=s.replace('fill="#0D3744"','fill="#134556"').replace('#E3EFF3','#134556')
    s=s.replace('--acc:#072730','--acc:#EFEFEF').replace('background:#E8FC5C;border:1px solid #072730','background:#FF860D;border:1px solid #FF860D')
    return s
if DARK:
    for k in list(blocks):
        v=blocks[k]
        if k=='01-header': v=v.replace(logo_dark,logo_light)
        v=to_dark(v)
        v=v.replace('class="ll ','class="ll ll-d ')
        blocks[k]=v
css=(ROOT/'src'/'ll.css').read_text()
if DARK: css+='\n'+(ROOT/'src'/'ll-dark.css').read_text()
HEAD=f'''<!-- Laserline: вставьте в Настройки сайта → Ещё → HTML-код для вставки внутрь HEAD -->
<style>
{css}
</style>'''
(ROOT/f'head{SUF}.html').write_text(HEAD)
# то же самое для тарифов без доступа к HEAD: стили и шрифты первым блоком T123
STYLES=HEAD.replace('<!-- Laserline: вставьте в Настройки сайта → Ещё → HTML-код для вставки внутрь HEAD -->','<!-- Laserline: первый блок T123 на странице (стили и шрифты). Ничего не показывает, только подключает оформление -->')
(ROOT/BDIR/'00-styles.html').write_text(STYLES.replace('<!-- Laserline: первый блок T123 на странице (стили и шрифты). Ничего не показывает, только подключает оформление -->','<!-- БЛОК 1 из 13 (файл 00-styles) · стили и шрифты (ничего не показывает) · вставить в отдельный блок T123 «HTML», самым первым -->')+'\n')
NAMES={'00-styles':'стили и шрифты (ничего не показывает)','01-header':'шапка','02-hero':'первый экран','03-catalog':'каталог и подбор станка','04-diagnostics':'консультация инженера','05-series':'серии','06-video':'видео','07-guarantees':'гарантии','08-clients':'заказчики','09-delivery':'условия поставки','10-request':'форма заявки','11-footer':'подвал','99-scripts':'скрипты (последний блок)'}
ORDER=['00-styles']+sorted(k for k in blocks if k[0]=='0' and k!='00-styles' or k[:2]=='10' or k[:2]=='11')+['99-scripts']
def tag(k):
    return '<!-- БЛОК %d из %d (файл %s) · %s · вставить в отдельный блок T123 «HTML» -->\n'%(ORDER.index(k)+1,len(ORDER),k,NAMES.get(k,k))
for k,v in blocks.items(): (ROOT/BDIR/f'{k}.html').write_text(tag(k)+v+'\n')
prev='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Laserline · предпросмотр блоков для Тильды</title>'+HEAD+'<style>body{margin:0;background:'+('#051A21' if DARK else '#EFEFEF')+'}</style></head><body>'+'\n'.join(blocks[k] for k in sorted(blocks))+'</body></html>'
(ROOT/f'preview{SUF}.html').write_text(prev)
print('ok', {k:len(v) for k,v in blocks.items()}, len(HEAD))
