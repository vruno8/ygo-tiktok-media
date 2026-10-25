import os, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image

BASE = pathlib.Path(__file__).parent.resolve()
F = (BASE / "node_modules/@fontsource").as_uri()

def ff(family, pkg, weights):
    return "\n".join(
        f"@font-face{{font-family:'{family}';font-weight:{w};src:url('{F}/{pkg}/files/{pkg}-latin-{w}-normal.woff2') format('woff2');}}"
        for w in weights)

FONTS = "\n".join([
    ff("Plex Cond", "ibm-plex-sans-condensed", [400, 500, 600, 700]),
    ff("Caveat", "caveat", [600, 700]),
    ff("Unbounded", "unbounded", [500, 700, 800, 900]),
    ff("Inter Tight", "inter-tight", [400, 500, 600, 700]),
    ff("Bricolage", "bricolage-grotesque", [500, 600, 700, 800]),
])

# ---------- shared fictional content ----------
WEEK = "27 oct al 2 nov"
ITEMS = [("TCG", "Set nuevo de 100 cartas"),
         ("OCG", "Cambios a la lista de prohibidas"),
         ("MD", "Evento nuevo en Master Duel"),
         ("TCG", "Fecha del próximo regional")]
NEWS = dict(tag="TCG", cat="Producto", title="Llega un set nuevo de 100 cartas",
            rows=[("Nombre", "Crónica del Duelista"), ("A la venta", "14 de noviembre"),
                  ("Formato", "Sobres de 9 cartas"), ("Lo destacado", "Soporte para 2 arquetipos nuevos")],
            ask="¿Lo vas a abrir?", ask2="Te leo en comentarios", src="Fuente: sitio oficial Yu-Gi-Oh! TCG")
HANDLE = "@vruno_"
SAMPLE = "Contenido de ejemplo"

def page(css, body):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{FONTS}\n*{{box-sizing:border-box;margin:0;padding:0}}\nhtml,body{{width:1080px;height:1920px;overflow:hidden}}\n{css}</style></head><body>{body}</body></html>"

# =============== A: Hoja de registro ===============
A_CSS = """
body{background:#EDF0F3;color:#1E2A5A;font-family:'Plex Cond';position:relative;
 background-image:linear-gradient(#C9D2DC 2px,transparent 2px);background-size:100% 64px;background-position:0 30px}
body:before{content:'';position:absolute;left:120px;top:0;bottom:0;width:3px;background:#E3A3AC}
.wrap{position:absolute;left:170px;right:150px;top:130px}
.sample{position:absolute;right:60px;top:56px;font:600 26px 'Plex Cond';color:#D1263B;border:3px solid #D1263B;padding:6px 16px;border-radius:6px}
.form{font:600 30px 'Plex Cond';color:#5B6690;letter-spacing:.5px}
h1{font:700 128px/1.0 'Plex Cond';margin:26px 0 30px;letter-spacing:-1px}
.mark{background:linear-gradient(transparent 55%,#F6E05E 55%,#F6E05E 92%,transparent 92%)}
.hand{font-family:'Caveat';font-weight:700;color:#1D4ED8}
.week{font-size:66px;margin-bottom:60px}
.list{list-style:none}
.list li{display:flex;align-items:baseline;gap:28px;min-height:150px;padding:40px 0 30px;border-bottom:2px dashed #9AA7BD;font:500 46px 'Plex Cond'}
.box{width:44px;height:44px;border:4px solid #1E2A5A;border-radius:4px;flex:none;position:relative;top:6px}
.box:after{content:'✓';position:absolute;left:4px;top:-30px;font:700 64px 'Caveat';color:#1D4ED8}
.rg{font:700 30px 'Plex Cond';color:#fff;background:#1E2A5A;padding:4px 12px;border-radius:4px;flex:none;position:relative;top:-6px}
.swipe{margin-top:120px;font-size:70px;transform:rotate(-3deg)}
.stamp{position:absolute;right:150px;top:190px;transform:rotate(-12deg);border:9px double #D1263B;color:#D1263B;
 font:700 120px/1 'Plex Cond';padding:18px 34px;border-radius:14px;opacity:.88;letter-spacing:4px}
.field{border-bottom:3px solid #1E2A5A;padding:22px 0 14px;display:flex;justify-content:space-between;align-items:baseline;gap:30px}
.field .k{font:600 30px 'Plex Cond';color:#5B6690}
.field .v{font:700 66px/1.05 'Caveat';color:#1D4ED8;text-align:right}
.ask{margin-top:80px;font-size:76px;line-height:1;transform:rotate(-2deg)}
.ask small{display:block;font-size:52px;color:#5B6690;margin-top:14px}
.foot{margin-top:70px;font:500 30px 'Plex Cond';color:#5B6690}
.handle{position:absolute;left:170px;top:60px;font:700 30px 'Plex Cond'}
"""
def A_cover():
    lis = "".join(f"<li><span class='box'></span><span class='rg'>{r}</span>{t}</li>" for r, t in ITEMS)
    return page(A_CSS, f"""<div class='handle'>{HANDLE}</div><div class='sample'>{SAMPLE}</div>
<div class='wrap'><div class='form'>Registro semanal de noticias · Yu-Gi-Oh! juego de cartas</div>
<h1>Lo que pasó <span class='mark'>esta semana</span></h1>
<div class='week hand'>Semana del {WEEK}</div><ul class='list'>{lis}</ul>
<div class='swipe hand'>Desliza para el detalle ⟶</div></div>""")
def A_news():
    rows = "".join(f"<div class='field'><span class='k'>{k}</span><span class='v'>{v}</span></div>" for k, v in NEWS['rows'])
    return page(A_CSS, f"""<div class='handle'>{HANDLE}</div><div class='sample'>{SAMPLE}</div>
<div class='stamp'>{NEWS['tag']}</div>
<div class='wrap'><div class='form'>Noticia 1 de 4 · {NEWS['cat']}</div>
<h1 style='margin-top:250px;max-width:700px'>{NEWS['title']}</h1>{rows}
<div class='ask hand'>{NEWS['ask']}<small>{NEWS['ask2']}</small></div><div class='foot'>{NEWS['src']}</div></div>""")

