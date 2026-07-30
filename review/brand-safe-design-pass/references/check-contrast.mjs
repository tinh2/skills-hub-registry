/**
 * Measures text contrast across every page, in BOTH themes, at rest AND on
 * hover.
 *
 *   npm run build && npm run preview   (in one terminal)
 *   npm run check:contrast             (in another)
 *
 * check:a11y already runs axe, which is stricter about markup than this is.
 * What axe does not do is move the mouse: it audits the resting page only.
 * That blind spot shipped a real bug — a section-level hover rule painted
 * body text --c-ink, which is nearly black, over the dark green crisis panel
 * on the contact page, because the panel happens to sit inside a .section.
 * Every automated check stayed green and the text was unreadable.
 *
 * So this walks the DOM, resolves the effective background behind each piece
 * of text (including through transparent ancestors), and measures WCAG 2.2
 * contrast. Then it hovers every element that any hover rule targets, and
 * every link, and measures again.
 *
 * Thresholds are the AA ones: 4.5:1 for body text, 3:1 for large text
 * (>=24px, or >=18.66px when bold).
 *
 * Text sitting on a photograph is REPORTED, not failed: a single ratio
 * cannot describe a gradient, and those cases are scrims that have to be
 * judged by eye.
 */
import { chromium } from "playwright";

const BASE = process.env.BASE_URL ?? "http://localhost:4331";
const PAGES = ["/", "/about", "/services", "/contact", "/this-page-does-not-exist"];
const THEMES = ["light", "dark"];
const UNLOCK = { name: "rmg:entered", value: "1" };

/*
 * Deduped, because each hover pass re-measures the whole page: without this
 * one bad element in a header reports once per hover target on the page.
 */
const problems = new Map();
const notes = new Map();
const fail = (key, m) => problems.set(key, m);
const note = (key, m) => notes.set(key, m);

const browser = await chromium.launch();

/* Runs inside the page: measure every text-bearing element. */
const MEASURE = () => {
  /*
   * Colours are resolved by PAINTING them and reading the pixel back, not by
   * parsing the string. getComputedStyle returns whatever colour space the
   * author's CSS produced — this site's translucent header resolves to
   * `oklab(0.95 0.0008 0.0086 / 0.88)` because of a color-mix — and canvas
   * `fillStyle` echoes that back verbatim rather than converting it. Reading
   * the numbers out of it treated a cream header as near-black and invented
   * four failures on every page. Rasterising handles every colour space,
   * including oklab, color-mix, hsl and named colours.
   */
  const cv = document.createElement("canvas").getContext("2d", { willReadFrequently: true });
  const parse = (c) => {
    cv.clearRect(0, 0, 1, 1);
    cv.fillStyle = "rgba(0, 0, 0, 0)";
    cv.fillStyle = c;
    cv.fillRect(0, 0, 1, 1);
    const [r, g, b, a] = cv.getImageData(0, 0, 1, 1).data;
    return [r, g, b, a / 255];
  };
  /* src over dst */
  const over = (s, d) => {
    const a = s[3] + d[3] * (1 - s[3]);
    if (!a) return [0, 0, 0, 0];
    return [
      (s[0] * s[3] + d[0] * d[3] * (1 - s[3])) / a,
      (s[1] * s[3] + d[1] * d[3] * (1 - s[3])) / a,
      (s[2] * s[3] + d[2] * d[3] * (1 - s[3])) / a,
      a,
    ];
  };
  const lum = ([r, g, b]) => {
    const [x, y, z] = [r, g, b]
      .map((v) => v / 255)
      .map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
    return 0.2126 * x + 0.7152 * y + 0.0722 * z;
  };
  const ratio = (a, b) => {
    const [x, y] = [lum(a), lum(b)].sort((m, n) => n - m);
    return (x + 0.05) / (y + 0.05);
  };

  const results = [];
  for (const el of document.querySelectorAll("body *")) {
    const own = [...el.childNodes]
      .filter((n) => n.nodeType === 3)
      .map((n) => n.textContent.trim())
      .join(" ")
      .trim();
    if (!own) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === "hidden" || cs.display === "none" || cs.opacity === "0") continue;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    if (el.closest(".visually-hidden")) continue;

    /* SVG text is painted by `fill`; `color` is only what currentColor
       resolves to and can differ, as it does in the logo. */
    const inSvg = el.ownerSVGElement || el.tagName.toLowerCase() === "svg";
    const fg = parse(inSvg && cs.fill && cs.fill !== "none" ? cs.fill : cs.color);

    /* Composite every translucent layer down to the first opaque one. */
    const layers = [];
    let overImage = false;
    for (let p = el; p; p = p.parentElement) {
      const pcs = getComputedStyle(p);
      if (pcs.backgroundImage && pcs.backgroundImage !== "none") overImage = true;
      if (p.querySelector(":scope > [aria-hidden='true'] img, :scope > picture img")) {
        overImage = true;
      }
      const c = parse(pcs.backgroundColor);
      if (c[3] > 0) {
        layers.push(c);
        if (c[3] >= 0.999) break;
      }
    }
    layers.push(parse(getComputedStyle(document.documentElement).backgroundColor || "#fff"));
    let bg = [255, 255, 255, 1];
    for (let i = layers.length - 1; i >= 0; i -= 1) bg = over(layers[i], bg);

    const size = parseFloat(cs.fontSize);
    const bold = Number(cs.fontWeight) >= 700;
    const large = size >= 24 || (size >= 18.66 && bold);

    results.push({
      tag: el.tagName.toLowerCase(),
      cls: (el.className || "").toString().split(" ")[0].slice(0, 28),
      text: own.slice(0, 42),
      overImage,
      large,
      ratio: Math.round(ratio(fg, bg) * 100) / 100,
    });
  }
  return results;
};

