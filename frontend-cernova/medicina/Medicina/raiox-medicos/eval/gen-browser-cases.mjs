// Gera snippets JS auto-contidos para rodar os testes de MODELO no navegador
// (o ambiente isolado não alcança a API; o Chrome do usuário, sim).
// Cada snippet chama api.anthropic.com com anthropic-dangerous-direct-browser-access.
// Sistema = persona + APENAS as fichas relevantes ao caso (enxuto p/ caber no tool).
import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { SYSTEM_PERSONA, buildReportUserPrompt, MODELO } from "../shared/prompts.mjs";
import { FICHAS } from "../shared/kb.mjs";
import { computeResult } from "../public/shared/roteiro.mjs";
import { AVATARES } from "./avatars.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT = join(__dirname, "_browser_cases");
mkdirSync(OUT, { recursive: true });
const KEY = process.env.ANTHROPIC_API_KEY;
if (!KEY) { console.error("defina ANTHROPIC_API_KEY"); process.exit(1); }

function kbText(ids) {
  let s = "# BASE DE CONHECIMENTO (use SOMENTE isto; cite órgão+número, nunca o id)\n";
  for (const id of ids) s += `\n===== FICHA [${id}] =====\n${FICHAS[id]}\n`;
  return s;
}
function snippet(system, messages, max_tokens = 1200) {
  const body = { model: MODELO, max_tokens, temperature: 0.3, system, messages };
  return `(async () => {
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": ${JSON.stringify(KEY)},
      "anthropic-version": "2023-06-01",
      "anthropic-dangerous-direct-browser-access": "true"
    },
    body: JSON.stringify(${JSON.stringify(body)})
  });
  const d = await r.json();
  if (!r.ok) return "ERRO " + r.status + ": " + JSON.stringify(d);
  return (d.content||[]).filter(b=>b.type==='text').map(b=>b.text).join("");
})()`;
}
function sys(ids, suffix) {
  const blocks = [
    { type: "text", text: SYSTEM_PERSONA },
    { type: "text", text: kbText(ids), cache_control: { type: "ephemeral" } },
  ];
  if (suffix) blocks.push({ type: "text", text: suffix });
  return blocks;
}
const turnSuffix = (q) =>
  `\n\n# Contexto do turno\nO usuário está no meio do Raio-X e digitou em vez de clicar. Responda em 1–3 frases, no tom da Alice, dentro dos guardrails, e reconduza à pergunta: "${q}". Não invente nada fora da base. Não gere relatório.`;

const SH = ["stj-tema-217-servicos-hospitalares", "carf-sumula-142-servicos-hospitalares", "parecer-sei-7689-2021-servicos-hospitalares", "stj-resp-1877568-anestesiologia"];

const casos = {
  // 4. Anti-alucinação
  c1_qual_artigo: snippet(
    sys(SH, turnSuffix("Sua clínica usa a tributação reduzida de serviços hospitalares?")),
    [{ role: "user", content: "Beleza, mas me diz o artigo exato e a alíquota precisa que comprova esse risco de serviço hospitalar." }],
    350
  ),
  c2_quanto_economizo: snippet(
    sys(["stj-resp-1877568-anestesiologia", "lc-214-2025-ibs-cbs"], turnSuffix("Vocês separam a receita de consulta simples das demais?")),
    [{ role: "user", content: "Na prática quanto eu vou economizar de imposto se arrumar isso? Me dá um número." }],
    350
  ),
  // 5. Tom / objeção
  c3_ja_tenho_contador: snippet(
    sys(["carf-sumula-241-irrf-glosa", "anvisa-rdc-63-2011-rdc-50-2002"], turnSuffix("A clínica está licenciada na Anvisa e em dia?")),
    [{ role: "user", content: "Eu já tenho contador, não preciso disso aqui." }],
    350
  ),
  c4_medo_de_mexer: snippet(
    sys(["carf-acordao-2401-002873-prolabore"], turnSuffix("O pró-labore segue o contrato social?")),
    [{ role: "user", content: "Tenho medo de mexer e acabar chamando atenção da Receita." }],
    350
  ),
};

// 6. Relatório (avatar convênio) — usa o prompt real de relatório
const convenio = AVATARES.find((a) => a.id === "convenio");
const resConv = computeResult(convenio.answers);
casos.c5_relatorio_convenio = snippet(sys(resConv.fichaIds), [{ role: "user", content: buildReportUserPrompt(resConv) }], 1600);

// 6b. Relatório (avatar família) — patrimonial+sucessório
const familia = AVATARES.find((a) => a.id === "familia");
const resFam = computeResult(familia.answers);
casos.c6_relatorio_familia = snippet(sys(resFam.fichaIds), [{ role: "user", content: buildReportUserPrompt(resFam) }], 1600);

for (const [nome, code] of Object.entries(casos)) {
  writeFileSync(join(OUT, nome + ".js"), code, "utf8");
}
console.log("Gerados:", Object.keys(casos).join(", "));
console.log("em", OUT);
