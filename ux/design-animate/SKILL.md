---
name: design-animate
description: "Add purposeful motion with modern CSS (scroll-driven animations, view transitions, @starting-style) or Flutter implicit animations, with reduced-motion support. Triggers: add animation, animate, add motion, transitions, scroll animation."
version: "1.1.0"
category: ux
platforms:
  - CLAUDE_CODE
---

Find where the interface feels abrupt or static and add motion that helps users: orientation, feedback, continuity or hierarchy. Implement it with platform-native features and no new animation libraries. Decide and implement rather than asking.

**Focus:** `$ARGUMENTS` if given (e.g. "scroll reveal on landing page", "page transitions", "button micro-interactions"); otherwise the whole UI.

## 1. Inventory

Detect the stack and existing motion (`@keyframes`, `transition`, View Transitions, `AnimationController`, installed libraries such as Framer Motion, GSAP, Lottie or flutter_animate) and read any design context in CLAUDE.md. Extend what exists. Use an animation library only if the project already has it.

Then fill gaps in this priority order: screen entry, route transitions, scroll reveals, interaction feedback (hover, press, focus, toggles), state changes (show/hide, expand, tab switch), staggered lists, dialog enter/exit, and decorative flourishes last. If the project has no motion yet, start with entries and micro-interactions only.

## 2. Motion rules

- **Durations:** micro-interactions 100 to 200ms; transitions 200 to 400ms; entrances 300 to 600ms; sequences 400 to 800ms total. Nothing over 1000ms.
- **Easing:** enter `cubic-bezier(0, 0, 0.2, 1)`; exit `cubic-bezier(0.4, 0, 1, 1)`; move `cubic-bezier(0.4, 0, 0.2, 1)`; overshoot `cubic-bezier(0.34, 1.56, 0.64, 1)`, used sparingly. `linear` only for continuous motion (spinners) and scroll-linked timelines.
- **Properties:** animate `transform` and `opacity` (compositor-friendly); `filter` and `clip-path` are acceptable in moderation. Don't animate `width`, `height`, `top`, `left`, `margin` or `padding`. For `height: auto`, use `interpolate-size: allow-keywords` (Chromium; set it on `:root`) with an instant fallback elsewhere.
- **Never block content:** load animations mustn't delay readable content by more than ~300ms, interaction stays possible mid-animation, no information is conveyed only through motion, and infinite animations pause when off-screen. Use `will-change` only on elements that need it, never globally.

## 3. Web patterns

Scroll reveal, gated so unsupported browsers (Firefox) show content normally:

```css
@supports (animation-timeline: view()) {
  .reveal {
    animation: reveal-up linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }
}
@keyframes reveal-up {
  from {
    opacity: 0;
    transform: translateY(2rem);
  }
}
```

Scroll-linked effects use the same mechanism: a progress bar is `scaleX(0 → 1)` with `animation-timeline: scroll(root)`, and parallax is a `translateY` range on `scroll()`. Items in a list each get their own `view()` timeline, so they stagger naturally without `nth-child` delays.

View transitions: cross-document with `@view-transition { navigation: auto; }`, and SPA navigation with `document.startViewTransition(() => updateDom())` (feature-detect it). Give shared elements a unique `view-transition-name` and tune `::view-transition-old/new(name)` timing.

Enter and exit for dialogs, popovers and inserted elements with `@starting-style`. Define the closed state too, so exit animates:

```css
dialog {
  opacity: 0;
  transform: translateY(1rem) scale(0.97);
  transition:
    opacity 0.25s,
    transform 0.25s,
    overlay 0.25s allow-discrete,
    display 0.25s allow-discrete;
}
dialog[open] {
  opacity: 1;
  transform: none;
  @starting-style {
    opacity: 0;
    transform: translateY(1rem) scale(0.97);
  }
}
```

Use the same approach for `[popover]:popover-open`, `::backdrop` and toasts.

Micro-interactions: press `scale(0.97)` on `:active` (~100ms); hover color transitions (~150ms); a toggle thumb `translateX` with overshoot easing; `:focus-visible` outlines that stay clearly visible. Loading: a skeleton shimmer (`background-position` sweep, ~1.5s, paused under reduced motion) or a CSS spinner.

## 4. Flutter patterns

- Prefer implicit animations: `AnimatedContainer`, `AnimatedSwitcher` (fade plus slight slide), `AnimatedOpacity`/`AnimatedScale`/`AnimatedSlide`, `TweenAnimationBuilder`. Reach for `AnimationController` only for sequences or staggering, and always dispose it.
- `Hero` with matching tags for shared elements; `PageRouteBuilder` or go_router `CustomTransitionPage` for slide or fade-and-scale route transitions using `Curves.easeOutQuart`/`easeOutCubic`.
- Stagger lists with a per-item controller delayed by ~50ms × index (check `mounted` before `forward()`), or flutter_animate if it's already a dependency.
- Press feedback: `AnimatedScale` to 0.97 driven by tap-down/up/cancel.

## 5. Reduced motion

Required everywhere motion is added.

- Web: `@media (prefers-reduced-motion: reduce)` either disables the added animations per selector (preferred: keep the end state visible) or applies the global reset (durations 0.01ms, a single iteration, `scroll-behavior: auto`).
- Flutter: `MediaQuery.disableAnimationsOf(context)` → use `Duration.zero`.
- With motion off, all content is visible and everything still works.

## Done when

The build passes (fix and retry up to 3 times); the rules in section 2 hold for everything you added; reduced motion is handled; and no new libraries were introduced.

## Output

```
## Motion Implementation Complete
Animations added: N (scroll-driven N, view transitions N, @starting-style N, micro-interactions N, Flutter implicit N, explicit N)
Reduced motion: method | Compositor-friendly properties only: yes/no | Build: passed/failed

### What I added (2 to 3 sentences on the motion decisions)

| Element | Type | Duration | Easing | Trigger |

### Files changed
- path: what was added
```

If you relied on platform features or APIs these instructions don't cover, list them under "Suggested Skill Improvements".
