---
name: dinner-calendar
description: "Generate an .ics calendar file from a weekly menu so the dinners can be imported into a shared Google/family calendar. Each weekday dinner becomes a calendar event with the dish, cooking time, when to start cooking, and the ingredient list. Use when the user wants dinners in the calendar, an .ics file, or to share the week's meals with the family via calendar."
argument-hint: "e.g. 'lägg veckans middagar i kalendern'"
---

# Dinner Calendar (.ics)

Turn a weekly menu into an `.ics` file that can be imported into any calendar
(Google Calendar, Apple, Outlook). Concept A — no accounts or secrets needed; the user
imports the file into their shared family calendar.

## When to use

- "Lägg veckans middagar i kalendern" / "gör en kalenderfil" / "dela middagarna med familjen".
- After a menu has been planned with the **weekly-menu-planner** skill.

## Inputs

- **Which menu** — default the most recent `menus/<year>-w<week>.md`.
- **Middagstid** — when the meal is eaten. Default **17:00**.
- **Plats** — default **Hemma**.
- **Kalenderns tidszon** — default **Europe/Stockholm**.

## Procedure

1. **Read the menu** and, for each weekday dinner, open the linked recipe to get its
   `title`, `cooking_time`, `servings` and ingredient list.
2. **Compute each dinner's date** from the ISO week: Monday = day 1 of `<year>-w<week>`,
   then Tue–Fri follow. (Verify with the calendar; ISO weeks start on Monday.)
3. **Build one `VEVENT` per dinner**:
   - `SUMMARY:Middag: <rätt>`
   - `DTSTART`/`DTEND` at the dinner time, 1 hour long (the meal), with
     `TZID=Europe/Stockholm`.
   - `DESCRIPTION` = the **full recipe**: a link to the recipe (see *Länk till receptet*),
     portions, cooking time and a **suggested start-cooking time** (dinner time minus
     `cooking_time`), the ingredients grouped by component, and the numbered steps. A whole
     recipe fits comfortably (see the size note below).
   - Unique `UID` (e.g. `<year>-w<week>-<weekday>-<slug>@the-helpful-chef`).
4. **Wrap** the events in a `VCALENDAR` with a `Europe/Stockholm` `VTIMEZONE` block.
5. **Save** to `calendars/<year>-w<week>.ics` and add it to `calendars/index.md`.
6. **Tell the user how to import**: double-click the file, or in Google Calendar →
   *Settings → Import & export → Import* and pick the **shared family calendar** as target.

## .ics format rules (important)

- **Storlek:** Google Calendar tillåter ca **8 kB (~8000 tecken)** per `DESCRIPTION`. Ett
  helt recept är oftast 1–3 kB, så det får gott om plats.
- Escape special characters in text values: `\` → `\\`, `,` → `\,`, `;` → `\;`, and use
  `\n` for line breaks inside `DESCRIPTION`.
- To avoid heavy comma-escaping, separate ingredients with `\n` (one per line).
- Use 24-hour local times in `YYYYMMDDTHHMMSS` form together with `TZID=Europe/Stockholm`.
- `DTSTAMP` is the generation time in UTC (`...Z`).
- Keep one property per line. Very long lines may be folded (a CRLF followed by a space),
  but Google Calendar tolerates unfolded lines.

## Template

```ics
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//The Helpful Chef//Middagsmeny//SV
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VTIMEZONE
TZID:Europe/Stockholm
BEGIN:STANDARD
DTSTART:19701025T030000
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
TZNAME:CET
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19700329T020000
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
TZNAME:CEST
END:DAYLIGHT
END:VTIMEZONE
BEGIN:VEVENT
UID:2026-w29-mon-korv-stroganoff@the-helpful-chef
DTSTAMP:20260709T120000Z
DTSTART;TZID=Europe/Stockholm:20260713T170000
DTEND;TZID=Europe/Stockholm:20260713T180000
SUMMARY:Middag: Korv Stroganoff
LOCATION:Hemma
DESCRIPTION:Recept: https://github.com/JonETJakobsson/the_helpfull_chef/blob/main/recipes/korv-stroganoff.md\n\nPortioner: 4\nTillagningstid: 30 min (börja laga ca 16:30)\n\nINGREDIENSER\nGryta:\n- 400 g falukorv\n- 1 gul lök\n- ...\n\nGÖR SÅ HÄR\n1. Koka riset.\n2. ... (escapa kommatecken som \, och radbrytningar som \n)
END:VEVENT
END:VCALENDAR
```

## Länk till receptet

Varje event inleds med en länk till receptet så mottagaren kan öppna den snyggt renderade
versionen:

- **GitHub (nu):** `https://github.com/JonETJakobsson/the_helpfull_chef/blob/main/recipes/<slug>.md`
  — kräver att repot är publikt (eller att mottagaren har åtkomst). GitHub renderar markdown
  fint, men OKF:s bundle-absoluta `/...`-länkar inuti filen är inte klickbara i blob-vyn.
- **GitHub Pages (rekommenderat mål):** publicera den delbara delen (`recipes/`,
  `ingredients/`, `knowledge/`) som en liten webbplats. `household/` är git-ignorerad och
  följer inte med, så inget privat läcker. Länken blir då
  `https://jonetjakobsson.github.io/the_helpfull_chef/recipes/<slug>/`.

Håll bas-URL:en konsekvent i alla events (default: GitHub-blob tills Pages är uppsatt).

## Future upgrade (Concept B)

When this works well, the same skill can push events straight into a shared Google
Calendar via the Calendar API (OAuth). Credentials/tokens must live **outside** the repo
or in the git-ignored `household/` — never commit them.

## Output

Report the `.ics` path and the one-line import instruction. Do **not** modify recipes,
ratings or history.