/* Everything a hover rule in the codebase targets. */
const HOVER_HOSTS =
  ".section, .service, .split, .page-hero, .hero, .cta, .faq, .crisis, .footer__brand, .footer__nav, .footer__contact, a, summary, button";

for (const theme of THEMES) {
  for (const route of PAGES) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    await ctx.addInitScript(({ name, value }) => {
      try {
        localStorage.setItem(name, value);
      } catch {}
    }, UNLOCK);
    const page = await ctx.newPage();
    await page.goto(BASE + route, { waitUntil: "networkidle" });
    await page.evaluate((t) => {
      document.documentElement.dataset.theme = t;
    }, theme);
    await page.evaluate(() => {
      for (const i of document.querySelectorAll("img")) i.loading = "eager";
      for (const d of document.querySelectorAll("details")) d.open = true;
    });
    await page.waitForTimeout(700);

    const label = `${theme} ${route}`;

    /* ---- resting ---- */
    for (const r of await page.evaluate(MEASURE)) {
      const min = r.large ? 3 : 4.5;
      if (r.ratio < min) {
        const key = `${theme}|${route}|rest|${r.tag}.${r.cls}|${r.text}`;
        if (r.overImage) {
          note(key, `  · ${label} over a photo, judge by eye: <${r.tag}.${r.cls}> ${r.ratio}:1 "${r.text}"`);
        } else {
          fail(key, `  ✗ ${label} AT REST: <${r.tag}.${r.cls}> ${r.ratio}:1 (needs ${min}) "${r.text}"`);
        }
      }
    }

    /* ---- hovered ---- */
    const hosts = await page.locator(HOVER_HOSTS).all();
    for (const host of hosts) {
      if (!(await host.isVisible().catch(() => false))) continue;
      try {
        await host.hover({ timeout: 1200, force: true });
      } catch {
        continue; /* off screen or covered; nothing to measure */
      }
      await page.waitForTimeout(260); /* let the colour transition land */
      for (const r of await page.evaluate(MEASURE)) {
        const min = r.large ? 3 : 4.5;
        if (r.ratio < min && !r.overImage) {
          const key = `${theme}|${route}|hover|${r.tag}.${r.cls}|${r.text}`;
          if (!problems.has(`${theme}|${route}|rest|${r.tag}.${r.cls}|${r.text}`)) {
            fail(key, `  ✗ ${label} ON HOVER: <${r.tag}.${r.cls}> ${r.ratio}:1 (needs ${min}) "${r.text}"`);
          }
        }
      }
    }

    await ctx.close();
  }
}

await browser.close();

for (const m of [...problems.values()].sort()) console.log(m);
if (notes.size) {
  console.log(`\n${notes.size} case(s) sit on a photograph and are reported, not failed:`);
  for (const m of [...notes.values()].sort()) console.log(m);
}
console.log(
  problems.size
    ? `\nFAIL: ${problems.size} distinct contrast problem(s).`
    : "\nPASS: text contrast clears AA everywhere, at rest and on hover.",
);
process.exit(problems.size ? 1 : 0);
