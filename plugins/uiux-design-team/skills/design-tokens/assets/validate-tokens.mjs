// Validate design tokens. Exits 1 on any failure; prints WARN for unused tokens.
// Usage: node scripts/validate-tokens.mjs   (Style Dictionary v4 or v5, Node 18+)
// Needs style-dictionary and @babel/parser (dev dependencies). Run from the
// project root. rawHex() is exported for the regression tests in
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
//    - CSS/SCSS/Less and <style> blocks: a small CSS walker checks every
//      declaration value (wrapped lines included) and skips selectors,
//      at-rule preludes and comments.
//    - JS/TS/JSX and <script> blocks are parsed with @babel/parser, and every
//      string and template piece is checked, except values of href/src/to/id/
//      selector keys or attributes, DOM selector-call arguments and import
//      paths. Templates tagged css`...`, styled.x`...`, styled(X)`...`,
//      createGlobalStyle, keyframes or injectGlobal are read as CSS, with
//      ${...} interpolations parsed as JS in their own right.
//    - HTML/Vue/Svelte markup: style="..." declarations and :style bindings.
//    url(...) contents are never colours (url(#gradient) is an SVG fragment).
//    An id string that is also valid hex, such as "#add", is reported when
//    used outside those keys; rename it.
const HEX = /#[0-9a-fA-F]{3,8}\b/g;
const NON_COLOR_KEYS = new Set(["href", "src", "to", "id", "for", "htmlFor", "target", "selector", "xlinkHref", "xlink:href", "action"]);
const SELECTOR_CALLS = new Set(["querySelector", "querySelectorAll", "getElementById", "closest", "matches", "$"]);
const CSS_TAGS = new Set(["css", "styled", "createGlobalStyle", "keyframes", "injectGlobal"]);

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

// The identifier at the root of a tag: css, styled.button, styled(Base),
// styled.div.attrs({...}) and styled(Base).attrs(...) all resolve to their root.
function tagRoot(node) {
  while (node) {
    if (node.type === "Identifier") return node.name;
    node = node.type === "MemberExpression" ? node.object : node.type === "CallExpression" ? node.callee : null;
  }
  return null;
}

const keyName = (key) => key && (key.name ?? key.value);
const jsxName = (name) => name && (name.namespace ? `${name.namespace.name}:${name.name.name}` : name.name);

// Does the parent make this string something other than a colour value?
function exempt(parent) {
  if (!parent) return false;
  if (parent.type === "ObjectProperty") return NON_COLOR_KEYS.has(keyName(parent.key));
  if (parent.type === "JSXAttribute") return NON_COLOR_KEYS.has(jsxName(parent.name));
  if (parent.type === "CallExpression") {
    const callee = parent.callee.type === "MemberExpression" ? parent.callee.property : parent.callee;
    return SELECTOR_CALLS.has(callee?.name);
  }
  return /^(Import|Export\w*)Declaration$|^ImportExpression$/.test(parent.type);
}

function walkJs(node, parent, base, src, hits) {
  if (!node || typeof node.type !== "string") return;
  if (node.type === "StringLiteral" && !exempt(parent)) {
    if (parent?.type === "JSXAttribute" && jsxName(parent.name) === "style") scanCss(node.value, base + node.start + 1, hits);
    else hexInValue(src.slice(node.start + 1, node.end - 1), base + node.start + 1, hits);
  } else if (node.type === "TemplateLiteral" && !exempt(parent)) {
    if (parent?.type === "TaggedTemplateExpression" && CSS_TAGS.has(tagRoot(parent.tag))) {
      // CSS template: blank the ${...} spans so offsets hold and the CSS walker
      // sees the declarations; the expressions are walked below as JS.
      const first = node.quasis[0].start, last = node.quasis.at(-1).end;
      let css = src.slice(first, last);
      for (const e of node.expressions) {
        const from = e.start - first - 2, to = e.end - first + 1; // include "${" and "}"
        css = css.slice(0, from) + " ".repeat(to - from) + css.slice(to);
      }
      scanCss(css, base + first, hits);
    } else {
      for (const q of node.quasis) hexInValue(src.slice(q.start, q.end), base + q.start, hits);
    }
  }
  for (const [k, v] of Object.entries(node)) {
    if (k === "loc" || k === "extra" || k.endsWith("Comments")) continue;
    if (Array.isArray(v)) v.forEach((child) => walkJs(child, node, base, src, hits));
    else if (v && typeof v.type === "string") walkJs(v, node, base, src, hits);
  }
}

async function scanJs(text, base, hits, { expression = false, file = "x.jsx" } = {}) {
  const { parse, parseExpression } = await import("@babel/parser");
  // .ts can't take the jsx plugin (it breaks <T>x assertions); .js/.jsx may hold JSX.
  const plugins = /\.[mc]?ts$/.test(file) ? ["typescript"] : /\.tsx$/.test(file) ? ["jsx", "typescript"] : ["jsx"];
  const opts = { sourceType: "module", plugins, errorRecovery: true };
  let ast;
  try {
    ast = expression ? parseExpression(text, opts) : parse(text, opts);
  } catch (err) {
    hits.push({ error: `cannot parse: ${err.message}`, index: base + (err.pos ?? 0) });
    return;
  }
  walkJs(ast, null, base, text, hits);
}

// HTML/Vue/Svelte: <style> as CSS, <script> as JS, then attributes.
async function scanMarkup(text, hits) {
  let markup = text;
  for (const [tag, scan] of [["style", scanCss], ["script", scanJs]]) {
    for (const m of text.matchAll(new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)</${tag}>`, "gi"))) {
      await scan(m[1], m.index + m[0].indexOf(">") + 1, hits, { file: /lang=["']ts/.test(m[0]) ? "x.ts" : "x.js" });
      markup = markup.slice(0, m.index) + " ".repeat(m[0].length) + markup.slice(m.index + m[0].length);
    }
  }
  for (const a of markup.matchAll(/([:@\w-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')/g)) {
    const value = a[2] ?? a[3];
    const at = a.index + a[0].length - value.length - 1;
    if (a[1] === "style") scanCss(value, at, hits);
    else if (/^(:|v-bind:)style$/.test(a[1])) await scanJs(value, at, hits, { expression: true });
  }
}

export async function rawHex(file, text) {
  const hits = [];
  if (/\.(css|scss|sass|less|pcss)$/.test(file)) scanCss(text, 0, hits);
  else if (/\.([mc]?[jt]sx?)$/.test(file)) await scanJs(text, 0, hits, { file });
  else if (/\.(html?|vue|svelte)$/.test(file)) await scanMarkup(text, hits);
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
    for (const h of await rawHex(file, text))
      fail(h.error ? `scan: ${file}:${h.line}: ${h.error}` : `raw hex ${h.hex} in ${file}:${h.line}`);
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
