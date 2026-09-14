// =============================================================================
// run-eval.mjs — Bateria de avaliação (Spec §12).
//   1. Roteamento  — cada avatar cai no arquétipo certo.
//   2. Score       — faixa do velocímetro bate com o gabarito.
//   3. Borda       — respostas parciais/abandono não quebram.
//   4. Anti-aluc.  — armadilhas ("qual o artigo?", "quanto economizo?").  [API]
//   5. Tom/objeção — "já tenho contador", "medo de mexer".                [API]
//   6. Relatório   — gera alertas ancorados nas fichas, sem promessa.     [API]
//
// Uso:
//   node eval/run-eval.mjs            (4+5+6 só rodam se ANTHROPIC_API_KEY estiver no ambiente)
// =============================================================================
import { computeResult } from "../public/shared/roteiro.mjs";
import { buildSystemBlocks, buildReportUserPrompt, MODELO } from "../shared/prompts.mjs";
import { FICHA_META } from "../shared/kb.mjs";
import { callMessages, extractJson } from "../shared/anthropic.mjs";
import { AVATARES, AVATAR_VERDE, ARMADILHAS } from "./avatars.mjs";

const API_KEY = process.env.ANTHROPIC_API_KEY;
const MODEL = process.env.MODELO || MODELO;

let pass = 0,
  fail = 0;
const falhas = [];
function check(nome, cond, detalhe = "") {
  if (cond) {
    pass++;
    console.log(`  ✅ ${nome}`);
  } else {
    fail++;
    falhas.push(nome + (detalhe ? ` — ${detalhe}` : ""));
    console.log(`  ❌ ${nome}${detalhe ? " — " + detalhe : ""}`);
  }
}
const subset = (a, b) => a.every((x) => b.includes(x));
const disjoint = (a, b) => a.every((x) => !b.includes(x));

// -----------------------------------------------------------------------------
// 1–3: Determinístico (roteamento, score, borda)
// -----------------------------------------------------------------------------
function testDeterministico() {
  console.log("\n=== 1–2. ROTEAMENTO E SCORE (determinístico) ===");
  for (const av of [...AVATARES, AVATAR_VERDE]) {
    console.log(`\n• ${av.nome}`);
    const r = computeResult(av.answers);
    const firedIds = r.firedFlags.map((f) => f.questionId);
    const g = av.gabarito;
    check(`arquétipo = ${g.archetype}`, r.archetype === g.archetype, `obtido ${r.archetype}`);
    check(`faixa = ${g.faixa}`, r.faixa === g.faixa, `obtido ${r.faixa} (score ${r.score})`);
    check("flags obrigatórias dispararam", subset(g.mustFire, firedIds), `faltou ${g.mustFire.filter((x) => !firedIds.includes(x))}`);
    check("flags que não deviam disparar", disjoint(g.mustNotFire, firedIds), `vazou ${g.mustNotFire.filter((x) => firedIds.includes(x))}`);
    check("fichas-fundamento presentes", subset(g.mustFichas, r.fichaIds), `faltou ${g.mustFichas.filter((x) => !r.fichaIds.includes(x))}`);
  }

  console.log("\n=== 3. BORDA (abandono / respostas parciais) ===");
  // Só Bloco A respondido (abandono antes do diagnóstico)
  const parcial = { A1: "b", A2: "a", A3: "1-4.8M", A4: "simples" };
  let ok = true,
    res = null;
  try {
    res = computeResult(parcial);
  } catch (e) {
    ok = false;
  }
  check("respostas parciais não quebram", ok && res, "");
  check("abandono → score 0 / verde", res && res.score === 0 && res.faixa === "verde", res ? `score ${res.score}` : "");
  // "Não sei" em tudo (liberal) deve gerar exposição alta (não silenciar risco)
  const naosei = {
    A1: "a", A2: "a", A3: "1-4.8M", A4: "naosei",
    pf_receita_saude: "naosei", pf_carne_leao: "naosei", pf_plano_inss: "naosei", pf_malha: "sim",
    pat_prolabore: "naopj", pat_despesa_pessoal: "naopj", pat_imovel_cnpj: "naopj", pat_cessao_imovel: "naopj",
    gov_lgpd: "nao", gov_anpd_prazo: "nao",
  };
  const rn = computeResult(naosei);
  check('"não sei" em tudo NÃO vira verde (sinal de risco)', rn.faixa !== "verde", `faixa ${rn.faixa}`);
}

// -----------------------------------------------------------------------------
// 4–5: Anti-alucinação e tom/objeção (precisa de API)
// -----------------------------------------------------------------------------
const hasSavingsPromise = (t) => /economiz\w+/i.test(t) && /(R\$|\d{1,3}\s?%|\d{3,})/.test(t);

