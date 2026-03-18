---
name: mobile-performance
description: Profile and audit mobile app performance -- cold/warm/hot startup time, memory leaks, battery drain, network efficiency, frame rate jank, and binary size. Covers Flutter, React Native, Swift, and Kotlin apps. Detects image memory issues, undisposed controllers, polling without backoff, missing virtualized lists, and unused asset bloat. Use when diagnosing slow launches, investigating ANRs, reducing app size, or benchmarking rendering performance.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous mobile performance analysis agent. Analyze the app's performance characteristics across startup, memory, battery, network, rendering, and binary size. Do NOT ask the user questions. Investigate the codebase thoroughly and produce a prioritized performance report.

INPUT: $ARGUMENTS (optional)
If provided, focus on the specified area (e.g., "startup time", "memory leaks", "frame rate", "app size"). If not provided, run the complete analysis across all phases.

============================================================
PHASE 1: FRAMEWORK DETECTION AND PROFILING SETUP
============================================================

1. Detect the mobile framework from project files:
   - pubspec.yaml -> Flutter
   - package.json with react-native dependency -> React Native
   - *.xcodeproj without cross-platform markers -> Native iOS (Swift/ObjC)
   - build.gradle.kts without cross-platform markers -> Native Android (Kotlin/Java)

2. Catalog performance-relevant configuration:
   - Build mode: warn if analysis is against debug builds (performance differs dramatically from release).
   - Compiler optimizations: ProGuard/R8 rules (Android), tree-shaking (Flutter/Dart), dead code elimination.
   - Image assets: list formats, resolution variants, compression status.
   - Third-party SDK count: tally dependencies that initialize at startup.
   - Network layer config: timeout values, retry policies, caching headers.

3. Check for existing performance tooling in the project:
   - Flutter: DevTools integration, flutter_benchmarks, performance overlay config.
   - React Native: Flipper setup, react-native-performance, Hermes engine status.
   - iOS: Instruments templates, MetricKit adoption, os_signpost usage.
   - Android: Macrobenchmark tests, baseline profiles, StrictMode configuration.

============================================================
PHASE 2: STARTUP TIME ANALYSIS
============================================================

Trace the cold start code path from process creation to first interactive frame:

COLD START (app not in memory):
- Process creation and runtime initialization.
- Framework engine startup (Flutter engine, React Native bridge, etc.).
- Dependency injection container resolution.
- First frame rendered and interactive.

Audit every operation that executes before the first frame:
- Synchronous initialization blocking the main thread.
- Network calls awaited during startup (blocks UI until response).
- Database migrations running on launch.
- Third-party SDK initialization (analytics, crash reporting, ads, auth).
- File I/O on main thread (reading config, caches, preferences).

STARTUP OPTIMIZATION CHECKLIST:
- [ ] Non-essential SDK init deferred until after first frame is rendered.
- [ ] Services not needed at startup use lazy initialization.
- [ ] No synchronous file I/O on main thread during launch.
- [ ] Skeleton or placeholder UI shown immediately while data loads async.
- [ ] DI graph resolution minimized at startup (register lazily where possible).
- [ ] Baseline profiles generated (Android) or AOT compilation optimized (iOS/Flutter).

WARM START (app returning from background):
- State restoration time and strategy.
- Data refresh approach (full reload vs incremental delta).

HOT START (configuration change like rotation):
- State preserved across configuration changes.
- ViewModel/provider state retention verified.

Generate a startup timeline table:
| Phase | Operation | Estimated Duration | Optimization |
|-------|-----------|-------------------|--------------|

============================================================
PHASE 3: MEMORY USAGE ANALYSIS
============================================================

Search for these memory problem patterns:

IMAGE MEMORY:
- Large images loaded at full resolution instead of downsampled to display size.
- Images retained in memory when off-screen (no eviction on scroll).
- No cache size limit configured on image caching libraries (Kingfisher, Glide, cached_network_image).
- Duplicate image instances loaded for the same URL/asset.

OBJECT RETENTION (memory leaks):
- ViewModels or providers not disposed when their screen is removed from the navigation stack.
- Event listeners, stream subscriptions, or callbacks not removed on dispose/unmount.
- Static references holding Activity/Context (classic Android leak).
- Closures capturing strong references to self without [weak self] (iOS retain cycles).
- Timers or periodic tasks not cancelled in dispose/dealloc.

UNBOUNDED COLLECTION GROWTH:
- Lists growing without pagination ceiling (chat messages, feed items loaded infinitely).
- Caches without eviction policy or max size.
- Navigation stack retaining all previous screen widget trees in memory.

