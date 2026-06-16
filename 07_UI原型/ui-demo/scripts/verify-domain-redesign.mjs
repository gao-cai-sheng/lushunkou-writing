import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));

const pages = {
  "index.html": ["campaign-table", "dispatch-map", "order-node"],
  "bastion-section.html": ["bastion-cutaway", "dimension-line", "casemate-chamber", "postern-tunnel"],
  "strategic-map.html": ["campaign-map", "sea-lane", "compass-rose", "intelligence-tag"],
  "map-builder.html": ["survey-grid", "frost-field", "site-stake", "construction-ledger"],
  "senate-roster.html": ["dossier-table", "archive-ledger", "seal-strip"],
  "diplomacy.html": ["envoy-desk", "treaty-table", "wax-seal", "credential-stack"],
  "tech-tree.html": [
    "research-board",
    "blueprint-grid",
    "research-docket",
    "tech-cutaway",
    "tech-cutaway-diagram",
    "tech-slice",
    "tech-layer-stack",
    "dependency-layer",
    "cutaway",
    "原料层",
    "配方层",
    "工艺层",
    "检验层",
    "包装运输层",
    "军事应用层",
    "扩散管控层",
  ],
};

const css = readFileSync(join(root, "ui-kit.css"), "utf8");
const cssTokens = [
  "--paper",
  "--brass",
  "--navy",
  "--brick",
  "--snow",
  ".material-grain",
  ".game-map-surface",
];

const failures = [];
for (const token of cssTokens) {
  if (!css.includes(token)) failures.push(`ui-kit.css missing ${token}`);
}

const pictographic = /[\u{1F300}-\u{1FAFF}]|[⚙⚔⚗⛏⛵]/u;

for (const [file, markers] of Object.entries(pages)) {
  const html = readFileSync(join(root, file), "utf8");
  if (!html.includes('href="ui-kit.css"')) {
    failures.push(`${file} does not link ui-kit.css`);
  }
  for (const marker of markers) {
    if (!html.includes(marker)) failures.push(`${file} missing ${marker}`);
  }
  const stripped = html.replace(/<title>.*?<\/title>/gs, "");
  if (pictographic.test(stripped)) {
    failures.push(`${file} still contains pictographic/emoji glyphs`);
  }
}

if (failures.length) {
  console.error("Domain redesign verification failed:");
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log("Domain redesign verification passed.");
