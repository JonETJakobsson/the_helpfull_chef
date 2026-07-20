# The Helpful Chef

A food-planning knowledge base driven by a VS Code custom agent, **The Helpful Chef**.
The agent is the interface between you and a set of Markdown files that store your
recipes, ingredients, family ratings and cooking history.

All data is stored as plain Markdown with YAML front matter following Google's
[Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md),
so it is human-readable, diffable and portable.

## Getting started

1. Open this folder in VS Code.
2. In the Chat view, select **The Helpful Chef** from the agent picker.
3. Ask it to write a recipe, plan a week of dinners, or build a shopping list.

## What the agent can do

| Skill | Purpose |
|-------|---------|
| `write-recipe` | Turn any recipe (text or a URL) into a structured recipe file. |
| `weekly-menu-planner` | Plan 5 weekday dinners from cravings, stock to use up, ratings, recency and this week's offers. |
| `shopping-list` | Build a grouped shopping list for a planned week, flagging each offer with its store. |
| `store-offers` | Capture this week's grocery deals so the menu and list can lean on what's cheap. |
| `dinner-calendar` | Export the week's dinners to an `.ics` file for your shared calendar. |

## Weekly workflow (offers → menu → list → calendar)

Plan a whole week in one flow, built on the deals that are live when you shop:

1. **Drop this week's offers.** On [matpriskollen.se](https://matpriskollen.se) (log in
   once and save your **favourite stores** + **ort**), open
   **Erbjudanden → Mina favoritbutiker** and save the page from the browser as
   **"Webpage, Single File" (`.mhtml`)** (Chrome/Edge: `Ctrl+S`). Drop it in the repo at
   `household/offers/matpriskollen-<ort>/<year>-w<week>.mhtml`. Everything under
   `household/` is git-ignored, so the raw flyer data stays private.
2. **Ask the agent to "hämta veckans erbjudanden".** It runs
   `scripts/parse-matpriskollen.py` to extract a compact table from the ~1 MB page (no
   giant HTML in the chat), then filters it to cooking staples, matches each item to the
   ingredient catalogue and saves the curated offers file.
3. **Ask it to plan the week.** The menu is **seeded** from the offers (plus your cravings,
   what to use up, family ratings and how recently a dish was served).
4. **Ask for the shopping list.** Each item that's on offer is flagged with its price and
   store, with a "what to buy where" summary and a clean copy-paste block for your todo app.
5. **Optional — export the calendar.** Turn the menu into an `.ics` you can import into a
   shared family calendar.

No scraping is involved — you save the page, the agent just reads it. If you'd rather not
save a file, you can paste the offers page text to the agent instead.

## Repository layout

```
recipes/          Reusable recipes (shareable)
ingredients/      Canonical ingredient catalogue (shareable)
knowledge/        Cooking principles, techniques, troubleshooting, substitutions (shareable)
household/        Members, ratings, meal history, store offers (private, git-ignored)
menus/            Planned weekly menus
shopping-lists/   Generated shopping lists
calendars/        Exported dinner calendars (.ics)
scripts/          Helper scripts (e.g. the Matpriskollen offers parser)
.github/          The agent, its skills and global conventions
```

Defaults: **Swedish** content, **metric** units, **4 portions** unless you say otherwise.