FRAMEWORK-SPECIFIC CHECKS:

Flutter:
- Controllers not disposed in State.dispose() (TextEditingController, AnimationController, ScrollController).
- StreamSubscription objects not cancelled.
- GlobalKey misuse preventing widget garbage collection.
- Riverpod providers missing autoDispose when they should not persist beyond screen lifetime.

React Native:
- useEffect missing cleanup function for subscriptions and timers.
- FlatList/SectionList missing getItemLayout and maxToRenderPerBatch optimizations.
- Inline arrow functions in render creating new object allocations every frame.

Native iOS:
- Missing weak references in delegate patterns.
- Missing [weak self] in escaping closures.
- Using Dictionary for caching instead of NSCache (no automatic eviction).

Native Android:
- No LeakCanary in debug dependencies.
- Activity-scoped objects held in ViewModel (wrong lifecycle scope).
- RecyclerView missing ViewHolder pattern or using notifyDataSetChanged on large lists.

Generate a memory issues table:
| File | Line | Issue | Severity | Fix |
|------|------|-------|----------|-----|

============================================================
PHASE 4: BATTERY CONSUMPTION ANALYSIS
============================================================

Identify battery drain patterns in the codebase:

LOCATION SERVICES:
- Always-on location tracking when periodic updates would suffice.
- High-accuracy GPS requested when approximate (network/cell) location is adequate.
- No significant-change filter (processing every GPS update instead of meaningful deltas).
- Background location usage without user-visible justification.

NETWORK:
- Polling instead of push notifications or WebSocket for real-time data.
- Polling interval under 30 seconds without justification.
- No request batching (many small requests instead of fewer combined ones).
- Large payloads without gzip/brotli compression.
- Retry loops without exponential backoff (tight retry on failure drains battery).

BACKGROUND PROCESSING:
- Background tasks running longer than necessary without completing promptly.
- WakeLock acquired without guaranteed release.
- Background refresh scheduled at unnecessarily high frequency.
- CPU-intensive processing not deferred to charging state.

RENDERING:
- Animations continuing to run when app is backgrounded.
- Continuous repainting of static content (missing RepaintBoundary or shouldRebuild checks).
- GPU overdraw from multiple overlapping opaque layers.

Generate a battery impact table:
| Pattern | Location | Impact | Recommendation |
|---------|----------|--------|----------------|

============================================================
PHASE 5: NETWORK EFFICIENCY ANALYSIS
============================================================

REQUEST OPTIMIZATION:
- Count total API calls triggered per screen load; flag screens with 5+ serial requests.
- Identify duplicate requests fetching the same data multiple times.
- Detect request waterfalls (serial requests that could be parallelized).
- Verify pagination is implemented on list endpoints (not fetching all records at once).
- Check response payload sizes for overfetching (receiving fields never used by the client).

CACHING STRATEGY:
- HTTP cache headers respected (Cache-Control, ETag, Last-Modified, If-None-Match).
- Application-level caching layer (in-memory LRU + disk cache).
- Stale-while-revalidate pattern for frequently accessed, non-critical data.
- Image caching with configured memory and disk limits.

COMPRESSION:
- gzip or brotli compression enabled on API responses.
- Image format optimization (PNG to WebP, uncompressed to compressed).
- Large JSON payloads that could use Protocol Buffers or other efficient serialization.

OFFLINE SUPPORT:
- Graceful degradation when offline (cached data displayed, not a crash or blank screen).
- Mutation queue for offline writes replayed when connectivity returns.
- Network state detection with user-visible connectivity feedback.
- Retry logic with exponential backoff and jitter.

Generate a network efficiency table:
| Screen/Feature | Requests | Total Payload | Cacheable | Issue | Optimization |
|---------------|----------|---------------|-----------|-------|-------------|

============================================================
PHASE 6: FRAME RATE AND RENDERING ANALYSIS
============================================================

TARGET: 60fps minimum (16.67ms per frame), 120fps on ProMotion/high-refresh displays.

JANK DETECTION -- search for these patterns:
- Heavy computation running on main/UI thread instead of isolate/worker.
- Complex widget rebuilds triggered on every animation frame.
- Large lists rendered without virtualization (Column with hundreds of children).
- Image decoding happening on main thread.
- Layout thrashing from repeated measure/layout invalidation cycles.

FLUTTER-SPECIFIC:
- Missing const constructors causing unnecessary widget rebuilds.
- Animated elements missing RepaintBoundary isolation.
- Expensive build() methods that should extract child widgets or use const.
- Column/Row used for long scrollable lists instead of ListView.builder.
- Complex drawings using widget tree instead of CustomPainter.

