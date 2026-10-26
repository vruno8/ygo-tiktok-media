"""Láminas de top 8 de torneo (estilo E Cyber Japan).

Uso: python3 render_torneo.py <torneo.json> <config.json> <carpeta_salida>
- torneo.json: salida de extraer_top.py + cruzar_banlist.py
- config.json: textos editoriales (título, bajada, pregunta, fuentes)
"""
import sys, json, pathlib
BASE = pathlib.Path(__file__).resolve().parent.parent
_src = (BASE / "render2.py").read_text(encoding="utf-8")
exec(_src.split("RUMOR = dict(")[0].split("SETS = {")[0].replace("pathlib.Path(__file__)", f"pathlib.Path(r'{BASE / 'render2.py'}')"))
from playwright.sync_api import sync_playwright

STAPLES = {"Ash Blossom & Joyous Spring", "Ghost Ogre & Snow Rabbit", "Effect Veiler", "Mulcharmy Fuwalos", "Mulcharmy Purulia",
           "Nibiru, the Primal Being", "Infinite Impermanence", "Dominus Impulse", "Dominus Purge", "Dominus Spark",
           "Pot of Desires", "Foolish Burial Goods", "Droll & Lock Bird", "Called by the Grave", "Triple Tactics Talent",
           "Crossout Designator", "Maxx \"C\"", "Kuriboh - Multiply!"}
POS = {"Winner": ("Campeón", "#C6FF3D"), "Runner-Up": ("Finalista", "#2EF2FF"), "Top 4": ("Top 4", "#FF3EA5"), "Top 8": ("Top 8", "#B79CFF")}
PAIS = {"United States": "EE.UU.", "Canada": "Canadá", "United Kingdom": "Reino Unido", "Mexico": "México"}

T_CSS = C_CSS + """
.pos{position:absolute;left:66px;z-index:10;font:700 150px/1 'Chakra Petch';letter-spacing:2px;text-shadow:0 0 18px currentColor,0 0 46px currentColor,-5px 0 0 rgba(255,62,165,.6)}
.who{position:absolute;left:72px;right:200px;z-index:10;font:600 46px/1.15 'Chakra Petch';color:#fff}
.who small{display:block;font:500 32px 'Chakra Petch';color:#8FA6D9;margin-top:6px}
.deck{position:absolute;left:70px;right:150px;z-index:10;font:700 70px/1.02 'Chakra Petch';color:#fff;
 text-shadow:-4px 0 0 rgba(46,242,255,.9),4px 0 0 rgba(255,62,165,.9),0 0 30px rgba(255,62,165,.4)}
.stack{position:absolute;left:70px;right:70px;z-index:10;display:flex;flex-direction:column;gap:24px}
.hud{position:relative;left:0;right:0}
.cnt{display:flex;gap:18px;padding:16px 0 4px}
.cnt div{flex:1;border:1px solid rgba(46,242,255,.35);padding:12px 16px}
.cnt b{display:block;font:700 56px/1 'Chakra Petch';color:#fff}
.cnt span{font:500 28px 'Chakra Petch';color:#8FA6D9}
.mix{font:500 30px 'Chakra Petch';color:#8FA6D9;padding:12px 0 2px}
.cards{list-style:none;padding:8px 0 0}
.cards li{font:600 36px/1.15 'Chakra Petch';padding:9px 0;border-top:1px solid rgba(46,242,255,.22)}
.cards li:first-child{border-top:0}
.cards em{font-style:normal;color:#2EF2FF;margin-right:14px}
.hud.loss{border-color:#FF3EA5;box-shadow:0 0 30px rgba(255,62,165,.4)}
.hud.loss:before{color:#FF3EA5;border-bottom-color:rgba(255,62,165,.4)}
.hud.ok{border-color:#C6FF3D;box-shadow:0 0 30px rgba(198,255,61,.35)}
.hud.ok:before{color:#C6FF3D;border-bottom-color:rgba(198,255,61,.4)}
.st{display:inline-block;font:700 26px 'Chakra Petch';padding:2px 10px;margin-right:12px;border:2px solid currentColor;vertical-align:4px}
.f{color:#FF3EA5}.l{color:#FFB020}
.bar{display:flex;align-items:center;gap:22px;padding:22px 0;font:600 42px 'Chakra Petch'}
.bar+.bar{border-top:1px solid rgba(46,242,255,.25)}
.bar .n{font:700 72px/1 'Chakra Petch';width:70px;text-align:center}
.bar .t{flex:1}
.blocks{display:flex;gap:8px}.blocks i{width:46px;height:46px;display:block;box-shadow:0 0 12px currentColor}
"""

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def cover(t, c):
    w = t["listas"][0]
    return page(T_CSS, f"""{skyline()}
<div class='sign' style='right:40px;top:170px;color:#C6FF3D'>大会</div>
<div class='sign' style='right:40px;top:440px;color:#FF3EA5;font-size:58px'>ベスト8</div>
<div class='top'><span class='handle'>{c['handle']}</span></div>
<div class='jp' style='top:170px;right:200px;font-size:36px'>{esc(c['etiqueta'])}</div>
<div class='hl' style='top:240px;right:200px;font-size:104px'>{esc(c['titulo'])}</div>
<div class='stack' style='top:620px;right:180px'>
<div class='hud' data-l='{esc(c["dato_portada"])}'>
 <div class='row'><div class='k'>Campeón</div><div class='v'>{esc(w['jugador'])}</div></div>
 <div class='row'><div class='k'>Con</div><div class='v'>{esc(w['deck'])}</div></div>
 <div class='row'><div class='k'>Por qué importa</div><div class='v'>{esc(c['bajada'])}</div></div>
</div></div>
<div class='swipe' style='top:1360px'>Sigue mirando ▸▸</div>""")

