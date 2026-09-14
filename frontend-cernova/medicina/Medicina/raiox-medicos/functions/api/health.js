// GET /api/health — confere a configuração sem vazar segredos.
export async function onRequestGet(context) {
  const { env } = context;
  return new Response(
    JSON.stringify({
      ok: true,
      anthropic_key: env.ANTHROPIC_API_KEY ? "configurada" : "FALTANDO",
      sheets_webhook: env.SHEETS_WEBHOOK_URL ? "configurado" : "FALTANDO (leads não serão gravados)",
      modelo: env.MODELO || "claude-sonnet-4-6 (padrão)",
    }),
    { headers: { "content-type": "application/json" } }
  );
}
