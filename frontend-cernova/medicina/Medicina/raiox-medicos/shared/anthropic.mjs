// =============================================================================
// anthropic.mjs — Cliente mínimo da Messages API (funciona em Worker e Node;
// ambos têm fetch). Usa prompt caching via cache_control nos blocos de sistema.
// =============================================================================
export async function callMessages({ apiKey, model, system, messages, max_tokens = 1500, temperature = 0.3 }) {
  const resp = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({ model, max_tokens, temperature, system, messages }),
  });

  const data = await resp.json();
  if (!resp.ok) {
    const msg = data && data.error ? data.error.message : JSON.stringify(data);
    throw new Error(`Anthropic API ${resp.status}: ${msg}`);
  }
  const text = (data.content || [])
    .filter((b) => b.type === "text")
    .map((b) => b.text)
    .join("");
  return { text, usage: data.usage, raw: data };
}

// Extrai o primeiro objeto JSON de uma string (tolerante a texto ao redor).
export function extractJson(text) {
  const start = text.indexOf("{");
  const end = text.lastIndexOf("}");
  if (start === -1 || end === -1) throw new Error("Sem JSON na resposta do modelo.");
  return JSON.parse(text.slice(start, end + 1));
}