def reparto(t, c):
    top = [l for l in t["listas"] if l["top8"]]
    cnt = {}
    for l in top: cnt[l["arquetipo_pagina"]] = cnt.get(l["arquetipo_pagina"], 0) + 1
    cols = ["#FF3EA5", "#2EF2FF", "#C6FF3D", "#B79CFF", "#FFB020"]
    bars = "".join(f"<div class='bar'><span class='n' style='color:{cols[i]}'>{n}</span><span class='t'>{esc(a)}</span>"
                   f"<span class='blocks' style='color:{cols[i]}'>{''.join('<i style=\"background:currentColor\"></i>' for _ in range(n))}</span></div>"
                   for i, (a, n) in enumerate(sorted(cnt.items(), key=lambda x: -x[1])))
    tot = sum(1 for l in top for a in l["afectadas"])
    return page(T_CSS, f"""{skyline()}
<div class='sign' style='right:40px;top:170px;color:#2EF2FF;font-size:66px'>分布</div>
<div class='top'><span class='handle'>{c['handle']}</span></div>
<div class='jp' style='top:170px'>EL TOP 8 EN NÚMEROS</div>
<div class='hl' style='top:240px;right:200px;font-size:96px'>{esc(c.get('titulo_reparto', 'Solo 3 decks en el top 8'))}</div>
<div class='stack' style='top:620px'>
<div class='hud' data-l='DECKS EN EL TOP 8'>{bars}</div>
<div class='hud loss' data-l='{esc(c.get("etiqueta_reparto", "DESPUÉS DEL 19/10"))}'><div class='mix' style='font:600 40px/1.2 Chakra Petch;color:#fff;padding:14px 0'>{esc(c['dato_reparto'])}</div></div>
</div>""")

