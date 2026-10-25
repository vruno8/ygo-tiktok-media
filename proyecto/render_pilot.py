import pathlib
BASE = pathlib.Path(__file__).parent.resolve()
src = (BASE / "render2.py").read_text(encoding="utf-8")
exec(src.split("SETS = {")[0].replace("pathlib.Path(__file__)", f"pathlib.Path(r'{BASE / 'render2.py'}')"))

from playwright.sync_api import sync_playwright
REG["WCS"] = "#FFFFFF"

WEEK = "19 al 25 oct"
COVER = [("TCG", "Nueva lista de prohibidas: 34 cartas fuera"),
         ("TCG", "El Mundial 2027 abre doble división"),
         ("OCG", "Immortal Phoenix sale en Japón el 31/10"),
         ("TCG", "Magnificent Maestros llega el 13/11")]

SLIDES = [
 dict(tag="TCG", sign="禁止", signc="#FF3EA5", n=1, cat="Lista de prohibidas",
      title="34 cartas prohibidas en la nueva lista",
      rows=[("Vigente desde", "19 de octubre"), ("Prohibidas", "34 (24 nuevas y 10 que estaban limitadas)"),
            ("Limitadas", "8, más 1 semilimitada"), ("Las más sonadas", "Called by the Grave, Trishula y Red-Eyes Dark Dragoon")],
      ask="¿Tu deck sobrevivió?", src="Fuente: lista oficial Konami TCG, 19/10"),
 dict(tag="TCG", sign="世界", signc="#C6FF3D", n=2, cat="Mundial 2027",
      title="El Mundial 2027 abre doble división",
      rows=[("Dónde", "Singapur"), ("Qué cambia", "Clasificados TCG pueden sumar una división digital"),
            ("Opciones", "Master Duel o Duel Links (Speed o Rush)"), ("Por qué importa", "Es la primera vez que se permite")],
      ask="¿Jugarías las dos?", src="Fuente: anuncio Konami WCS, 23/10"),
 dict(tag="OCG", sign="新弾", signc="#2EF2FF", n=3, cat="Producto",
      title="Immortal Phoenix sale en Japón el 31/10",
      rows=[("Dónde", "Solo OCG (Japón) por ahora"), ("Formato", "Sobres de 5 cartas, cajas de 30"),
            ("Esta semana", "Soporte para Umbral Horror, Ashtra y Dark Time Wizard"), ("¿Llega al TCG?", "Sin fecha anunciada")],
      ask="¿Cuál quieres en TCG?", src="Fuente: anuncio Konami OCG"),
 dict(tag="TCG", sign="発売", signc="#FF3EA5", n=4, cat="Producto",
      title="Magnificent Maestros llega el 13/11",
      rows=[("A la venta", "13 de noviembre en América"), ("Qué trae", "18 cartas del anime reimaginadas"),
            ("Rareza estrella", "Grand Master Rare numerada del 001 al 100"),
            ("Ojo", "Activa el límite a Perfectron Hydradrive Dragon")],
      ask="¿Vas por una numerada?", src="Fuente: Konami TCG"),
]
SOURCES = [("Lista de prohibidas TCG", "yugioh-card.com · 19/10"), ("Mundial 2027", "Konami WCS vía YGOrganization · 23/10"),
           ("Immortal Phoenix", "Konami OCG vía Yu-Gi-Oh! Meta"), ("Magnificent Maestros", "yugioh-card.com · Europa"),]

P_CSS = C_CSS + ".v{font-size:42px}"

def cover():
    its = "".join(f"<div class='it'><span class='chip' style='color:{REG[r]}'>{r}</span>{t}</div>" for r, t in COVER)
    return page(P_CSS, f"""{skyline()}
<div class='sign' style='right:40px;top:170px;color:#FF3EA5'>速報</div>
<div class='sign' style='right:40px;top:470px;color:#2EF2FF;font-size:62px'>決闘者</div>
<div class='top'><span class='handle'>{HANDLE}</span></div>
<div class='jp' style='top:170px'>今週のニュース</div>
<div class='hl' style='top:240px;right:200px'>Lo que pasó esta semana</div>
<div class='hud' style='top:620px;right:180px' data-l='YU-GI-OH! JUEGO DE CARTAS // {WEEK.upper()}'>{its}</div>
<div class='swipe' style='top:1360px'>Desliza para el detalle ▸▸</div>""")

def news(s):
    rows = "".join(f"<div class='row'><div class='k'>{k}</div><div class='v'>{v}</div></div>" for k, v in s['rows'])
    return page(P_CSS, f"""{skyline()}
<div class='sign' style='right:40px;top:170px;color:{s['signc']};font-size:66px'>{s['sign']}</div>
<div class='top'><span class='handle'>{HANDLE}</span></div>
<div class='big' style='top:150px;color:{REG[s['tag']]}'>{s['tag']}</div>
<div class='jp' style='top:390px'>NOTICIA {s['n']}/4 · {s['cat'].upper()}</div>
<div class='hl' style='top:460px;font-size:80px;right:150px'>{s['title']}</div>
<div style='position:absolute;left:70px;right:70px;top:700px;z-index:10'>
<div class='hud' style='position:relative;left:0;right:0' data-l='DATOS'>{rows}</div>
<div class='ask' style='position:relative;left:0;margin-top:44px'>{s['ask']}<small>Te leo en comentarios</small></div>
<div class='src' style='position:relative;left:0;margin-top:22px'>{s['src']}</div></div>""")

def sources():
    rows = "".join(f"<div class='row' style='grid-template-columns:1fr'><div class='v' style='font-size:44px'>{a}</div><div class='k'>{b}</div></div>" for a, b in SOURCES)
    return page(P_CSS, f"""{skyline()}
<div class='sign' style='right:40px;top:170px;color:#2EF2FF;font-size:66px'>出典</div>
<div class='top'><span class='handle'>{HANDLE}</span></div>
<div class='jp' style='top:170px'>FUENTES DE ESTA SEMANA</div>
<div class='hl' style='top:240px;right:200px;font-size:96px'>Revisa la fuente oficial</div>
<div class='hud' style='top:560px;right:70px' data-l='CONSULTADAS'>{rows}</div>
<div class='swipe' style='top:1430px;color:#2EF2FF;text-shadow:0 0 14px #2EF2FF'>Sígueme: resumen cada semana</div>""")

OUT = BASE / "piloto"; OUT.mkdir(exist_ok=True)
pages = [cover()] + [news(s) for s in SLIDES] + [sources()]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    files = []
    for i, html in enumerate(pages, 1):
        h = OUT / f"lamina_{i}.html"; h.write_text(html, encoding="utf-8")
        pg.goto(h.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(700)
        png = OUT / f"lamina_{i}.png"; pg.screenshot(path=str(png)); files.append(png)
    b.close()
ims = [Image.open(f) for f in files]; gap = 30; cols = 3
sheet = Image.new("RGB", (cols * 1080 + (cols + 1) * gap, 2 * 1920 + 3 * gap), (40, 40, 44))
for j, im in enumerate(ims): sheet.paste(im, (gap + (j % cols) * (1080 + gap), gap + (j // cols) * (1920 + gap)))
sheet.resize((sheet.width // 3, sheet.height // 3), Image.LANCZOS).save(OUT / "piloto_vista_general.png")
print("ok", len(files))
