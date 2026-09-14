// POST /api/report  — gera os alertas detalhados a partir das fichas disparadas.
// O score e o arquétipo são RECALCULADOS no servidor (não confia no cliente).
import { computeResult } from "../../public/shared/roteiro.mjs";
import { buildSystemBlocks, buildReportUserPrompt, MODELO, DISCLAIMER } from "../../shared/prompts.mjs";
import { callMessages, extractJson } from "../../shared/anthropic.mjs";
import { FAIXA_META } from "../../public/shared/roteiro.mjs";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "content-type",
};

export async function onRequestOptions() {
  return new Response(null, { headers: CORS });
}

const CTA = {
  vermelho:
    "Sua exposição está alta. No Diagnóstico Executivo a gente quantifica cada um desses alertas e monta o plano de blindagem. Quer que o nosso time te chame para conversar?",
  amarelo:
    "Há pontos que merecem atenção. No Diagnóstico Essencial a gente mede o tamanho real de cada alerta e mostra o caminho. Quer entender melhor?",
  verde:
    "Sua estrutura aparenta estar organizada. Mesmo assim, o Diagnóstico Essencial confirma se não há nada escondido e te deixa coberto contra as mudanças de 2026. Quer dar esse passo?",
};

export async function onRequestPost(context) {
  try {
    const { env, request } = context;
    if (!env.ANTHROPIC_API_KEY) {
      return json({ error: "ANTHROPIC_API_KEY não configurada no servidor." }, 500);
    }
    const body = await request.json();
    const answers = body.answers || {};

    // Autoritativo: recalcula no servidor.
    const result = computeResult(answers);

    let report;
    if (result.firedFlags.length === 0) {
      // Sem flags: relatório honesto, sem chamar o modelo.
      report = {
        leitura: FAIXA_META[result.faixa].frase,
        alertas: [],
        naoAvaliado:
          "Este Raio-X é uma triagem preliminar. O diagnóstico completo confirma se não há exposição escondida fora do que foi perguntado aqui.",
      };
    } else {
      const system = buildSystemBlocks();
      const userPrompt = buildReportUserPrompt(result);
      const { text } = await callMessages({
        apiKey: env.ANTHROPIC_API_KEY,
        model: env.MODELO || MODELO,
        system,
        messages: [{ role: "user", content: userPrompt }],
        max_tokens: 1600,
        temperature: 0.3,
      });
      report = extractJson(text);
    }

    return json({
      archetype: result.archetype,
      archetypeLabel: result.archetypeLabel,
      faixa: result.faixa,
      faixaMeta: FAIXA_META[result.faixa],
      score: result.score,
      nAlertas: report.alertas ? report.alertas.length : 0,
      report,
      cta: CTA[result.faixa],
      disclaimer: DISCLAIMER,
    });
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
