// Regression tests for the raw-hex scanner in validate-tokens.mjs.
// Run: node --test validate-tokens.test.mjs   (needs style-dictionary and
// @babel/parser installed, as validate-tokens.mjs does)
import assert from "node:assert/strict";
import { test } from "node:test";
import { rawHex } from "./validate-tokens.mjs";

const hexes = async (file, text) => (await rawHex(file, text)).map((h) => h.hex ?? h.error);

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
  "js: untagged template variable": ["a.jsx", "const border = `1px solid #abc`;\nexport function Button() {\n  return <button style={{ border }}>OK</button>;\n}", ["#abc"]],
  "js: returned template": ["a.js", "function c() { return `#abc`; }", ["#abc"]],
  "js: template argument": ["a.js", "setColor(`#abc`);", ["#abc"]],
  "js: styled call form": ["a.js", "const B = styled(Base)`\n  color: #abc;\n`;", ["#abc"]],
  "js: styled attrs selector": ["a.js", "const B = styled.div.attrs({})`\n  #abc & { color: var(--x); }\n`;", []],
  "js: String.raw is not CSS": ["a.jsx", "const border = String.raw`1px solid #abc`;\nexport function Button() {\n  return <button style={{ border }}>OK</button>;\n}", ["#abc"]],
  "js: interpolation in styled template": ["a.js", 'const Button = styled.button`color: ${(props) => "#fff"};`;', ["#fff"]],
  "js: nested template in interpolation": ["a.js", "const B = styled.div`border: ${(p) => `1px solid #abc`};`;", ["#abc"]],
  "js: hex after interpolation in declaration": ["a.js", "const B = styled.div`border: ${w}px solid #abc;`;", ["#abc"]],
  "js: interpolation then id selector": ["a.js", "const B = styled.div`${Icon} { color: var(--x); }\n  #abc & { color: var(--y); }`;", []],
  "ts: type assertion file": ["a.ts", 'const c = <string>"#abc";\nconst id = { id: "#add" };', ["#abc"]],
  "tsx: typed component": ["a.tsx", 'const B = (p: { c: string }) => <div style={{ color: "#abc" }} />;', ["#abc"]],
  "js: import path": ["a.js", 'import x from "#abc";', []],
  "js: dynamic import path": ["a.jsx", 'const Button = lazy(() => import("#abc"));', []],
  "jsx: htmlFor": ["a.jsx", '<label htmlFor="#abc">x</label>', []],
  "js: spaced interpolation then hex": ["a.js", "const B = styled.div`border: ${ width }px solid #abc;`;", ["#abc"]],
  "js: parenthesized interpolation then hex": ["a.js", "const B = styled.div`border: ${(width)}px solid #abc;`;", ["#abc"]],
  "js: commented interpolation then hex": ["a.js", "const B = styled.div`border: ${ /* w */ width }px solid #abc;`;", ["#abc"]],
  "jsx: href expression": ["a.jsx", '<a href={"#abc"}>top</a>', []],
  "jsx: conditional href": ["a.jsx", '<a href={open ? "#abc" : "#def"}>x</a>', []],
  "jsx: conditional style value": ["a.jsx", '<div style={{ color: dark ? "#fff" : "#000" }} />', ["#fff", "#000"]],
  "js: optional querySelector": ["a.js", 'document.querySelector?.("#abc");', []],
  "js: style value through a call": ["a.jsx", '<div style={{ color: shade("#abc") }} />', ["#abc"]],
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
  test(name, async () => assert.deepEqual(await hexes(file, source), expected));
}

for (const [name, source] of Object.entries({
  "redeclared const": "const width = 1; const width = 2;",
  "malformed JSX": 'export const B = () => <div style={{ color: "#abc" }>;',
})) {
  test(`parse error is a failure: ${name}`, async () => {
    const hits = await rawHex("a.jsx", source);
    assert.ok(hits.some((h) => h.error?.startsWith("cannot parse")), JSON.stringify(hits));
  });
}

test("reports the line of a wrapped value", async () => {
  assert.equal((await rawHex("a.css", ".x {\n  color:\n    #abc;\n}"))[0].line, 3);
});
