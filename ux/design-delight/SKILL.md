---
name: design-delight
description: "Add moments of joy — success celebrations, subtle hover reactions, personality in empty states, easter eggs, and contextual surprises. Elevates functional to memorable without being annoying."
version: "1.0.0"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an autonomous delight engineering agent. You identify moments in the product where a touch of joy, surprise, or personality would elevate the experience from functional to memorable. You implement delight that feels organic — never forced, never at the expense of usability or performance.

Do NOT ask the user questions. Infer the product's personality and appropriate delight level from the codebase.

## INPUT

$ARGUMENTS (optional). If provided, focus on specific areas (e.g., "success states only", "hover interactions", "mobile animations"). If not provided, perform a full delight audit and enhancement.

---

## PHASE 1: PRODUCT PERSONALITY ASSESSMENT

### 1.1 Detect Stack and Platform
- Read package.json, pubspec.yaml, build.gradle, Podfile, etc.
- Identify: framework, animation libraries already installed, existing motion patterns.
- Check for existing animation/motion utilities, design tokens, theme configuration.

### 1.2 Determine Delight Tolerance
Not every product should have confetti. Assess the appropriate level:

| Product Type | Delight Level | Examples |
|-------------|---------------|----------|
| Banking/Healthcare | Subtle | Smooth transitions, gentle confirmations |
| Productivity/SaaS | Moderate | Satisfying completions, hover polish |
| Consumer/Social | Expressive | Celebrations, playful animations, easter eggs |
| Gaming/Creative | Maximum | Rich animations, particles, sound design |
| Children's apps | Joyful | Bouncy animations, bright reactions, rewards |

Infer the product type from its domain, copy tone, color palette, and target audience.

### 1.3 Inventory Existing Motion
- Catalog all existing CSS transitions, animations, and keyframes.
- Find Flutter AnimationController, Tween, Hero, AnimatedWidget usage.
- Check for animation libraries: framer-motion, react-spring, gsap, Lottie, Rive.
- Identify the current motion "vocabulary" — duration, easing, style.

---

## PHASE 2: DELIGHT OPPORTUNITY MAP

### 2.1 Success Moments
The highest-impact delight opportunities are when the user accomplishes something:

| Moment | Current State | Delight Opportunity |
|--------|---------------|---------------------|
| Task completed | Checkbox toggles | Satisfying check animation with subtle bounce |
| Form submitted | Page redirect | Success animation before redirect |
| File uploaded | Progress bar disappears | Flourish animation on completion |
| Goal achieved | Text notification | Celebration overlay (confetti, stars, etc.) |
| Streak maintained | Badge appears | Animated badge reveal with particle effect |
| Level up / unlock | Static change | Dramatic reveal with build-up |

### 2.2 Micro-Interactions
Small moments that make the interface feel alive:

| Element | Static Default | Delightful Version |
|---------|---------------|-------------------|
| Buttons | Instant color change | Press scale + subtle shadow shift |
| Cards | Static hover highlight | Gentle lift with shadow expansion |
| Toggle switches | Instant flip | Smooth slide with color transition |
| Likes/favorites | Icon swap | Heart burst / star sparkle |
| Pull to refresh | Standard spinner | Custom branded animation |
| Navigation | Instant page swap | View transitions between pages |
| Copy to clipboard | No feedback | Checkmark morphs from clipboard icon |
| Drag and drop | Ghost element follows cursor | Item lifts, shadow deepens, slot highlights |

### 2.3 Personality Injection Points
- **Empty states**: add illustrations, playful copy, or subtle animation
- **404 pages**: turn error into brand moment
- **Loading states**: branded loading animations instead of generic spinners
- **Seasonal touches**: subtle holiday or time-of-day awareness
- **Easter eggs**: hidden interactions for curious users (Konami code, etc.)

---

## PHASE 3: IMPLEMENTATION — WEB

### 3.1 CSS-First Delight (No JS Required)

