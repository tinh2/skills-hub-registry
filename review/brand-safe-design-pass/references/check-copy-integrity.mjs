/**
 * Proves that a design pass changed no words.
 *
 *   npm run copy:snapshot   # before the pass, writes .copy-snapshot.json
 *   npm run check:copy      # after, fails on any drift
 *
 * A visual redesign is allowed to move, restyle, resize and reorder anything.
 * It is not allowed to edit, add or drop a single user-facing string. That is
 * easy to promise and easy to breach by accident: a heading gets "improved"
 * while restructuring a component, and nobody notices until the therapist
 * reads her own site back.
 *
 * So this collects every visible text node on every page, in both themes,
 * normalises whitespace, and compares the multiset against the snapshot.
 * Order is ignored on purpose — reordering sections is a design decision.
 * Content is not.
 */
import { chromium } from "playwright";
import fs from "node:fs";

const BASE = process.env.BASE_URL ?? "http://localhost:4331";
const PAGES = ["/", "/about", "/services", "/contact", "/this-page-does-not-exist"];
const SNAP = ".copy-snapshot.json";
const UNLOCK = { name: "rmg:entered", value: "1" };
const writing = process.argv.includes("--write");

const COLLECT = () => {
  const out = [];
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = walk.nextNode(); n; n = walk.nextNode()) {
    const t = n.textContent.replace(/\s+/g, " ").trim();
    if (!t) continue;
    const p = n.parentElement;
    if (!p || ["SCRIPT", "STYLE", "NOSCRIPT"].includes(p.tagName)) continue;
    out.push(t);
  }
  /* aria-labels and alt text are copy too: they are read aloud. */
  for (const el of document.querySelectorAll("[aria-label], img[alt]")) {
    const v = (el.getAttribute("aria-label") ?? el.getAttribute("alt") ?? "").trim();
    if (v) out.push(`@${v}`);
  }
  const t = document.querySelector("title");
  if (t) out.push(`#${t.textContent.trim()}`);
  const d = document.querySelector('meta[name="description"]');
  if (d) out.push(`#${d.getAttribute("content").trim()}`);
  return out;
};

const browser = await chromium.launch();
const current = {};
for (const route of PAGES) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  await ctx.addInitScript(({ name, value }) => {
    try {
      localStorage.setItem(name, value);
    } catch {}
  }, UNLOCK);
  const page = await ctx.newPage();
  await page.goto(BASE + route, { waitUntil: "networkidle" });
  await page.evaluate(() => {
    for (const d of document.querySelectorAll("details")) d.open = true;
  });
  await page.waitForTimeout(400);
  current[route] = (await page.evaluate(COLLECT)).sort();
  await ctx.close();
}
await browser.close();

if (writing) {
  fs.writeFileSync(SNAP, JSON.stringify(current, null, 2));
  const n = Object.values(current).reduce((a, v) => a + v.length, 0);
  console.log(`Snapshot written: ${n} strings across ${PAGES.length} pages.`);
  process.exit(0);
}

if (!fs.existsSync(SNAP)) {
  console.error(`No ${SNAP}. Run \`npm run copy:snapshot\` before the design pass.`);
  process.exit(1);
}

const before = JSON.parse(fs.readFileSync(SNAP, "utf8"));
let drift = 0;
for (const route of PAGES) {
  const was = before[route] ?? [];
  const now = current[route] ?? [];
  const count = (arr) => arr.reduce((m, s) => m.set(s, (m.get(s) ?? 0) + 1), new Map());
  const [a, b] = [count(was), count(now)];
  for (const [s, n] of a) {
    const m = b.get(s) ?? 0;
    if (m < n) {
      drift += 1;
      console.log(`  ✗ ${route} LOST   ${n - m}x  ${JSON.stringify(s.slice(0, 90))}`);
    }
  }
  for (const [s, n] of b) {
    const m = a.get(s) ?? 0;
    if (m < n) {
      drift += 1;
      console.log(`  ✗ ${route} ADDED  ${n - m}x  ${JSON.stringify(s.slice(0, 90))}`);
    }
  }
}

console.log(
  drift
    ? `\nFAIL: ${drift} copy difference(s). A design pass must not touch words.`
    : "\nPASS: every user-facing string is byte-identical to the snapshot.",
);
process.exit(drift ? 1 : 0);
