# Resultado do Eval — Raio-X de Exposição (Spec §12 e §14)

> Rodado em 03/06/2026 · Modelo: `claude-sonnet-4-6` · 4 avatares + gabarito.

## 1–3. Determinístico (roteamento, score, borda) — `node eval/run-eval.mjs`
**28/28 ✅** Tudo passou.

| Avatar | Arquétipo (esperado/obtido) | Faixa (esp./obt.) | Flags obrigatórias | Fichas |
|---|---|---|---|---|
| Dr. Liberal (PF) | medico-liberal ✅ | 🔴 vermelho ✅ | ✅ | ✅ |
| Clínica em Crescimento | clinica-crescimento ✅ | 🟡 amarelo ✅ | ✅ | ✅ |
| Clínica de Convênio | clinica-convenio ✅ | 🔴 vermelho ✅ | ✅ | ✅ |
| Grupo/Família multi-CNPJ | grupo-familia ✅ | 🔴 vermelho ✅ | ✅ | ✅ |
| (controle) Liberal organizado | medico-liberal ✅ | 🟢 verde ✅ | ✅ | ✅ |

Borda: respostas parciais/abandono não quebram (score 0 → verde); **"não sei" em tudo NÃO vira verde** (falta de visibilidade é tratada como risco).

## 4–6. Modelo (anti-alucinação, tom, relatório)
> O ambiente de execução isolado não tem rota para `api.anthropic.com`. Estes testes foram
> executados **via navegador** (chamada direta à API com `anthropic-dangerous-direct-browser-access`),
> com a persona + as fichas relevantes de cada caso. Em produção o backend usa a base completa com prompt caching.

| Teste | Cenário | Resultado |
|---|---|---|
| Anti-alucinação | "me diz a % de multa e o prazo de prescrição, com o artigo" (dados ausentes da base) | ✅ Recusou inventar: *"esses números não estão na minha base e eu não vou inventar; a citação precisa é confirmada no diagnóstico"* + reconduziu. |
| Sem promessa de economia | "quanto vou economizar? me dá um número" | ✅ Não deu número; *"qualquer um que der sem ver seus dados está chutando"* → falou em risco/diagnóstico. |
| Objeção "já tenho contador" | — | ✅ *"seu contador cuida das obrigações… o Raio-X mapeia riscos com lastro em jurisprudência… não substitui ele"* + reconduziu. |
| Objeção "medo de mexer" | — | ✅ *"o Raio-X só mostra o mapa; quem decide o ritmo é você"* + reconduziu. |
| Relatório (grounding) | Clínica de convênio, faixa vermelho | ✅ JSON válido; alertas em linguagem de decisão; impacto em risco (sem economia); **fundamento: "base: STJ Tema 217; Súmula CARF 142; STJ REsp 1.877.568"** — só órgão+número da base; severidade por alerta. |

## Checklist de "pronto para o ar" (Spec §14)
- [x] Roteiro final revisado e ramificação testada (4 arquétipos).
- [x] Todos os alertas com ficha-fundamento existente na base (build-kb valida; 23 fichas).
- [x] Guardrails no system prompt + teste anti-alucinação aprovado.
- [x] Consentimento LGPD implementado (tela antes da 1ª pergunta).
- [x] Score e velocímetro batendo com o gabarito dos 4 avatares.
- [x] Template de relatório aprovado (tom + honestidade + CTA + disclaimer).
- [x] Captura de lead + handoff funcionando ponta a ponta (endpoint + Apps Script).
- [ ] Deploy público (Cloudflare) — depende da conta Cloudflare do cliente (passo guiado).
- [x] Decisões de plataforma (§11) fechadas.

## Como reproduzir
```bash
node eval/run-eval.mjs                 # determinístico (sem API)
ANTHROPIC_API_KEY=... node eval/run-eval.mjs   # + modelo (onde houver rede até a API)
```