# =============== B: Foil ===============
B_CSS = """
body{background:#140F2E;color:#F3F0FF;font-family:'Inter Tight';position:relative}
.foil{background:linear-gradient(115deg,#7CF5FF 0%,#B79CFF 18%,#FF9DE2 34%,#FFE59A 50%,#9DFFC8 66%,#7CB8FF 82%,#E0A8FF 100%)}
.band{position:absolute;left:-200px;right:-200px;height:250px;transform:rotate(-14deg);opacity:.95}
.band:after{content:'';position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.0) 0 14px,rgba(255,255,255,.28) 14px 16px)}
.wrap{position:absolute;left:80px;right:150px}
.top{position:absolute;left:80px;right:80px;top:70px;display:flex;justify-content:space-between;font:500 28px 'Inter Tight';color:#A79FD1}
.sample{border:2px solid #A79FD1;border-radius:40px;padding:6px 20px}
h1{font:800 104px/1.02 'Unbounded';letter-spacing:-2px}
.week{font:600 40px 'Inter Tight';color:#A79FD1;margin-top:34px}
.item{display:flex;align-items:center;gap:30px;padding:38px 0;border-top:1px solid #3A3170;font:500 44px/1.15 'Inter Tight'}
.item:last-child{border-bottom:1px solid #3A3170}
.chip{font:700 28px 'Unbounded';color:#140F2E;padding:10px 0;width:118px;text-align:center;border-radius:12px;flex:none}
.swipe{font:600 40px 'Inter Tight';margin-top:60px;color:#F3F0FF}
.badge{display:inline-block;font:900 150px/1 'Unbounded';color:#140F2E;padding:26px 46px 30px;border-radius:28px;letter-spacing:-3px}
.cat{font:600 34px 'Inter Tight';color:#A79FD1;margin:46px 0 22px}
.row{display:grid;grid-template-columns:300px 1fr;gap:30px;padding:28px 0;border-top:1px solid #3A3170}
.row .k{font:500 32px 'Inter Tight';color:#A79FD1;padding-top:6px}
.row .v{font:700 46px/1.15 'Inter Tight'}
.ask{margin-top:66px;font:800 66px/1.1 'Unbounded'}
.ask small{display:block;font:500 38px 'Inter Tight';color:#A79FD1;margin-top:18px}
.foot{margin-top:60px;font:500 30px 'Inter Tight';color:#7D74B0}
"""
def B_cover():
    its = "".join(f"<div class='item'><span class='chip foil'>{r}</span>{t}</div>" for r, t in ITEMS)
    return page(B_CSS, f"""<div class='band foil' style='top:250px'></div>
<div class='top'><span>{HANDLE}</span><span class='sample'>{SAMPLE}</span></div>
<div class='wrap' style='top:620px'><h1>Lo que pasó esta semana</h1><div class='week'>Yu-Gi-Oh! juego de cartas · {WEEK}</div>
<div style='margin-top:70px'>{its}</div><div class='swipe'>Desliza para el detalle</div></div>""")
def B_news():
    rows = "".join(f"<div class='row'><span class='k'>{k}</span><span class='v'>{v}</span></div>" for k, v in NEWS['rows'])
    return page(B_CSS, f"""<div class='band foil' style='top:1720px;opacity:.55'></div>
<div class='top'><span>{HANDLE}</span><span class='sample'>{SAMPLE}</span></div>
<div class='wrap' style='top:190px'><span class='badge foil'>{NEWS['tag']}</span>
<div class='cat'>Noticia 1 de 4 · {NEWS['cat']}</div><h1 style='font-size:84px'>{NEWS['title']}</h1>
<div style='margin-top:50px'>{rows}</div><div class='ask'>{NEWS['ask']}<small>{NEWS['ask2']}</small></div><div class='foot'>{NEWS['src']}</div></div>""")

