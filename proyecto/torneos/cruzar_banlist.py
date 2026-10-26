"""Cruza cada lista del top con la lista de prohibidas vigente (TCG) vía API de YGOPRODeck,
y con los cambios oficiales del 19/10/2026 (transcritos de yugioh-card.com, ver CAMBIOS_2026_10_19).

Uso: python3 cruzar_banlist.py <torneo.json>   → agrega 'afectadas' a cada lista del top 8
"""
import sys, json, urllib.request

LIMITE = {"Forbidden": 0, "Limited": 1, "Semi-Limited": 2}

# Cambios oficiales lista 19/10/2026 (fuente: yugioh-card.com/en/limited/list_2026-10-19/)
CAMBIOS_2026_10_19 = {
 "Forbidden": ["Amorphage Goliath", "Amorphage Sloth", "Magicians' Souls", "Pharaonic Advent", "Spell Canceller",
   "Aerial Eater", "Albion the Branded Dragon", "Azamina Ilia Silvia", "Red-Eyes Dark Dragoon", "Charmer Quartet in Bloom",
   "Cross-Sheep", "Saryuja Skull Dread", "Zenna's Deceiving Doll Maidens", "Beelze of the Diabolic Dragons",
   "Crystal Wing Synchro Dragon", "Naturia Beast", "Trishula, Dragon of the Ice Barrier", "XX-Saber Gottoms",
   "D/D/D Wave High King Caesar", "Number 41: Bagooska the Terribly Tired Tapir", "Number 60: Dugares the Timeless",
   "Varudras, the Final Bringer of the End Times", "Secret Village of the Spellcasters", "F.A. Dawn Dragster",
   "Elfnote Tinia", "Ame no Habakiri no Mitsurugi", "Cupsy★Yummy Way", "Called by the Grave", "Crossout Designator",
   "Triple Tactics Talent", "Anti-Spell Fragrance", "Gozen Match", "Rivalry of Warlords", "There Can Be Only One"],
 "Limited": ["Griffoh", "Perfectron Hydradrive Dragon", "Superdreadnought Rail Cannon Gustav Max", "Branded Opening",
   "Toon Bookmark", "Toon Table of Contents", "Droll & Lock Bird", "Branded in High Spirits"],
 "Semi-Limited": ["Sky Striker Mobilize - Engage!"],
}
NORM = lambda s: s.lower().replace("★", "").replace("☆", "").replace("  ", " ").strip()
OFICIAL = {NORM(n): st for st, ns in CAMBIOS_2026_10_19.items() for n in ns}

def api(ids):
    out = {}
    ids = list(ids)
    for i in range(0, len(ids), 40):
        u = "https://db.ygoprodeck.com/api/v7/cardinfo.php?id=" + ",".join(ids[i:i + 40])
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r:
            for c in json.load(r)["data"]:
                out[str(c["id"])] = c
    return out

def main(path):
    d = json.load(open(path, encoding="utf-8"))
    top = [l for l in d["listas"] if l.get("top8")]
    ids = {c["id"] for l in top for k in ("main", "extra", "side") for c in l[k]["cartas"]}
    info = api(ids)
    faltan = ids - set(info)
    for l in top:
        af = []
        for k in ("main", "extra", "side"):
            for c in l[k]["cartas"]:
                ci = info.get(c["id"], {})
                if ci and ci["name"] != c["nombre"]:
                    c["nombre_api"] = ci["name"]
                c["arquetipo"] = ci.get("archetype")
                st_api = (ci.get("banlist_info") or {}).get("ban_tcg")
                c["estado_actual"] = st_api  # estado vigente en TCG hoy: Forbidden / Limited / Semi-Limited / None
                st_of = OFICIAL.get(NORM(c["nombre"]))
                if st_of or (st_api and c["copias"] > LIMITE[st_api]):
                    af.append(dict(nombre=c["nombre"], seccion=k, copias=c["copias"], estado_api=st_api,
                                   cambio_19_10=st_of, coincide=(st_api == st_of) if st_of else None))
        l["afectadas"] = af
    json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ids sin respuesta API:", faltan or "ninguno")
    for l in top:
        print(f"\n{l['posicion']} · {l['jugador']} · {l['deck']}")
        for a in l["afectadas"]:
            print(f"   {a['copias']}x {a['nombre']} [{a['seccion']}] → oficial 19/10: {a['cambio_19_10']} · API hoy: {a['estado_api']}"
                  + ("" if a['coincide'] in (True, None) else "  ⚠ NO COINCIDE"))

if __name__ == "__main__":
    main(sys.argv[1])