def deck_slide(l, n, c):
    lab, col = POS[l["posicion"]]
    tot = lambda k: sum(x["copias"] for x in l[k]["cartas"])
    tipos = {"m": 0, "s": 0, "t": 0}
    for x in l["main"]["cartas"]:
        tipos["m" if "Monster" in x["tipo"] else "s" if "Spell" in x["tipo"] else "t"] += x["copias"]
    copias = {x["nombre"]: x["copias"] for x in l["main"]["cartas"]}
    motor = [x["nombre"] for x in sorted(l["main"]["cartas"], key=lambda x: -x["copias"]) if x["copias"] == 3 and x["nombre"] not in STAPLES][:3]
    if len(motor) < 3:
        motor += [x["nombre"] for x in l["main"]["cartas"] if x["copias"] == 2 and x["nombre"] not in STAPLES and x["nombre"] not in motor][:3 - len(motor)]
    lis = "".join(f"<li><em>{copias[m]}x</em>{esc(m)}</li>" for m in motor)
    af = l["afectadas"]
    claves = {w.lower() for w in l["deck"].replace("-", " ").split() if len(w) > 3}
    del_deck = lambda a: any(w in a["nombre"].lower() for w in claves)
    # primero: prohibidas del propio arquetipo; luego otras del motor; staples al final
    prioridad = sorted(af, key=lambda a: (a["cambio_19_10"] != "Forbidden", not del_deck(a), a["nombre"] in STAPLES, a["seccion"] != "main"))
    nf = sum(1 for a in af if a["cambio_19_10"] == "Forbidden"); nl = len(af) - nf
    motor_tocado = any((a["nombre"] not in STAPLES) for a in af if a["seccion"] in ("main", "extra"))
    if not motor_tocado:
        loss = (f"<div class='hud ok' data-l='QUÉ PERDIÓ EL 19/10'><ul class='cards'>"
                f"<li style='color:#C6FF3D'>Su motor quedó intacto</li>"
                + "".join(f"<li><span class='st {'f' if a['cambio_19_10']=='Forbidden' else 'l'}'>{'PROHIBIDA' if a['cambio_19_10']=='Forbidden' else 'LIMITADA'}</span>{esc(a['nombre'])}</li>" for a in prioridad[:2])
                + "</ul></div>")
    else:
        mostrar = prioridad[:3]; resto = len(af) - len(mostrar)
        loss = (f"<div class='hud loss' data-l='QUÉ PERDIÓ EL 19/10 · {nf} {"PROHIBIDA" if nf==1 else "PROHIBIDAS"} · {nl} {"LIMITADA" if nl==1 else "LIMITADAS"}'><ul class='cards'>"
                + "".join(f"<li><span class='st {'f' if a['cambio_19_10']=='Forbidden' else 'l'}'>{'PROHIBIDA' if a['cambio_19_10']=='Forbidden' else 'LIMITADA'}</span>{esc(a['nombre'])}</li>" for a in mostrar)
                + (f"<li style='color:#8FA6D9'>y {resto} más</li>" if resto > 0 else "") + "</ul></div>")
    return page(T_CSS, f"""{skyline()}
<div class='sign' style='right:40px;top:170px;color:{col};font-size:66px'>{'優勝' if l['posicion']=='Winner' else '決闘'}</div>
<div class='top'><span class='handle'>{c['handle']}</span></div>
<div class='pos' style='top:130px;color:{col}'>{lab}</div>
<div class='who' style='top:310px'>{esc(l['jugador'])}<small>{PAIS.get(l['pais'], l['pais'] or '')} · lista {n} de 8</small></div>
<div class='deck' style='top:430px;font-size:{60 if len(l["deck"])>34 else 70}px'>{esc(l['deck'])}</div>
<div class='stack' style='top:{650 if len(l['deck'])>34 else 590}px'>
<div class='hud' data-l='LA LISTA'>
 <div class='cnt'><div><b>{tot('main')}</b><span>Main</span></div><div><b>{tot('extra')}</b><span>Extra</span></div><div><b>{tot('side')}</b><span>Side</span></div></div>
 <div class='mix'>{tipos['m']} monstruos, {tipos['s']} mágicas, {tipos['t']} trampas</div>
 <ul class='cards' style='margin-top:6px'>{lis}</ul>
</div>{loss}</div>""")

