import pathlib
from playwright.sync_api import sync_playwright
from PIL import Image

BASE = pathlib.Path(__file__).parent.resolve()
FS = (BASE / "node_modules/@fontsource").as_uri()
LINKS = "".join(f"<link rel='stylesheet' href='{FS}/{c}'>" for c in [
    "dotgothic16/400.css", "vt323/400.css", "chakra-petch/500.css", "chakra-petch/600.css",
    "chakra-petch/700.css", "chakra-petch/700-italic.css", "rubik-mono-one/400.css",
    "zen-kaku-gothic-new/700.css", "zen-kaku-gothic-new/900.css", "inter-tight/500.css", "inter-tight/700.css"])

WEEK = "27 oct al 2 nov"
ITEMS = [("TCG", "Set nuevo de 100 cartas"), ("OCG", "Cambios a la lista de prohibidas"),
         ("MD", "Evento nuevo en Master Duel"), ("TCG", "Fecha del próximo regional")]
NEWS = dict(tag="TCG", cat="Producto", title="Llega un set nuevo de 100 cartas",
            rows=[("Nombre", "Crónica del Duelista"), ("A la venta", "14 de noviembre"),
                  ("Formato", "Sobres de 9 cartas"), ("Lo destacado", "Soporte para 2 arquetipos nuevos")],
            ask="¿Lo vas a abrir?", ask2="Te leo en comentarios", src="Fuente: sitio oficial Yu-Gi-Oh! TCG")
HANDLE, SAMPLE = "@vruno_", "Contenido de ejemplo"

GRAIN = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 0'/></filter>"
         "<rect width='300' height='300' filter='url(%23n)'/></svg>\")")

COMMON = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1920px;overflow:hidden;position:relative}}
.fx{{position:absolute;inset:0;pointer-events:none;z-index:50;
 background:repeating-linear-gradient(0deg,rgba(0,0,0,.16) 0 2px,transparent 2px 5px),{GRAIN};
 background-size:auto,300px 300px;mix-blend-mode:overlay;opacity:.55}}
