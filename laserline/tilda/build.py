#!/usr/bin/env python3
"""Сборка пакета для Тильды: python3 build.py  →  head.html, blocks/*.html, preview.html"""
import math, re, pathlib, html
ROOT = pathlib.Path(__file__).parent
(ROOT/'blocks').mkdir(exist_ok=True)

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
<nav class="ll-nav" id="llNav" aria-label="Основное меню"><a href="#catalog">Каталог</a><a href="#series">Серии</a><a href="#diagnostics">Экспресс-диагностика</a><a href="#guarantees">Гарантии</a><a href="#delivery">Условия</a><a href="#video">Видео</a><a href="#contacts">Контакты</a></nav>
<a class="ll-btn" href="#request">Связаться с инженером</a>
<button class="ll-burger" id="llBurger" type="button" aria-label="Меню" aria-expanded="false" aria-controls="llNav"><i></i><i></i><i></i></button>
</div></header>'''
# ---------- 02 hero ----------
mach_dark=machine(NAVY,BG,LIME,BLUE)
blocks['02-hero']=f'''<section class="ll ll-sec ll-hero" id="top"><div class="ll-wrap"><div class="ll-bento">
<div class="ll-card ll-card--dark ll-main ll-reveal"><div>
<h1 class="ll-h1">Гофрозащита для лазерных станков раскроя металла</h1>
<p class="ll-body">Комплект под марку и модель станка. Три серии — под толщину металла, окалину и температуру в зоне резания.</p></div>
<a class="ll-btn ll-btn--lime" href="#catalog">Подобрать комплект</a>
<div class="ll-main-art">{mach_dark}</div>{ARROW}</div>
<a class="ll-card ll-ca ll-reveal" style="--d:.1s" href="#catalog"><h3>Подбор комплекта по модели станка</h3>{ARROW}
<div class="ll-art">{accordion(PAPER,GREY,NAVY)}</div>
<div class="ll-tags"><span class="ll-tag">Bystronic</span><span class="ll-tag">Trumpf</span><span class="ll-tag">Bodor</span><span class="ll-tag">HSG Laser</span><span class="ll-tag">Han's Laser</span><span class="ll-tag">+5 марок</span></div></a>
<a class="ll-card ll-cb ll-reveal" style="--d:.15s" href="#diagnostics"><h3>Экспресс-диагностика: расчёт за 2 часа по двум фото</h3>{ARROW}
<div class="ll-art">{photos(PAPER,GREY,NAVY)}</div>
<div class="ll-tags"><span class="ll-tag">{SOC['tg'].replace('<svg','<svg fill="#072730"')}Telegram</span><span class="ll-tag">{SOC['max'].replace('<svg','<svg fill="#072730"')}MAX</span><span class="ll-tag">{SOC['vk'].replace('<svg','<svg fill="#072730"')}VK</span></div></a>
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
<div><i style="background:{BLUE}"></i><p><b>Нижние гофры — 4 шт.</b><span>вдоль направляющих</span></p></div>
<div><i style="background:{ORANGE}"></i><p><b>Верхние гофры — 2 шт.</b><span>по траверсе</span></p></div></div>{mach_light}</div>
<div class="ll-steps ll-reveal" style="--d:.1s">
<div class="ll-card ll-step"><div class="ll-label">Шаг 1</div><h3>Марка станка</h3><div id="llBrands"></div></div>
<div class="ll-card ll-step"><div class="ll-label">Шаг 2</div><h3>Модель</h3><div id="llModels"></div></div>
<div class="ll-card ll-step"><div class="ll-label">Шаг 3</div><h3>Серия</h3><div id="llSeries"></div><p class="ll-hint">Серия зависит от толщины металла и характера резки. <a class="ll-link" href="#series">Как выбрать серию →</a></p></div>
<button type="button" class="ll-btn" id="llShow" style="justify-content:flex-start;text-align:left">Показать комплект</button>
<p class="ll-cfg-note">Нет вашей модели в списке? <a class="ll-link" href="#diagnostics">Подберём по двум фотографиям →</a></p></div></div>
<div class="ll-modal" id="llModal" role="dialog" aria-modal="true" aria-labelledby="llMTitle"><div class="ll-modal-box">
<div><div class="ll-modal-img">{modal_art}</div><div class="ll-modal-draw">Чертежи здесь будут</div><p class="ll-modal-pdf">Скачать полную спецификацию (PDF)</p></div>
<div><div class="ll-modal-top"><span class="ll-label">Модель гофрозащиты</span><button class="ll-close" type="button" id="llClose" aria-label="Закрыть"></button></div>
<div class="ll-modal-title"><h3 class="ll-title" id="llMTitle">Optimal</h3><span class="ll-modal-tag" id="llMTag">Для регулярного раскроя</span></div>
<p class="ll-modal-desc" id="llMDesc"></p>
<dl class="ll-specs"><div><dt>Состав</dt><dd>4 нижние + 2 верхние гофры</dd></div><div><dt>Назначение</dt><dd id="llMUse"></dd></div><div><dt>Условия резки</dt><dd id="llMCut"></dd></div><div><dt>Толщина металла</dt><dd id="llMTh"></dd></div><div><dt>Цена и срок</dt><dd>по запросу — рассчитаем в КП</dd></div><div><dt>Совместимость</dt><dd id="llMFit"></dd></div></dl>
<button type="button" class="ll-btn ll-btn--lime ll-btn--block" id="llPick">Подобрать эту модель</button></div></div></div>'''
blocks['03-catalog']=wrap(cat_inner,id='catalog')
# ---------- 04 диагностика ----------
def dstep(time,title,txt,art):
    return f'<div class="ll-card ll-dstep ll-reveal"><div class="ll-dbody"><div class="ll-dtop"><div class="ll-art">{art}</div><span class="ll-time">{time}</span></div><h3 class="ll-h4">{title}</h3><p class="ll-body ll-muted">{txt}</p></div></div>'
diag=sec_head('02','Экспресс-диагностика','Подбор защиты по двум фотографиям — расчёт за 2 часа','Для нестандартных моделей и изношенных узлов. Инженер-конструктор определит причину износа и подберёт материал под ваши условия: окалина, температура, СОЖ. Без опросных листов.')
diag+='<div class="ll-steps3">'+dstep('0 мин','Фотографии узла','Общий план защиты на станке и крупный план повреждения. Модель станка — по табличке или в сообщении.',photos(PAPER,GREY,NAVY))+dstep('≤ 1 час','Анализ инженером','Заявку ведёт инженер-конструктор. Определяет причину износа и подбирает материал под окалину, температуру и СОЖ.',analysis(PAPER,NAVY,BLUE))+dstep('2 часа','Расчёт','Причина износа, материал, стоимость и срок изготовления — за 2 часа. Без опросных листов.',calc(PAPER,NAVY,BLUE))+'</div>'
diag+=f'''<div class="ll-cta"><div class="ll-cta-photo ll-reveal"><div><h3 class="ll-h3">Отправить фото инженеру</h3><p class="ll-body">Без опросных листов и обязательств</p></div>
<div class="ll-msg"><a href="{TG_URL}" target="_blank" rel="noopener">{SOC['tg']}Telegram</a><a href="{MAX_URL}" target="_blank" rel="noopener">{SOC['max']}MAX</a><a href="{VK_URL}" target="_blank" rel="noopener">{SOC['vk']}VK</a></div></div>
<div class="ll-urgent ll-reveal" style="--d:.1s"><b>24 ч</b><div><span class="ll-label">Аварийная остановка?</span><p>Напишите «срочно» — отгрузим в течение 24 часов после оплаты.</p></div></div></div>'''
blocks['04-diagnostics']=wrap(diag,id='diagnostics')
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
<div class="ll-ph ll-cap">Фото: фирменный конверт с тремя образцами 5×5 см (Econom, Optimal, Pro) и распечатка цифрового паспорта</div></div>'''
blocks['10-request']=wrap(fm,id='request',dark=True)
# ---------- 11 футер ----------
logo_light_cls=logo_light.replace('<svg','<svg class="logo"',1)
blocks['11-footer']=f'''<footer class="ll ll-footer" id="contacts"><div class="ll-wrap"><div class="ll-fgrid">
<div>{logo_light_cls}<p>Гофрозащита для лазерных станков. Суб-бренд Станкозащиты.рф.</p></div>
<div><h4>Навигация</h4><ul><li><a href="#catalog">Каталог</a></li><li><a href="#series">Серии</a></li><li><a href="#diagnostics">Экспресс-диагностика</a></li><li><a href="#delivery">Условия</a></li></ul></div>
<div><h4>Информация</h4><ul><li><a href="#guarantees">Гарантии</a></li><li><a href="#video">Видео</a></li><li><a href="#guarantees">Рекомендации по сроку службы</a></li></ul></div>
<div><h4>Контакты</h4><p>Телефон: +7 (___) ___-__-__</p><p>E-mail: info@…</p><p>Производство: Таганрог</p>
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
  function render(){
    chips($('#llBrands'),Object.keys(DATA),'brand',function(){st.model=DATA[st.brand][0]});
    chips($('#llModels'),DATA[st.brand],'model');
    chips($('#llSeries'),Object.keys(SER),'series');
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
blocks['99-scripts']=JS

# ---------- выгрузка ----------
css=(ROOT/'src'/'ll.css').read_text()
HEAD=f'''<!-- Laserline: вставьте в Настройки сайта → Ещё → HTML-код для вставки внутрь HEAD -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@700;800&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
{css}
</style>'''
(ROOT/'head.html').write_text(HEAD)
# то же самое для тарифов без доступа к HEAD: стили и шрифты первым блоком T123
STYLES=HEAD.replace('<!-- Laserline: вставьте в Настройки сайта → Ещё → HTML-код для вставки внутрь HEAD -->','<!-- Laserline: первый блок T123 на странице (стили и шрифты). Ничего не показывает, только подключает оформление -->')
(ROOT/'blocks'/'00-styles.html').write_text(STYLES+'\n')
for k,v in blocks.items(): (ROOT/'blocks'/f'{k}.html').write_text(v+'\n')
prev='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Laserline · предпросмотр блоков для Тильды</title>'+HEAD+'<style>body{margin:0;background:#EFEFEF}</style></head><body>'+'\n'.join(blocks[k] for k in sorted(blocks))+'</body></html>'
(ROOT/'preview.html').write_text(prev)
print('ok', {k:len(v) for k,v in blocks.items()}, len(HEAD))
