#!/usr/bin/env bash
# Descifra las pistas de música del proyecto.
# Uso: bash musica/recuperar.sh <archivo_con_clave> <carpeta_destino>
# La clave está en el Google Drive de Bruno: documento "ygo-tiktok · clave de música (privado)".
set -euo pipefail
KEY="$1"; OUT="$2"; DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT"
for f in "$DIR"/*.mp3.enc; do
  openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in "$f" -out "$OUT/$(basename "${f%.enc}")" -pass file:"$KEY"
done
( cd "$OUT" && sha256sum -c "$DIR/huellas.sha256" )
