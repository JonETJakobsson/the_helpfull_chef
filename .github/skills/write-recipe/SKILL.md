---
name: write-recipe
description: "Convert any recipe (pasted text, notes, or a URL) into a structured OKF recipe file with ingredients grouped by component (sås, stek, marinad, salladsmix …) and a step-by-step timeline that gets every part ready at the same time. Use when the user shares or dictates a recipe, or asks to save, capture, structure or clean up a dish."
argument-hint: "paste a recipe or give a URL"
---

# Write Recipe

Turn a raw recipe into a consistent recipe file under `recipes/`.

## When to use

- The user pastes recipe text or gives a link to a recipe.
- The user describes a dish and wants it saved.
- An existing recipe needs restructuring into the standard format.

## Inputs to gather

- The recipe source (text or URL — fetch the URL if given).
- Portions: default **4** if not stated. If the source uses another yield, scale to 4
  (or the requested number) and note the original yield.
- Anything the user wants tagged (category, cuisine) that isn't obvious from the source.

## Procedure

1. **Read the source.** If it's a URL, fetch it. Extract the ingredient list, quantities
   and the method.
2. **Normalise units** to metric (g, kg, ml, dl, msk, tsk, st) and **scale** to the
   target portions. Record base `servings` in front matter.
3. **Group ingredients by component** — the part of the dish each ingredient belongs to,
   e.g. `Stek`, `Sås`, `Marinad`, `Salladsmix`, `Tillbehör`, `Garnering`. Use one
   `### <Component>` subheading per group under a `# Ingredienser` heading.
4. **Link every ingredient** to its concept in `ingredients/` using a bundle-absolute
   link, e.g. `[Potatis](/ingredients/potatis.md)`. If a concept is missing, create it
   first (see below), reusing existing entries where an alias matches.
5. **Write an ordered timeline** under `# Gör så här`. Order the steps by real cooking
   time so all components finish together (e.g. start what takes longest first, marinate
   ahead, make the sauce while the roast rests). Mention timings.
6. **Fill the front matter** (see schema) and choose a filename slug (lowercase,
   ASCII-folded Swedish, hyphenated).
7. **Save** the file to `recipes/<slug>.md` and add a line to `recipes/index.md`.

## Recipe front matter schema

```yaml
---
type: Recipe
title: <Rättens namn>
description: <En mening om rätten>
cuisine: <t.ex. Svensk, Italiensk, Thailändsk>
category: <vardag | fest | fine dining | snabb | ...>
cooking_time: <t.ex. 45 min>
servings: 4
nutrition: <valfritt — bästa uppskattning per portion, markera "uppskattad">
tags: [<tag>, <tag>]
timestamp: <ISO 8601>
---
```

- `nutrition` is optional and best-effort; only include it if useful, and label estimates.
- Add any extra keys that help (e.g. `oven_temp`).

## Creating a missing ingredient concept

Create `ingredients/<slug>.md`:

```yaml
---
type: Ingredient
title: <Kanoniskt namn>
description: <Kort beskrivning>
unit: <standardmått, t.ex. g, st, dl>
section: <butiksavdelning, t.ex. Frukt & Grönt, Mejeri, Kött & Chark>
aliases: [<alternativ stavning>, ...]
tags: [ingredient]
timestamp: <ISO 8601>
---
```

Then add it to the correct section in `ingredients/index.md`.

## Body template

```markdown
# Ingredienser

### Stek
* 500 g [Nötfärs](/ingredients/notfars.md)
* ...

### Sås
* 2 dl [Grädde](/ingredients/gradde.md)
* ...

# Gör så här

1. (t.ex. 0 min) Sätt ugnen på 200°C och koka upp saltat vatten till potatisen.
2. ...
```

## Output

Report the new file path and a one-line summary. Do **not** touch ratings or history.
