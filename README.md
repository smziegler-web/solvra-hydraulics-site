# Solvra Hydraulics Website

Initial "Coming Soon" site for solvrahydraulics.com.

## Structure
- `public/index.html` — current site
- `wrangler.jsonc` — Cloudflare Workers configuration
- `package.json` — Wrangler dependency and local commands

## Cloudflare
This repo is intended to be imported into Cloudflare Workers Builds.
On each push to the production branch, Cloudflare can automatically deploy the site.

## Local preview
1. Install Node.js
2. Run `npm install`
3. Run `npm run dev`
