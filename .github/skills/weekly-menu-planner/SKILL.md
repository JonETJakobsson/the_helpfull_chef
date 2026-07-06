---
name: weekly-menu-planner
description: "Plan a week of weekday dinners (5 by default) from the user's current cravings, ingredients to use up, food already at home, family ratings, and how recently each dish was served (favouring dishes not eaten for a while). Use when the user asks what to eat this week, to plan/replan dinners, or for a menu."
argument-hint: "e.g. 'plan week 28, we have salmon to use up'"
---

# Weekly Menu Planner

Produce a balanced week of **5 weekday dinners** (Mon–Fri) and save it as a menu file.

## When to use

- "What should we eat this week?" / "Plan next week's dinners."
- The user wants to replan or adjust an existing week.

## Inputs

Gather these — ask briefly for what's missing, but proceed with sensible defaults:

1. **Which week.** Default to the upcoming Mon–Fri; derive `<year>-w<week>` (ISO week).
2. **Cravings** — what the family feels like this week (a cuisine, a specific dish, "något
   snabbt på tisdag", vegetarian night, etc.).
3. **Use up** — ingredients that must be used soon (conversational, not stored anywhere
   else). These get **priority** in dish selection.
4. **Already have** — things the user says are at home (so the shopping list can pre-check
   them later). Capture verbatim with any quantity given.
5. **Portions** — default 4.

## Data to read

- `recipes/` — candidate dishes (respect any allergies/dislikes in `household/members.md`).
- `household/members.md` — members, allergies, diets, dislikes, defaults.
- `household/ratings/<member>.md` — each member's scores (read all member files once).
- `household/meal-history/log.md` — when each dish was last served.

## Selection logic

Score each candidate recipe and pick 5 that also give variety across the week:

- **Cravings match** — strong boost for dishes fitting the stated cravings.
- **Use-up match** — strong boost for dishes that consume the "use up" ingredients.
- **Family rating** — average of members' scores (treat unrated as neutral). Avoid dishes
  a member strongly dislikes or can't eat.
- **Recency** — boost dishes not served for a long time; penalise anything served very
  recently (check the log).
- **Variety** — avoid repeating the same protein or cuisine on consecutive days; mix
  quick and slower dishes across the week.

If there aren't enough suitable recipes, offer to create new ones with the
**write-recipe** skill.

## Output — `menus/<year>-w<week>.md`

```markdown
---
type: WeeklyMenu
title: Meny vecka <WW> <YYYY>
description: Vardagsmiddagar måndag–fredag.
week: <YYYY>-w<WW>
servings: 4
tags: [menu]
timestamp: <ISO 8601>
---

# Planeringsunderlag

- **Sug:** <det användaren önskade>
- **Använd upp:** <råvaror att prioritera>
- **Finns hemma:** <sådant användaren sa att de har, med mängd om angiven>

# Middagar

| Dag | Rätt | Varför |
|-----|------|--------|
| Måndag  | [<Rätt>](/recipes/<slug>.md) | <t.ex. använder upp laxen> |
| Tisdag  | [<Rätt>](/recipes/<slug>.md) | <t.ex. snabb, högt betyg> |
| Onsdag  | [<Rätt>](/recipes/<slug>.md) | <...> |
| Torsdag | [<Rätt>](/recipes/<slug>.md) | <...> |
| Fredag  | [<Rätt>](/recipes/<slug>.md) | <...> |
```

Then add the menu to `menus/index.md`.

## After planning

- Offer to build the shopping list (**shopping-list** skill).
- Only log to `household/meal-history/log.md` when the family confirms a dish was actually
  cooked — not at planning time.
