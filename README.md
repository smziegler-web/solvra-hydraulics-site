# Solvra Hydraulics Website

Coming in 2027 site for solvrahydraulics.com, using the Precision Atlas 4 visual direction.

The product is Solvra Hydraulics. The copyright holder is Solvra Hydraulics LLC.

The local branding mockup uses the existing Solvra application icon, a fictional
map illustration, and a blue/steel/navy palette. The illustration is editorial
artwork; it is not an application screenshot or a real hydraulic model.

## Structure
- `public/index.html` — single-page site with overview and development sections
- `public/styles.css` — responsive layout and Precision Atlas palette
- `public/assets/` — approved icon, generated map, and self-hosted Michroma font
- `public/favicon.ico` — approved multiresolution Windows icon
- `wrangler.jsonc` — Cloudflare Workers configuration
- `package.json` — Wrangler dependency and local commands

## Cloudflare
This repo is intended to be imported into Cloudflare Workers Builds.
On each push to the production branch, Cloudflare can automatically deploy the site.

## Local preview
1. Install Node.js
2. Run `npm install`
3. Run `npm run dev`

For a static preview, open `public/index.html` directly in a browser, or run
`python -m http.server 8765 --bind 127.0.0.1 --directory public` and visit
`http://127.0.0.1:8765`. No client-side JavaScript or third-party requests are needed.

## Assets and licenses

- The S icon is the existing Solvra Hydraulics branding asset.
- The map was generated with built-in imagegen using only the approved Precision
  Atlas 4 concept board as a reference. No internal model screenshot or data was used.
  Its master and generation prompt are kept in the Gasnet workspace under
  `Branding/Web/precision-atlas-4-map-master.png` and
  `Branding/Web/precision-atlas-4-map-prompt.md`.
- Michroma is supplied by Google Fonts and is licensed under the SIL Open Font
  License; see `public/assets/fonts/OFL.txt`. It approximates the concept board's
  technical wordmark typography using editable HTML text.

This remains a prerelease page announcing "Coming in 2027." No signup, download,
specific release date, contact form, or claims about future transient or AI
features are included.
