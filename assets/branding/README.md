# Eve brand assets

Approved identity: Eve inspecting a PCB, framed by natural leaves, in a dark-green
engraved oval with the prominent **eve.engineer** serif wordmark. Keep the natural
foliage, bare forehead, portrait, PCB, and proportions. No magnifier or technical
replacement leaves belong in the approved identity.

Download the complete approved package: [eve-logo-icon-package.zip](eve-logo-icon-package.zip).
Historical concepts are excluded from this archive.

## Logos

| Use | Light | Dark |
| --- | --- | --- |
| Full-resolution PNG | [Logo](logo/eve-logo-light.png) | [Logo](logo/eve-logo-dark.png) |
| README / web, 768 px | [Logo](logo/eve-logo-light-768.png) | [Logo](logo/eve-logo-dark-768.png) |

The light master is an unchanged copy of the approved concept. The dark edition
preserves the green/ivory portrait, uses an ivory wordmark and outer rim, and a
charcoal background. Do not invert the portrait shading for dark mode.

## Icons and favicons

- Transparent cameo PNGs: `icon/eve-icon-transparent-{1024,512,256,128,64}.png`.
- Opaque square avatars: `icon/light/` and `icon/dark/`, in the same five sizes.
- Apple touch icon: [180 px PNG](icon/apple-touch-icon.png).
- Theme-specific favicon PNGs: `favicon/light/` and `favicon/dark/`, at 16, 32,
  48, and 64 px, plus multiresolution ICO files.
- [Light favicon](favicon/light/favicon.ico) · [Dark favicon](favicon/dark/favicon.ico).

Use the full logo when the brand name is needed and the cameo alone for avatars
and application icons. The engraving loses fine detail at favicon sizes; those
files preserve the approved silhouette rather than introducing a different mark.

## README theme selection

The repository README uses a `<picture>` with light/dark media queries and a
light fallback, as supported by [GitHub's theme-aware images](https://github.blog/changelog/2022-08-15-specify-theme-context-for-images-in-markdown-ga/).
Relative paths keep the assets tied to the checkout and revision. The images
have opaque backgrounds; the transparent cameo can be used on other surfaces.

## Source and exports

The portrait is inspired by Peter Paul Rubens's *Adam and Eve* (1598–1600),
City of Antwerp Collection, Rubenshuis, Antwerp, Belgium. See
[artwork credits and public-domain image sources](source/artwork-credits.md).
The original painting and its public-domain reproductions are separate from
the generated logo assets; the repository license does not change their status.

`source/eve-approved.png` is the original approved logo; the light and dark
full-resolution files in `logo/` are the release raster masters.
`source/eve-icon-transparent.png` is the transparent icon master. Dark recoloring
and icon extraction used the built-in image generator; prompts are recorded in
`source/generation-prompts.md`. `export.sh` uses ImageMagick 7 for mechanical
resizing, background compositing, and ICO export:

```sh
bash assets/branding/export.sh
```

These are raster assets, not SVG/vector masters or a verified single spot-color
print separation. Retain the original masters; do not repeatedly resize small
exports. Use green-and-ivory styling consistently and preserve clear space.
The nominal supporting palette is forest green `#193E2C`, warm ivory `#FFFCF1`,
and charcoal `#0D1117`; generated raster shading contains additional pixel values.

Assets follow the repository's AGPL-3.0-only license. `concepts/` holds historical
explorations, not approved alternatives. Nothing in this package changes KiCad's
own branding or implies project affiliation.