_PLEX = (BASE / "node_modules/@fontsource/ibm-plex-sans-condensed/files").as_uri()
FULL_CSS = T_CSS + "".join(f"@font-face{{font-family:'Plex Cond';font-weight:{w};src:url('{_PLEX}/ibm-plex-sans-condensed-latin-{w}-normal.woff2') format('woff2');}}" for w in (500, 600)) + """
.pos2{position:absolute;left:66px;top:118px;z-index:10;font:700 96px/1 'Chakra Petch';text-shadow:0 0 16px currentColor,0 0 40px currentColor}
.who2{position:absolute;left:70px;right:190px;top:232px;z-index:10;font:600 38px/1.1 'Chakra Petch';color:#fff}
.who2 span{color:#8FA6D9;font-weight:500}
.deck2{position:absolute;left:70px;right:190px;top:278px;z-index:10;font:700 40px/1.05 'Chakra Petch';color:#fff;
 text-shadow:-3px 0 0 rgba(46,242,255,.9),3px 0 0 rgba(255,62,165,.9)}
.list{position:absolute;left:36px;right:36px;z-index:10;background:rgba(5,7,26,.88);border:2px solid #2EF2FF;padding:10px 16px 14px;
 box-shadow:0 0 26px rgba(46,242,255,.35)}
.sec{display:flex;align-items:center;gap:14px;font:700 26px 'Chakra Petch';color:#2EF2FF;letter-spacing:1px;margin:8px 0 6px}
.sec b{font:700 30px 'Chakra Petch';color:#05071A;background:#2EF2FF;padding:0 12px}
.sec .ty{margin-left:auto;display:flex;gap:6px}
.sec .ty i{font:700 24px 'Plex Cond';font-style:normal;color:#05071A;padding:0 10px;min-width:44px;text-align:center}
.grid{display:grid;grid-template-columns:repeat(var(--cols,3),1fr);gap:6px}
.c{display:flex;align-items:stretch;height:var(--h);background:#0B1036;border:1px solid rgba(143,166,217,.25);overflow:hidden;position:relative}
.c .fr{width:12px;flex:none}
.c .q{width:var(--qw,44px);flex:none;display:flex;align-items:center;justify-content:center;font:700 28px 'Chakra Petch';color:#fff;background:rgba(255,255,255,.06)}
.c .n{flex:1;padding:0 8px;display:flex;align-items:center;font:500 var(--fs)/1.04 'Plex Cond';color:#EAF6FF;overflow:hidden}
.c .n span{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.c.ban{border-color:#FF3EA5;box-shadow:inset 0 0 0 1px #FF3EA5}
.c.lim{border-color:#FFB020;box-shadow:inset 0 0 0 1px #FFB020}
.c.ban .n,.c.lim .n{padding-right:54px}
.c .tag{position:absolute;right:0;top:0;font:700 15px/1 'Chakra Petch';padding:3px 5px;color:#05071A}
.leg{display:flex;gap:22px;font:500 22px 'Chakra Petch';color:#8FA6D9;margin-top:10px;flex-wrap:wrap}
.leg i{display:inline-block;width:18px;height:18px;margin-right:8px;vertical-align:-2px}
.gh{grid-column:1/-1;display:flex;align-items:center;gap:10px;font:700 19px/1 'Chakra Petch';letter-spacing:2px;margin:4px 0 0;height:22px}
.gh:after{content:'';flex:1;height:1px;background:currentColor;opacity:.45}
.c.semi{border-color:#C6FF3D;box-shadow:inset 0 0 0 1px #C6FF3D}
.c.ban .n,.c.lim .n,.c.semi .n{padding-right:50px}
.list[style*="--cols:4"] .c .em{font-size:22px;right:4px}
.list[style*="--cols:4"] .c.ban .n,.list[style*="--cols:4"] .c.lim .n,.list[style*="--cols:4"] .c.semi .n{padding-right:32px}
.c .em{position:absolute;right:6px;top:50%;transform:translateY(-50%);font:28px/1 'Noto Color Emoji';
 filter:drop-shadow(0 0 4px var(--g)) drop-shadow(0 0 10px var(--g))}
.leg .e{font:24px/1 'Noto Color Emoji';margin-right:8px;vertical-align:-3px;filter:drop-shadow(0 0 6px var(--g))}
"""
FRAME = [("Ritual", "#7FA8D8"), ("Fusion", "#A086B7"), ("Synchro", "#E9E9E9"), ("Xyz", "#3A3A3A"), ("Link", "#2A5BD7"),
         ("Pendulum", "linear-gradient(#FF8B53 50%,#1D9E74 50%)"), ("Normal Monster", "#E8C35A"), ("Monster", "#FF8B53"),
         ("Spell", "#1D9E74"), ("Trap", "#BC5A84")]
def frame(t):
    if "Spell" in t: return "#1D9E74"   # "Ritual Spell" es mágica, no monstruo ritual
    if "Trap" in t: return "#BC5A84"
    return next(col for k, col in FRAME if k in t)
def grupo(t): return 0 if "Monster" in t else 1 if "Spell" in t else 2

EXTRA_ORDEN = ["Fusion", "Synchro", "Xyz", "Link"]
MARCA = {"Forbidden": ("ban", "🚫", "#FF3EA5"), "Limited": ("lim", "1️⃣", "#FFB020"), "Semi-Limited": ("semi", "2️⃣", "#C6FF3D")}
GRUPOS = [("MONSTRUOS", "#FF8B53"), ("MÁGICAS", "#1D9E74"), ("TRAMPAS", "#E07AA8")]

