# Raio-X de Exposição — Agente Alice (degrau 0) · Médicos e Clínicas

Triagem gratuita que revela a exposição jurídico-fiscal do médico/clínica, mostra o velocímetro
de risco, captura o lead e abre a venda do Diagnóstico. Construído na **Claude Developer Platform**
(API, Sonnet 4.6+), com **roteiro e score determinísticos** e o modelo redigindo só o tom e os
alertas a partir das **36 fichas validadas** em `../base-conhecimento/`.

---

## O que tem aqui (mapa dos arquivos)

```
raiox-medicos/
├── public/                     # frontend (servido como site estático)
│   ├── index.html              #   landing + consentimento + quiz + velocímetro + gate + relatório
│   ├── app.js                  #   lógica de tela (importa o roteiro)
│   └── shared/roteiro.mjs      #   ⭐ FONTE DE VERDADE do fluxo: perguntas, arquétipos, flags, score
├── functions/api/              # backend (Cloudflare Pages Functions — guardam a chave)
│   ├── report.js               #   POST /api/report  → gera os alertas das fichas (com prompt caching)
│   ├── chat.js                 #   POST /api/chat    → turno de conversa livre da Alice
│   ├── lead.js                 #   POST /api/lead    → grava o lead no Google Sheets
│   └── health.js               #   GET  /api/health  → confere a configuração
├── shared/
│   ├── prompts.mjs             #   system prompt da Alice + montagem de contexto (caching) + relatório
│   ├── kb.mjs                  #   base de conhecimento empacotada (AUTO-GERADA — não editar à mão)
│   └── anthropic.mjs           #   cliente da Messages API
├── eval/                       # harness de avaliação (Spec §12)
│   ├── avatars.mjs             #   4 avatares + gabarito
│   └── run-eval.mjs            #   roda a bateria
├── build-kb.mjs                # gera shared/kb.mjs a partir de ../base-conhecimento
├── google-apps-script.gs       # webhook da planilha de leads (Google Sheets)
├── deploy.command              # ⭐ DEPLOY EM 1 CLIQUE (Mac) → publica e te dá o link
├── EVAL-RESULTS.md             # resultado dos testes
└── wrangler.toml / package.json
```

A base muda? Rode `npm run build:kb` para reempacotar as fichas. O roteiro muda? Edite só
`public/shared/roteiro.mjs` (frontend, backend e eval usam o mesmo arquivo).

---

## Publicar e ter o link do WhatsApp (3 passos)

Você precisa de **uma conta gratuita no Cloudflare** (https://dash.cloudflare.com/sign-up) e do
**Node.js** instalado (https://nodejs.org — versão LTS). A chave da API já está no `.dev.vars`.

### Caminho fácil (Mac): clique duplo
1. Crie a conta no Cloudflare (link acima) — leva 2 minutos.
2. Dê **clique duplo** no arquivo `deploy.command` (nesta pasta). Vai abrir o Terminal.
3. Quando abrir o navegador pedindo para autorizar o Cloudflare, clique **Allow**. Pronto.

No fim ele mostra o link público (ex.: `https://raiox-medicos.pages.dev`) — é esse que vai no WhatsApp.

### Caminho manual (qualquer sistema)
No Terminal, dentro desta pasta:
```bash
npx wrangler login                                   # abre o navegador → Allow
npx wrangler pages deploy public --project-name=raiox-medicos --commit-dirty=true
npx wrangler pages secret put ANTHROPIC_API_KEY --project-name=raiox-medicos   # cole a chave
npx wrangler pages secret put SHEETS_WEBHOOK_URL --project-name=raiox-medicos  # cole a URL do Apps Script
```
Confira em `https://SEU-PROJETO.pages.dev/api/health` se aparece `"anthropic_key":"configurada"`.

---

## Captura de leads no Google Sheets (uma vez)
1. Crie uma planilha no Google Sheets (ex.: "Leads Raio-X").
2. **Extensões › Apps Script**, apague tudo e cole o conteúdo de `google-apps-script.gs`.
3. **Implantar › Nova implantação › App da Web** · executar como **Eu mesmo** · acesso **Qualquer pessoa**.
4. Copie a URL `/exec` e use no `SHEETS_WEBHOOK_URL` (passo de secret acima).
Cada lead vira uma linha: contato + arquétipo + faixa + score + alertas + respostas.

> Enquanto o `SHEETS_WEBHOOK_URL` não estiver configurado, o site funciona normalmente, mas os
> leads não são gravados (o `/api/health` avisa).

## Botão de CTA → WhatsApp do comercial
Em `public/app.js`, no topo, preencha `CONFIG.comercialWhatsApp` com o número (só dígitos, com 55).
Ex.: `"5567999999999"`. Se ficar vazio, o CTA mostra "Recebemos seu contato" (o lead já foi gravado).

---

## Testar antes de publicar (opcional)
```bash
npm run dev      # abre local em http://localhost:8788 (usa a chave do .dev.vars)
npm run eval     # roda a bateria determinística (e o modelo, onde houver rede até a API)
```

## Migrar para domínio próprio depois
No painel do Cloudflare › Pages › seu projeto › **Custom domains** › adicionar
`raiox.juniorcontabilidade.com.br` e seguir o apontamento de DNS. Nada no código muda.

## Custos
- **Cloudflare Pages:** gratuito nessa escala.
- **API Anthropic:** paga por uso. A base (estática) usa **prompt caching**, então o custo por
  Raio-X é baixo (poucos centavos). Acompanhe em platform.claude.com › Faturamento.
- A chave criada para isto chama-se **`raiox-medicos`** (revogável a qualquer momento no Console).

## Segurança / LGPD
- A chave da API fica **só no servidor** (secret do Cloudflare); nunca no navegador do paciente.
- Consentimento LGPD é exigido **antes** da 1ª pergunta; não se coleta nenhum dado de paciente.
- `.dev.vars` (com a chave) está no `.gitignore` — não suba para repositório público.