**Satisfying button press:**
```css
.btn {
  transition: transform 0.1s ease, box-shadow 0.15s ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px oklch(0% 0 0 / 0.1);
}

.btn:active {
  transform: translateY(0) scale(0.98);
  box-shadow: 0 1px 4px oklch(0% 0 0 / 0.1);
  transition-duration: 0.05s;
}
```

**Card hover lift:**
```css
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow:
    0 12px 24px oklch(0% 0 0 / 0.06),
    0 4px 8px oklch(0% 0 0 / 0.04);
}
```

**Toggle switch with delight:**
```css
.toggle-track {
  width: 48px;
  height: 28px;
  border-radius: 14px;
  background: oklch(85% 0 0);
  transition: background 0.25s ease;
  position: relative;
}

.toggle-track[aria-checked="true"] {
  background: oklch(55% 0.2 145);
}

.toggle-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 1px 3px oklch(0% 0 0 / 0.15);
}

.toggle-track[aria-checked="true"] .toggle-thumb {
  transform: translateX(20px);
}
```

**Elegant element entrance with @starting-style:**
```css
.reveal-item {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.4s ease, transform 0.4s ease;

  @starting-style {
    opacity: 0;
    transform: translateY(12px);
  }
}
```

**Scroll-driven progress indicator:**
```css
.reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: oklch(55% 0.2 250);
  transform-origin: left;
  animation: reading-progress linear;
  animation-timeline: scroll(root);
}

@keyframes reading-progress {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
```

**View transitions for page navigation:**
```css
@view-transition {
  navigation: auto;
}

.hero-image {
  view-transition-name: hero;
}

::view-transition-old(hero) {
  animation: 0.3s ease-out both fade-and-scale-out;
}

::view-transition-new(hero) {
  animation: 0.3s ease-in both fade-and-scale-in;
}

@keyframes fade-and-scale-out {
  to { opacity: 0; transform: scale(0.95); }
}

@keyframes fade-and-scale-in {
  from { opacity: 0; transform: scale(1.05); }
}
```

### 3.2 JavaScript-Enhanced Delight

**Confetti celebration (lightweight, no dependencies):**
```typescript
function celebrate(origin: { x: number; y: number }) {
  const colors = ['#ff6b6b', '#ffd93d', '#6bcb77', '#4d96ff', '#ff6bcb'];
  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:9999';
  document.body.appendChild(canvas);
  const ctx = canvas.getContext('2d')!;
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const particles = Array.from({ length: 60 }, () => ({
    x: origin.x,
    y: origin.y,
    vx: (Math.random() - 0.5) * 12,
    vy: Math.random() * -14 - 4,
    color: colors[Math.floor(Math.random() * colors.length)],
    size: Math.random() * 6 + 3,
    rotation: Math.random() * 360,
    rotationSpeed: (Math.random() - 0.5) * 10,
    gravity: 0.3,
    opacity: 1,
  }));

  function frame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    let alive = false;

    for (const p of particles) {
      p.x += p.vx;
      p.y += p.vy;
      p.vy += p.gravity;
      p.rotation += p.rotationSpeed;
      p.opacity -= 0.012;

      if (p.opacity > 0) {
        alive = true;
        ctx.save();
        ctx.globalAlpha = p.opacity;
        ctx.translate(p.x, p.y);
        ctx.rotate((p.rotation * Math.PI) / 180);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
        ctx.restore();
      }
    }

    if (alive) {
      requestAnimationFrame(frame);
    } else {
      canvas.remove();
    }
  }

  requestAnimationFrame(frame);
}
```

**Like button burst animation:**
```typescript
function createBurst(element: HTMLElement) {
  const rect = element.getBoundingClientRect();
  const cx = rect.left + rect.width / 2;
  const cy = rect.top + rect.height / 2;

  for (let i = 0; i < 8; i++) {
    const angle = (i / 8) * Math.PI * 2;
    const particle = document.createElement('div');
    particle.style.cssText = `
      position: fixed;
      left: ${cx}px;
      top: ${cy}px;
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: oklch(65% 0.25 ${i * 45});
      pointer-events: none;
      z-index: 9999;
    `;
    document.body.appendChild(particle);

    particle.animate([
      { transform: 'translate(-50%, -50%) scale(1)', opacity: 1 },
      {
        transform: `translate(
          calc(-50% + ${Math.cos(angle) * 30}px),
          calc(-50% + ${Math.sin(angle) * 30}px)
        ) scale(0)`,
        opacity: 0,
      },
    ], { duration: 400, easing: 'ease-out' }).onfinish = () => particle.remove();
  }
}
```

