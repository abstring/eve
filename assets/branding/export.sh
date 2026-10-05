#!/usr/bin/env bash
# Export approved raster masters; requires ImageMagick 7. No creative edits.
set -euo pipefail
cd "$(dirname "$0")"

for theme in light dark; do
  magick "logo/eve-logo-$theme.png" -resize 768x512 "logo/eve-logo-$theme-768.png"
done

mkdir -p icon/light icon/dark favicon/light favicon/dark
for size in 1024 512 256 128 64; do
  magick source/eve-icon-transparent.png -resize "${size}x${size}" "icon/eve-icon-transparent-$size.png"
  magick "icon/eve-icon-transparent-$size.png" -background '#FFFCF1' -alpha remove -alpha off "icon/light/eve-icon-$size.png"
  magick "icon/eve-icon-transparent-$size.png" -background '#0D1117' -alpha remove -alpha off "icon/dark/eve-icon-$size.png"
done
magick icon/light/eve-icon-256.png -resize 180x180 icon/apple-touch-icon.png
for theme in light dark; do
  for size in 64 48 32 16; do
    magick "icon/$theme/eve-icon-256.png" -resize "${size}x${size}" "favicon/$theme/favicon-$size.png"
  done
  magick "icon/$theme/eve-icon-256.png" -define icon:auto-resize=64,48,32,16 "favicon/$theme/favicon.ico"
done
