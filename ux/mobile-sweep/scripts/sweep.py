#!/usr/bin/env python3
"""
mobile-sweep — find layouts that look fine on desktop but break on phones.

Loads a URL in headless Chromium at three breakpoints (small Android, iPhone,
iPad portrait), walks every visible interactive element + every visible
dialog/modal, and surfaces:

  ERROR  — touch targets < 44px, off-screen horizontal overflow, clipped text
  WARN   — modals wider than 100vw - 16px, narrow fixed-width inputs

Optionally also runs a static scan of local CSS for grid-template-columns
patterns that pack too many fixed-pixel widths without a mobile override.

Usage:
  python3 sweep.py <URL>
  python3 sweep.py <URL> --open-selectors "#open-modal-btn,#open-settings-btn"
  python3 sweep.py <URL> --static-css <PATH>
  python3 sweep.py <URL> --out mobile-sweep-out
  python3 sweep.py <URL> --breakpoints 360,390,768

Requires: pip install playwright && playwright install chromium
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
except ImportError:
    print("ERROR: playwright is not installed.", file=sys.stderr)
    print("Install with: pip install playwright && playwright install chromium", file=sys.stderr)
    sys.exit(2)

DEFAULT_BREAKPOINTS = [
    (360, 640, "Small Android"),
    (390, 844, "iPhone 13/14/15"),
    (768, 1024, "iPad portrait"),
]

# JS that runs in the page to collect findings. Takes an opts object:
#   { ignoreSelectors: string[], disableDefaultIgnores: boolean }
# Returns an array of finding objects ({ kind, severity, selector, label,
# rect, text, scrollWidth, clientWidth, width, height, computedRule, ... }).
COLLECT_JS = r"""
(opts) => {
  const findings = [];
  const ignoreSelectors = (opts && opts.ignoreSelectors) || [];
  const disableDefaultIgnores = !!(opts && opts.disableDefaultIgnores);
  const viewportW = document.documentElement.clientWidth;
  const viewportH = document.documentElement.clientHeight;
  const isInteractive = (el) => {
    const tag = el.tagName.toLowerCase();
    if (["button", "a", "input", "select", "textarea"].includes(tag)) return true;
    const role = (el.getAttribute("role") || "").toLowerCase();
    return ["button", "link", "menuitem", "tab", "checkbox", "switch"].includes(role);
  };
  // Default exemptions for findings the user can't usefully act on:
  //
  // (1) Visually-hidden a11y elements — skip-to-content links, sr-only
  //     containers. They're intentionally 1×1px and/or positioned off-screen
  //     until focused. Exempted from ALL kinds (small-touch-target,
  //     clipped-text, off-screen-left).
  //
  // (2) Inline text links in prose — WCAG 2.5.8 explicitly exempts these
  //     from the 24×24 target-size rule. Exempted from small-touch-target.
  //
  // Pass --no-default-ignores to disable; pass --ignore-selectors to add more.
  const matchesUserIgnore = (el) => {
    for (const sel of ignoreSelectors) {
      try { if (el.matches(sel)) return true; } catch (_) {}
    }
    return false;
  };
  const isVisuallyHidden = (el) => {
    if (disableDefaultIgnores) return false;
    const cls = (typeof el.className === "string" ? el.className : "") || "";
    const aria = (el.getAttribute("aria-label") || "").toLowerCase();
    if (/(^|\s)(skip[-_]?(to|content|nav)|sr-only|visually-hidden|screen-reader-text|usa-sr-only)/i.test(cls)) return true;
    if (/^skip\b/.test(aria)) return true;
    // Structural detection: a 1×1 (or smaller) absolutely-positioned element
    // with overflow hidden / clip / clip-path is the canonical SR-only pattern.
    const r = el.getBoundingClientRect();
    if (r.width <= 2 && r.height <= 2) {
      const s = getComputedStyle(el);
      if (
        s.position === "absolute" &&
        (s.overflow === "hidden" || s.clipPath !== "none" || s.clip !== "auto")
      ) return true;
    }
    return false;
  };
  const isExemptFromTouchTargetCheck = (el) => {
    if (matchesUserIgnore(el)) return true;
    if (isVisuallyHidden(el)) return true;
    if (disableDefaultIgnores) return false;
    if (el.tagName.toLowerCase() === "a") {
      const proseAncestor = el.closest(
        "p, li, td, dd, blockquote, [class*='prose'], [class*='Prose']",
      );
      if (proseAncestor) return true;
    }
    return false;
  };
  const isVisible = (el) => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return false;
    const s = getComputedStyle(el);
    if (s.visibility === "hidden" || s.display === "none" || s.opacity === "0") return false;
    if (r.bottom < 0 || r.top > viewportH * 3) return false; // ignore far-off-screen content
    return true;
  };
  // Build a stable-ish selector — id if present, else tag + class chain
  const sel = (el) => {
    if (el.id) return "#" + el.id;
    let s = el.tagName.toLowerCase();
    if (el.className && typeof el.className === "string") {
      const cls = el.className.trim().split(/\s+/).slice(0, 3).join(".");
      if (cls) s += "." + cls;
    }
    return s;
  };
  const label = (el) => {
    const aria = el.getAttribute("aria-label");
    if (aria) return aria.slice(0, 60);
    const t = (el.textContent || "").trim().replace(/\s+/g, " ");
    if (t) return t.slice(0, 60);
    const ph = el.getAttribute("placeholder") || el.getAttribute("title");
    if (ph) return ph.slice(0, 60);
    return "";
  };

  const all = document.querySelectorAll("button, a, input, select, textarea, [role='button'], [role='link'], [role='menuitem'], [role='tab'], [role='checkbox'], [role='switch']");
  for (const el of all) {
    if (!isVisible(el)) continue;
    // Visually-hidden a11y elements are intentionally tiny / off-screen — they
    // shouldn't trigger any of the geometry checks (off-screen, clipped-text,
    // or small-touch-target). User-provided --ignore-selectors also short-
    // circuits the whole element, not just touch-target.
    if (matchesUserIgnore(el) || isVisuallyHidden(el)) continue;
    const r = el.getBoundingClientRect();

    // Off-screen horizontal overflow
    if (r.right > viewportW + 1) {
      findings.push({
        kind: "off-screen",
        severity: "error",
        selector: sel(el),
        label: label(el),
        rect: { x: r.x, y: r.y, w: r.width, h: r.height },
        overflowPx: Math.round(r.right - viewportW),
      });
    }
    if (r.left < -1) {
      findings.push({
        kind: "off-screen-left",
        severity: "error",
        selector: sel(el),
        label: label(el),
        rect: { x: r.x, y: r.y, w: r.width, h: r.height },
        overflowPx: Math.round(-r.left),
      });
    }

    // Touch target too small (only flag if not pure decoration and not
    // WCAG-exempt — see isExemptFromTouchTargetCheck above).
    const minDim = Math.min(r.width, r.height);
    if (
      isInteractive(el)
      && minDim > 0
      && minDim < 44
      && !isExemptFromTouchTargetCheck(el)
    ) {
      findings.push({
        kind: "small-touch-target",
        severity: "error",
        selector: sel(el),
        label: label(el),
        rect: { x: r.x, y: r.y, w: r.width, h: r.height },
        width: Math.round(r.width),
        height: Math.round(r.height),
      });
    }

    // Clipped text inside inputs/buttons
    const sw = el.scrollWidth, cw = el.clientWidth;
    if (sw > cw + 4 && el.tagName !== "SELECT") {
      // Inputs naturally support scrollLeft when focused — still flag because
      // it means the visible label is being cut off when the user isn't typing.
      findings.push({
        kind: "clipped-text",
        severity: "error",
        selector: sel(el),
        label: label(el),
        rect: { x: r.x, y: r.y, w: r.width, h: r.height },
        scrollWidth: sw,
        clientWidth: cw,
        clippedPx: sw - cw,
      });
    }
  }

  // Modals / dialogs / popovers — check width and inside-bounds
  const dialogs = document.querySelectorAll('[role="dialog"], .modal, .modal-content, [aria-modal="true"], dialog');
  for (const el of dialogs) {
    if (!isVisible(el)) continue;
    const r = el.getBoundingClientRect();
    const maxAcceptable = viewportW - 16;
    if (r.width > maxAcceptable + 1) {
      findings.push({
        kind: "modal-too-wide",
        severity: "warn",
        selector: sel(el),
        label: label(el) || "(dialog)",
        rect: { x: r.x, y: r.y, w: r.width, h: r.height },
        width: Math.round(r.width),
        max: maxAcceptable,
      });
    }
    if (r.right > viewportW + 1 || r.left < -1) {
      findings.push({
        kind: "modal-off-screen",
        severity: "error",
        selector: sel(el),
        label: label(el) || "(dialog)",
        rect: { x: r.x, y: r.y, w: r.width, h: r.height },
        overflowPx: Math.round(Math.max(r.right - viewportW, -r.left, 0)),
      });
    }
  }
  return findings;
}
"""

def static_css_scan(root: Path):
    """Surface grid-template-columns / grid-template-areas with too many fixed pixels.

    Heuristic: if a grid-template-columns has 3+ fixed-pixel values whose sum
    exceeds 200px, AND the same selector has no @media (max-width: ...)
    override of grid-template-columns or grid-template-areas, flag it.
    """
    warnings = []
    css_paths = []
    for p in root.rglob("*"):
        if p.suffix.lower() in (".css", ".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"):
            if any(part in {"node_modules", ".git", "dist", "build", ".next", "out"} for part in p.parts):
                continue
            css_paths.append(p)
    grid_re = re.compile(r"([\.#][A-Za-z0-9_\-]+(?:\s*[>+~]\s*[\.#A-Za-z0-9_\-]+)*)\s*\{[^}]*?grid-template-columns\s*:\s*([^;}]+)", re.DOTALL)
    media_re = re.compile(r"@media[^{]*max-width[^{]*\{(.*?)\}\s*\}", re.DOTALL)
    px_re = re.compile(r"\b(\d+(?:\.\d+)?)px\b")
    for path in css_paths:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # Find media-query-protected selectors so we can skip them
        protected = set()
        for m in media_re.finditer(text):
            body = m.group(1)
            for sm in re.finditer(r"([\.#][A-Za-z0-9_\-]+).*?grid-template-(columns|areas)", body, re.DOTALL):
                protected.add(sm.group(1))
        for m in grid_re.finditer(text):
            selector = m.group(1).strip().split()[0]  # leading token
            columns = m.group(2).strip()
            if selector in protected:
                continue
            px_vals = [float(x) for x in px_re.findall(columns)]
            if len(px_vals) >= 3 and sum(px_vals) > 200:
                line = text[:m.start()].count("\n") + 1
                warnings.append({
                    "kind": "rigid-grid",
                    "severity": "warn",
                    "src": str(path),
                    "line": line,
                    "selector": selector,
                    "columns": columns[:120],
                    "fixed_sum": sum(px_vals),
                    "fix": "Add a @media (max-width: 640px) override that uses grid-template-areas to stack fields, or switch fixed widths to fr/minmax(0,1fr).",
                })
    return warnings

def sweep_url(
    url,
    breakpoints,
    out_dir,
    open_selectors=None,
    wait_selectors=None,
    ignore_selectors=None,
    disable_default_ignores=False,
):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    open_selectors = open_selectors or []
    wait_selectors = wait_selectors or []
    ignore_selectors = ignore_selectors or []
    collect_opts = {
        "ignoreSelectors": ignore_selectors,
        "disableDefaultIgnores": disable_default_ignores,
    }
    all_findings = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for (w, h, name) in breakpoints:
            context = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=2,
                                          is_mobile=w <= 480, has_touch=w <= 480)
            page = context.new_page()
            try:
                page.goto(url, wait_until="networkidle", timeout=20000)
            except PWTimeout:
                pass  # proceed with whatever loaded
            for s in wait_selectors:
                try: page.wait_for_selector(s, timeout=3000)
                except PWTimeout: pass
            page.wait_for_timeout(500)
            # Sweep the default state
            findings = page.evaluate(COLLECT_JS, collect_opts)
            for f in findings:
                f["breakpoint"] = f"{w}x{h} ({name})"
                f["state"] = "default"
            # Screenshot one per finding (capped)
            for i, f in enumerate(findings[:30]):
                try:
                    shot_path = out_dir / f"finding-{w}-default-{i}.png"
                    box = f.get("rect", {})
                    if box.get("w", 0) > 0 and box.get("h", 0) > 0:
                        x = max(0, box["x"] - 8); y = max(0, box["y"] - 8)
                        cw = min(w - x, box["w"] + 16); ch = min(h - y, box["h"] + 16)
                        if cw > 4 and ch > 4:
                            page.screenshot(path=str(shot_path), clip={"x": x, "y": y, "width": cw, "height": ch})
                            f["screenshot"] = str(shot_path)
                except Exception:
                    pass
            all_findings.extend(findings)
            # If the user passed --open-selectors, click each one and re-sweep
            for s in open_selectors:
                try:
                    el = page.query_selector(s)
                    if not el: continue
                    el.click()
                    page.wait_for_timeout(400)
                    extra = page.evaluate(COLLECT_JS, collect_opts)
                    for f in extra:
                        f["breakpoint"] = f"{w}x{h} ({name})"
                        f["state"] = f"after click {s}"
                    all_findings.extend(extra)
                except Exception:
                    pass
            context.close()
        browser.close()
    return all_findings

def render_report(runtime, static_warnings, url, breakpoints, out_dir):
    lines = []
    lines.append(f"# Mobile Sweep — {url}")
    lines.append("")
    bp_str = ", ".join(f"{w}x{h} ({n})" for (w, h, n) in breakpoints)
    err_count = sum(1 for f in runtime if f.get("severity") == "error")
    warn_count = sum(1 for f in runtime if f.get("severity") == "warn") + len(static_warnings)
    lines.append(f"_Breakpoints: {bp_str}_")
    lines.append(f"_**{err_count} errors**, **{warn_count} warnings**_")
    lines.append("")
    if not runtime and not static_warnings:
        lines.append("Clean. No off-screen overflow, no clipped text, no undersized touch targets, no rigid grids found.")
        return "\n".join(lines)

    errors = [f for f in runtime if f.get("severity") == "error"]
    warns_rt = [f for f in runtime if f.get("severity") == "warn"]

    def write_finding(lines, f):
        kind = f.get("kind", "?")
        bp = f.get("breakpoint", "")
        sel = f.get("selector", "")
        label = f.get("label", "")
        lines.append(f"### {kind} — `{sel}` ({bp})")
        if label:
            lines.append(f"_Label: \"{label}\"_")
        if kind == "small-touch-target":
            lines.append(f"- Size: {f.get('width')}×{f.get('height')}px (minimum 44×44 on touch surfaces)")
            lines.append(f"- Fix: bump `min-width` / `min-height` to 44px on a `@media (hover: none)` query, or use 48px to match Material guidance.")
        elif kind == "off-screen" or kind == "off-screen-left":
            lines.append(f"- Element extends {f.get('overflowPx')}px past the viewport edge.")
            lines.append(f"- Fix: confirm the parent container has `overflow: hidden` / `min-width: 0`, or shrink the element's grid/flex column.")
        elif kind == "clipped-text":
            lines.append(f"- scrollWidth {f.get('scrollWidth')} > clientWidth {f.get('clientWidth')} (clipped by {f.get('clippedPx')}px)")
            lines.append(f"- Fix: give the element more width on mobile, or restructure the layout (e.g., stack input fields vertically below 640px).")
        elif kind == "modal-too-wide":
            lines.append(f"- Modal width: {f.get('width')}px exceeds the safe max ({f.get('max')}px)")
            lines.append(f"- Fix: set the modal to `width: min(<desktop-width>, calc(100vw - 16px))`.")
        elif kind == "modal-off-screen":
            lines.append(f"- Modal hangs {f.get('overflowPx')}px past the viewport edge.")
        if f.get("screenshot"):
            lines.append(f"![]({Path(f['screenshot']).name})")
        lines.append("")

    if errors:
        lines.append("## Errors")
        lines.append("")
        for f in errors:
            write_finding(lines, f)

    if warns_rt:
        lines.append("## Warnings — runtime")
        lines.append("")
        for f in warns_rt:
            write_finding(lines, f)

    if static_warnings:
        lines.append("## Warnings — static CSS scan")
        lines.append("")
        for w in static_warnings:
            lines.append(f"### rigid-grid at `{w['selector']}`")
            lines.append(f"- `{w['src']}:{w['line']}`")
            lines.append(f"- columns: `{w['columns']}` (sum of fixed widths: {int(w['fixed_sum'])}px)")
            lines.append(f"- {w['fix']}")
            lines.append("")
    return "\n".join(lines)

def main():
    p = argparse.ArgumentParser(description="Sweep a web app at mobile breakpoints for layout bugs.")
    p.add_argument("url", help="URL of the app (Firebase Hosting URL, localhost:3000, file://… all work)")
    p.add_argument("--breakpoints", default="360,390,768",
                   help="Comma-separated viewport widths to test (default 360,390,768)")
    p.add_argument("--open-selectors", default="",
                   help="Comma-separated CSS selectors to click on each breakpoint before sweeping (lets you reach modals/menus)")
    p.add_argument("--wait-selectors", default="",
                   help="Comma-separated selectors to wait for after navigation")
    p.add_argument("--static-css", default="",
                   help="Path to scan for rigid-grid CSS issues (defaults to '.' — disable with '')")
    p.add_argument("--out", default="mobile-sweep-out",
                   help="Output directory for the report and screenshots")
    p.add_argument("--ignore-selectors", default="",
                   help="Comma-separated CSS selectors to skip during touch-target checks (in addition to the WCAG defaults: skip-to-content links + inline prose anchors)")
    p.add_argument("--no-default-ignores", action="store_true",
                   help="Disable the built-in WCAG exemptions (skip-to-content links, inline prose anchors). Use to verify a clean baseline.")
    args = p.parse_args()

    widths = [int(w) for w in args.breakpoints.split(",") if w.strip()]
    bp_map = {360: (360, 640, "Small Android"), 390: (390, 844, "iPhone"), 768: (768, 1024, "iPad portrait")}
    breakpoints = [bp_map.get(w, (w, max(640, int(w * 1.78)), f"{w}px")) for w in widths]

    open_sels = [s for s in args.open_selectors.split(",") if s.strip()]
    wait_sels = [s for s in args.wait_selectors.split(",") if s.strip()]
    ignore_sels = [s.strip() for s in args.ignore_selectors.split(",") if s.strip()]

    print(f"Sweeping {args.url} at {len(breakpoints)} breakpoints…", file=sys.stderr)
    runtime = sweep_url(
        args.url,
        breakpoints,
        args.out,
        open_selectors=open_sels,
        wait_selectors=wait_sels,
        ignore_selectors=ignore_sels,
        disable_default_ignores=args.no_default_ignores,
    )

    static_warnings = []
    if args.static_css != "":
        static_root = Path(args.static_css or ".")
        if static_root.exists():
            static_warnings = static_css_scan(static_root)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    report = render_report(runtime, static_warnings, args.url, breakpoints, args.out)
    report_path = out_dir / "mobile-sweep-report.md"
    report_path.write_text(report, encoding="utf-8")
    print(report)
    print(f"\nReport saved to: {report_path}", file=sys.stderr)

    # Exit nonzero if any errors so this can gate CI
    err_count = sum(1 for f in runtime if f.get("severity") == "error")
    sys.exit(1 if err_count else 0)

if __name__ == "__main__":
    main()
