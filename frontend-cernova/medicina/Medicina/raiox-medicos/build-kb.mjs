// =============================================================================
// build-kb.mjs — Gera shared/kb.mjs a partir das fichas validadas em
// ../base-conhecimento. NÃO redigita conteúdo: lê a fonte de verdade.
//
// Rodar:  node build-kb.mjs
// Saída:  shared/kb.mjs  (export FICHAS = {id: markdown}, FICHA_META = {...})
//
// Empacota APENAS as fichas referenciadas pelo roteiro (as 23 usadas pelos
// alertas) para manter o contexto enxuto. A lista vem do próprio roteiro.
// =============================================================================
import { readFileSync, writeFileSync, readdirSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { BLOCKS } from "./public/shared/roteiro.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const KB_DIR = join(__dirname, "..", "base-conhecimento");

// Coleta os ids de ficha realmente usados pelo roteiro
const usados = new Set();
for (const arr of Object.values(BLOCKS)) {
  for (const q of arr) {
    for (const o of q.options) {
      if (o.fires && o.fichas) o.fichas.forEach((f) => usados.add(f));
    }
  }
}

// Varre recursivamente os .md
function walk(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    if (name.startsWith("_") || name === "README.md") continue;
    const p = join(dir, name);
    const st = statSync(p);
    if (st.isDirectory()) out.push(...walk(p));
    else if (name.endsWith(".md")) out.push(p);
  }
  return out;
}

function parseFrontmatter(txt) {
  const m = txt.match(/^---\n([\s\S]*?)\n---/);
  if (!m) return {};
  const fm = {};
  for (const line of m[1].split("\n")) {
    const mm = line.match(/^([a-z_]+):\s*(.*)$/i);
    if (mm) fm[mm[1]] = mm[2].replace(/^"(.*)"$/, "$1").trim();
  }
  return fm;
}

const files = walk(KB_DIR);
const FICHAS = {};
const META = {};
const encontrados = new Set();

for (const f of files) {
  const txt = readFileSync(f, "utf8");
  const fm = parseFrontmatter(txt);
  if (!fm.id || !usados.has(fm.id)) continue;
  // Remove o frontmatter e o banner de validação para enxugar tokens;
  // mantém o corpo (teor, o que decide, aplicação ao ICP).
  let body = txt.replace(/^---\n[\s\S]*?\n---\n/, "");
  FICHAS[fm.id] = body.trim();
  META[fm.id] = { numero: fm.numero || "", titulo: fm.titulo || "", orgao: fm.orgao || "" };
  encontrados.add(fm.id);
}

const faltando = [...usados].filter((u) => !encontrados.has(u));
if (faltando.length) {
  console.error("ERRO: fichas referenciadas pelo roteiro NÃO encontradas:", faltando);
  process.exit(1);
}

const header = `// AUTO-GERADO por build-kb.mjs a partir de ../base-conhecimento — NÃO editar à mão.
// ${encontrados.size} fichas validadas (fonte oficial, 02/06/2026).\n\n`;

const out =
  header +
  "export const FICHAS = " +
  JSON.stringify(FICHAS, null, 2) +
  ";\n\nexport const FICHA_META = " +
  JSON.stringify(META, null, 2) +
  ";\n";

writeFileSync(join(__dirname, "shared", "kb.mjs"), out, "utf8");
console.log(`OK: shared/kb.mjs gerado com ${encontrados.size} fichas.`);
console.log("Fichas:", [...encontrados].sort().join(", "));
