# Solvra Hydraulics Website

Four-page prerelease website for [solvrahydraulics.com](https://solvrahydraulics.com),
using the established Precision Atlas 4 identity.

The product is **Solvra Hydraulics**. The company and copyright holder are
**Solvra Hydraulics LLC**. The planned first commercial release is 2027, subject
to development, readiness, and validation.

## Pages and source

| URL | Source | Purpose |
| --- | --- | --- |
| `/` | `public/index.html` | Product introduction and primary actions |
| `/product/` | `public/product/index.html` | Steady-state capabilities and modeling limitations |
| `/applications/` | `public/applications/index.html` | Engineering applications and decision-oriented questions |
| `/early-evaluation/` | `public/early-evaluation/index.html` | Selective future evaluation inquiries |

- `public/styles.css` — shared responsive design, typography, and keyboard focus styles.
- `public/assets/` — approved icon, illustrative geographic artwork, and self-hosted font.
- `public/favicon.ico` — approved multiresolution application icon.
- `public/robots.txt` and `public/sitemap.xml` — crawl information for exactly four public pages.
- `scripts/check-site.py` — dependency-free static checks and optional local HTTP checks.
- `docs/website-v2-review.md` — implementation, validation, and owner review notes.
- `wrangler.jsonc` — existing Cloudflare Workers static-assets configuration.
- `package.json` — existing Wrangler development dependency and commands.

The checked-in HTML is the source of truth. There is no page generation or build
step. When changing shared navigation or the footer, keep all four pages consistent
and run the checks.

## Local preview

Install Node.js, then run:

```sh
npm install
npm run dev
```

Wrangler prints its local URL, normally `http://localhost:8787`. This emulates
Cloudflare static-asset routing, including directory URLs and missing-page responses.
No Cloudflare account or deployment is needed for local preview.

A simpler static preview is also available with Python:

```sh
python -m http.server 8766 --bind 127.0.0.1 --directory public
```

Visit `http://127.0.0.1:8766/`. Use a web server rather than opening the HTML
directly; navigation and shared assets use root-relative URLs.

## Checks

With Python 3:

```sh
python scripts/check-site.py
```

With a local Wrangler preview running:

```sh
python scripts/check-site.py --base-url http://127.0.0.1:8787
```

Checks cover unique titles, descriptions and H1s; canonical and social metadata;
heading structure; consistent navigation; local assets and anchors; email links;
structured-data scope; selected editorial guardrails; and the four-page sitemap.
The HTTP option also checks real page/asset responses, directory redirects, and 404s.

Browser review is still required for layout, keyboard behavior, text contrast,
and editorial accuracy. Automated checks do not establish engineering readiness
or guarantee SEO rankings.

## Deployment and review

The canonical repository is `smziegler-web/solvra-hydraulics-site`.
Production is the existing Cloudflare Worker `solvra-hydraulics`, serving
`./public` through `wrangler.jsonc`. The connected production branch is `main`;
an approved merge/push to main triggers the existing deployment workflow.

Website V2 is prepared on `review/website-v2-2026-10-30` for owner review.
Do not merge or run `npm run deploy` without explicit owner approval.
A manually created Cloudflare preview deployment is not part of this review change.
If automatic branch previews are enabled by the existing hosting configuration,
review the returned preview URL separately before approving a production merge.

Do not replace the Worker, domain, DNS records, or deployment architecture.

## Content and contact

- Initial commercial scope: steady-state gas and single-phase liquid network modeling.
- Studies and visualization workflows retain prerelease and integration qualifications.
- Distribution is described as an emerging application requiring more validation.
- Supported legacy import compatibility, engineering review, and independence
  qualifications appear together on Product.
- Early Evaluation uses a `mailto:` link to `info@solvrahydraulics.com` with
  subject `Solvra Early Evaluation Inquiry`.
- There is no signup form, model-upload service, download, pricing, login,
  video embed, or promise of prerelease access.
- The business mailbox and outgoing reply workflow need owner verification before outreach.
- Search Console and Bing Webmaster verification remain owner-controlled future work.

## SEO

Each page has its own title, description, H1, production canonical URL, Open Graph
and Twitter metadata. The social image reuses the approved illustrative map; it is
not a product screenshot. Home includes only factual Organization structured data
for Solvra Hydraulics LLC. There are no offer, review, rating, or software-sale schemas,
fabricated dates, verification tags, or competitor keyword lists.

## Assets and licenses

- The S icon and favicon are the existing approved Solvra application branding.
- `public/assets/atlas-map.webp` is the existing illustrative geographic artwork,
  originally generated from the approved Precision Atlas 4 branding board.
  It is not an application screenshot or a real hydraulic model.
- Original map source and prompt were retained in the Gasnet workspace under
  `Branding/Web/precision-atlas-4-map-master.png` and
  `Branding/Web/precision-atlas-4-map-prompt.md`.
- Michroma is supplied by Google Fonts under the SIL Open Font License.
  Its original license is retained at `public/assets/fonts/OFL.txt`.
- The supplied future Engineering Units concept is visual-reference-only and is
  not included in the repository or public assets. No application screenshots,
  proprietary networks, or internal models are used.

No external fonts, analytics, client-side scripts, or third-party image requests
are required to render or navigate the site.
