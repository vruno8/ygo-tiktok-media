"""Arma el video semanal (TikTok + YouTube Short) desde las láminas JPG y una pista de la rotación.

Uso:  python3 make_video.py <carpeta_laminas> <id_pista> <salida.mp4>
      id_pista: 04 | 06 | 14   (ver PISTAS y musica/rotacion.json)

- Cada lámina queda 10 s en pantalla, con fundido de 0,5 s entre láminas.
- La música se nivela (-14 LUFS), entra con fundido corto y sale con fundido de 2,5 s.
- Pistas más cortas que el video se repiten en bucle con transición suave, sin sus silencios internos.
"""
import sys, subprocess, pathlib, tempfile, json, random

BASE = pathlib.Path(__file__).parent.resolve()
MUS = BASE / "musica"
SEG = 10.0      # segundos por lámina
XF = 0.5        # fundido entre láminas
LOOP_XF = 1.0   # transición entre repeticiones del bucle
VOLUMEN = 0.5   # música al 50% (pedido de Bruno, 26/10/2026), después de nivelar
FADE_IN = 1.5   # entrada suave de la música

# segmentos con música (inicio, fin) en segundos; None = pista completa
PISTAS = {
    # medidos con silencedetect (-40 dB): todas traen ~1,1 s de silencio inicial; Interlude tiene 3 frases separadas por pausas
    "04": dict(archivo="04_passionate_duelist.mp3", nombre="Passionate Duelist", segmentos=[(1.15, 95.9)]),
    "06": dict(archivo="06_carefree_after_school.mp3", nombre="Carefree After School", segmentos=[(1.13, 178.3)]),
    "14": dict(archivo="14_interlude.mp3", nombre="Interlude", segmentos=[(1.17, 6.40), (7.87, 13.58), (15.80, 20.42)]),
}
ORDEN_ROTACION = ["04", "06", "14"]

def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())

def preparar_audio(pista, total, tmp):
    p = PISTAS[pista]; src = MUS / p["archivo"]
    base = src
    if p["segmentos"]:
        # 1) unir los segmentos con música (sin los silencios) con un cruce corto
        parts = []
        for i, (a, b) in enumerate(p["segmentos"]):
            f = tmp / f"seg{i}.wav"; run(["ffmpeg", "-y", "-i", str(src), "-ss", str(a), "-to", str(b), str(f)]); parts.append(f)
        base = tmp / "limpia.wav"
        if len(parts) == 1:
            base = parts[0]
        else:
            ins = sum([["-i", str(f)] for f in parts], [])
            chain, last = [], "[0]"
            for i in range(1, len(parts)):
                lab = f"[c{i}]"; chain.append(f"{last}[{i}]acrossfade=d=0.25:c1=tri:c2=tri{lab}"); last = lab
            run(["ffmpeg", "-y", *ins, "-filter_complex", ";".join(chain), "-map", last, str(base)])
    # 2) repetir en bucle con transición hasta cubrir el video
    d = dur(base); reps = 1
    while reps * d - (reps - 1) * LOOP_XF < total + 0.5:
        reps += 1
    looped = base
    if reps > 1:
        looped = tmp / "bucle.wav"
        ins = sum([["-i", str(base)] for _ in range(reps)], [])
        chain, last = [], "[0]"
        for i in range(1, reps):
            lab = f"[l{i}]"; chain.append(f"{last}[{i}]acrossfade=d={LOOP_XF}:c1=tri:c2=tri{lab}"); last = lab
        run(["ffmpeg", "-y", *ins, "-filter_complex", ";".join(chain), "-map", last, str(looped)])
    # 3) recortar, nivelar y fundidos
    final = tmp / "audio.m4a"
    run(["ffmpeg", "-y", "-i", str(looped), "-t", str(total),
         "-af", f"loudnorm=I=-14:TP=-1.5:LRA=11,volume={VOLUMEN},afade=t=in:d={FADE_IN},afade=t=out:st={total - 2.5}:d=2.5",
         "-c:a", "aac", "-b:a", "160k", "-ar", "44100", str(final)])
    return final, reps

