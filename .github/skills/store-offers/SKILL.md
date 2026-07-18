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

## Rhythm — do this at the start of the shopping week

Grocery offers are weekly and often **expire within a day or two**. Capture them at the
**start of the week you're planning for** (e.g. **Monday**) and plan the menu right after —
then the menu is built on offers that are still valid when you shop. Pull fresh each week;
don't reuse last week's list.

## Store registry

The user's stores live in `household/offers/stores.md` (name, chain, offer URL). Add or
update stores there — offer pages are location-specific. This whole area is private and
git-ignored.

## Getting the offers

Store offer pages (ICA, City Gross …) are JS-heavy and usually block direct fetching, so
use an aggregator you can copy from. **Matpriskollen** is the recommended source.

### Using Matpriskollen (recommended)

1. On [matpriskollen.se](https://matpriskollen.se) the user logs in and, once, saves their
   **favourite stores** (their local shops) and sets their **ort/location**.
2. Open **Erbjudanden → Mina favoritbutiker** so the page lists this week's offers across
   all those stores at once — one location covers every nearby store.
3. The user **copies the whole offers page and pastes it** to the agent.
4. The agent parses it (see Procedure). No scraping — the user does the copy; we just read it.

### Other options

- **App export / paste** from a single store's app — same idea, one store at a time.
- **Official API:** **Tjek** (tjek.com) has an API/SDK but is B2B (agreement/key). If you
  get a key, keep it in `household/` and never commit it. **Matspar** (matspar.se) compares
  online prices. Prefer an official feed over scraping; respect each service's terms.
- **Direct fetch** of a store page is a last resort — expect it blocked or empty, and never
  build an aggressive scraper.

## Procedure

1. Determine the ISO week you're planning for.
2. Obtain the offers (see *Getting the offers*).
3. **Filter to cooking staples.** Drop non-food (pets, household, hygiene), sweets/snacks/
   ice cream and ready meals. Keep the deals worth cooking around.
4. **Match** each kept item to an ingredient concept in `ingredients/` (resolve via
   title/aliases). Only create a missing concept if it's a real staple you'd cook with.
5. Note the advertised price and store for context. Keep it light — the goal is a simple
   *list of which ingredients are cheap this week*, not a price database.
6. **Save** it (type: `Offers`), private and git-ignored — never publish store flyer data:
   - **Matpriskollen (aggregated):** one file per location per week —
     `household/offers/matpriskollen-<ort>/<year>-w<week>.md`, with a `Butik` column.
   - **Single store:** `household/offers/<store-slug>/<year>-w<week>.md`.

## Offers file format

Aggregated (Matpriskollen) — one file per location, with a `Butik` column:

```yaml
---
type: Offers
source: Matpriskollen (Uppsala)
week: 2026-w30
fetched: 2026-07-18
stores: [City Gross Boländerna, ICA Maxi Gnista, Lidl Boländerna, Stora Coop Boländerna]
tags: [offers]
timestamp: 2026-07-18T00:00:00Z
---

| Vara (annonserad) | Ingrediens | Pris | Butik |
|-------------------|-----------|------|-------|
| Blandfärs 70/30 | [Nötfärs](/ingredients/notfars.md) | 89,95/kg | City Gross |
| Kycklingdelar 1 kg | [Kycklingfilé](/ingredients/kycklingfile.md) | 2 för 59,00 | City Gross |
| Champinjoner 400 g | [Svamp](/ingredients/svamp.md) | 24,00/frp | ICA Maxi |
```

Group rows by section (Kött, Fisk, Grönt, Mejeri & Ost, Skafferi …) for readability. For a
single store, drop the `Butik` column and add `store:` / `source_url:` to the front matter.

## Feeds the other skills

- **weekly-menu-planner** reads the current week's offers and softly boosts recipes whose
  key ingredients are on offer.
- **shopping-list** marks items that are on offer (and at which store).

## Output

Report the offers file path and a short **"veckans fynd"** summary (top deals matched to
ingredients). Do not modify recipes, ratings, or the shareable ingredient catalogue beyond
adding a genuinely-missing staple.