# =============== C: Booster pop ===============
C_CSS = """
body{background:#FFD23F;color:#1B2CC1;font-family:'Bricolage';position:relative;
 background-image:radial-gradient(#F2BC1A 3px,transparent 3.5px);background-size:34px 34px}
.wrap{position:absolute;left:70px;right:140px}
.top{position:absolute;left:70px;right:70px;top:66px;display:flex;justify-content:space-between;font:700 30px 'Bricolage'}
.sample{background:#fff;border:4px solid #1B2CC1;border-radius:40px;padding:4px 20px;font-size:26px}
h1{font:800 148px/.92 'Bricolage';letter-spacing:-4px}
.panel{background:#fff;border:6px solid #1B2CC1;border-radius:34px;box-shadow:14px 14px 0 #1B2CC1;padding:20px 44px}
.item{display:flex;align-items:center;gap:26px;padding:36px 0;font:700 48px/1.1 'Bricolage'}
.item+.item{border-top:4px dotted #1B2CC1}
.tag{font:800 30px 'Bricolage';color:#fff;padding:8px 0;width:108px;text-align:center;border-radius:40px;flex:none}
.t-TCG{background:#1B2CC1}.t-OCG{background:#FF4F6D}.t-MD{background:#0FA36B}
.week{display:inline-block;background:#FF4F6D;color:#fff;font:800 44px 'Bricolage';padding:10px 28px;border-radius:16px;transform:rotate(-3deg);margin:36px 0 56px}
.swipe{font:800 56px 'Bricolage';margin-top:70px}
.sticker{position:absolute;right:120px;top:190px;width:300px;height:300px;border-radius:50%;background:#1B2CC1;color:#FFD23F;
 display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(10deg);border:8px solid #fff;box-shadow:10px 10px 0 #FF4F6D}
.sticker b{font:800 110px/1 'Bricolage';letter-spacing:-3px}.sticker span{font:700 32px 'Bricolage';color:#fff}
.row{padding:24px 0}.row+.row{border-top:4px dotted #1B2CC1}
.row .k{font:700 30px 'Bricolage';color:#FF4F6D}.row .v{font:800 52px/1.08 'Bricolage'}
.ask{margin-top:60px;display:inline-block;background:#1B2CC1;color:#fff;font:800 64px/1 'Bricolage';padding:26px 36px;border-radius:30px;transform:rotate(-2deg)}
.ask small{display:block;font:600 36px 'Bricolage';color:#FFD23F;margin-top:12px}
.foot{margin-top:56px;font:600 30px 'Bricolage'}
"""
def C_cover():
    its = "".join(f"<div class='item'><span class='tag t-{r}'>{r}</span>{t}</div>" for r, t in ITEMS)
    return page(C_CSS, f"""<div class='top'><span>{HANDLE}</span><span class='sample'>{SAMPLE}</span></div>
<div class='wrap' style='top:200px'><h1>Lo que pasó esta semana en Yu-Gi-Oh!</h1>
<div class='week'>{WEEK}</div><div class='panel'>{its}</div><div class='swipe'>Desliza, hay más 👉</div></div>""")
def C_news():
    rows = "".join(f"<div class='row'><div class='k'>{k}</div><div class='v'>{v}</div></div>" for k, v in NEWS['rows'])
    return page(C_CSS, f"""<div class='top'><span>{HANDLE}</span><span class='sample'>{SAMPLE}</span></div>
<div class='sticker'><b>{NEWS['tag']}</b><span>{NEWS['cat']}</span></div>
<div class='wrap' style='top:200px'><div style='font:700 34px Bricolage;margin-bottom:20px'>Noticia 1 de 4</div>
<h1 style='font-size:104px;max-width:600px'>{NEWS['title']}</h1>
<div class='panel' style='margin-top:50px'>{rows}</div>
<div class='ask'>{NEWS['ask']}<small>{NEWS['ask2']}</small></div><div class='foot'>{NEWS['src']}</div></div>""")

SETS = {"A_hoja": (A_cover, A_news), "B_foil": (B_cover, B_news), "C_pop": (C_cover, C_news)}
OUT = BASE / "out"; OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    for name, (cv, nw) in SETS.items():
        files = []
        for i, fn in enumerate((cv, nw)):
            h = OUT / f"{name}_{i}.html"; h.write_text(fn(), encoding="utf-8")
            pg.goto(h.as_uri()); pg.wait_for_timeout(400)
            png = OUT / f"{name}_{i}.png"; pg.screenshot(path=str(png)); files.append(png)
        ims = [Image.open(f) for f in files]
        gap = 40; W = 1080 * 2 + gap * 3; H = 1920 + gap * 2
        sheet = Image.new("RGB", (W, H), (40, 40, 44))
        for j, im in enumerate(ims): sheet.paste(im, (gap + j * (1080 + gap), gap))
        sheet.resize((W // 2, H // 2), Image.LANCZOS).save(OUT / f"propuesta_{name}.png")
    b.close()
print("ok")