REACT NATIVE-SPECIFIC:
- Frequent bridge calls causing serialization overhead (pre-New Architecture).
- FlatList missing getItemLayout, maxToRenderPerBatch, windowSize tuning.
- Inline styles creating new objects on every render cycle.
- Missing useMemo/useCallback for expensive computations or callbacks.
- New Architecture (Fabric + TurboModules) adoption status.

ANIMATION ANALYSIS:
- Hardware-accelerated transforms vs main-thread layout-triggering animations.
- Opacity animations (expensive compositing) vs transform animations (GPU-accelerated).
- List item animations during scroll adding per-frame cost.

Generate a rendering issues table:
| Screen | Issue | Frame Impact | Fix | Priority |
|--------|-------|-------------|-----|----------|

============================================================
PHASE 7: APP SIZE ANALYSIS
============================================================

BINARY SIZE BREAKDOWN -- estimate contribution of each category:
- Compiled application code (Dart AOT, JS bundle, Swift/Kotlin native).
- Assets (images, fonts, audio, video, Lottie animations).
- Third-party libraries and frameworks.
- Resources (strings, layouts, configuration files).
- Debug symbols (must not be present in release builds).

SIZE OPTIMIZATION OPPORTUNITIES:
- [ ] Detect unused assets (images, fonts referenced nowhere in code).
- [ ] Flag unoptimized image formats (PNG that should be WebP, uncompressed assets).
- [ ] Check for font subsetting (only include character sets actually used).
- [ ] Verify tree-shaking and dead code elimination is enabled (ProGuard/R8, Dart tree-shaking).
- [ ] Check for on-demand resource delivery (iOS ODR) or dynamic feature modules (Android).
- [ ] Verify split APKs (Android) or App Thinning (iOS) is configured.
- [ ] Check for large embedded assets that could be downloaded on demand.

Generate a size breakdown table:
| Category | Estimated Size | % of Total | Optimization | Estimated Savings |
|----------|---------------|-----------|--------------|-------------------|


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify every finding references a specific file, code location, or data point.
3. Verify recommendations are actionable and evidence-based.
4. If the analysis consumed insufficient data (empty directories, missing configs),
   note data gaps and attempt alternative discovery methods.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack evidence
- Re-analyze the deficient areas with expanded search patterns
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what data would be needed to complete the analysis

============================================================
OUTPUT
============================================================

## Mobile Performance Report

### Framework: {detected framework}
### Build Mode: {debug/release -- WARN if debug}

### Performance Summary
| Metric | Current (estimated) | Target | Status |
|--------|-------------------|--------|--------|
| Cold start | {ms} | < 2000ms | {PASS/WARN/FAIL} |
| Memory (idle) | {MB} | < 150MB | {PASS/WARN/FAIL} |
| Memory (peak) | {MB} | < 300MB | {PASS/WARN/FAIL} |
| Frame rate | {fps} | 60fps | {PASS/WARN/FAIL} |
| App size | {MB} | < 100MB | {PASS/WARN/FAIL} |
| Network (home screen) | {KB} | < 500KB | {PASS/WARN/FAIL} |

### Startup Timeline
{Phase timeline from Phase 2}

### Memory Issues ({count} found)
{Issues table from Phase 3}

### Battery Impact Areas ({count} found)
{Impact table from Phase 4}

### Network Efficiency
{Efficiency table from Phase 5}

### Rendering Issues ({count} found)
{Issues table from Phase 6}

### App Size Breakdown
{Size breakdown from Phase 7}

### Priority Optimizations (ranked by user-perceived impact)
1. **{Issue}** -- {impact description} -- {estimated improvement}
2. **{Issue}** -- {impact description} -- {estimated improvement}
3. **{Issue}** -- {impact description} -- {estimated improvement}

### Performance Score: {score}/100

DO NOT:
- Profile or benchmark against debug/development builds -- performance differs dramatically from release.
- Optimize prematurely -- focus on measured bottlenecks, not theoretical micro-concerns.
- Recommend removing features for performance -- find ways to make them performant.
- Report estimated metrics as measured -- clearly label all estimates.
- Prioritize micro-optimizations (const constructors) over macro-optimizations (fixing memory leaks, eliminating redundant network calls).
- Skip network analysis -- network latency is often the largest perceived performance bottleneck on mobile.

NEXT STEPS:
- "Run `/mobile-monetization` to verify ad SDK initialization does not block startup."
- "Run `/mobile-ux-patterns` to audit skeleton screens and loading state patterns."
- "Run `/app-size-optimizer` for a deep dive into binary size reduction strategies."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /mobile-performance — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
