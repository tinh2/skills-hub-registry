# Pattern: design-overhaul

Modernize an interface with tokens, build, polish, and optionally motion or audit.

## Trigger Phrases

* redesign the UI
* overhaul the design
* modernize the design
* design overhaul
* rebuild the interface
* make it look better
* polish the design

## Required Steps

1. **design-setup.** Skill: `design-setup`. Purpose: extract design tokens and brand context from the codebase.
2. **design-build.** Skill: `design-build`. Purpose: build distinctive interfaces using the extracted tokens.
3. **design-polish.** Skill: `design-polish`. Purpose: final pixel quality pass.

## Optional Steps

4. **design-audit.** Skill: `design-audit`. Include when accessibility or performance is a stated goal.
5. **design-animate.** Skill: `design-animate`. Include when motion is part of the brief.

## Handoff Notes

* design-setup to design-build: pass the extracted tokens file path.
* design-build to design-polish: pass the list of touched components.