def patron_parpadeo(rng):
    """Ventanas de 'apagado' irregulares dentro de un ciclo: tartamudeo rápido y, a veces, una caída larga."""
    P = rng.uniform(2.4, 4.6); ev = []
    t = rng.uniform(0.3, P * 0.5)
    for _ in range(rng.choice([2, 3, 4])):          # tartamudeo
        d = rng.uniform(0.03, 0.08); ev.append((t, t + d)); t += d + rng.uniform(0.04, 0.12)
    if rng.random() < 0.45:                           # caída larga ocasional
        t2 = rng.uniform(t + 0.4, P - 0.4) if P - 0.4 > t + 0.4 else t + 0.4
        ev.append((t2, t2 + rng.uniform(0.18, 0.35)))
    return P, rng.uniform(0, P), [(a, b) for a, b in ev if b < P]

def clip_animado(base, off, cajas, largo, salida, semilla):
    rng = random.Random(semilla)
    n = len(cajas)
    f = [f"[1]split={n}" + "".join(f"[b{i}]" for i in range(n))] if n > 1 else ["[1]null[b0]"]
    last = "[0]"
    for i, c in enumerate(cajas):
        P, fase, ev = patron_parpadeo(rng)
        cond = "+".join(f"between(mod(t+{fase:.3f},{P:.3f}),{a:.3f},{b:.3f})" for a, b in ev) or "0"
        f.append(f"[b{i}]crop={c['w']}:{c['h']}:{c['x']}:{c['y']}[c{i}]")
        f.append(f"{last}[c{i}]overlay={c['x']}:{c['y']}:enable='{cond}'[o{i}]"); last = f"[o{i}]"
    f.append(f"{last}fps=30,format=yuv420p,setsar=1[v]")
    run(["ffmpeg", "-y", "-loop", "1", "-t", str(largo), "-i", str(base), "-loop", "1", "-t", str(largo), "-i", str(off),
         "-filter_complex", ";".join(f), "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-t", str(largo), str(salida)])

def main(carpeta, pista, salida):
    carpeta = pathlib.Path(carpeta)
    laminas = sorted(carpeta.glob("lamina_*.jpg"), key=lambda p: int(p.stem.split("_")[1]))
    n = len(laminas); total = SEG * n
    with tempfile.TemporaryDirectory() as t:
        tmp = pathlib.Path(t)
        audio, reps = preparar_audio(pista, total, tmp)
        ins, filt = [], []
        for i, f in enumerate(laminas):
            ln = SEG + XF if i < n - 1 else SEG
            off = carpeta / f"{f.stem}_off.png"; cj = carpeta / f"{f.stem}_neon.json"
            if off.exists() and cj.exists() and json.load(open(cj)):
                base = carpeta / "_html" / f"{f.stem}.png"
                clip = tmp / f"{f.stem}.mp4"
                clip_animado(base if base.exists() else f, off, json.load(open(cj)), ln, clip, semilla=i * 7919)
                ins += ["-i", str(clip)]
            else:
                ins += ["-loop", "1", "-t", str(ln), "-i", str(f)]
            filt.append(f"[{i}]fps=30,scale=1080:1920,format=yuv420p,setsar=1[v{i}]")
        last = "[v0]"
        for i in range(1, n):
            lab = f"[x{i}]"; filt.append(f"{last}[v{i}]xfade=transition=fade:duration={XF}:offset={SEG * i}{lab}"); last = lab
        ins += ["-i", str(audio)]
        run(["ffmpeg", "-y", *ins, "-filter_complex", ";".join(filt), "-map", last, "-map", f"{n}:a",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
             "-c:a", "copy", "-t", str(total), "-movflags", "+faststart", str(salida)])
    print(f"ok: {salida} · {n} láminas · {total:.0f} s · pista {pista} ({PISTAS[pista]['nombre']})"
          + (f" · bucle x{reps}" if reps > 1 else ""))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