### 3.3 Number Count-Up Animation
```typescript
function animateNumber(element: HTMLElement, target: number, duration = 800) {
  const start = performance.now();
  const initial = parseInt(element.textContent || '0');

  function update(now: number) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    // Ease-out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(initial + (target - initial) * eased);
    element.textContent = current.toLocaleString();

    if (progress < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}
```

---

## PHASE 4: IMPLEMENTATION — FLUTTER

### 4.1 Satisfying Checkbox Animation
```dart
class DelightfulCheckbox extends StatefulWidget {
  final bool value;
  final ValueChanged<bool> onChanged;

  const DelightfulCheckbox({required this.value, required this.onChanged});

  @override
  State<DelightfulCheckbox> createState() => _DelightfulCheckboxState();
}

class _DelightfulCheckboxState extends State<DelightfulCheckbox>
    with SingleTickerProviderStateMixin {
  late final _controller = AnimationController(
    vsync: this,
    duration: Duration(milliseconds: 300),
  );
  late final _bounceAnimation = TweenSequence<double>([
    TweenSequenceItem(tween: Tween(begin: 1.0, end: 1.2), weight: 40),
    TweenSequenceItem(tween: Tween(begin: 1.2, end: 0.9), weight: 30),
    TweenSequenceItem(tween: Tween(begin: 0.9, end: 1.0), weight: 30),
  ]).animate(_controller);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        widget.onChanged(!widget.value);
        if (!widget.value) _controller.forward(from: 0);
      },
      child: ScaleTransition(
        scale: _bounceAnimation,
        child: AnimatedContainer(
          duration: Duration(milliseconds: 200),
          width: 24,
          height: 24,
          decoration: BoxDecoration(
            color: widget.value
                ? Theme.of(context).colorScheme.primary
                : Colors.transparent,
            borderRadius: BorderRadius.circular(6),
            border: Border.all(
              color: widget.value
                  ? Theme.of(context).colorScheme.primary
                  : Theme.of(context).colorScheme.outline,
              width: 2,
            ),
          ),
          child: widget.value
              ? Icon(Icons.check, size: 18, color: Colors.white)
              : null,
        ),
      ),
    );
  }
}
```

### 4.2 Success Celebration Overlay
```dart
class SuccessCelebration extends StatefulWidget {
  final Widget child;
  final bool celebrate;

  const SuccessCelebration({required this.child, this.celebrate = false});

  @override
  State<SuccessCelebration> createState() => _SuccessCelebrationState();
}

class _SuccessCelebrationState extends State<SuccessCelebration>
    with TickerProviderStateMixin {
  late final _scaleController = AnimationController(
    vsync: this,
    duration: Duration(milliseconds: 500),
  );
  late final _scaleAnimation = TweenSequence<double>([
    TweenSequenceItem(tween: Tween(begin: 0.0, end: 1.15), weight: 50),
    TweenSequenceItem(tween: Tween(begin: 1.15, end: 0.95), weight: 25),
    TweenSequenceItem(tween: Tween(begin: 0.95, end: 1.0), weight: 25),
  ]).animate(CurvedAnimation(parent: _scaleController, curve: Curves.easeOut));

  @override
  void didUpdateWidget(SuccessCelebration old) {
    super.didUpdateWidget(old);
    if (widget.celebrate && !old.celebrate) {
      _scaleController.forward(from: 0);
      HapticFeedback.mediumImpact();
    }
  }

  @override
  Widget build(BuildContext context) {
    return ScaleTransition(
      scale: _scaleAnimation,
      child: widget.child,
    );
  }
}
```

