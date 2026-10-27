// Validate design tokens. Exits 1 on any failure; prints WARN for unused tokens.
// Usage: node scripts/validate-tokens.mjs   (Style Dictionary v4 or v5, Node 18+)
// Expects tokens/global.json, tokens/alias.json, tokens/components/*.json,
// style-dictionary.config.mjs at the project root and components in src/components/.
import StyleDictionary from "style-dictionary";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import config from "../style-dictionary.config.mjs";

const failures = [];
const fail = (msg) => failures.push(msg);
const SEGMENT = /^[a-z0-9]+(-[a-z0-9]+)*$/;
// Literal values a component token may use without an alias.
const KEYWORDS = new Set(["transparent", "none", "inherit", "currentColor", "0"]);
const tierOf = (file) =>
  file.includes("/components/") ? "component"
  : file.endsWith("alias.json") ? "alias"
  : file.endsWith("global.json") ? "global"
  : "unknown";
const refsIn = (value) =>
  [...JSON.stringify(value).matchAll(/\{([^}]+)\}/g)].map((m) => m[1]);

function filesUnder(dir) {
  return readdirSync(dir).flatMap((name) => {
    const path = join(dir, name);
    return statSync(path).isDirectory() ? filesUnder(path) : [path];
  });
}

// Build the css platform in memory. Broken references throw here.
const sd = new StyleDictionary({
  ...config,
  log: { verbosity: "silent", errors: { brokenReferences: "throw" } },
});
let allTokens;
try {
  ({ allTokens } = await sd.getPlatformTokens("css"));
} catch (err) {
  console.error(`FAIL: tokens do not resolve: ${err.message}`);
  process.exit(1);
}

const byPath = new Map(allTokens.map((t) => [t.path.join("."), t]));
const referenced = new Set();

for (const token of allTokens) {
  const path = token.path.join(".");
  const tier = tierOf(token.filePath);

  // 1. Naming: every path segment is lowercase kebab-case.
  if (!token.path.every((s) => SEGMENT.test(s))) fail(`name: "${path}" is not lowercase kebab-case`);

  // 2. Tiers: globals hold raw values, aliases point at globals,
  //    components point at aliases only.
  const refs = refsIn(token.original.value);
  refs.forEach((r) => referenced.add(r));
  const refTiers = refs.map((r) => tierOf(byPath.get(r)?.filePath ?? ""));
  if (tier === "unknown") fail(`tier: "${path}" is in ${token.filePath}, outside global/alias/components`);
  if (tier === "global" && refs.length) fail(`tier: global "${path}" references other tokens`);
  const keyword = KEYWORDS.has(String(token.original.value));
  if (tier === "alias" && ((!refs.length && !keyword) || refTiers.some((t) => t !== "global")))
    fail(`tier: alias "${path}" must reference globals, got ${JSON.stringify(token.original.value)}`);
  if (tier === "component" && ((!refs.length && !keyword) || refTiers.some((t) => t !== "alias")))
    fail(`tier: component "${path}" must reference alias tokens, got ${JSON.stringify(token.original.value)}`);
}

// 3. No raw hex colours in components (tokens only). Hex counts only inside a
//    declaration value: CSS `prop: value` (values may wrap across lines) or a
//    JS/JSX style property `prop: "#abc"`. Selectors (`#abc {`), href="#abc"
//    links and url(#abc) fragment references pass.
const blank = (m) => m.replace(/[^\n]/g, " "); // keep offsets and line numbers
const HEX = /#[0-9a-fA-F]{3,8}\b/g;
function rawHex(text) {
  const src = text.replace(/\/\*[\s\S]*?\*\//g, blank).replace(/url\([^)]*\)/g, blank);
  const hits = [];
  // CSS declarations: start after { ; or a quote (style="..."), end at ; } or a quote.
  for (const d of src.matchAll(/(?<=^|[{;"'`])\s*[-\w]+\s*:([^;{}"'`]*)(?=[;}"'`])/g)) {
    const start = d.index + d[0].length - d[1].length;
    for (const h of d[1].matchAll(HEX)) hits.push({ hex: h[0], index: start + h.index });
  }
  // JS/JSX style objects: color: "#abc"
  for (const d of src.matchAll(/[-\w]+["']?\s*:\s*["'`](#[0-9a-fA-F]{3,8})\b/g))
    hits.push({ hex: d[1], index: d.index + d[0].length - d[1].length });
  const line = (i) => src.slice(0, i).split("\n").length;
  return [...new Map(hits.map((h) => [h.index, { ...h, line: line(h.index) }])).values()];
}

let componentFiles = [];
try {
  componentFiles = filesUnder("src/components");
} catch (err) {
  fail(`scan: cannot read src/components: ${err.message}`);
}
const used = new Set();
for (const file of componentFiles) {
  const text = readFileSync(file, "utf8");
  for (const h of rawHex(text)) fail(`raw hex ${h.hex} in ${file}:${h.line}`);
  for (const m of text.matchAll(/var\(--([a-z0-9-]+)/g)) used.add(m[1]);
}

// 4. Unused: component tokens no source file uses (warning only).
for (const token of allTokens) {
  if (tierOf(token.filePath) === "component" && !used.has(token.name))
    console.warn(`WARN: unused component token --${token.name}`);
}
// Alias or global tokens nothing references and no source uses.
for (const token of allTokens) {
  const path = token.path.join(".");
  if (tierOf(token.filePath) !== "component" && !referenced.has(path) && !used.has(token.name))
    console.warn(`WARN: unreferenced token --${token.name}`);
}

if (failures.length) {
  failures.forEach((f) => console.error(`FAIL: ${f}`));
  process.exit(1);
}
console.log(`OK: ${allTokens.length} tokens valid`);
