# Checklist semanal — Resumen Yu-Gi-Oh! en TikTok (@vruno_)

Se ejecuta cada domingo a las 10:00 (Chile) cuando llega el aviso agendado a este chat.
Antes de empezar: leer `DECISIONES.md`.

## 1. Investigar (semana lunes a domingo)
- [ ] Buscar noticias del período en: Konami TCG (yugioh-card.com, incl. /lat-am/), Konami OCG, anuncios Master Duel / Duel Links, listas de Prohibidas y Limitadas.
- [ ] Secundarias solo para confirmar: YGOrganization, Yu-Gi-Oh! Meta / Master Duel Meta.
- [ ] Elegir máximo 4 noticias (si hay más, priorizar: listas de prohibidas > productos TCG > Mundial/eventos > OCG > digital).
- [ ] Rumores: permitidos, siempre con `"rumor": true` (cinta amarilla, campos Qué se dice / Origen / Estado).
- [ ] Anime solo si afecta al juego de cartas.
- [ ] Toda fecha o cifra con fuente. Si dos fuentes discrepan, decirlo a Bruno y no elegir en silencio.

## 2. Armar el JSON de la semana
- [ ] Copiar `semanas/_prueba_renderizador.json` a `semanas/AAAA-MM-DD.json` (fecha del lunes).
- [ ] Títulos de lámina ≤ 40 caracteres. Máximo 4 filas por panel. Valores cortos.
- [ ] Etiquetas: TCG / OCG / MD (WCS solo eventos mundiales).
- [ ] Letreros en japonés: usar solo palabras ya traducidas en DECISIONES.md o agregar la traducción ahí.

## 3. Renderizar y revisar
- [ ] `python3 render_semana.py semanas/AAAA-MM-DD.json ../ygo-tiktok-media/AAAA/semana-AAAA-MM-DD video`
- [ ] Abrir `_html/vista_general.png` y revisar: sin textos superpuestos, nada en el tercio inferior, títulos completos.
- [ ] No subir la carpeta `_html` a GitHub.
- [ ] Pista de la semana: leer `musica/rotacion.json` → campo `proxima`.
- [ ] `python3 make_video.py ../ygo-tiktok-media/AAAA/semana-AAAA-MM-DD <pista> ../ygo-tiktok-media/AAAA/semana-AAAA-MM-DD/video.mp4`
- [ ] Revisar: duración = 10 s × láminas, sin silencios (silencedetect -40 dB), fotogramas en 5 s y en la última lámina.
- [ ] Tras publicar: agregar la semana al `historial` y avanzar `proxima` al siguiente del `orden`.
- [ ] Si `musica/` no existe (contenedor reciclado), recuperar:
      1. Clonar `vruno8/ygo-tiktok-media` si no está (`/home/claude/ygo-tiktok-media`).
      2. Leer la clave desde Google Drive: archivo id `1shI9GEBeAKFw_FVpgvNVJf2z00KNg-_g`
         ("ygo-tiktok · clave de música (privado).txt") con read_file_content.
      3. Guardarla en un archivo temporal (umask 077) y correr
         `bash ygo-tiktok-media/musica/recuperar.sh <archivo_clave> /home/claude/ygo-tiktok/musica`.
      4. Debe imprimir OK para las 3 pistas. Borrar el archivo temporal de la clave.
      5. Si falla: pedir a Bruno que adjunte de nuevo los MP3.
- [ ] Si falta todo el proyecto local: copiar `ygo-tiktok-media/proyecto/` a `/home/claude/ygo-tiktok/` y correr `npm install`.

## 4. Subir imágenes
- [ ] En `ygo-tiktok-media`: `git pull`, `git add AAAA/semana-*/lamina_*.jpg`, commit, push.
- [ ] Verificar que una URL raw.githubusercontent.com responda 200 image/jpeg.

## 5. Borrador + aprobación
- [ ] Crear en Metricool 2 BORRADORES (`draft: true`) con el MISMO video.mp4, fecha domingo 19:00, ambos PÚBLICOS:
      TikTok video → `privacyOption: "PUBLIC_TO_EVERYONE"`, `autoAddMusic: false` (el audio ya va en el video).
      YouTube Short → `privacy: "public"`, type short, madeForKids false, categoría GAMING.
      (Privado solo en pilotos/pruebas acordadas explícitamente.)
- [ ] Contador del límite Metricool (ver regla en DECISIONES.md): getScheduledPosts del MES de la publicación,
      contar cada red por separado. Publicadas = status PUBLISHED; programadas = PENDING (draft:false).
      Cifra a informar = publicadas + programadas + las que agrega este post.
- [ ] Enviar a Bruno en el chat: vista general + caption + lista de dudas/fuentes en conflicto +
      línea "Límite Metricool (<mes>): X de 20 (A publicadas + B programadas + C de este post) · quedan N".
      Si X ≥ 16 → avisar. Si X > 20 → NO programar: la publicación 21 no saldría; proponer mover al mes siguiente.
- [ ] Esperar "sí" explícito. Sin "sí" no se programa.
- [ ] Con "sí": actualizar a programado (`draft: false`). Si el "sí" llega después de las 19:00, publicar 15 min después.
- [ ] Sin respuesta al lunes 12:00: no publicar, avisar que la semana se saltó.

## 6. Cerrar la semana
- [ ] Agendar el aviso del domingo siguiente a las 10:00 (send_later a este chat).
- [ ] Confirmar a Bruno la fecha del próximo aviso.
- [ ] Anotar en DECISIONES.md cualquier regla nueva.
- [ ] Respaldar cambios del proyecto en `ygo-tiktok-media/proyecto/`.

## Especial de torneo (top 8) — a pedido de Bruno, con link de YGOPRODeck
1. `python3 torneos/extraer_top.py <url_torneo> torneos/<slug>.json` → revisa que Main/Extra/Side coincidan con lo declarado.
2. Completar jugador/posición/país desde la tabla del torneo (ver bloque en extraer_top; si falla, revisar HTML).
3. `python3 torneos/cruzar_banlist.py torneos/<slug>.json` → si hay banlist nuevo, actualizar CAMBIOS en el script.
4. Escribir `torneos/<slug>_config.json` (título, bajada, dato de reparto, pregunta, fuentes). Todo dato del reparto debe salir del JSON.
5. `python3 torneos/render_torneo.py torneos/<slug>.json torneos/<slug>_config.json <carpeta>` → revisar vista general y borde inferior ≤ 1520 px.
6. `python3 make_video.py <carpeta> <pista> <carpeta>/video.mp4` (pista: la próxima de la rotación).
7. Mismo flujo de borrador + "sí" de Bruno, con la línea del contador del límite Metricool (suma 2: TikTok + YouTube).

## Caption (estilo 4, cercano)
Título: `Resumen Yu-Gi-Oh! | DD al DD mes` (≤ 90 caracteres)
Texto: apertura cercana + las 4 noticias en una frase + pregunta + hashtags
`#yugioh #yugiohtcg #yugiohespañol` + 1-2 según tema (`#banlist`, `#masterduel`, `#yugiohocg`).