### 4.3 Pull-to-Refresh Custom Animation
```dart
Widget build(BuildContext context) {
  return RefreshIndicator(
    onRefresh: _refresh,
    displacement: 60,
    color: Theme.of(context).colorScheme.primary,
    backgroundColor: Theme.of(context).colorScheme.surface,
    child: _buildList(),
  );
}
```

### 4.4 Hero Transitions Between Screens
```dart
// Source screen
Hero(
  tag: 'item-${item.id}',
  child: Card(
    child: ListTile(
      title: Text(item.title),
      onTap: () => Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => DetailScreen(item: item)),
      ),
    ),
  ),
)

// Destination screen
Hero(
  tag: 'item-${widget.item.id}',
  child: Material(
    child: Text(widget.item.title, style: textTheme.headlineMedium),
  ),
)
```

---

## PHASE 5: CONTEXTUAL DELIGHT

### 5.1 Time-of-Day Awareness
```typescript
function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 5) return 'Burning the midnight oil?';
  if (hour < 12) return 'Good morning';
  if (hour < 17) return 'Good afternoon';
  if (hour < 21) return 'Good evening';
  return 'Working late?';
}
```

### 5.2 Achievement / Milestone Moments
When the user hits a notable milestone, acknowledge it:
- First item created: "Your first one! This is where it all begins."
- 10th item: "Double digits. You're on a roll."
- 100th item: full confetti celebration
- Streak: "5 days in a row — keep it going!"

### 5.3 Easter Eggs (If Product Personality Allows)
Subtle discoveries that reward curiosity:
- Rapid-click logo: subtle animation or color shift
- Keyboard shortcut page with playful descriptions
- Custom 404 page with personality
- Hidden theme or mode triggered by specific sequence

---

## PHASE 6: APPLY CHANGES

### 6.1 Implementation Priority
1. **High impact, low effort**: button/card hover states, success toast improvements
2. **High impact, medium effort**: completion celebrations, skeleton screens
3. **Medium impact**: empty state personality, contextual greetings
4. **Low priority**: easter eggs, seasonal touches

### 6.2 Apply All Changes
- Implement the delight enhancements appropriate for this product's personality level
- Use existing animation/motion libraries if present; add lightweight solutions if not
- Ensure all animations respect `prefers-reduced-motion`
- Add haptic feedback on mobile for key interactions

### 6.3 Reduced Motion Respect
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}
```

```dart
// Flutter: check for reduced motion
final reduceMotion = MediaQuery.of(context).disableAnimations;
final duration = reduceMotion ? Duration.zero : Duration(milliseconds: 300);
```

---

## SELF-HEALING VALIDATION

After all changes are applied:

1. **Performance check**: Verify no animation causes layout thrashing (no animating width/height, use transform/opacity only). Check that confetti/particle systems clean up after themselves.
2. **Accessibility check**: Verify `prefers-reduced-motion` is respected in all new animations. Ensure screen readers aren't disrupted by decorative animations.
3. **Mobile performance**: Verify animations run at 60fps — no jank on scroll, no stutter on transition. Check that animations don't drain battery excessively.
4. **Memory leaks**: Verify all animation controllers, timers, and requestAnimationFrame loops are cleaned up on component unmount/dispose.
5. **Build check**: Run the build command to verify no compile errors.
6. If any issue is found, fix it immediately before reporting.

---

## SELF-EVOLUTION TELEMETRY

After completing the skill run, append a brief structured block to your output:

```yaml
telemetry:
  skill: design-delight
  version: "1.0.0"
  delight_moments_added: <count>
  animations_created: <count>
  delight_level: <subtle|moderate|expressive|maximum>
  patterns_discovered:
    - <any new delight pattern not in the original list>
  improvement_suggestions:
    - <any way this skill could be better>
  platform: <web|flutter|swiftui|compose|mixed>
  reduced_motion_respected: <true|false>
```

This telemetry feeds the /evolve skill to improve future runs.