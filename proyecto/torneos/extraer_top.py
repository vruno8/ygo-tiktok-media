"""Extrae el top de un torneo de YGOPRODeck y sus listas (nombres de cartas incluidos).

Uso: python3 extraer_top.py <url_torneo> <salida.json>
Data cruda guardada en salida.json para revisarla antes de diseñar.
"""
import sys, re, json, html, urllib.request, collections, time

UA = {"User-Agent": "Mozilla/5.0"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")

def secciones(h):
    out = {}
    ids = {"main_deck": "main", "extra_deck": "extra", "side_deck": "side"}
    pos = {k: h.find(f'id="{k}"') for k in ids}
    orden = sorted([(p, k) for k, p in pos.items() if p >= 0])
    for i, (p, k) in enumerate(orden):
        fin = orden[i + 1][0] if i + 1 < len(orden) else h.find("</div></div>", p + 10) + 12
        bloque = h[p:fin]
        cartas = re.findall(r'data-name="(\d+)"\s+data-card="\d+"\s+data-cardname="([^"]+)"\s+data-cardtype="([^"]+)"', bloque)
        cnt = collections.Counter((cid, html.unescape(n), t) for cid, n, t in cartas)
        decl = re.search(r"--num-cards:\s*(\d+)", bloque)
        out[ids[k]] = dict(declarado=int(decl.group(1)) if decl else None,
                           cartas=[dict(id=c, nombre=n, tipo=t, copias=q) for (c, n, t), q in cnt.items()])
    return out

def main(url, salida):
    h = get(url)
    titulo = re.search(r"<title>([^<]+)</title>", h)
    links = list(dict.fromkeys(re.findall(r'href="(/deck/[a-z0-9\-]+-\d+)"', h)))
    data = dict(fuente=url, titulo=html.unescape(titulo.group(1)).strip() if titulo else "", listas=[])
    for l in links:
        u = "https://ygoprodeck.com" + l
        dh = get(u)
        meta = {}
        for campo, pat in [("deck", r"<h1[^>]*>\s*([^<]+?)\s*</h1>"), ("jugador", r"Player:\s*</[^>]+>\s*<[^>]+>\s*([^<]+)"),
                           ("posicion", r"Placement:\s*</[^>]+>\s*<[^>]+>\s*([^<]+)")]:
            m = re.search(pat, dh); meta[campo] = html.unescape(m.group(1)).strip() if m else None
        data["listas"].append(dict(url=u, **meta, **secciones(dh)))
        time.sleep(0.6)
    json.dump(data, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"ok: {len(data['listas'])} listas → {salida}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
