// POST /api/chat — turno de conversa livre (usuário digitou em vez de clicar).
// A Alice responde no tom + reconduz à pergunta atual, dentro dos guardrails.
import { buildSystemBlocks, buildChatSystemSuffix, MODELO } from "../../shared/prompts.mjs";
import { callMessages } from "../../shared/anthropic.mjs";

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
    if (!env.ANTHROPIC_API_KEY) {
      return json({ error: "ANTHROPIC_API_KEY não configurada no servidor." }, 500);
    }
    const body = await request.json();
    const history = Array.isArray(body.messages) ? body.messages.slice(-8) : [];
    const currentQuestionText = body.currentQuestionText || "";

    // Blocos de sistema cacheados (persona + base) + sufixo dinâmico do turno.
    const system = buildSystemBlocks();
    system.push({ type: "text", text: buildChatSystemSuffix(currentQuestionText) });

    const { text } = await callMessages({
      apiKey: env.ANTHROPIC_API_KEY,
      model: env.MODELO || MODELO,
      system,
      messages: history.length ? history : [{ role: "user", content: "(sem mensagem)" }],
      max_tokens: 350,
      temperature: 0.5,
    });

    return json({ reply: text.trim() });
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
