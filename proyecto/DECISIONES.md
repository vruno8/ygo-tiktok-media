# Proyecto YGO TikTok — registro de decisiones

## Cuenta y publicación
- Publicación vía Metricool (plan Free, límite 20 posts). Marca ID 7638648, TikTok @vruno_, zona horaria America/Santiago.
- Cada post público requiere aprobación explícita de Bruno en el chat antes de programarse.

- Imágenes: se suben como JPG al repo público GitHub vruno8/ygo-tiktok-media, carpeta `AAAA/semana-AAAA-MM-DD/`,
  y se pasan a Metricool como URL raw.githubusercontent.com (Metricool las copia a su almacenamiento).
  Google Drive descartado: la integración de Metricool con Drive es solo para planes pagados.
- TikTok conectado como cuenta PERSONAL: autopublica y acepta carruseles de hasta 35 fotos; música solo aleatoria.

## Piloto
- Semana 19–25 oct 2026, 6 láminas, reprogramado a 25/10/2026 02:25 (Chile), privado (SELF_ONLY), sin música.
- Metricool post id 405454331 (uuid 7415805753760826493; el id cambia en cada edición, el uuid no).
- RESULTADO: publicado OK el 25/10/2026, revisado por Bruno ("se ve bien"). Paso 4 cerrado.
- Música: vía Metricool con TikTok personal NO se puede elegir canción (solo aleatoria). Para música elegida: autoPublish=false y completar en la app.

## Operación semanal (desde paso 5, acordado 25/10/2026)
- Aviso agendado a ESTE chat cada domingo 10:00 (Chile); al terminar cada semana se agenda el siguiente.
- Flujo: investigar → JSON → render_semana.py → GitHub → borrador Metricool → vista previa en chat → "sí" de Bruno → programar.
- Publicación: domingo 19:00, PÚBLICA en TikTok y YouTube directamente desde Metricool (Bruno no debe entrar a las apps a cambiar privacidad), sin música (revisar música tras 3 semanas con métricas).
- Aprobación: "sí" explícito en el chat. Si llega después de las 19:00 → publicar 15 min después. Sin respuesta al lunes 12:00 → se salta la semana.
- Procedimiento detallado: RUNBOOK.md.

## YouTube Shorts (acordado 25/10/2026)
- Canal conectado en Metricool (UCBPpcx4ytiA_Ao50i-tEndA).
- Mismas láminas convertidas a video vertical (~30 s: portada 4 s, noticias 6 s c/u, fuentes 4 s, fundido 0,5 s).
- madeForKids = false (contenido NO dirigido a niños; no implica restricción 18+).
- Sin audio por ahora. Si Bruno entrega un MP3 con licencia, se incrusta en el video.
- Una sola aprobación cubre TikTok + YouTube.
- Short piloto: programado 25/10/2026 02:56, privado, Metricool id 405462857 (uuid 2928272605170385166).
  Metricool aceptó el MP4 desde raw.githubusercontent.com pese al content-type genérico.
- YouTube: título "Resumen Yu-Gi-Oh! | DD al DD mes #shorts", categoría GAMING, tags yugioh/yugioh tcg/yugioh español + tema.

## Contenido
- Cobertura: juego de cartas Yu-Gi-Oh! (TCG, OCG, Master Duel, Duel Links). Anime solo si afecta al juego de cartas.
- Cada noticia lleva etiqueta de región: TCG (cian #2EF2FF), OCG (rosa #FF3EA5), MD (lima #C6FF3D).
- Frecuencia: resumen semanal (carrusel: portada + 1 lámina por noticia + fuentes).
- Tono: estilo 4 "cercano" — hechos + pregunta final a la audiencia. Sin opiniones de meta.
- Fuentes: Konami oficial primero; secundarias solo para confirmar.
- Rumores: SÍ se publican, siempre marcados:
  - Lámina propia con cinta amarilla "RUMOR · NO CONFIRMADO", letrero 噂 (rumor) y panel con borde punteado ámbar (#FFB020).
  - Campos fijos: Qué se dice / Origen / Estado ("Sin confirmar por Konami").
  - Fuente no oficial nombrada en la lámina.
  - En la portada y el caption, el ítem va con la palabra "Rumor".
  - Si se confirma después, la semana siguiente se publica como noticia normal.
- Prohibido: arte de cartas, logos de Konami, marcos que imiten cartas, texto de efectos copiado.

## Estilo visual
- ACTIVO: E Cyber Japan (noche, skyline, lluvia, letreros neón verticales en japonés, panel HUD).
  Fuentes: Chakra Petch (latín), Zen Kaku Gothic New (japonés).
- GUARDADO para más adelante: D Vaporwave.
- Descartados: A Hoja de registro, B Foil, C Pop.
- Formato 1080×1920. Tercio inferior libre (overlay de TikTok).
- Render: `render2.py` (Playwright + fuentes @fontsource locales).

## Textos en japonés usados (traducción propia, por confirmar)
- 今週のニュース: noticias de la semana · 速報: último minuto · 新弾: nueva expansión · 決闘者: duelista
- 禁止: prohibido · 世界: mundial · 発売: lanzamiento · 出典: fuente · 噂: rumor
