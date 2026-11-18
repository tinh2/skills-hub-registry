#!/usr/bin/env node
// Rebuilds the "View on skills-hub.ai" index blocks in the top-level README
// and in each category README.
//
// Usage: node scripts/gen-index.mjs [--dry-run]
//
// - Reads every <category>/<skill>/SKILL.md (frontmatter name + description).
// - Site slug = slugify(frontmatter name), the same rule the platform's
//   registry sync uses (apps/api/src/modules/external-source/sync.service.ts).
//   Falls back to the folder name when the frontmatter has no name.
// - Verifies each slug against the production API (GET /api/v1/skills/<slug>),
//   at most CONCURRENCY requests in flight. A skill is linked only if the API
//   returns 200 and the skill is published by an account in OWNERS. A 404
//   lists the skill without a link. Any other failure (5xx, network) is retried
//   and then aborts the run, so an API blip never silently drops links.
// - Only the text between the BEGIN/END GENERATED markers is replaced.
//   SKILL.md files and skill folders are never touched.
//
// No dependencies beyond Node 18+ (global fetch).

import { readFileSync, writeFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const API = "https://api.skills-hub.ai/api/v1";
const SITE = "https://skills-hub.ai";
const OWNER = "skills-hub";
// Accounts whose pages count as this repo's skills: the registry bot, plus the
// repo owner, who published a few of these skills by hand before the sync existed.
const OWNERS = new Set([OWNER, "tinh2"]);
// The API allows 120 requests/minute per client; stay well under it.
const CONCURRENCY = 2;
const MIN_INTERVAL_MS = 650; // global spacing between requests (~92/min)
const DRY_RUN = process.argv.includes("--dry-run");
const SKIP_DIRS = new Set(["scripts", "node_modules", ".git", ".github"]);
const BEGIN = "<!-- BEGIN GENERATED: skills-hub-index (scripts/gen-index.mjs, do not edit by hand) -->";
const END = "<!-- END GENERATED: skills-hub-index -->";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 100);
}

// Minimal frontmatter reader: top-level scalar keys, quoted or plain,
// plus folded/literal block scalars (">", "|", with optional chomping).
function readFrontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return {};
  const lines = m[1].split(/\r?\n/);
  const out = {};
  for (let i = 0; i < lines.length; i++) {
    const kv = lines[i].match(/^([A-Za-z_][\w-]*):\s*(.*)$/);
    if (!kv) continue;
    const [, key, raw] = kv;
    let val = raw.trim();
    if (/^[>|][+-]?$/.test(val)) {
      const parts = [];
      while (i + 1 < lines.length && (/^\s+\S/.test(lines[i + 1]) || lines[i + 1].trim() === "")) {
        parts.push(lines[++i].trim());
      }
      val = parts.join(" ").trim();
    } else if (val.startsWith('"') && val.endsWith('"') && val.length > 1) {
      val = val.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, "\\");
    } else if (val.startsWith("'") && val.endsWith("'") && val.length > 1) {
      val = val.slice(1, -1).replace(/''/g, "'");
    }
    out[key] = val;
  }
  return out;
}

function oneLine(desc, max = 140) {
  let s = (desc || "").replace(/\s+/g, " ").trim();
  // First sentence if it is reasonably long, otherwise truncate.
  const sentence = s.match(/^(.{40,}?[.!?])(\s|$)/);
  if (sentence) s = sentence[1];
  if (s.length > max) s = s.slice(0, max - 3).replace(/\s+\S*$/, "") + "...";
  return s.replace(/\|/g, "\\|");
}

function collectSkills() {
  const skills = [];
  for (const cat of readdirSync(ROOT).sort()) {
    if (cat.startsWith(".") || SKIP_DIRS.has(cat)) continue;
    const catDir = join(ROOT, cat);
    if (!statSync(catDir).isDirectory()) continue;
    for (const dir of readdirSync(catDir).sort()) {
      const file = join(catDir, dir, "SKILL.md");
      if (!existsSync(file)) continue;
      const fm = readFrontmatter(readFileSync(file, "utf8"));
      const name = (fm.name || dir).trim();
      skills.push({ category: cat, dir, name, slug: slugify(name), description: fm.description || "" });
    }
  }
  return skills;
}

let lastRequest = 0;
async function pace() {
  const wait = lastRequest + MIN_INTERVAL_MS - Date.now();
  lastRequest = Math.max(Date.now(), lastRequest + MIN_INTERVAL_MS);
  if (wait > 0) await sleep(wait);
}

async function fetchJson(url) {
  let rateLimitWaits = 0;
  for (let attempt = 1; attempt <= 4; attempt++) {
    await pace();
    try {
      const res = await fetch(url, { headers: { accept: "application/json", "user-agent": "skills-hub-registry-gen-index" } });
      if (res.status === 404) return { status: 404 };
      if (res.ok) return { status: 200, body: await res.json() };
      if (res.status === 429 && rateLimitWaits < 5) {
        rateLimitWaits++;
        attempt--; // rate limiting is not a failure, just wait for the window
        const secs = Number(res.headers.get("retry-after") || res.headers.get("x-ratelimit-reset")) || 60;
        console.error(`rate limited, waiting ${secs}s`);
        await sleep(secs * 1000 + 500);
        continue;
      }
      if (res.status < 500 && res.status !== 429) return { status: res.status };
    } catch {
      /* network error: retry */
    }
    await sleep(2000 * attempt);
  }
  throw new Error(`gave up on ${url} after retries (API unhealthy?), aborting without writing`);
}

