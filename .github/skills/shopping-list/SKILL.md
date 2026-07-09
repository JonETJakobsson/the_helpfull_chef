---
name: shopping-list
description: "Build a grouped shopping list from a planned weekly menu — aggregating every recipe's ingredients scaled to the right portions, merging duplicates via the ingredient catalogue, grouping by store section, and pre-checking items the user already has at home. Use when the user wants groceries, an inköpslista, or to know what to buy for a menu."
argument-hint: "e.g. 'shopping list for week 28'"
---

# Shopping List

Turn a weekly menu into a grouped shopping list.

## When to use

- The user asks for groceries / an inköpslista for a planned week.
- After the weekly-menu-planner has produced a menu.

## Inputs

- **Which menu** — default to the most recent `menus/<year>-w<week>.md`.
- **Already have** — read the "Finns hemma" section of the menu file; also accept new
  "we already have X" statements in the conversation.
- **Portions** — use the menu's `servings` (default 4) unless the user overrides.

## Procedure

1. **Read the menu** and open each linked recipe.
2. **Collect ingredients** from every recipe, scaling quantities to the menu's portions.
3. **Normalise & merge** using the ingredient catalogue (`ingredients/`): resolve aliases
   to the canonical name and unit, then sum quantities for the same ingredient across
   recipes. Keep quantities in the ingredient's `unit`; if units genuinely differ and
   can't be combined, list them separately.
4. **Group by store section** using each ingredient's `section` (e.g. Frukt & Grönt,
   Kött & Chark, Fisk, Mejeri, Skafferi, Fryst, Bröd). Put anything without a known
   section under "Övrigt".
5. **Mark already-have items.** Every ingredient the menu needs is listed. For items the
   user said they already have, render the checkbox as checked `- [x]` and append
   `(finns hemma<, mängd om angiven>)`. Everything else is `- [ ]` (to buy).
6. **Save** to `shopping-lists/<year>-w<week>.md` and add it to `shopping-lists/index.md`.
7. **Append a plain copy-paste block** at the end of the file: a fenced code block titled
   "Kopiera till att-göra-app" with **one item per line**, `<mängd> <namn>` and no
   checkboxes, links or section headings. Include **only the items still to buy** (skip
   anything marked already-have). This block is what the user pastes straight into a todo
   app; the grouped checklist above stays for reading and ticking off.

## Output — `shopping-lists/<year>-w<week>.md`

````markdown
---
type: ShoppingList
title: Inköpslista vecka <WW> <YYYY>
description: Inköp för veckans middagar.
week: <YYYY>-w<WW>
menu: /menus/<YYYY>-w<WW>.md
servings: 4
tags: [shopping-list]
timestamp: <ISO 8601>
---

# Frukt & Grönt
- [ ] 1 kg [Potatis](/ingredients/potatis.md)
- [x] 2 st [Citron](/ingredients/citron.md) (finns hemma)

# Kött & Chark
- [ ] 500 g [Nötfärs](/ingredients/notfars.md)

# Fisk
- [x] 600 g [Laxfilé](/ingredients/laxfile.md) (finns hemma, ca 500 g — kontrollera)

# Mejeri
- [ ] 3 dl [Grädde](/ingredients/gradde.md)

# Kopiera till att-göra-app

```
1 kg Potatis
2 st Citron
500 g Nötfärs
3 dl Grädde
```
````

- The plain block lists **only items to buy** (no already-have rows), one per line, so it
  pastes cleanly into a todo/checklist app. Keep the grouped checklist above it intact.
- If a user's "already have" amount looks smaller than what's needed, still check it but
  add a short note (e.g. "ca 500 g — kontrollera") so they can verify before shopping.

## Output message

Point the user to the file and mention how many items are still to buy.
Do **not** modify ratings, recipes or history.
