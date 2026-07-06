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
| `weekly-menu-planner` | Plan 5 weekday dinners from cravings, stock to use up, ratings and recency. |
| `shopping-list` | Build a grouped shopping list for a planned week. |

## Repository layout

```
recipes/         Reusable recipes (shareable)
ingredients/     Canonical ingredient catalogue (shareable)
household/        Members, ratings, meal history (private, git-ignored)
menus/            Planned weekly menus
shopping-lists/   Generated shopping lists
.github/          The agent, its skills and global conventions
```

Defaults: **Swedish** content, **metric** units, **4 portions** unless you say otherwise.