async function verify(skills) {
  const unique = [...new Set(skills.map((s) => s.slug))];
  const result = new Map();
  let next = 0;
  async function worker() {
    while (next < unique.length) {
      const slug = unique[next++];
      const r = await fetchJson(`${API}/skills/${encodeURIComponent(slug)}`);
      const owner = r.body?.author?.username;
      result.set(slug, { status: r.status, owner, ok: r.status === 200 && OWNERS.has(owner) });
    }
  }
  await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  return result;
}

function replaceBlock(text, block, insert) {
  const start = text.indexOf(BEGIN);
  const end = text.indexOf(END);
  const wrapped = `${BEGIN}\n${block.trim()}\n${END}`;
  if (start !== -1 && end > start) return text.slice(0, start) + wrapped + text.slice(end + END.length);
  return insert(text, wrapped);
}

const titleCase = (s) => s.charAt(0).toUpperCase() + s.slice(1);

async function main() {
  const skills = collectSkills();
  const status = await verify(skills);
  let siteCategories = new Set();
  try {
    const r = await fetchJson(`${API}/categories`);
    siteCategories = new Set((r.body || []).map((c) => c.slug));
  } catch {
    /* category browse links are optional */
  }

  const byCat = new Map();
  for (const s of skills) {
    s.linked = status.get(s.slug)?.ok === true;
    if (!byCat.has(s.category)) byCat.set(s.category, []);
    byCat.get(s.category).push(s);
  }

  const linked = skills.filter((s) => s.linked);
  const unlinked = skills.filter((s) => !s.linked);
  const changed = [];

  for (const [cat, list] of byCat) {
    const nLinked = list.filter((s) => s.linked).length;
    const rows = list.map((s) => {
      const page = s.linked ? `[View on skills-hub](${SITE}/skills/${s.slug})` : "Not on the site yet";
      return `| [${s.name}](${s.dir}/) | ${oneLine(s.description)} | ${page} |`;
    });
    const browse = siteCategories.has(cat)
      ? ` You can also [browse the ${titleCase(cat)} category on skills-hub.ai](${SITE}/browse?category=${cat}), which includes skills from other publishers.`
      : "";
    const block = [
      `## All ${titleCase(cat)} skills on skills-hub.ai`,
      "",
      `Each skill page on skills-hub.ai shows ratings and reviews, install counts, a one-command install, and related skills. ${nLinked} of ${list.length} skills in this folder have a page.${browse}`,
      "",
      "| Skill | Description | Page |",
      "|-------|-------------|------|",
      ...rows,
    ].join("\n");

    const file = join(ROOT, cat, "README.md");
    const before = existsSync(file) ? readFileSync(file, "utf8") : `# ${titleCase(cat)}\n`;
    const after = replaceBlock(before, block, (t, w) => `${t.replace(/\s*$/, "")}\n\n${w}\n`);
    if (after !== before) {
      changed.push(`${cat}/README.md`);
      if (!DRY_RUN) writeFileSync(file, after);
    }
  }

  const catLinks = [...byCat.entries()].map(([cat, list]) => {
    const n = list.filter((s) => s.linked).length;
    return `- [${cat}](${cat}/README.md): ${list.length} skills, ${n} with a skills-hub.ai page`;
  });
  const top = [
    "## Browse on skills-hub.ai",
    "",
    `Browse all ${linked.length} skills from this repo on [skills-hub.ai](${SITE}/u/${OWNER}). Each skill page shows ratings and reviews, install counts, a one-command install, and related skills. Every category index below lists its skills with a direct link to each page.`,
    "",
    ...catLinks,
  ].join("\n");
  const readme = join(ROOT, "README.md");
  const beforeTop = readFileSync(readme, "utf8");
  const afterTop = replaceBlock(beforeTop, top, (t, w) => {
    const i = t.indexOf("\n## ");
    return i === -1 ? `${t.replace(/\s*$/, "")}\n\n${w}\n` : `${t.slice(0, i)}\n${w}\n${t.slice(i)}`;
  });
  if (afterTop !== beforeTop) {
    changed.push("README.md");
    if (!DRY_RUN) writeFileSync(readme, afterTop);
  }

  console.log(`skills: ${skills.length}, linked: ${linked.length}, unlinked: ${unlinked.length}`);
  for (const s of unlinked) {
    const st = status.get(s.slug);
    console.log(`  unlinked ${s.category}/${s.dir} (slug ${s.slug}): HTTP ${st?.status}${st?.owner ? `, owner ${st.owner}` : ""}`);
  }
  console.log(`${DRY_RUN ? "would change" : "changed"}: ${changed.join(", ") || "nothing"}`);
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
