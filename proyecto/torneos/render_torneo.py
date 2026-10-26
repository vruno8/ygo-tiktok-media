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
<div class='hl' style='top:240px;right:200px;font-size:96px'>Solo 3 decks en el top 8</div>
<div class='stack' style='top:620px'>
<div class='hud' data-l='DECKS EN EL TOP 8'>{bars}</div>
<div class='hud loss' data-l='DESPUÉS DEL 19/10'><div class='mix' style='font:600 40px/1.2 Chakra Petch;color:#fff;padding:14px 0'>{esc(c['dato_reparto'])}</div></div>
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
    pages = [cover(t, c), reparto(t, c)] + [deck_slide(l, i, c) for i, l in enumerate(top, 1)] + [cierre(t, c)]
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True); tmp = out / "_html"; tmp.mkdir(exist_ok=True)
    files = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for i, h in enumerate(pages, 1):
            f = tmp / f"lamina_{i}.html"; f.write_text(h, encoding="utf-8")
            pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(700)
            png = tmp / f"lamina_{i}.png"; pg.screenshot(path=str(png)); files.append(png)
            Image.open(png).convert("RGB").save(out / f"lamina_{i}.jpg", quality=88)
        b.close()
    ims = [Image.open(f) for f in files]; gap, cols = 30, 4; rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (cols * 1080 + (cols + 1) * gap, rows * 1920 + (rows + 1) * gap), (40, 40, 44))
    for j, im in enumerate(ims): sh.paste(im, (gap + (j % cols) * (1080 + gap), gap + (j // cols) * (1920 + gap)))
    sh.resize((sh.width // 4, sh.height // 4), Image.LANCZOS).save(tmp / "vista_general.png")
    print(f"ok: {len(files)} láminas → {out}")

if __name__ == "__main__":
    main(*sys.argv[1:4])