def deck_full(l, n, c, total=8):
    lab, col = POS[l["posicion"]]
    af = {a["nombre"]: a["cambio_19_10"] for a in l["afectadas"]}
    estado = lambda x: x.get("estado_actual") if "estado_actual" in x else af.get(x["nombre"])
    unicas = sum(len(l[k]["cartas"]) for k in ("main", "extra", "side"))
    cols = 4 if unicas > 50 else 3   # listas muy largas (p. ej. 60 cartas) pasan a 4 columnas
    ancho = lambda x: 2 if cols == 4 and len(x["nombre"]) > 34 else 1   # en 4 columnas, los nombres largos ocupan 2 celdas
    def filas_sec(k):
        if k == "extra": return -(-sum(ancho(x) for x in l[k]["cartas"]) // cols), 0
        gs = [sum(ancho(x) for x in l[k]["cartas"] if grupo(x["tipo"]) == g) for g in (0, 1, 2)]
        return sum(-(-v // cols) for v in gs), sum(1 for v in gs if v)
    fm, gm = filas_sec("main"); fe, _ = filas_sec("extra"); fsd, gsd = filas_sec("side")
    nf = fm + fe + fsd; ngh = gm + gsd
    top_y = 380 if len(l["deck"]) > 40 else 336
    h = max(38, min(62, int((1545 - top_y - 3 * 50 - 64 - ngh * 30) / nf) - 6)); fs = 25 if h >= 54 else 22 if h >= 46 else 20
    if cols == 4: fs = min(fs, 19)
    def seccion(k, nombre):
        sub = lambda t: next((i for i, s in enumerate(EXTRA_ORDEN) if s in t), 9)
        cs = sorted(l[k]["cartas"], key=lambda x: (grupo(x["tipo"]), sub(x["tipo"]) if k == "extra" else 0, -x["copias"], x["nombre"]))
        tot = sum(x["copias"] for x in cs)
        cnt = [sum(x["copias"] for x in cs if grupo(x["tipo"]) == g) for g in (0, 1, 2)]
        ty = "".join(f"<i style='background:{bg}'>{v}</i>" for v, bg in zip(cnt, ("#FF8B53", "#1D9E74", "#BC5A84")) if v) if k != "extra" else ""
        tiles = ""; g_prev = None
        for x in cs:
            g = grupo(x["tipo"])
            if k != "extra" and g != g_prev:
                nom_g, col_g = GRUPOS[g]
                tiles += f"<div class='gh' style='color:{col_g}'>{nom_g} · {cnt[g]}</div>"
                g_prev = g
            st = estado(x)
            cls = f" {MARCA[st][0]}" if st else ""
            tag = f"<span class='em' style='--g:{MARCA[st][2]}'>{MARCA[st][1]}</span>" if st else ""
            fr = frame(x["tipo"])
            lim_len = (18 if st else 24) if cols == 4 and ancho(x) == 1 else (60 if cols == 4 else 32)
            fsx = f" style='font-size:{min(fs, 20 if cols == 3 else 17) - ((3 if cols == 4 else 2) if len(x['nombre']) > 44 else 0)}px'" if len(x["nombre"]) > lim_len else ""
            wide = " style='grid-column:span 2'" if ancho(x) == 2 else ""
            tiles += (f"<div class='c{cls}'{wide}><span class='fr' style='background:{fr}'></span><span class='q'>{x['copias']}</span>"
                      f"<span class='n'{fsx}><span>{esc(x['nombre'])}</span></span>{tag}</div>")
        return f"<div class='sec'><b>{tot}</b>{nombre}<span class='ty'>{ty}</span></div><div class='grid'>{tiles}</div>"
    todas = [x for k in ("main", "extra", "side") for x in l[k]["cartas"]]
    cuenta = {e: sum(1 for x in todas if estado(x) == e) for e in MARCA}
    leyenda = ("<div class='leg'>" + "".join(
        f"<span><span class='e' style='--g:{MARCA[e][2]}'>{MARCA[e][1]}</span>{t} ({cuenta[e]})</span>"
        for e, t in (("Forbidden", "Prohibida"), ("Limited", "Limitada"), ("Semi-Limited", "Semilimitada")))
        + "<span>· lista vigente</span></div>")
    return page(FULL_CSS, f"""{skyline()}
<div class='sign' style='right:40px;top:150px;color:{col};font-size:60px'>{'優勝' if l['posicion']=='Winner' else '決闘'}</div>
<div class='top'><span class='handle'>{c['handle']}</span></div>
<div class='pos2' style='color:{col}'>{lab}</div>
<div class='who2' style='white-space:nowrap;font-size:{32 if len(l["jugador"]) > 24 else 38}px'>{esc(l['jugador'])} <span>· {PAIS.get(l['pais'], l['pais'] or '')} · lista {n}/{total}</span></div>
<div class='deck2'>{esc(l['deck'])}</div>
<div class='list' style='top:{top_y}px;--h:{h}px;--fs:{fs}px;--cols:{cols}'>
{seccion('main','MAIN')}{seccion('extra','EXTRA')}{seccion('side','SIDE')}{leyenda}</div>""")

def cierre(t, c):
    rows = "".join(f"<div class='row' style='grid-template-columns:1fr'><div class='v' style='font-size:42px'>{esc(a)}</div><div class='k'>{esc(b)}</div></div>" for a, b in c["fuentes"])
    return page(T_CSS, f"""{skyline()}
<div class='sign' style='right:40px;top:170px;color:#2EF2FF;font-size:66px'>出典</div>
<div class='top'><span class='handle'>{c['handle']}</span></div>
<div class='jp' style='top:170px'>TU TURNO</div>
<div class='hl' style='top:240px;right:200px;font-size:100px'>{esc(c['pregunta'])}</div>
<div class='ask' style='top:560px;font-size:52px'>Te leo en comentarios</div>
<div class='hud' style='top:700px;right:70px' data-l='FUENTES'>{rows}</div>
<div class='swipe' style='top:1360px;color:#2EF2FF;text-shadow:0 0 14px #2EF2FF'>Sígueme para el próximo torneo grande</div>""")

def main(tj, cj, out):
    t = json.load(open(tj, encoding="utf-8")); c = json.load(open(cj, encoding="utf-8")); c.setdefault("handle", "@vruno_")
    top = [l for l in t["listas"] if l["top8"]]
    slide = (lambda l, i: deck_full(l, i, c, len(top))) if c.get("formato_lista", "completa") == "completa" else (lambda l, i: deck_slide(l, i, c))
    pages = [cover(t, c), reparto(t, c)] + [slide(l, i) for i, l in enumerate(top, 1)] + [cierre(t, c)]
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True); tmp = out / "_html"; tmp.mkdir(exist_ok=True)
    files = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for i, h in enumerate(pages, 1):
            f = tmp / f"lamina_{i}.html"; f.write_text(h, encoding="utf-8")
            pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(700)
            png = tmp / f"lamina_{i}.png"; pg.screenshot(path=str(png)); files.append(png)
            Image.open(png).convert("RGB").save(out / f"lamina_{i}.jpg", quality=88)
            if c.get("parpadeo", True):
                # zonas de neón (con margen para el brillo) + versión "apagada" para el parpadeo en video
                cajas = pg.evaluate("""[...document.querySelectorAll('.sign,.pos,.pos2,.big,.jp')].map(e=>{const r=e.getBoundingClientRect();
                    const m=34, x=Math.max(0,Math.floor(r.left-m)), y=Math.max(0,Math.floor(r.top-m));
                    return {x, y, w:Math.min(1080,Math.ceil(r.right+m))-x, h:Math.min(1920,Math.ceil(r.bottom+m))-y}})""")
                pg.add_style_tag(content=".sign,.pos,.pos2,.big,.jp{opacity:.2 !important;text-shadow:none !important;box-shadow:none !important;filter:saturate(.35) brightness(.7)}")
                pg.wait_for_timeout(150)
                pg.screenshot(path=str(out / f"lamina_{i}_off.png"))
                json.dump(cajas, open(out / f"lamina_{i}_neon.json", "w"))
        b.close()
    ims = [Image.open(f) for f in files]; gap, cols = 30, 4; rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (cols * 1080 + (cols + 1) * gap, rows * 1920 + (rows + 1) * gap), (40, 40, 44))
    for j, im in enumerate(ims): sh.paste(im, (gap + (j % cols) * (1080 + gap), gap + (j // cols) * (1920 + gap)))
    sh.resize((sh.width // 4, sh.height // 4), Image.LANCZOS).save(tmp / "vista_general.png")
    print(f"ok: {len(files)} láminas → {out}")

if __name__ == "__main__":
    main(*sys.argv[1:4])