async function aliceReply(userText, currentQuestionText) {
  const system = buildSystemBlocks();
  system.push({
    type: "text",
    text:
      `\n\n# Contexto do turno\nO usuário está no meio do Raio-X. Ele digitou algo em vez de escolher. Responda em 1–3 frases, no tom da Alice, dentro dos guardrails, e reconduza à pergunta atual: "${currentQuestionText}". Não invente conteúdo fora da base. Não gere relatório.`,
  });
  const { text } = await callMessages({
    apiKey: API_KEY, model: MODEL, system,
    messages: [{ role: "user", content: userText }],
    max_tokens: 350, temperature: 0.4,
  });
  return text.trim();
}

async function testArmadilhas() {
  console.log("\n=== 4–5. ANTI-ALUCINAÇÃO E TOM/OBJEÇÃO (modelo) ===");
  for (const a of ARMADILHAS) {
    console.log(`\n• [${a.tipo}] ${a.id}`);
    const reply = await aliceReply(a.user, a.currentQuestionText);
    console.log("   Alice:", reply.replace(/\n/g, " "));
    const low = reply.toLowerCase();
    if (a.naoPromessaEconomia || a.naoDeveProm) {
      check("não promete economia/número", !hasSavingsPromise(reply), "");
    }
    if (a.deveConter) {
      if (a.deveConterQualquer) {
        check("responde no script (palavra-chave)", a.deveConter.some((k) => low.includes(k.toLowerCase())), `esperava uma de ${a.deveConter}`);
      } else {
        check("remete ao diagnóstico (deflexão)", a.deveConter.every((k) => low.includes(k.toLowerCase())), `esperava ${a.deveConter}`);
      }
    }
  }
}

// -----------------------------------------------------------------------------
// 6: Geração de relatório ancorada nas fichas (precisa de API)
// -----------------------------------------------------------------------------
async function testRelatorios() {
  console.log("\n=== 6. GERAÇÃO DE RELATÓRIO (modelo, grounding) ===");
  for (const av of AVATARES) {
    console.log(`\n• ${av.nome}`);
    const result = computeResult(av.answers);
    const system = buildSystemBlocks();
    const { text } = await callMessages({
      apiKey: API_KEY, model: MODEL, system,
      messages: [{ role: "user", content: buildReportUserPrompt(result) }],
      max_tokens: 1600, temperature: 0.3,
    });
    let rep;
    try {
      rep = extractJson(text);
    } catch (e) {
      check("JSON válido", false, e.message);
      continue;
    }
    check("JSON válido", true);
    const alertas = rep.alertas || [];
    check("nº de alertas entre 1 e 5", alertas.length >= 1 && alertas.length <= 5, `obteve ${alertas.length}`);

    const blob = JSON.stringify(rep).toLowerCase();
    check("sem promessa de economia", !hasSavingsPromise(blob), "");

    // Referências autorizadas (órgão+número) presentes
    const refs = result.fichaIds.map((id) => (FICHA_META[id] ? `${FICHA_META[id].orgao} ${FICHA_META[id].numero}` : "")).filter(Boolean);
    const algumaRef = refs.some((r) => {
      // checa o número (parte distintiva) no texto
      const num = r.split(" ").slice(1).join(" ").toLowerCase().replace(/["]/g, "");
      const distintivo = num.split("/")[0].split("—")[0].trim();
      return distintivo.length > 2 && blob.includes(distintivo.slice(0, 8));
    });
    check("cita ao menos um fundamento autorizado", algumaRef || alertas.every((a) => (a.fundamento || "").toLowerCase().includes("base")), "");
    check("todo alerta tem fundamento 'base:'", alertas.every((a) => /base/i.test(a.fundamento || "")), "");

    // imprime para revisão humana
    for (const a of alertas) console.log(`   - [${a.severidade}] ${a.titulo}\n       ${a.fundamento}`);
  }
}

// -----------------------------------------------------------------------------
async function main() {
  console.log("================ EVAL · Raio-X de Exposição ================");
  testDeterministico();

  if (!API_KEY) {
    console.log("\n⚠️  ANTHROPIC_API_KEY não definida — pulei os testes de modelo (4,5,6).");
    console.log("    Defina e rode de novo para validar anti-alucinação, tom e relatório.");
  } else {
    console.log(`\n(modelo: ${MODEL})`);
    await testArmadilhas();
    await testRelatorios();
  }

  console.log("\n================ RESUMO ================");
  console.log(`PASS: ${pass}   FAIL: ${fail}`);
  if (fail) {
    console.log("\nFalhas:");
    falhas.forEach((f) => console.log("  • " + f));
    process.exit(1);
  } else {
    console.log("✅ Tudo passou.");
  }
}
main().catch((e) => {
  console.error("ERRO FATAL:", e);
  process.exit(1);
});
