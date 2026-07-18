---
name: store-offers
description: "Gather this week's grocery special offers (erbjudanden/extrapris) from nearby stores, normalise them to the ingredient catalogue, and use them to steer the weekly menu toward cheap ingredients and flag deals on the shopping list. Use when the user wants this week's offers, to plan cheaply, or to check grocery prices."
argument-hint: "e.g. 'hämta veckans erbjudanden' eller klistra in erbjudanden"
---

# Store Offers

Capture this week's grocery deals and make them usable by the planner and shopping list.

## When to use

- "Vad är på extrapris denna vecka?" / "hämta erbjudanden" / "planera billigt".
- Just before **weekly-menu-planner**, to bias the menu toward discounted ingredients.

## Store registry

The user's stores live in `household/offers/stores.md` (name, chain, offer URL). Add or
update stores there — offer pages are location-specific. This whole area is private and
git-ignored.

## Getting the offers (tiered — the pages are JS-heavy and often block direct fetch)

1. **Paste (most reliable):** ask the user to paste this week's offers, or export them
   from the store's app. Then parse them. This always works and avoids blocking.
2. **Aggregator/app data:** if a structured offers source is available, prefer it over
   scraping a single store's HTML.
3. **Direct fetch:** last resort only. Expect it to be blocked or empty, and respect each
   site's terms — do **not** build an aggressive scraper or hammer the site.

## Procedure

1. Determine the ISO week and which stores (default: all in the registry).
2. Obtain the offers (see the tiered approach above).
3. **Keep only the good deals** — the items worth cooking around — and **match** each to an
   ingredient concept in `ingredients/` (resolve via title/aliases). Only create a missing
   concept if it's a real staple you'd cook with.
4. Note the advertised price next to each item for context (optional). Keep it light — the
   goal is a simple *list of which ingredients are cheap this week*, not a price database.
5. **Save** to `household/offers/<store-slug>/<year>-w<week>.md` (type: `Offers`). Never
   publish store flyer data — keep it in the private area only.

## Offers file format

```yaml
---
type: Offers
store: ICA Maxi Gnista
week: 2026-w30
source_url: https://www.ica.se/erbjudanden/maxi-ica-stormarknad-gnista-uppsala-1003431/
fetched: 2026-07-18
tags: [offers]
timestamp: 2026-07-18T00:00:00Z
---

| Vara (annonserad) | Ingrediens | Pris |
|-------------------|-----------|------|
| Nötfärs 500 g | [Nötfärs](/ingredients/notfars.md) | 39 kr |
| Kycklinglårfilé 900 g | [Kycklingfilé](/ingredients/kycklingfile.md) | 69 kr |
```
```

## Feeds the other skills

- **weekly-menu-planner** reads the current week's offers and softly boosts recipes whose
  key ingredients are on offer.
- **shopping-list** marks items that are on offer (and at which store).

## Output

Report the offers file path and a short **"veckans fynd"** summary (top deals matched to
ingredients). Do not modify recipes, ratings, or the shareable ingredient catalogue beyond
adding a genuinely-missing staple.
