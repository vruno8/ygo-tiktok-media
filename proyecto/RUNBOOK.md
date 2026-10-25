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
- [ ] `python3 render_semana.py semanas/AAAA-MM-DD.json ../ygo-tiktok-media/AAAA/semana-AAAA-MM-DD`
- [ ] Abrir `_html/vista_general.png` y revisar: sin textos superpuestos, nada en el tercio inferior, títulos completos.
- [ ] No subir la carpeta `_html` a GitHub.

## 4. Subir imágenes
- [ ] En `ygo-tiktok-media`: `git pull`, `git add AAAA/semana-*/lamina_*.jpg`, commit, push.
- [ ] Verificar que una URL raw.githubusercontent.com responda 200 image/jpeg.

## 5. Borrador + aprobación
- [ ] Crear el post en Metricool como BORRADOR (`draft: true`), TikTok, público, sin música, fecha domingo 19:00.
- [ ] Enviar a Bruno en el chat: vista general + caption + lista de dudas/fuentes en conflicto.
- [ ] Esperar "sí" explícito. Sin "sí" no se programa.
- [ ] Con "sí": actualizar a programado (`draft: false`). Si el "sí" llega después de las 19:00, publicar 15 min después.
- [ ] Sin respuesta al lunes 12:00: no publicar, avisar que la semana se saltó.

## 6. Cerrar la semana
- [ ] Agendar el aviso del domingo siguiente a las 10:00 (send_later a este chat).
- [ ] Confirmar a Bruno la fecha del próximo aviso.
- [ ] Anotar en DECISIONES.md cualquier regla nueva.
- [ ] Respaldar cambios del proyecto en `ygo-tiktok-media/proyecto/`.

## Caption (estilo 4, cercano)
Título: `Resumen Yu-Gi-Oh! | DD al DD mes` (≤ 90 caracteres)
Texto: apertura cercana + las 4 noticias en una frase + pregunta + hashtags
`#yugioh #yugiohtcg #yugiohespañol` + 1-2 según tema (`#banlist`, `#masterduel`, `#yugiohocg`).
