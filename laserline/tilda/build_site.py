#!/usr/bin/env python3
"""Сборка самостоятельного сайта (без Тильды) из тёмной версии: python3 build_site.py
Результат: ../site/ (index.html, assets/css, assets/js, assets/img, assets/fonts, send.php) и ../laserline-site.zip
Сначала собирается тёмная версия блоков: LL_THEME=dark python3 build.py
"""
import pathlib, re, shutil, zipfile, subprocess, os, sys
ROOT = pathlib.Path(__file__).parent
OUT = ROOT.parent / 'site'
env = dict(os.environ, LL_THEME='dark')
subprocess.run([sys.executable, str(ROOT / 'build.py')], check=True, env=env, stdout=subprocess.DEVNULL)

if OUT.exists(): shutil.rmtree(OUT)
for d in ('assets/css', 'assets/js', 'assets/img', 'assets/fonts'): (OUT / d).mkdir(parents=True)

def strip_tag(s): return re.sub(r'^<!--.*?-->\s*', '', s, count=1, flags=re.S)

blocks = {p.stem: strip_tag(p.read_text()) for p in sorted((ROOT / 'blocks-dark').glob('*.html'))}

# --- CSS: стили темы + локальные шрифты ---
head = (ROOT / 'head-dark.html').read_text()
css = re.search(r'<style>(.*?)</style>', head, re.S).group(1)
css = css.replace('Всё под классом .ll', 'Всё под классом .ll').replace('для Тильды', 'для сайта')
fontface = '''/* Шрифты лежат в assets/fonts. Имена файлов можно менять, тогда поправьте адреса ниже. */
@font-face{font-family:"Magistral CTT";src:url(../fonts/MagistralCTT-Bold.woff2) format("woff2"),url(../fonts/MagistralCTT-Bold.woff) format("woff"),url(../fonts/MagistralCTT-Bold.ttf) format("truetype");font-weight:700 800;font-style:normal;font-display:swap}
@font-face{font-family:"MagistralC";src:url(../fonts/MagistralC-Regular.woff2) format("woff2"),url(../fonts/MagistralC-Regular.woff) format("woff"),url(../fonts/MagistralC-Regular.ttf) format("truetype");font-weight:400 500;font-style:normal;font-display:swap}
@font-face{font-family:"MagistralC";src:url(../fonts/MagistralC-Bold.woff2) format("woff2"),url(../fonts/MagistralC-Bold.woff) format("woff"),url(../fonts/MagistralC-Bold.ttf) format("truetype");font-weight:600 800;font-style:normal;font-display:swap}
body{margin:0;background:#051A21}
'''
(OUT / 'assets/css/style.css').write_text(fontface + css.strip() + '\n')

# --- JS: скрипты страницы; форма шлёт запрос на send.php и сообщает об ошибке ---
js = re.search(r'<script>(.*?)</script>', blocks['99-scripts'], re.S).group(1).strip()
fail = "function(){alert('Не удалось отправить заявку. Напишите нам в Telegram или на почту.')}"
js = js.replace(".then(done).catch(done)", ".then(function(r){if(r.ok)done();else (%s)()}).catch(%s)" % (fail, fail))
(OUT / 'assets/js/script.js').write_text(js + '\n')

