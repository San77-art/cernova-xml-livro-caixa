#!/bin/bash
# =============================================================================
# Deploy do Raio-X de Exposição no Cloudflare Pages (clique duplo no Mac).
# Publica o site + backend e mostra o link público para o WhatsApp.
# Pré-requisitos: Node.js instalado (nodejs.org) e conta no Cloudflare (grátis).
# =============================================================================
cd "$(dirname "$0")" || exit 1
PROJ="raiox-medicos"

echo "================================================================"
echo "  Raio-X de Exposição — publicação no Cloudflare"
echo "================================================================"
echo

if ! command -v node >/dev/null 2>&1; then
  echo "❌ Node.js não encontrado. Instale a versão LTS em https://nodejs.org e rode de novo."
  read -r -p "Enter para sair."; exit 1
fi

# Carrega variáveis do .dev.vars (chave da API e, se houver, token do Cloudflare)
set -a; [ -f .dev.vars ] && . ./.dev.vars; set +a
: "${CLOUDFLARE_ACCOUNT_ID:=ee7f86487c8c24683fd5ada3617a19f3}"
export CLOUDFLARE_ACCOUNT_ID

# Autenticação por TOKEN (sem navegador). O token fica só na sua máquina.
if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
  echo "1/4 · Autenticação do Cloudflare por token."
  echo "      Cole abaixo o token que você criou no painel (Conta · Cloudflare Pages · Editar)."
  echo "      Ele fica só no seu computador — ninguém mais vê."
  printf "      Cole o token e aperte Enter: "
  read -r CLOUDFLARE_API_TOKEN
fi
export CLOUDFLARE_API_TOKEN
if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
  echo "❌ Nenhum token informado."; read -r -p "Enter para sair."; exit 1
fi
echo "→ Verificando o token…"
npx --yes wrangler whoami >/dev/null 2>&1 && echo "   token OK" || echo "   (seguindo; o deploy confirma o acesso)"

echo
echo "2/4 · Publicando o site e o backend…"
npx --yes wrangler pages deploy public --project-name="$PROJ" --branch=production --commit-dirty=true || {
  echo "Falha no deploy."; read -r -p "Enter para sair."; exit 1; }

echo
echo "3/4 · Configurando a chave da API (lida do .dev.vars)…"
KEY=$(grep '^ANTHROPIC_API_KEY=' .dev.vars | cut -d= -f2-)
if [ -n "$KEY" ]; then
  printf '%s' "$KEY" | npx --yes wrangler pages secret put ANTHROPIC_API_KEY --project-name="$PROJ"
else
  echo "⚠️  Não achei a chave no .dev.vars — configure depois com:"
  echo "    npx wrangler pages secret put ANTHROPIC_API_KEY --project-name=$PROJ"
fi

echo
echo "4/4 · Configurando o webhook do Google Sheets (gravação de leads)…"
SHEET="${SHEETS_WEBHOOK_URL:-}"
if [ -z "$SHEET" ]; then
  read -r -p "Cole a URL /exec do Apps Script e Enter (ou só Enter para pular): " SHEET
fi
if [ -n "$SHEET" ]; then
  printf '%s' "$SHEET" | npx --yes wrangler pages secret put SHEETS_WEBHOOK_URL --project-name="$PROJ"
else
  echo "   (pulado — leads não serão gravados até configurar)"
fi

echo
echo "→ Republicando para aplicar a chave da API e os segredos…"
npx --yes wrangler pages deploy public --project-name="$PROJ" --branch=production --commit-dirty=true >/dev/null 2>&1

echo
echo "================================================================"
echo "✅ Pronto! Seu Raio-X está no ar."
echo "   Link (use no WhatsApp):  https://$PROJ.pages.dev"
echo "   Conferir config:         https://$PROJ.pages.dev/api/health"
echo "================================================================"
read -r -p "Enter para fechar."
