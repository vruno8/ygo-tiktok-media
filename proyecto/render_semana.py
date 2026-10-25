"""Genera las láminas del resumen semanal (estilo E Cyber Japan).

Uso:  python3 render_semana.py semanas/AAAA-MM-DD.json  <carpeta_salida>
Salida: lamina_1.jpg ... lamina_N.jpg + vista_general.png
"""
import sys, json, pathlib
BASE = pathlib.Path(__file__).parent.resolve()
_src = (BASE / "render2.py").read_text(encoding="utf-8")
exec(_src.split("RUMOR = dict(")[0].split("SETS = {")[0])  # CSS, page(), skyline(), REG, R_CSS no incluido
from playwright.sync_api import sync_playwright

REG["WCS"] = "#FFFFFF"
P_CSS = C_CSS + ".v{font-size:42px}"
R_CSS = P_CSS + """
.tape{position:absolute;left:-60px;right:-60px;height:86px;z-index:11;display:flex;align-items:center;overflow:hidden;white-space:nowrap;
 background:repeating-linear-gradient(135deg,#FFB020 0 34px,#05071A 34px 68px);border-top:4px solid #FFB020;border-bottom:4px solid #FFB020}
.tape span{background:#FFB020;color:#05071A;font:700 44px 'Chakra Petch';padding:4px 26px;margin-right:60px;letter-spacing:3px}
.hud.r{border:3px dashed #FFB020;box-shadow:0 0 30px rgba(255,176,32,.35)}
.hud.r:before{color:#FFB020;border-bottom-color:rgba(255,176,32,.4)}
"""

def cover(d):
    RUM = "<b style='color:#FFB020'>Rumor:</b>&nbsp;"
    its = "".join(
        f"<div class='it'><span class='chip' style='color:{REG[i['tag']]}'>{i['tag']}</span>"
        f"<span>{RUM if i.get('rumor') else ''}{i['texto']}</span></div>" for i in d["portada"])
    return page(P_CSS, f"""{skyline()}
<div class='sign' style='right:40px;top:170px;color:#FF3EA5'>速報</div>
<div class='sign' style='right:40px;top:470px;color:#2EF2FF;font-size:62px'>決闘者</div>
<div class='top'><span class='handle'>{d['handle']}</span></div>
<div class='jp' style='top:170px'>今週のニュース</div>
<div class='hl' style='top:240px;right:200px'>Lo que pasó esta semana</div>
<div class='hud' style='top:620px;right:180px' data-l='YU-GI-OH! JUEGO DE CARTAS // {d['semana'].upper()}'>{its}</div>
<div class='swipe' style='top:1360px'>Desliza para el detalle ▸▸</div>""")

def _flow(s, rumor):
    rows = "".join(f"<div class='row'><div class='k'>{k}</div><div class='v'>{v}</div></div>" for k, v in s['filas'])
    tape2 = (f"<div class='tape' style='position:relative;left:-130px;width:1220px;margin-top:40px;transform:rotate(4deg)'>{'<span>RUMOR · NO CONFIRMADO</span>' * 4}</div>" if rumor else "")
    cls, lab = ("hud r", "LO QUE SE SABE") if rumor else ("hud", "DATOS")
    color = "#FFB020" if rumor else "#8FA6D9"
    return f"""<div style='position:absolute;left:70px;right:70px;top:{740 if rumor else 700}px;z-index:10'>
<div class='{cls}' style='position:relative;left:0;right:0' data-l='{lab}'>{rows}</div>{tape2}
<div class='ask' style='position:relative;left:0;margin-top:44px'>{s['pregunta']}<small>Te leo en comentarios</small></div>
<div class='src' style='position:relative;left:0;margin-top:22px;color:{color}'>{s['fuente']}</div></div>"""

def news(s, n, total, handle):
    rumor = s.get("rumor", False)
    head = (f"<div class='tape' style='top:395px;transform:rotate(-4deg)'>{'<span>RUMOR · NO CONFIRMADO</span>' * 4}</div>"
            if rumor else f"<div class='jp' style='top:390px'>NOTICIA {n}/{total} · {s['categoria'].upper()}</div>")
    sign, signc = ("噂", "#FFB020") if rumor else (s['letrero'], s.get('letrero_color', '#FF3EA5'))
    return page(R_CSS if rumor else P_CSS, f"""{skyline()}
<div class='sign' style='right:40px;top:170px;color:{signc};font-size:66px'>{sign}</div>
<div class='top'><span class='handle'>{handle}</span></div>
<div class='big' style='top:150px;color:{REG[s['tag']]}'>{s['tag']}</div>{head}
<div class='hl' style='top:{510 if rumor else 460}px;font-size:80px;right:150px'>{s['titulo']}</div>
{_flow(s, rumor)}""")

def sources(d):
    rows = "".join(f"<div class='row' style='grid-template-columns:1fr'><div class='v' style='font-size:44px'>{a}</div><div class='k'>{b}</div></div>" for a, b in d["fuentes"])
    return page(P_CSS, f"""{skyline()}
<div class='sign' style='right:40px;top:170px;color:#2EF2FF;font-size:66px'>出典</div>
<div class='top'><span class='handle'>{d['handle']}</span></div>
<div class='jp' style='top:170px'>FUENTES DE ESTA SEMANA</div>
<div class='hl' style='top:240px;right:200px;font-size:96px'>Revisa la fuente oficial</div>
<div class='hud' style='top:560px;right:70px' data-l='CONSULTADAS'>{rows}</div>
<div class='swipe' style='top:1430px;color:#2EF2FF;text-shadow:0 0 14px #2EF2FF'>Sígueme: resumen cada semana</div>""")

def main(json_path, out_dir):
    d = json.loads(pathlib.Path(json_path).read_text(encoding="utf-8"))
    d.setdefault("handle", "@vruno_")
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    total = len(d["noticias"])
    pages = [cover(d)] + [news(s, i, total, d["handle"]) for i, s in enumerate(d["noticias"], 1)] + [sources(d)]
    tmp = out / "_html"; tmp.mkdir(exist_ok=True)
    files = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for i, html in enumerate(pages, 1):
            h = tmp / f"lamina_{i}.html"; h.write_text(html, encoding="utf-8")
            pg.goto(h.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(700)
            png = tmp / f"lamina_{i}.png"; pg.screenshot(path=str(png))
            jpg = out / f"lamina_{i}.jpg"; Image.open(png).convert("RGB").save(jpg, quality=88); files.append(png)
        b.close()
    ims = [Image.open(f) for f in files]; gap, cols = 30, 3
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 1080 + (cols + 1) * gap, rows * 1920 + (rows + 1) * gap), (40, 40, 44))
    for j, im in enumerate(ims): sheet.paste(im, (gap + (j % cols) * (1080 + gap), gap + (j // cols) * (1920 + gap)))
    sheet.resize((sheet.width // 3, sheet.height // 3), Image.LANCZOS).save(tmp / "vista_general.png")
    print(f"ok: {len(files)} láminas en {out}; vista general en {tmp / 'vista_general.png'}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