# --- HTML ---
order = ['01-header', '02-hero', '03-catalog', '04-diagnostics', '05-series', '06-video', '07-guarantees', '08-clients', '09-delivery', '10-request', '11-footer']
body = '\n'.join(blocks[k] for k in order)
body = body.replace('src="" alt="Гофрозащита для лазерных станков"', 'src="assets/img/bellows-render.png" alt="Гофрозащита для лазерных станков" onerror="this.style.display=\'none\'"')
html = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Laserline — гофрозащита для лазерных станков раскроя металла</title>
<meta name="description" content="Гофрозащита под марку и модель лазерного станка: нижние 4 шт., верхние 2 шт. Расчёт по двум фотографиям за 2 часа.">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
{body}
<script>window.LL_FORM_ENDPOINT='send.php';</script>
<script src="assets/js/script.js"></script>
</body>
</html>
'''
(OUT / 'index.html').write_text(html)

# --- send.php: приём заявок на почту (замените адрес) ---
(OUT / 'send.php').write_text('''<?php
// Приём заявок с формы. Замените адрес получателя и проверьте, что на хостинге работает mail().
$TO = 'info@example.com';           // ← ваш адрес
$SUBJECT = 'Заявка с сайта Laserline';
header('Content-Type: application/json; charset=utf-8');
$d = json_decode(file_get_contents('php://input'), true);
if (!is_array($d) || empty($d['name']) || empty($d['email']) || !filter_var($d['email'], FILTER_VALIDATE_EMAIL)) {
  http_response_code(400); echo '{"ok":false}'; exit;
}
$lines = [];
foreach ($d as $k => $v) { $lines[] = $k . ': ' . trim(strip_tags((string)$v)); }
$ok = mail($TO, '=?UTF-8?B?' . base64_encode($SUBJECT) . '?=', implode("\\n", $lines),
  "Content-Type: text/plain; charset=utf-8\\r\\nReply-To: " . $d['email']);
http_response_code($ok ? 200 : 500); echo $ok ? '{"ok":true}' : '{"ok":false}';
''')

# --- логотипы и README ---
for n in ('logo-dark.svg', 'logo-light.svg'): shutil.copy(ROOT / 'assets' / n, OUT / 'assets/img' / n)
(OUT / 'assets/fonts/README.txt').write_text('Положите сюда файлы шрифтов (лицензия на веб-использование):\nMagistralCTT-Bold.woff2 — заголовки\nMagistralC-Regular.woff2 и MagistralC-Bold.woff2 — основной текст\nЕсли файлы названы иначе, поправьте адреса в assets/css/style.css (блок @font-face в начале).\nПока файлов нет, сайт показывается шрифтом Arial.\n')
(OUT / 'assets/img/README.txt').write_text('Положите сюда bellows-render.png: рендер гофры для главной карточки первого экрана (в Фигме слой image 1 в карточке «Главная», экспорт PNG 2x).\nПока файла нет, картинка скрыта.\n')
(OUT / 'README.md').write_text('''# Laserline · сайт (тёмная версия)

Статический сайт без сборки: открывается двойным кликом по `index.html`, выкладывается на любой хостинг папкой целиком.

## Что внутри
- `index.html` — вся страница (шапка, первый экран, каталог, диагностика, серии, видео, гарантии, заказчики, условия, форма, подвал).
- `assets/css/style.css` — стили и подключение шрифтов.
- `assets/js/script.js` — меню на телефоне, появление блоков, подбор станка со схемой и анимацией, окно модели, форма.
- `assets/img`, `assets/fonts` — сюда нужно положить рендер гофры и шрифты (см. README.txt в этих папках).
- `send.php` — приём заявок на почту (нужен PHP на хостинге).

## Что заменить
1. Рендер гофры: `assets/img/bellows-render.png`.
2. Шрифты Magistral CTT и MagistralC: `assets/fonts/`.
3. Адрес в `send.php` (`$TO`). Без PHP замените строку `window.LL_FORM_ENDPOINT` в `index.html` на адрес своего обработчика.
4. Ссылки на соцсети (Telegram, MAX, VK), телефон и e-mail в подвале, логотипы и отзывы заказчиков (заглушки), адрес политики конфиденциальности.
5. Видео краш-теста: в блоке `id="video"` у `<div class="ll-player" id="llPlayer">` добавьте `data-src="адрес iframe"`.

Исходники генератора и светлая версия лежат в `laserline/tilda/` (скрипт `build_site.py` пересобирает эту папку).
''')

# --- архив ---
zp = OUT.parent / 'laserline-site.zip'
if zp.exists(): zp.unlink()
with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file(): z.write(p, 'laserline-site/' + str(p.relative_to(OUT)))
print('ok', OUT, zp.stat().st_size, len(html), len(css), len(js))
