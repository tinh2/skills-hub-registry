---
name: css-token-sweep
description: |
  Statically scan a CSS / single-file HTML / multi-file frontend project for
  references to undefined CSS custom properties — the silent class of bug
  where `color: var(--ink-2)` is written but `--ink-2` is never declared in
  any `:root { ... }` block, and the text renders invisible because `var()`
  with no fallback resolves to the unset initial value.

  TRIGGER this skill whenever the user says any of: "css token", "design
  token", "var(", "custom property", "css variable", "theme variants",
  "invisible text", "missing token", "lint css", "audit my design system",
  "check theme", "verify dark mode tokens", "find undefined css vars",
  "make sure my styles are consistent", "sweep my app", "make sure this
  doesn't happen again" (in the context of a CSS contrast / visibility bug),
  or whenever they're adding theme variants / tokens to a Firebase-style
  single-file HTML app. Also use this proactively after writing new CSS
  styles in a project that uses CSS custom properties — the safety net is
  cheap; the silent invisible-text bug is expensive.

  Output: a markdown report grouped by severity, with file:line, the bad
  `var(--…)` reference, and a "did you mean?" suggestion mapping the typo
  to the closest existing token.
version: "1.0.0"
category: analyze
platforms: [CLAUDE_CODE]
---

# css-token-sweep

Find every `var(--name)` in a project where `--name` is not defined in any
`:root { ... }` block. Surface tokens defined in default `:root` but
quietly inherited (not overridden) by theme variants. Optionally flag
hardcoded colors that duplicate an existing token's value.

This is the missing lint pass that most design-system codebases never
add. Without it, a typo like `var(--ink-2)` instead of `var(--ink-soft)`
renders text in the unset color (often invisible against a white button)
and ships to production unnoticed.

The skill bundles `scripts/sweep.py` — a zero-dependency Python scanner.
Most of the work is mechanical, so the script does it deterministically;
the skill body just orchestrates running it, interpreting the output, and
proposing fixes.

============================================================
=== PRE-FLIGHT ===
============================================================

Before running, verify:

- [ ] A path was either passed in the slash-command args or there's an
      obvious project root in the current working directory.
- [ ] `python3` is on PATH (`python3 --version`).
- [ ] The path contains at least one `.css`, `.html`, `.htm`, `.jsx`,
      `.tsx`, `.vue`, or `.svelte` file. If it doesn't, the scan has nothing
      to do — say so and exit.

Recovery:

- No path given → default to the current working directory.
- No CSS sources found → tell the user and exit; do not invent files.
- Python missing → tell the user to install Python 3.8+ and stop.

============================================================
=== PHASE 1: RUN THE SCANNER ===
============================================================

Invoke the bundled scanner with the user's path (or `.`):

```bash
python3 ~/.claude/skills/css-token-sweep/scripts/sweep.py <PATH>
```

Useful flags:

| Flag                     | When to use                                                                                                                                                                                                             |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--strict`               | Wire into CI — exit 1 if any errors.                                                                                                                                                                                    |
| `--skip-warnings`        | First-pass triage; surface only the invisible-text errors.                                                                                                                                                              |
| `--ignore=--dx,--dy,--r` | Suppress CSS custom properties that are set at runtime via JS (`element.style.setProperty('--dx', '12px')`). The static scanner cannot see runtime sets, so animation-param vars are false positives unless added here. |
| `--json`                 | Machine-readable output for chaining into other tools or for the optional runtime-contrast follow-up below.                                                                                                             |

The scanner reports three findings:

1. **Errors — undefined `var(--name)` with no fallback.** This is the
   canonical invisible-text bug. A `var(--ink-2)` reference where
   `--ink-2` is defined nowhere falls back to the unset initial value;
   for `color` that is the unset paint color, which depending on context
   may render the text the same color as the background.

2. **Warnings — tokens defined in `:root` but not overridden in a
   `[data-theme="..."]` variant.** Heuristic: only color-like tokens
   (anything whose name contains `ink`, `surface`, `paper`, `bg`,
   `border`, `accent`, `text`, etc.) are surfaced, because shape and
   shadow tokens often legitimately stay shared across themes. The
   warning is a prompt to confirm the default value still reads
   correctly under each variant, not an automatic fix.

3. **Warnings — hardcoded hex colors that duplicate a token's value.**
   These are stylistic; the code works fine, but switching themes won't
   move them. Suggest replacing with `var(--matching-token)`.

VALIDATION: scanner exits cleanly and prints either "Clean." or a
report with concrete file:line locations.
FALLBACK: if the scanner errors on a specific file (permissions, weird
encoding), note the file in the report and continue with the rest.

============================================================
=== PHASE 2: INTERPRET AND FIX ===
============================================================

For each **error**, the report includes a "Did you mean?" suggestion
based on edit distance to the closest defined token. Take that
suggestion seriously — in nine cases out of ten it is exactly the right
fix, because the bug pattern is almost always a typo / wrong tier name
(`--ink-2` vs `--ink-soft`, `--bg-muted` vs `--surface-muted`, etc.).

Workflow:

1. Read the file the scanner pointed at.
2. Replace the bad `var(--…)` with the suggested token, or — if the
   suggestion is wrong — define the new token in `:root` (and in each
   theme variant).
3. Re-run the scanner. The errors block should be empty.

For **theme-variant warnings**, do not blindly add overrides. Read each
warning, look at the component that uses the token, and decide whether
the default value actually reads correctly in that variant. Many
shadow / radius / motion tokens legitimately stay the same across
themes — only color tokens need variant-specific overrides.

For **hardcoded-color warnings**, replace in place. This usually takes
one sed pass per color.

VALIDATION: a second scanner run reports 0 errors.
FALLBACK: if you cannot resolve an error (e.g., the token genuinely
does not exist anywhere in any related file), surface it to the user
explicitly with a recommendation — either define the token or remove
the dead reference.

============================================================
=== PHASE 3 (OPTIONAL): RUNTIME CONTRAST SWEEP ===
============================================================

Static token-existence checks do not catch a token that exists but
resolves to an unreadable color under a given theme. If the project has
multiple `data-theme` variants and the user wants belt-and-suspenders
coverage, do a runtime sweep with Playwright:

```javascript
// Pseudocode — adapt to the project's entry point.
for (const theme of ["light", "dark", "morning", "dusk"]) {
  await page.evaluate((t) => {
    document.documentElement.dataset.theme = t;
  }, theme);
  const lowContrast = await page.evaluate(() => {
    const out = [];
    const interactive = document.querySelectorAll(
      'button, a, input, [role="button"]',
    );
    for (const el of interactive) {
      const cs = getComputedStyle(el);
      const ratio = contrastRatio(cs.color, cs.backgroundColor);
      if (ratio < 3.0)
        out.push({ tag: el.tagName, text: el.textContent.slice(0, 40), ratio });
    }
    return out;
  });
  console.log(theme, lowContrast);
}
```

Only do this if (a) Playwright is already available in the environment
and (b) the project actually has multiple themes. Otherwise it is more
overhead than the static scan.

VALIDATION: each theme returns 0 low-contrast interactive elements, or
the user has reviewed and accepted any remaining hits.
FALLBACK: if Playwright is not available, document the gap in the final
report and stop. Do not try to install Playwright unprompted — the
static check already catches the highest-impact bugs.

============================================================
=== SELF-REVIEW ===
============================================================

Score the output (1–5):

- **Complete**: Every undefined-var error has been resolved (or
  explicitly noted as needs-human-judgment)?
- **Robust**: Did you account for runtime-set custom properties via
  `--ignore`? Did you skip false-positive warnings rather than apply
  noisy fixes?
- **Clean**: Is the report concise enough that the user can act on it
  without reading the underlying CSS line by line?

If any score < 4:

- Re-run with different flags to narrow the noise.
- For genuinely ambiguous cases (the suggested token is wrong), flag
  the case to the user with the two or three candidate tokens rather
  than silently picking one.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

After each run, append one entry to
`~/.claude/skills/css-token-sweep/LEARNINGS.md`:

```markdown
## <YYYY-MM-DD> — <project name + scan scope>

- **What worked:** <specific suggestion that was correct, or a flag
  combo that produced an actionable report>
- **What was awkward:** <false positive that the scanner could have
  avoided, a missed bug, or a slow step>
- **Suggested patch:** <one concrete improvement — "auto-detect
  inline-style runtime vars and skip them", "add `--include` glob
  to scan only one subdirectory", etc.>
- **Verdict:** [Smooth / Minor friction / Major friction]
```

---

## Anti-patterns this skill refuses

- Inventing a token to "fix" the error. If `var(--ink-2)` is bad, fix
  the reference or genuinely add the token — do not silently leave the
  reference and pretend the bug went away.
- Adding `var(--name, fallback)` everywhere as a workaround. Fallbacks
  hide real bugs and create theme inconsistency. Use them only for
  intentionally optional vars (e.g., user-customizable accents) and
  document the intent.
- Disabling the scanner for a whole file with `--ignore` instead of
  fixing the underlying issue. `--ignore` is for runtime-set vars,
  not for silencing bugs.
- Treating every theme-variant warning as a fix-required error. Many
  are intentional. Read each one and decide.