.top{{position:absolute;left:70px;right:70px;top:64px;display:flex;justify-content:space-between;align-items:center;z-index:20}}
"""

def page(css, body):
    return (f"<!doctype html><html><head><meta charset='utf-8'>{LINKS}<style>{COMMON}{css}</style></head>"
            f"<body>{body}<div class='fx'></div></body></html>")

REG = {"TCG": "#2EF2FF", "OCG": "#FF3EA5", "MD": "#C6FF3D"}

# ======================= VAPORWAVE =======================
V_CSS = """
body{background:linear-gradient(180deg,#24104F 0%,#5B1E86 30%,#C2449F 52%,#FF8FC8 62%,#FFC6E4 68.5%,#2A0B4A 68.6%);font-family:'Inter Tight';color:#24104F}
.sun{position:absolute;left:50%;width:600px;height:600px;margin-left:-300px;border-radius:50%;
 background:linear-gradient(180deg,#FFF27A 0%,#FFB347 40%,#FF4FA3 80%);
 -webkit-mask:linear-gradient(#000 0 50%,transparent 0) top/100% 100% no-repeat,repeating-linear-gradient(180deg,#000 0 26px,transparent 26px 40px) bottom/100% 50% no-repeat;
 filter:drop-shadow(0 0 60px rgba(255,120,190,.7))}
.floor{position:absolute;left:-600px;right:-600px;top:1316px;height:1300px;transform-origin:top;transform:perspective(500px) rotateX(62deg);
 background:linear-gradient(transparent 0 0),repeating-linear-gradient(90deg,#FF4FD8 0 4px,transparent 4px 120px),repeating-linear-gradient(0deg,#FF4FD8 0 4px,transparent 4px 120px),#2A0B4A;
 box-shadow:inset 0 40px 80px rgba(255,79,216,.45);z-index:0}
.kata{position:absolute;right:46px;writing-mode:vertical-rl;font:400 120px/1 'DotGothic16';color:rgba(255,255,255,.9);
 text-shadow:5px 0 0 #2EF2FF,-5px 0 0 #FF3EA5;letter-spacing:10px;z-index:3}
.handle{font:400 44px 'VT323';color:#fff}
.sample{font:400 34px 'VT323';color:#24104F;background:#FFF27A;padding:2px 16px;border:3px solid #24104F}
.hl{position:absolute;left:70px;right:200px;font:400 104px/1.02 'Rubik Mono One';color:#fff;transform:skew(-8deg);z-index:5;
 text-shadow:6px 6px 0 #2EF2FF,-5px -3px 0 #FF3EA5,12px 12px 0 #24104F}
.jp{position:absolute;left:70px;font:400 46px 'DotGothic16';color:#FFF27A;z-index:5;text-shadow:3px 3px 0 #24104F}
.win{position:absolute;left:70px;right:110px;background:#EDE3FF;border:4px solid #24104F;box-shadow:16px 16px 0 #24104F, inset -4px -4px 0 #B9A6E8, inset 4px 4px 0 #fff;z-index:6}
.bar{height:72px;background:linear-gradient(90deg,#24104F,#7A3BD1 60%,#2EF2FF);display:flex;align-items:center;justify-content:space-between;padding:0 14px 0 22px;
 font:400 44px 'VT323';color:#fff}
.btns{display:flex;gap:10px}.btns i{width:48px;height:44px;background:#EDE3FF;border:3px solid #24104F;box-shadow:inset -3px -3px 0 #B9A6E8,inset 3px 3px 0 #fff;
 font:normal 400 36px/38px 'VT323';color:#24104F;text-align:center}
.body{padding:26px 40px 34px}
.it{display:flex;align-items:center;gap:24px;padding:24px 0;font:700 44px/1.15 'Inter Tight'}
.it+.it{border-top:3px dashed #9B86D6}
.chip{font:400 40px/1 'VT323';color:#24104F;width:104px;text-align:center;padding:8px 0;border:3px solid #24104F;flex:none}
.swipe{position:absolute;left:0;right:0;text-align:center;font:400 64px 'VT323';color:#fff;z-index:12;transform:translateZ(0);text-shadow:3px 3px 0 #FF3EA5}
.k{font:400 36px 'VT323';color:#7A3BD1;letter-spacing:1px}.v{font:700 46px/1.12 'Inter Tight';margin-top:2px}
.row{padding:14px 0}.row+.row{border-top:3px dashed #9B86D6}
.tag{position:absolute;right:66px;z-index:8;transform:rotate(8deg);font:400 96px/1 'Rubik Mono One';color:#24104F;padding:22px 30px;border:5px solid #24104F;box-shadow:10px 10px 0 #24104F}
.dlg{position:absolute;left:150px;right:150px;z-index:9;background:#EDE3FF;border:4px solid #24104F;box-shadow:14px 14px 0 #FF3EA5}
.dlg .bar{height:62px;font-size:38px;background:linear-gradient(90deg,#FF3EA5,#7A3BD1)}
.dlg p{font:700 54px/1.1 'Inter Tight';padding:28px 34px 10px}
.dlg .ok{display:flex;gap:22px;padding:14px 34px 30px}
.dlg .ok span{font:400 40px 'VT323';padding:6px 26px;border:3px solid #24104F;box-shadow:inset -3px -3px 0 #B9A6E8,inset 3px 3px 0 #fff}
.src{position:absolute;left:70px;z-index:12;transform:translateZ(0);font:400 36px 'VT323';color:#fff}
"""
BTNS = "<span class='btns'><i>_</i><i>□</i><i>×</i></span>"
def V_cover():
    its = "".join(f"<div class='it'><span class='chip' style='background:{REG[r]}'>{r}</span>{t}</div>" for r, t in ITEMS)
    return page(V_CSS, f"""<div class='sun' style='top:830px;margin-left:-60px'></div><div class='floor'></div>
<div class='kata' style='top:150px;font-size:96px'>今週の決闘</div>
<div class='top'><span class='handle'>{HANDLE}</span><span class='sample'>{SAMPLE}</span></div>
<div class='hl' style='top:170px'>Lo que pasó esta semana</div>
<div class='jp' style='top:560px'>今週のカードゲームニュース</div>
<div class='win' style='top:650px;right:250px'><div class='bar'><span>resumen_{WEEK.replace(' ','_')}.exe</span>{BTNS}</div><div class='body'>{its}</div></div>
<div class='swipe' style='top:1410px'>desliza ▶▶ hay más</div>""")
def V_news():
    rows = "".join(f"<div class='row'><div class='k'>{k}</div><div class='v'>{v}</div></div>" for k, v in NEWS['rows'])
    return page(V_CSS, f"""<div class='sun' style='top:830px;margin-left:-60px'></div><div class='floor'></div>
<div class='top'><span class='handle'>{HANDLE}</span><span class='sample'>{SAMPLE}</span></div>
<div class='jp' style='top:150px'>速報 · 新弾</div>
<div class='hl' style='top:330px;font-size:76px;right:110px'>{NEWS['title']}</div>
<div class='tag' style='top:130px;font-size:76px;background:{REG[NEWS['tag']]}'>{NEWS['tag']}</div>
<div class='win' style='top:640px'><div class='bar'><span>noticia_01_{NEWS['cat'].lower()}.exe</span>{BTNS}</div><div class='body'>{rows}</div></div>
<div class='dlg' style='top:1250px;left:240px;right:70px'><div class='bar'><span>pregunta.exe</span>{BTNS}</div><p>{NEWS['ask']}</p>
<div class='ok'><span>Sí</span><span>No</span><span>{NEWS['ask2']}</span></div></div>
<div class='src' style='top:1545px'>{NEWS['src']}</div>""")

# ======================= CYBER JAPAN =======================
C_CSS = """
body{background:radial-gradient(120% 60% at 50% 100%,#3A0F5E 0%,transparent 60%),linear-gradient(180deg,#05071A 0%,#0A1140 55%,#13093A 100%);color:#EAF6FF;font-family:'Chakra Petch'}
.rain{position:absolute;inset:0;z-index:2;background:repeating-linear-gradient(103deg,transparent 0 22px,rgba(160,200,255,.10) 22px 23px,transparent 23px 61px);}
.sky{position:absolute;left:0;right:0;bottom:0;height:1150px;z-index:1;display:flex;align-items:flex-end;gap:6px;padding:0 0 380px}
.bld{flex:1;background:#0B0F33;position:relative;border-top:2px solid #1B2466;
 background-image:repeating-linear-gradient(0deg,transparent 0 22px,rgba(255,214,120,.0) 22px 30px),repeating-linear-gradient(90deg,rgba(120,200,255,.16) 0 8px,transparent 8px 22px),repeating-linear-gradient(0deg,rgba(120,200,255,.0) 0 14px,#0B0F33 14px 26px)}
.refl{position:absolute;left:0;right:0;bottom:0;height:380px;z-index:1;background:linear-gradient(180deg,#0B0F33,#0A0626);}
.refl:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,62,165,.0) 0 60px,rgba(255,62,165,.22) 60px 66px,transparent 66px 140px,rgba(46,242,255,.18) 140px 146px,transparent 146px 230px);filter:blur(6px)}
.sign{position:absolute;z-index:3;writing-mode:vertical-rl;font:900 78px/1 'Zen Kaku Gothic New';padding:22px 12px;border:4px solid currentColor;border-radius:10px;letter-spacing:12px;
 text-shadow:0 0 12px currentColor,0 0 30px currentColor;box-shadow:0 0 24px currentColor,inset 0 0 24px currentColor;background:rgba(5,7,26,.55)}
.handle{font:600 34px 'Chakra Petch';color:#2EF2FF;text-shadow:0 0 12px #2EF2FF}
.sample{font:600 26px 'Chakra Petch';color:#C6FF3D;border:2px solid #C6FF3D;padding:4px 14px;box-shadow:0 0 12px rgba(198,255,61,.6)}
.hl{position:absolute;left:70px;right:70px;z-index:10;font:700 112px/.98 'Chakra Petch';text-transform:none;color:#fff;
 text-shadow:-5px 0 0 rgba(46,242,255,.9),5px 0 0 rgba(255,62,165,.9),0 0 40px rgba(255,62,165,.5)}
.jp{position:absolute;left:72px;z-index:10;font:700 44px 'Zen Kaku Gothic New';color:#FF3EA5;letter-spacing:6px;text-shadow:0 0 14px #FF3EA5}
.hud{position:absolute;left:70px;right:150px;z-index:10;background:rgba(5,7,26,.86);border:2px solid #2EF2FF;padding:22px 40px 28px;
 box-shadow:0 0 30px rgba(46,242,255,.45),inset 0 0 40px rgba(46,242,255,.08);clip-path:polygon(0 0,calc(100% - 46px) 0,100% 46px,100% 100%,46px 100%,0 calc(100% - 46px))}
.hud:before{content:attr(data-l);display:block;font:600 28px 'Chakra Petch';color:#2EF2FF;letter-spacing:2px;padding-bottom:12px;border-bottom:1px solid rgba(46,242,255,.4)}
.it{display:flex;align-items:center;gap:24px;padding:26px 0;font:600 44px/1.15 'Chakra Petch'}
.it+.it{border-top:1px solid rgba(46,242,255,.25)}
.chip{font:700 32px 'Chakra Petch';width:110px;text-align:center;padding:6px 0;border:2px solid currentColor;flex:none;text-shadow:0 0 10px currentColor;box-shadow:0 0 14px currentColor,inset 0 0 10px currentColor}
.swipe{position:absolute;left:70px;z-index:10;font:700 48px 'Chakra Petch';color:#C6FF3D;text-shadow:0 0 14px #C6FF3D}
.row{display:grid;grid-template-columns:270px 1fr;gap:20px;padding:22px 0}.row+.row{border-top:1px solid rgba(46,242,255,.25)}
.k{font:500 32px 'Chakra Petch';color:#8FA6D9;padding-top:6px}.v{font:700 46px/1.12 'Chakra Petch'}
.big{position:absolute;left:66px;z-index:10;font:700 210px/1 'Chakra Petch';letter-spacing:6px;
 text-shadow:0 0 18px currentColor,0 0 50px currentColor,-6px 0 0 rgba(255,62,165,.7)}
.ask{position:absolute;left:70px;z-index:10;font:700 68px/1.05 'Chakra Petch';color:#fff;text-shadow:0 0 20px #FF3EA5}
.ask small{display:block;font:600 38px 'Chakra Petch';color:#FF3EA5;margin-top:12px}
.src{position:absolute;left:70px;z-index:10;font:500 28px 'Chakra Petch';color:#8FA6D9}
"""
def skyline():
    hs = [520, 760, 430, 900, 610, 820, 480, 700, 560]
    return "<div class='sky'>" + "".join(f"<div class='bld' style='height:{h}px'></div>" for h in hs) + "</div><div class='refl'></div><div class='rain'></div>"
def C_cover():
    its = "".join(f"<div class='it'><span class='chip' style='color:{REG[r]}'>{r}</span>{t}</div>" for r, t in ITEMS)
    return page(C_CSS, f"""{skyline()}
<div class='sign' style='right:40px;top:170px;color:#FF3EA5'>速報</div>
<div class='sign' style='right:40px;top:470px;color:#2EF2FF;font-size:62px'>決闘者</div>
<div class='top'><span class='handle'>{HANDLE}</span><span class='sample'>{SAMPLE}</span></div>
<div class='jp' style='top:170px'>今週のニュース</div>
<div class='hl' style='top:240px;right:200px'>Lo que pasó esta semana</div>
<div class='hud' style='top:620px;right:180px' data-l='YU-GI-OH! JUEGO DE CARTAS // {WEEK.upper()}'>{its}</div>
<div class='swipe' style='top:1330px'>Desliza para el detalle ▸▸</div>""")
def C_news():
    rows = "".join(f"<div class='row'><div class='k'>{k}</div><div class='v'>{v}</div></div>" for k, v in NEWS['rows'])
    return page(C_CSS, f"""{skyline()}
<div class='sign' style='right:40px;top:170px;color:#C6FF3D;font-size:66px'>新弾</div>
<div class='top'><span class='handle'>{HANDLE}</span><span class='sample'>{SAMPLE}</span></div>
<div class='big' style='top:150px;color:{REG[NEWS['tag']]}'>{NEWS['tag']}</div>
<div class='jp' style='top:390px'>NOTICIA 1/4 · {NEWS['cat'].upper()}</div>
<div class='hl' style='top:460px;font-size:86px;right:190px'>{NEWS['title']}</div>
<div class='hud' style='top:720px;right:110px' data-l='DATOS'>{rows}</div>
<div class='ask' style='top:1350px'>{NEWS['ask']}<small>{NEWS['ask2']}</small></div>
<div class='src' style='top:1500px'>{NEWS['src']}</div>""")

RUMOR = dict(tag="TCG", title="Posible reimpresión de un set clásico",
             rows=[("Qué se dice", "Volvería a la venta a inicios de 2027"), ("Origen", "Filtración de una tienda"),
                   ("Estado", "Sin confirmar por Konami")],
             ask="¿Crees que se confirma?", ask2="Te leo en comentarios", src="Fuente: [sitio no oficial]")
R_CSS = C_CSS + """
.tape{position:absolute;left:-60px;right:-60px;height:86px;z-index:11;transform:rotate(-4deg);display:flex;align-items:center;overflow:hidden;white-space:nowrap;
 background:repeating-linear-gradient(135deg,#FFB020 0 34px,#05071A 34px 68px);border-top:4px solid #FFB020;border-bottom:4px solid #FFB020}
.tape span{background:#FFB020;color:#05071A;font:700 44px 'Chakra Petch';padding:4px 26px;margin-right:60px;letter-spacing:3px}
.hud.r{border:3px dashed #FFB020;box-shadow:0 0 30px rgba(255,176,32,.35)}
.hud.r:before{color:#FFB020;border-bottom-color:rgba(255,176,32,.4)}
"""
def C_rumor():
    rows = "".join(f"<div class='row'><div class='k'>{k}</div><div class='v'>{v}</div></div>" for k, v in RUMOR['rows'])
    tape = "<span>RUMOR · NO CONFIRMADO</span>" * 4
    return page(R_CSS, f"""{skyline()}
<div class='sign' style='right:40px;top:170px;color:#FFB020;font-size:70px'>噂</div>
<div class='top'><span class='handle'>{HANDLE}</span><span class='sample'>{SAMPLE}</span></div>
<div class='big' style='top:150px;color:{REG[RUMOR['tag']]}'>{RUMOR['tag']}</div>
<div class='tape' style='top:395px'>{tape}</div>
<div class='hl' style='top:510px;font-size:82px;right:150px'>{RUMOR['title']}</div>
<div class='hud r' style='top:740px;right:70px' data-l='LO QUE SE SABE'>{rows}</div>
<div class='tape' style='top:1250px;transform:rotate(4deg)'>{tape}</div>
<div class='ask' style='top:1380px'>{RUMOR['ask']}<small>{RUMOR['ask2']}</small></div>
<div class='src' style='top:1530px;color:#FFB020'>{RUMOR['src']}</div>""")

SETS = {"D_vaporwave": (V_cover, V_news), "E_cyberjapan": (C_cover, C_news), "E_rumor": (C_news, C_rumor)}
OUT = BASE / "out"; OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    for name, fns in SETS.items():
        files = []
        for i, fn in enumerate(fns):
            h = OUT / f"{name}_{i}.html"; h.write_text(fn(), encoding="utf-8")
            pg.goto(h.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(700)
            png = OUT / f"{name}_{i}.png"; pg.screenshot(path=str(png)); files.append(png)
        ims = [Image.open(f) for f in files]; gap = 40
        sheet = Image.new("RGB", (1080 * 2 + gap * 3, 1920 + gap * 2), (40, 40, 44))
        for j, im in enumerate(ims): sheet.paste(im, (gap + j * (1080 + gap), gap))
        sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS).save(OUT / f"propuesta_{name}.png")
    b.close()
print("ok")
