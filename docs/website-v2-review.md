# Website V2 — owner review

Prepared October 30, 2026 on `review/website-v2-2026-10-30`.

## Scope

This implements the owner's October 30 Website V2 specification as a review-only
change to `smziegler-web/solvra-hydraulics-site`. The owner's explicit authorization
to implement on a review branch supersedes the attachment's draft/no-implementation
banner. Production approval is still required separately.

The starting point is production commit
`0bf04be71407bb4b71b0b62122b1152686599ddb`.

## What changed

- Four static pages: Home, Product, Applications, and Early Evaluation.
- Consistent header/footer navigation, current-page indication, company copyright,
  contact email, prerelease status, and cross-page links.
- Refined Precision Atlas 4 presentation using the existing S icon, Michroma
  wordmark, geographic illustration, and navy/steel/blue palette.
- Light reading surfaces, selective navy sections, modular product sections,
  Product contents links, and decision-oriented application questions.
- A direct email inquiry action with the approved subject and an adjacent
  confidentiality reminder. No signup or upload workflow.
- Unique titles, descriptions and H1s; production canonicals; Open Graph and
  Twitter metadata; factual Organization structured data on Home.
- A four-URL sitemap, robots file, and no fabricated publication dates.
- Dependency-free static/local HTTP checks and development-artifact ignore rules.

There is no framework migration, new application dependency, runtime JavaScript,
backend, form, account system, analytics integration, or change to Cloudflare
configuration. The existing package definition, favicon, font/license, logo,
and geographic artwork remain unchanged.

The future Engineering Units concept was reviewed only for visual direction.
It was not copied, cropped, reproduced, or used as a feature-readiness source.
No engineering application code, internal model, proprietary network, or
application screenshot is included in this change.

## Editorial treatment

- Initial release scope is steady-state gas and single-phase liquid modeling.
- Forecast, parametric, scenario, and visualization workflows retain development
  and integration qualifications.
- Map-derived lengths and elevation lookup carry data-quality/engineering-review limits.
- Gas transmission is a potential application. Distribution is emerging and needs
  further utility-specific regulator/workflow validation.
- The sole legacy-model brand mention is on Product, together with compatibility,
  engineering-validation, and independence/non-endorsement qualifications.
- No product sale, guaranteed access, supported-everywhere claim, benchmarking,
  testimonial, pricing, or additional release-date promise is introduced.
- No transient, AI, multiphase, automated-optimization, or live integration
  functionality is advertised.

Implementation directives from the brief were not published as marketing copy.
For example, the Studies section uses a development/coverage qualification
instead of printing the brief's instruction to the implementer.

## Validation performed

### Static and local Cloudflare routing

The following passed:

```sh
python scripts/check-site.py
python scripts/check-site.py --base-url http://127.0.0.1:8787
git diff --check
```

The local HTTP run used the existing `wrangler.jsonc` with Wrangler 4.155.0,
installed from the existing allowed development dependency. It checked:

- Four unique titles, descriptions, H1s, canonicals, and matching social metadata.
- Semantic heading order, unique IDs, focusable skip-link target, and matching navigation.
- All local page/asset references and cross-page anchor targets.
- Mailto recipient and subject, consistent status/copyright, and the import disclaimer.
- Factual structured-data scope and selected prohibited-claim guardrails.
- Exactly four sitemap URLs and the matching robots sitemap directive.
- HTTP 200 for the real pages/assets, directory redirects for slashless URLs,
  and HTTP 404 for unknown pages, nested pages, and missing assets.

No hosted deployment was needed to validate routing.

### Browser checks

All four pages were checked in the Codex in-app browser at widths
**1440, 768, 390, and 320 pixels**. Each checked page fit its viewport without
horizontal overflow. Icon images and the local font loaded. The existing map
was inspected in the rendered layout.

Browser interaction checks covered all four header navigation destinations,
active-page indicators, a Product contents anchor, visible 3px keyboard focus,
and the skip link focusing the main landmark. The email action's destination
was inspected without sending a message. No page console warnings or errors
were reported.

Desktop and mobile screenshots of each page, responsive measurements, navigation
results, and contrast calculations are retained in the owner's Codex visualization
workspace under the current chat's `website-v2` folder. Screenshots document this
website only; they are not new marketing assets.

Eight explicit text/background color pairs met at least 4.5:1 in the selected
palette. Ratios ranged from 4.59:1 for white text on the primary button to
16.58:1 for body text on white. This is targeted accessibility verification,
not a full independent WCAG certification or cross-browser audit.

## Items for the owner before merge/deployment

- [ ] Approve the four-page copy and factual feature descriptions.
- [ ] Review desktop and phone screenshots and the local preview.
- [ ] Confirm the business mailbox can receive inquiries and send replies.
- [ ] If the existing Cloudflare integration supplies a nonproduction branch
      preview, verify the page links there. No preview or production deployment
      was manually created as part of implementation.
- [ ] Explicitly approve a later production merge/deployment.

Search Console/Bing verification and live social-card crawler behavior remain
future owner-controlled checks. There are no arbitrary verification tags.

The specification does not establish commercial readiness; automated tests
cannot replace engineering validation or the owner's final claims review.
