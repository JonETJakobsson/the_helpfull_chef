---
name: write-recipe
description: "Convert any recipe (pasted text, notes, or a URL) into a structured OKF recipe file with ingredients grouped by component (sås, stek, marinad, salladsmix …) and a step-by-step timeline that gets every part ready at the same time. Also refines existing recipes from cooking feedback using the culinary knowledge base. Use when the user shares or dictates a recipe, asks to save/capture/structure a dish, or reports how a dish turned out and wants it improved."
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
6. **Link related knowledge (required).** Identify the core techniques and principles the
   recipe relies on (e.g. bryning, bräsering, emulsion, glutenutveckling). For each one,
   search `knowledge/` and add a `# Relaterad kunskap` section with bundle-absolute links
   to the matching concepts. If a technique or principle the recipe genuinely uses has
   **no** concept yet, create it as a stub (see below), add it to the bucket `index.md`,
   then link it — so the knowledge base grows with the recipes and no method is left
   unlinked.
7. **Fill the front matter** (see schema) and choose a filename slug (lowercase,
   ASCII-folded Swedish, hyphenated).
8. **Save** the file to `recipes/<slug>.md` and add a line to `recipes/index.md`.

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

## Creating a missing knowledge concept (stub)

When a recipe uses a technique/principle that has no concept yet, create a **stub** so the
link resolves and the gap is trackable. Put it in the right bucket
(`knowledge/principles/`, `techniques/`, `troubleshooting/` or `substitutions/`):

```yaml
---
type: <Principle | Technique | Troubleshooting | Substitution>
title: <Namn>
description: <En mening om vad det är>
status: stub
tags: [<tag>]
timestamp: <ISO 8601>
---

# Sammanfattning

<Några meningar med egna ord. Kopiera aldrig källtext.>

# Citations

[1] <Källa — t.ex. bok, uppslagsverk>.
```

- Tag it `status: stub` so a later deep-dive can find and flesh it out.
- Add a linked row to the bucket's `index.md`.
- Write notes **in your own words** with a `# Citations` section — never copy source text.

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

# Relaterad kunskap

* [Bryning & fräsning](/knowledge/techniques/bryning-och-fransning.md)
* [Maillardreaktionen](/knowledge/principles/maillardreaktionen.md)
```

## Refining a recipe from feedback

When the user reports how a dish turned out ("det blev för salt", "såsen sprack", "torrt"),
improve the recipe instead of writing a new one:

1. **Match the symptom** to a concept in `knowledge/troubleshooting/` and read it.
2. **Understand the cause** via the linked `principles/` concept.
3. **Propose concrete adjustments** to quantities, temperatures or steps, and explain the
   "why" in one line, citing the knowledge concept.
4. On the user's OK, **edit the recipe file** (quantities/steps), and make sure the
   `# Relaterad kunskap` section links the relevant technique/principle.
5. Optionally note the change so the improvement isn't lost.

## Output

Report the file path and a one-line summary. When refining, summarise what changed and why
(with the knowledge link). Do **not** touch ratings or history.
