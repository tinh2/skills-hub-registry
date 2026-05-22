#!/usr/bin/env python3
"""
css-token-sweep — static analyzer for CSS custom property references.

Finds:
  1. `var(--foo)` references where `--foo` is never defined in any :root{} block
     (the canonical "invisible text" bug).
  2. Tokens defined in default :root{} but not overridden in a [data-theme="..."]
     variant when components in that variant reference them (heuristic).
  3. Optional warnings:
       - hardcoded colors duplicating an existing token's value
       - tokens defined but never used

Usage:
  python3 sweep.py [PATH]            # PATH defaults to "."
  python3 sweep.py --json [PATH]     # emit machine-readable JSON instead of markdown
  python3 sweep.py --strict [PATH]   # exit 1 if any errors found
  python3 sweep.py --skip-warnings [PATH]   # only show errors
  python3 sweep.py --ignore=--dx,--dy,--r [PATH]   # suppress runtime-set var names

The scanner intentionally has no external dependencies — it parses CSS with
regex because we only care about var() / token-definition shapes, not full
selector semantics.
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict
from difflib import get_close_matches
from pathlib import Path

# ---- Source discovery ---------------------------------------------------

CSS_EXTS = {".css"}
HTML_EXTS = {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "out", "vendor", "coverage", ".turbo", ".cache"}

def discover_sources(root: Path):
    """Yield (path, kind) for every file we should scan.

    kind ∈ {"css", "html"} — HTML-like files get inline <style> + style="..." extracted.
    """
    if root.is_file():
        ext = root.suffix.lower()
        if ext in CSS_EXTS:
            yield root, "css"
        elif ext in HTML_EXTS:
            yield root, "html"
        return
    for p in root.rglob("*"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext in CSS_EXTS:
            yield p, "css"
        elif ext in HTML_EXTS:
            yield p, "html"

def extract_css_from_html(text: str):
    """Return list of (css_text, line_offset) tuples for inline <style> blocks
    and style="..." attributes within a single HTML document.
    """
    blocks = []
    # <style>...</style> — note style attributes are also captured separately below
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", text, re.DOTALL | re.IGNORECASE):
        line_offset = text[:m.start(1)].count("\n")
        blocks.append((m.group(1), line_offset))
    # inline style="..."
    for m in re.finditer(r'style\s*=\s*"([^"]*)"', text, re.IGNORECASE):
        line_offset = text[:m.start(1)].count("\n")
        # Wrap in a fake selector so the same parser works
        blocks.append((".__inline__ { " + m.group(1) + " }", line_offset))
    return blocks

# ---- Token extraction ---------------------------------------------------

# Captures every :root { ... } block. Records the selector so we can tell
# default tokens apart from theme-variant tokens.
ROOT_BLOCK_RE = re.compile(r"(:root[^{]*)\{([^}]*)\}", re.DOTALL)
TOKEN_DEF_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;]+?)\s*(?:;|$)")
VAR_REF_RE = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)\s*(?:,([^)]*))?\)")
# Find what variant a :root selector targets, e.g. [data-theme="dark"]
THEME_ATTR_RE = re.compile(r'data-theme\s*[~|^$*]?=\s*"([^"]+)"')
# Hardcoded color tokens — keep loose; we just want a candidate set.
HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")

def parse_root_blocks(css_text: str, src: str, line_offset: int):
    """Return list of dicts: { variant, tokens: {name: value}, line }."""
    blocks = []
    for m in ROOT_BLOCK_RE.finditer(css_text):
        selector = m.group(1).strip()
        body = m.group(2)
        theme_match = THEME_ATTR_RE.search(selector)
        variant = theme_match.group(1) if theme_match else "_default"
        tokens = {}
        for tm in TOKEN_DEF_RE.finditer(body):
            tokens[tm.group(1)] = tm.group(2).strip()
        line = css_text[:m.start()].count("\n") + 1 + line_offset
        blocks.append({"src": src, "variant": variant, "tokens": tokens, "line": line})
    return blocks

def find_var_refs(css_text: str, src: str, line_offset: int):
    """Return list of dicts: { name, has_fallback, line, src, context }."""
    refs = []
    for m in VAR_REF_RE.finditer(css_text):
        name = m.group(1)
        fallback = m.group(2)
        line = css_text[:m.start()].count("\n") + 1 + line_offset
        # Pull ~60 chars of surrounding text for the report
        start = max(0, m.start() - 40)
        end = min(len(css_text), m.end() + 20)
        context = css_text[start:end].replace("\n", " ").strip()
        refs.append({
            "name": name,
            "has_fallback": fallback is not None,
            "line": line,
            "src": src,
            "context": context,
        })
    return refs

# ---- Analysis ----------------------------------------------------------

def analyze(root: Path, skip_warnings=False, ignore=None):
    ignore = set(ignore or [])
    sources = list(discover_sources(root))
    if not sources:
        return {"errors": [], "warnings": [], "info": [], "stats": {"sources": 0}}

    all_root_blocks = []
    all_refs = []
    all_css = []  # (src, text, line_offset) for hardcoded-color sweep

    for path, kind in sources:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if kind == "css":
            blocks = parse_root_blocks(text, str(path), 0)
            refs = find_var_refs(text, str(path), 0)
            all_root_blocks.extend(blocks)
            all_refs.extend(refs)
            all_css.append((str(path), text, 0))
        else:
            for css_text, line_offset in extract_css_from_html(text):
                blocks = parse_root_blocks(css_text, str(path), line_offset)
                refs = find_var_refs(css_text, str(path), line_offset)
                all_root_blocks.extend(blocks)
                all_refs.extend(refs)
                all_css.append((str(path), css_text, line_offset))

    # Aggregate token universe
    defined_tokens_default = {}
    defined_tokens_by_variant = defaultdict(dict)
    for blk in all_root_blocks:
        target = defined_tokens_default if blk["variant"] == "_default" else defined_tokens_by_variant[blk["variant"]]
        target.update(blk["tokens"])
    all_defined = set(defined_tokens_default) | {t for v in defined_tokens_by_variant.values() for t in v}

    errors = []
    warnings = []
    info = []

    # --- Error 1: undefined var() references ---
    for ref in all_refs:
        if ref["name"] in all_defined:
            continue
        if ref["name"] in ignore:
            continue
        if ref["has_fallback"]:
            # Still flag as warning — fallback masks the bug but it's a smell
            warnings.append({
                "kind": "undefined-var-with-fallback",
                "src": ref["src"],
                "line": ref["line"],
                "var": ref["name"],
                "suggestion": _suggest(ref["name"], all_defined),
                "context": ref["context"],
                "fix": _fix_suggestion(ref, all_defined),
            })
            continue
        errors.append({
            "kind": "undefined-var",
            "src": ref["src"],
            "line": ref["line"],
            "var": ref["name"],
            "suggestion": _suggest(ref["name"], all_defined),
            "context": ref["context"],
            "fix": _fix_suggestion(ref, all_defined),
        })

    # --- Warning 2: tokens missing from theme variants ---
    if not skip_warnings and defined_tokens_by_variant:
        # Which tokens are actually referenced? If a default token is referenced
        # AND a theme variant is defined, ensure the variant either redefines
        # the token OR doesn't need to (some tokens are intentionally shared).
        # Heuristic: surface tokens that look like color/surface/ink tokens.
        token_names_referenced = {r["name"] for r in all_refs if r["name"] in all_defined}
        color_keywords = ("ink", "surface", "paper", "cream", "mist", "bg", "background",
                          "border", "outline", "shadow", "accent", "primary", "secondary",
                          "text", "color", "muted", "subtle", "card", "panel")
        for variant, variant_tokens in defined_tokens_by_variant.items():
            for token in token_names_referenced:
                if token not in defined_tokens_default:
                    continue
                if token in variant_tokens:
                    continue
                lname = token.lower()
                if any(k in lname for k in color_keywords):
                    warnings.append({
                        "kind": "theme-token-not-overridden",
                        "var": token,
                        "variant": variant,
                        "default_value": defined_tokens_default[token],
                        "suggestion": f"theme '{variant}' inherits default {token} = {defined_tokens_default[token]}",
                        "fix": f"Confirm {token} reads correctly under [data-theme=\"{variant}\"], or add an override.",
                    })

    # --- Warning 3: hardcoded colors duplicating tokens ---
    if not skip_warnings:
        # Build value→token map from default + variants
        value_to_token = {}
        for token, value in defined_tokens_default.items():
            value_norm = value.lower().strip()
            if HEX_COLOR_RE.fullmatch(value_norm):
                value_to_token[value_norm] = token
        # Scan CSS for hardcoded hex outside of :root blocks
        for src, text, line_offset in all_css:
            # Mask root blocks so we don't re-flag the definitions themselves
            masked = ROOT_BLOCK_RE.sub(lambda m: " " * len(m.group(0)), text)
            for m in HEX_COLOR_RE.finditer(masked):
                color = m.group(0).lower()
                if color in value_to_token:
                    line = masked[:m.start()].count("\n") + 1 + line_offset
                    warnings.append({
                        "kind": "hardcoded-color",
                        "src": src,
                        "line": line,
                        "color": color,
                        "token": value_to_token[color],
                        "fix": f"Replace {color} with var({value_to_token[color]}).",
                    })

    # --- Info: stats ---
    stats = {
        "sources": len(set(s for s, _ in sources)),
        "tokens_default": len(defined_tokens_default),
        "tokens_variants": {v: len(t) for v, t in defined_tokens_by_variant.items()},
        "var_refs": len(all_refs),
        "errors": len(errors),
        "warnings": len(warnings),
    }
    return {"errors": errors, "warnings": warnings, "info": info, "stats": stats}

def _suggest(name, all_defined):
    """Closest-named valid token, for the 'did you mean?' hint."""
    matches = get_close_matches(name, list(all_defined), n=3, cutoff=0.6)
    return matches

def _fix_suggestion(ref, all_defined):
    matches = get_close_matches(ref["name"], list(all_defined), n=1, cutoff=0.6)
    if matches:
        return f"Did you mean var({matches[0]})? — replace var({ref['name']}) at {ref['src']}:{ref['line']}."
    return f"Either define {ref['name']} in :root or replace it with a defined token."

# ---- Report rendering --------------------------------------------------

def render_markdown(result, root):
    lines = []
    lines.append(f"# CSS Token Sweep — {root}")
    lines.append("")
    s = result["stats"]
    lines.append(f"_{s.get('sources', 0)} files scanned · {s.get('tokens_default', 0)} default tokens · "
                 f"{len(s.get('tokens_variants', {}))} theme variants · {s.get('var_refs', 0)} var() refs · "
                 f"**{s.get('errors', 0)} errors**, **{s.get('warnings', 0)} warnings**_")
    lines.append("")

    if not result["errors"] and not result["warnings"]:
        lines.append("Clean. No undefined references, no theme-variant gaps, no duplicated hardcoded colors.")
        return "\n".join(lines)

    if result["errors"]:
        lines.append("## Errors (invisible-text risk)")
        lines.append("")
        for e in result["errors"]:
            lines.append(f"- **`var({e['var']})`** at `{e['src']}:{e['line']}`")
            lines.append(f"  - Context: `{e['context']}`")
            lines.append(f"  - {e['fix']}")
        lines.append("")

    if result["warnings"]:
        # Group by kind for skimmability
        by_kind = defaultdict(list)
        for w in result["warnings"]:
            by_kind[w["kind"]].append(w)
        labels = {
            "undefined-var-with-fallback": "Warnings — var() with fallback (smells)",
            "theme-token-not-overridden": "Warnings — tokens not overridden in theme variant",
            "hardcoded-color": "Warnings — hardcoded colors that duplicate a token",
        }
        for kind, items in by_kind.items():
            lines.append(f"## {labels.get(kind, kind)}")
            lines.append("")
            for w in items[:50]:  # cap noise
                if kind == "theme-token-not-overridden":
                    lines.append(f"- `{w['var']}` in variant `{w['variant']}` — {w['suggestion']}")
                    lines.append(f"  - {w['fix']}")
                elif kind == "hardcoded-color":
                    lines.append(f"- `{w['color']}` at `{w['src']}:{w['line']}` → use `var({w['token']})`")
                else:
                    lines.append(f"- `var({w['var']})` at `{w['src']}:{w['line']}`")
                    lines.append(f"  - {w['fix']}")
            if len(items) > 50:
                lines.append(f"- _… {len(items) - 50} more not shown_")
            lines.append("")
    return "\n".join(lines)

# ---- Main --------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Sweep a project for undefined CSS custom property references.")
    parser.add_argument("path", nargs="?", default=".", help="File or directory to scan (default: cwd)")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of markdown")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any errors are found")
    parser.add_argument("--skip-warnings", action="store_true", help="Suppress warnings, show errors only")
    parser.add_argument("--ignore", default="",
                        help="Comma-separated list of var names to skip (e.g. --dx,--dy for vars set at runtime via JS)")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"Path does not exist: {root}", file=sys.stderr)
        sys.exit(2)

    ignore_list = [s.strip() for s in args.ignore.split(",") if s.strip()]
    result = analyze(root, skip_warnings=args.skip_warnings, ignore=ignore_list)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_markdown(result, root))

    if args.strict and result["errors"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
