# The Helpful Chef — Repository Conventions

This repository is a food-planning knowledge base. The primary interface is the
custom agent **The Helpful Chef** (`.github/agents/the-helpful-chef.agent.md`).
These conventions apply to all work in this repo.

## Knowledge format (OKF)

All data files are Markdown with YAML front matter, following the
[Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).

- Every non-reserved `.md` file MUST start with a front-matter block delimited by `---`
  containing a non-empty `type` field.
- Recommended front-matter fields: `title`, `description`, `tags`, `timestamp`
  (ISO 8601). Producers may add any extra keys.
- Reserved filenames: `index.md` (directory listing, **no** front matter — except the
  bundle-root `index.md` which may carry `okf_version`) and `log.md` (dated history,
  no front matter).
- Cross-link concepts with Markdown links. Prefer **bundle-absolute** paths starting
  with `/` (e.g. `[Potatis](/ingredients/potatis.md)`) so links survive file moves.
- Favour structural Markdown (headings, tables, lists) over prose.

## Language & units

- Content language: **Swedish**.
- Units: **metric** (g, kg, ml, l, dl, msk, tsk, st).

## Portions

- Default to **4 portions** when the user does not specify.
- Scale ingredient quantities linearly on request; recipes store their base `servings`
  in front matter so scaling is unambiguous.

## File & slug naming

- Filenames are lowercase, hyphen-separated slugs.
- ASCII-fold Swedish characters in slugs: `å`→`a`, `ä`→`a`, `ö`→`o`, `é`→`e`.
  Example: "Köttbullar med gräddsås" → `kottbullar-med-graddsas.md`.
- Weekly files use `<year>-w<week>.md`, e.g. `2026-w28.md` (ISO week number).

## Where things live

| Content | Location | `type` |
|---------|----------|--------|
| Recipes | `recipes/<slug>.md` | `Recipe` |
| Ingredient catalogue | `ingredients/<slug>.md` | `Ingredient` |
| Culinary principle | `knowledge/principles/<slug>.md` | `Principle` |
| Cooking technique | `knowledge/techniques/<slug>.md` | `Technique` |
| Troubleshooting fix | `knowledge/troubleshooting/<slug>.md` | `Troubleshooting` |
| Ingredient substitution | `knowledge/substitutions/<slug>.md` | `Substitution` |
| Family members & defaults | `household/members.md` | `Household` |
| Per-member ratings | `household/ratings/<member>.md` | `Rating` |
| Meal history | `household/meal-history/log.md` | _(log, no front matter)_ |
| Store registry | `household/offers/stores.md` | `Stores` |
| Weekly store offers | `household/offers/<store>/<year>-w<week>.md` | `Offers` |
| Weekly menu | `menus/<year>-w<week>.md` | `WeeklyMenu` |
| Shopping list | `shopping-lists/<year>-w<week>.md` | `ShoppingList` |
| Dinner calendar | `calendars/<year>-w<week>.ics` | _(iCalendar, not OKF)_ |

## Privacy & sharing

- `recipes/`, `ingredients/` and `knowledge/` are the **shareable** knowledge.
- `household/` holds **private** data and is git-ignored by default.
- Never copy ratings, member names or history into `recipes/`, `ingredients/` or `knowledge/`.

## Ingredient catalogue

- Every ingredient referenced by a recipe should exist as a concept in `ingredients/`.
- When a recipe needs an ingredient that is missing, create the concept first, then link
  to it. Reuse existing concepts (check `aliases`) instead of creating duplicates.
- Ingredient front matter: `unit` (default measure), `section` (store section) and
  `aliases` (alternative spellings) drive shopping-list aggregation.

## No persistent inventory

There is **no** pantry/stock file. "Already have" and "must use up" items are
conversational inputs captured per week inside the relevant `menus/<week>.md` file.

## Culinary knowledge

- `knowledge/` holds general cooking know-how the agent uses to improve recipes and give
  tips: `principles/` (food chemistry — the "why"), `techniques/` (methods — the "how"),
  `troubleshooting/` (symptom → cause → fix) and `substitutions/` (swaps & scaling).
- Write notes **in your own words**; never copy source text. Back claims with a
  `# Citations` section linking to authoritative sources.
- Cross-link recipes to the principles/techniques they rely on, and consult
  `troubleshooting/` when the user reports how a dish turned out.
