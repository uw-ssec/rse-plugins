// Validate design tokens. Exits 1 on any failure; prints WARN for unused tokens.
// Usage: node scripts/validate-tokens.mjs   (Style Dictionary v4 or v5, Node 18+)
// Run from the project root. rawHex() is exported for the regression tests in
// validate-tokens.test.mjs (`node --test`).
// Expects tokens/global.json, tokens/alias.json, tokens/components/*.json,
// style-dictionary.config.mjs at the project root and components in src/components/.
import StyleDictionary from "style-dictionary";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

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

// Raw hex colours in component sources (check 3 below).
//    Files are tokenized by type rather than matched with regexes:
//    - CSS/SCSS/Less and <style> blocks: hex in any declaration value
//      (`prop: value`, wrapped lines included). Selectors such as `#abc {`
//      and comments are skipped.
//    - JS/TS/JSX and <script> blocks: hex in any string or template literal,
//      except values of href/src/to/id/selector keys or attributes and
//      arguments of DOM selector calls (querySelector("#main")). Tagged
//      template literals (styled.div`...`, css`...`) are read as CSS.
//    - HTML/Vue/Svelte markup: style="..." declarations and :style bindings.
//    url(...) contents are never treated as colours (url(#gradient) is an SVG
//    fragment reference). An id string that happens to be valid hex, such as
//    "#add", is reported when used outside those keys; rename it.
const HEX = /#[0-9a-fA-F]{3,8}\b/g;
const NON_COLOR_KEYS = new Set(["href", "src", "to", "id", "for", "target", "selector", "xlinkHref", "xlink:href", "action"]);
// A template is tagged when an identifier, member or call ends right before it.
const TAGGED = /[\w$)\]]$/;
const KEYWORD_BEFORE = /(?:^|[^\w$.])(?:return|typeof|void|await|yield|in|of|case|else|do|throw|new|delete|instanceof)$/;
const SELECTOR_CALLS = /(?:querySelector(?:All)?|getElementById|closest|matches|\$)\s*\($/;

function hexInValue(value, base, hits) {
  const cleaned = value.replace(/url\(\s*(?:"[^"]*"|'[^']*'|[^)]*)\)/g, (m) => " ".repeat(m.length));
  for (const h of cleaned.matchAll(HEX)) hits.push({ hex: h[0], index: base + h.index });
}

// Walk CSS. A segment ending in "{" is a selector or at-rule prelude and is
// skipped; a segment ending in ";" or "}" (or the end, for style="...") is a
// declaration, and its value is everything after the first top-level ":".
function scanCss(text, base, hits) {
  let colon = -1, depth = 0;
  const flush = (end) => {
    if (colon >= 0) hexInValue(text.slice(colon + 1, end), base + colon + 1, hits);
    colon = -1;
  };
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === "/" && text[i + 1] === "*") {
      const end = text.indexOf("*/", i + 2) < 0 ? text.length : text.indexOf("*/", i + 2) + 2;
      text = text.slice(0, i) + " ".repeat(end - i) + text.slice(end); // keep offsets
      i = end - 1;
    } else if (c === '"' || c === "'") {
      i = skipString(text, i);
    } else if (c === "(") depth++;
    else if (c === ")") depth = Math.max(0, depth - 1);
    else if (depth === 0 && c === ":" && colon < 0) colon = i;
    else if (depth === 0 && c === "{") colon = -1;
    else if (depth === 0 && (c === ";" || c === "}")) flush(i);
  }
  flush(text.length);
}

function skipString(text, i) {
  const q = text[i];
  for (let j = i + 1; j < text.length; j++) {
    if (text[j] === "\\") j++;
    else if (text[j] === q) return j;
  }
  return text.length;
}

// Walk JS/TS/JSX: skip comments, check every string and template literal.
function scanJs(text, base, hits) {
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === "/" && text[i + 1] === "/") {
      const nl = text.indexOf("\n", i);
      i = nl < 0 ? text.length : nl;
    } else if (c === "/" && text[i + 1] === "*") {
      const close = text.indexOf("*/", i + 2);
      i = close < 0 ? text.length : close + 1;
    } else if (c === '"' || c === "'" || c === "`") {
      const end = skipString(text, i);
      const body = text.slice(i + 1, end);
      const before = text.slice(Math.max(0, i - 80), i).trimEnd();
      const key = before.match(/([\w:-]+)["']?\s*[:=]$/)?.[1];
      if (key === "style" && before.endsWith("=")) scanCss(body, base + i + 1, hits);
      else if (!(key && NON_COLOR_KEYS.has(key)) && !SELECTOR_CALLS.test(before)) {
        // Only a tagged template (styled.div`...`, css`...`) is a stylesheet;
        // any other template is an ordinary string value.
        if (c === "`" && TAGGED.test(before) && !KEYWORD_BEFORE.test(before)) scanCss(body, base + i + 1, hits);
        else hexInValue(body, base + i + 1, hits);
      }
      i = end;
    }
  }
}

// HTML/Vue/Svelte: <style> as CSS, <script> as JS, then attributes.
function scanMarkup(text, hits) {
  let markup = text;
  for (const [tag, scan] of [["style", scanCss], ["script", scanJs]]) {
    for (const m of text.matchAll(new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)</${tag}>`, "gi"))) {
      const bodyStart = m.index + m[0].indexOf(">") + 1;
      scan(m[1], bodyStart, hits);
      markup = markup.slice(0, m.index) + " ".repeat(m[0].length) + markup.slice(m.index + m[0].length);
    }
  }
  for (const a of markup.matchAll(/([:@\w-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')/g)) {
    const value = a[2] ?? a[3];
    const at = a.index + a[0].length - value.length - 1;
    if (a[1] === "style") scanCss(value, at, hits);
    else if (/^(:|v-bind:)style$/.test(a[1])) scanJs(value, at, hits);
  }
}

export function rawHex(file, text) {
  const hits = [];
  if (/\.(css|scss|sass|less|pcss)$/.test(file)) scanCss(text, 0, hits);
  else if (/\.(m?[jt]sx?|cjs)$/.test(file)) scanJs(text, 0, hits);
  else if (/\.(html?|vue|svelte)$/.test(file)) scanMarkup(text, hits);
  const line = (i) => text.slice(0, i).split("\n").length;
  return [...new Map(hits.map((h) => [h.index, { ...h, line: line(h.index) }])).values()];
}

async function main() {
  const failures = [];
  const fail = (msg) => failures.push(msg);
  const { default: config } = await import(pathToFileURL(resolve("style-dictionary.config.mjs")).href);

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

    // 3. No raw hex colours in components (tokens only); see rawHex above.
  let componentFiles = [];
  try {
    componentFiles = filesUnder("src/components");
  } catch (err) {
    fail(`scan: cannot read src/components: ${err.message}`);
  }
  const used = new Set();
  for (const file of componentFiles) {
    const text = readFileSync(file, "utf8");
    for (const h of rawHex(file, text)) fail(`raw hex ${h.hex} in ${file}:${h.line}`);
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
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? "").href) await main();
