// Regression tests for the raw-hex scanner in validate-tokens.mjs.
// Run: node --test validate-tokens.test.mjs   (needs style-dictionary installed,
// since validate-tokens.mjs imports it)
import assert from "node:assert/strict";
import { test } from "node:test";
import { rawHex } from "./validate-tokens.mjs";

const hexes = (file, text) => rawHex(file, text).map((h) => h.hex);

// Each case: [file name, source, hex values that must be reported].
const cases = {
  // Stylesheets
  "css: inline value": ["a.css", ".x { color: #abc; }", ["#abc"]],
  "css: value without semicolon": ["a.css", ".x { color: #abc }", ["#abc"]],
  "css: value wrapped onto next line": ["a.css", ".x {\n  color:\n    #abc;\n}", ["#abc"]],
  "css: wrapped border": ["a.css", ".x {\n  border: 1px solid\n    #123456;\n}", ["#123456"]],
  "css: url() then hex": ["a.css", ".x { background: url(#a) #abc; }", ["#abc"]],
  "css: gradient": ["a.css", ".x { background: linear-gradient(#fff, #000); }", ["#fff", "#000"]],
  "scss: variable": ["a.scss", "$brand: #abc;", ["#abc"]],
  "css: id selector": ["a.css", "#abc { background: var(--button-bg); }", []],
  "css: pseudo-class then id": ["a.css", ".x:hover #abc .y { color: var(--button-text); }", []],
  "scss: nested selector": ["a.scss", ".p {\n  a:hover #abc { color: var(--x); }\n}", []],
  "css: url fragment": ["a.css", ".x { filter: url(#abc); }", []],
  "css: quoted url fragment": ["a.css", '.x { mask: url("#abc") center; }', []],
  "css: hex in comment": ["a.css", "/* was #abc */ .x { color: var(--x); }", []],
  // JS / JSX
  "jsx: style object": ["a.jsx", 'const s = { color: "#fff" };', ["#fff"]],
  "jsx: inline style": ["a.jsx", '<div style={{ backgroundColor: "#fff" }} />', ["#fff"]],
  "jsx: compound border": ["a.jsx", '<div style={{ border: "1px solid #abc" }} />', ["#abc"]],
  "jsx: gradient string": ["a.jsx", '<div style={{ background: "linear-gradient(#fff, #000)" }} />', ["#fff", "#000"]],
  "js: ternary": ["a.js", 'const c = dark ? "#fff" : "#000";', ["#fff", "#000"]],
  "js: template value": ["a.js", "const s = { border: `1px solid ${w} #abc` };", ["#abc"]],
  "js: styled-components": ["a.js", "const B = styled.button`\n  color: #abc;\n`;", ["#abc"]],
  "jsx: href fragment": ["a.jsx", '<a href="#abc">top</a>', []],
  "js: querySelector": ["a.js", 'document.querySelector("#abc");', []],
  "js: hex in comment": ["a.js", '// fallback "#abc"\nconst s = { color: "var(--x)" };', []],
  "js: styled id selector": ["a.js", "const G = css`\n  #abc { color: var(--x); }\n`;", []],
  "js: url fragment": ["a.js", 'const s = { filter: "url(#abc)" };', []],
  // Markup
  "html: style attribute": ["a.html", '<div style="color: #abc">x</div>', ["#abc"]],
  "html: style block": ["a.html", "<style>\n.x { color: #abc; }\n</style>", ["#abc"]],
  "vue: style binding": ["a.vue", "<div :style=\"{ color: '#abc' }\"></div>", ["#abc"]],
  "html: href fragment": ["a.html", '<a href="#abc">top</a>', []],
  "html: id selector in style block": ["a.html", "<style>#abc { color: var(--x); }</style>", []],
};

for (const [name, [file, source, expected]] of Object.entries(cases)) {
  test(name, () => assert.deepEqual(hexes(file, source), expected));
}

test("reports the line of a wrapped value", () => {
  assert.equal(rawHex("a.css", ".x {\n  color:\n    #abc;\n}")[0].line, 3);
});
