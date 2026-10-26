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
- Publicación: domingo 19:00, PÚBLICA en TikTok y YouTube directamente desde Metricool (Bruno no debe entrar a las apps a cambiar privacidad), con música de la rotación incrustada en el video (revisar música tras 3 semanas con métricas).
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

## Formato video para ambas redes (instrucción de Bruno, 25/10/2026 23:18)
- TikTok y YouTube reciben el MISMO video vertical 1080×1920 (reemplaza el carrusel de TikTok).
- 10 s por lámina, fundido 0,5 s. Portada dice "Sigue mirando ▸▸". 6 láminas = 60 s.
- Música en rotación semanal 04 Passionate Duelist → 06 Carefree After School → 14 Interlude (estado en musica/rotacion.json).
  Copyright: Bruno declara tenerlo resuelto.
- Audio: se recorta el silencio inicial (~1,1 s), nivelado a -14 LUFS, fundido de salida 2,5 s.
- Interlude (23 s, 3 frases con pausas): se unen las frases sin pausas y se repite en bucle con transición de 1 s.
- Herramientas: render_semana.py (modo video) + make_video.py.
- Estado: muestras enviadas el 25/10 23:30, PENDIENTE visto bueno de Bruno.

## Especiales de torneo
- Formato aprobado por Bruno (25/10/2026): portada, reparto, 1 lámina por lista con la lista COMPLETA en grilla de texto
  (franja de color por tipo de carta, cantidades, marcas PROH/LIM del banlist vigente), cierre con pregunta y fuentes.
- Sin ilustraciones oficiales de cartas (decisión de Claude: no reproduce arte de Konami en contenido publicado).
- YCS Houston 2026: programado 26/10/2026 12:00 Chile, PÚBLICO.
  YouTube id 406179788 (uuid 2839759467113367336) · TikTok id 406179805 (uuid 7518058148912844050). Música: 06.
- La rotación de música avanza con CADA publicación (semanal o especial).

## Mejoras visuales v3 — EN PRUEBA (26/10/2026, pendiente de aprobación de Bruno)
- Neones de títulos (letreros, posición, etiquetas) parpadean en bucle irregular, tipo "mal estado".
- Listas ordenadas Monstruos → Mágicas → Trampas con subtítulo por grupo; Extra por Fusión → Sincronía → Xyz → Link.
- Estado de cartas con emojis: 🚫 prohibida · 1️⃣ limitada · 2️⃣ semilimitada (lista vigente, vía API YGOPRODeck).
- Música al 50% de volumen (≈ -20 LUFS) con entrada suave de 1,5 s.
- Listas de más de 50 cartas distintas pasan a 4 columnas; nombres largos ocupan 2 celdas.
- Prueba: Regional WCQ Santiago 2026 (17/10, 128 jugadores). Solo 6 de 8 listas publicadas. NO programado en Metricool.

## Contador del límite del plan Free de Metricool (pedido por Bruno 26/10/2026)
- Regla oficial (help.metricool.com, "Main differences between Free and paid plans"):
  20 publicaciones POR MES CALENDARIO; cuenta UNA POR CADA RED (TikTok + YouTube = 2);
  solo cuentan las PUBLICADAS (los programados y borradores no); se reinicia el día 1.
  Se puede programar más de 20, pero solo se publican 20: la 21 no sale.
- En cada entrega (semanal o especial) informar: "Límite Metricool (<mes>): X de 20 · quedan N".
- Base esperada: 2 por semana → 8 a 10 al mes; espacio para 5 especiales en un mes de 5 domingos.

## Almacenamiento de la música (resuelto 26/10/2026)
- MP3 cifrados con AES-256 en el repo público: `ygo-tiktok-media/musica/*.mp3.enc` (no se pueden escuchar sin clave).
- Clave en Google Drive de Bruno (cuenta bruno@digitalgrowth.cl), archivo privado sin compartir,
  id 1shI9GEBeAKFw_FVpgvNVJf2z00KNg-_g. Recuperación: `musica/recuperar.sh` (verifica huellas SHA-256).
- Probado: clon limpio + clave leída desde Drive → 3 pistas idénticas a las originales.

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
