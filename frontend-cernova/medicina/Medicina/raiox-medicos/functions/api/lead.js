// POST /api/lead — grava o lead no Google Sheets (via webhook do Apps Script).
// Guarda: contato + arquétipo + faixa + score + alertas disparados + respostas.
import { computeResult } from "../../public/shared/roteiro.mjs";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "content-type",
};

export async function onRequestOptions() {
  return new Response(null, { headers: CORS });
}

export async function onRequestPost(context) {
  try {
    const { env, request } = context;
    const body = await request.json();
    const lead = body.lead || {};
    const answers = body.answers || {};

    if (!lead.consentimento) {
      return json({ error: "Consentimento LGPD obrigatório." }, 400);
    }

    const result = computeResult(answers);
    const alertasResumo = result.firedFlags
      .map((f) => `${f.severity.toUpperCase()}: ${f.block} — ${f.respostaLabel}`)
      .join(" | ");

    const row = {
      timestamp: new Date().toISOString(),
      nome: lead.nome || "",
      email: lead.email || "",
      whatsapp: lead.whatsapp || "",
      especialidade: lead.especialidade || "",
      cidade: lead.cidade || "",
      arquetipo: result.archetypeLabel,
      faixa: result.faixa,
      score: result.score,
      n_alertas: result.firedFlags.length,
      alertas: alertasResumo,
      respostas: JSON.stringify(answers),
      consentimento: "sim",
      origem: lead.origem || "raio-x-web",
    };

    let gravado = false;
    if (env.SHEETS_WEBHOOK_URL) {
      const r = await fetch(env.SHEETS_WEBHOOK_URL, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(row),
      });
      gravado = r.ok;
    }

    // Handoff por faixa (Spec §8) — devolvido para a UI/observabilidade.
    const handoff =
      result.faixa === "vermelho" ? "quente-24h" : result.faixa === "amarelo" ? "morno" : "nutricao";

    return json({ ok: true, gravado, handoff, faixa: result.faixa });
  } catch (e) {
    return json({ error: String(e && e.message ? e.message : e) }, 500);
  }
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json", ...CORS },
  });
}
