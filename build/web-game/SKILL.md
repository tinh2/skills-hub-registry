---
name: web-game
description: "Scaffold a production-ready browser game (Phaser, PixiJS or Three.js) with Vite, TypeScript, input, audio, saves, responsive canvas and itch.io/PWA deploy. Triggers: web game, browser game, html5 game, phaser game, pixi game, three.js game."
version: "2.1.0"
category: build
platforms:
  - CLAUDE_CODE
---

Scaffold a complete, runnable browser game project that builds cleanly and is ready for real gameplay work. Infer choices from the arguments rather than asking.

## Arguments (`$ARGUMENTS`)

- Project name (first positional; default `WebGame`). Use kebab-case for the package, PascalCase for classes.
- Framework: `phaser` (default), `pixi`, `three`. Install the current stable major of each and check its docs for API changes (Phaser 4 and PixiJS 8 differ meaningfully from older tutorials).
- `2d` / `3d` (default 2D for Phaser/Pixi, 3D for Three).
- Genre hint (`platformer`, `puzzle`, `shooter`, `card`, `idle`, `match3`, `runner`…): shape the starter gameplay scene around it.
- `itch`, `pwa`, `mobile`: enable those targets.

## What to build

**Toolchain:** current Vite + TypeScript (`strict`, `moduleResolution: "bundler"`, `@/` alias matching Vite), ESLint flat config + Prettier, scripts `dev`, `build`, `preview`, `lint`, `typecheck`.

**Layout:** `src/{config,scenes|core,entities,systems,ui,utils,types}` and `public/assets/{images,audio/{music,sfx},fonts,data}`. Large assets live in `public/`, not in the bundle.

**Framework core**

- Phaser: typed game config (WebGL with Canvas fallback; Arcade physics for simple games, Matter for complex), Scale Manager, scenes Boot → Preload (progress bar) → Menu → Game → GameOver, plus a UI scene running in parallel for the HUD. Pixel-art settings when the genre calls for it.
- PixiJS: async `Application.init`, ticker-driven loop, a small scene manager with `init/enter/update/exit`, transitions and an overlay stack.
- Three.js: renderer, scene, camera and controls; ambient + directional light; `EffectComposer` post-processing; GLTF/texture loading; stats overlay in dev only.

**Systems**

- Input: keyboard (down / just pressed / just released), pointer and touch, gamepad, an action map that abstracts physical inputs, virtual joystick when `mobile`, pointer lock for 3D.
- Audio: music with crossfade, pooled SFX, per-channel volume, persisted mute, and resuming the AudioContext on first user gesture (browsers block autoplay). Spatial audio for 3D.
- Saves: versioned localStorage format with migrations, typed save data, debounced autosave, base64 import/export.
- Object pool for bullets, particles and enemies, with pre-warm and a max size.
- Responsive canvas: fit while keeping aspect ratio, debounced resize, fullscreen toggle, safe-area and no-zoom on mobile, device-pixel-ratio aware.
- Typed asset manifest (atlases, audio sprites, fonts, data) and a preloader with a minimum display time, error handling and retry.
- Game loop on `requestAnimationFrame` or the framework ticker with a fixed timestep, never `setInterval`.
- Dev-only debug tools: FPS overlay, collision debug draw, console cheats (skip level, god mode, spawn).

**Deploy**

- `itch`: GitHub Action that builds, zips `dist` and pushes with butler to the `html5` channel; note embed dimensions and fullscreen/mobile flags.
- `pwa`: manifest plus a service worker (cache-first for hashed assets, network-first for data, offline fallback).
- Static hosting config (Netlify or Vercel) with immutable cache headers for hashed files and basic security headers; a CI workflow running lint, typecheck and build.

Avoid `any`; define real interfaces for entities, events and save data.

## Done when

`npm install`, `npm run typecheck` and `npm run build` succeed and `npm run dev` shows the menu and a playable starter scene. If a check fails, make a minimal targeted fix and re-run (up to 3 attempts); if it still fails, report the error output for manual follow-up.

## Output

```
## Web Game Project Scaffolded
Project / Framework (+version) / Mode / Targets
| Category | Files | Description |   (source, config, scenes, systems, build, assets)
Core systems included: …
Setup: npm install → npm run dev (http://localhost:5173) → npm run build
```

Suggest follow-ups where useful: `/game-code-review`, `/game-performance`, `/game-ux`, `/game-qa`.

## Telemetry

If a project memory directory exists under `~/.claude/projects/`, append to its `skill-telemetry.md` (skip silently otherwise):

```
### /web-game — YYYY-MM-DD
- Outcome: SUCCESS | PARTIAL | FAILED
- Self-healed: yes (what) | no
- Iterations used: N / 3
- Bottleneck: phase that struggled, or none
- Suggestion: one-line improvement, or none
```
