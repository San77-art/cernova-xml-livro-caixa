/**
 * Google Apps Script — Webhook de captura de leads do Raio-X de Exposição.
 *
 * COMO USAR (3 minutos):
 * 1. Crie uma planilha no Google Sheets (ex.: "Leads Raio-X").
 * 2. Menu Extensões > Apps Script. Apague o conteúdo e cole este arquivo.
 * 3. Salve. Clique em "Implantar" > "Nova implantação" > tipo "App da Web".
 *    - Executar como: Eu mesmo.
 *    - Quem pode acessar: Qualquer pessoa.
 * 4. Copie a URL gerada (termina em /exec). É essa URL que vai no secret
 *    SHEETS_WEBHOOK_URL do Cloudflare.
 *
 * Cada lead vira uma linha. O cabeçalho é criado automaticamente.
 */

var CABECALHO = [
  "timestamp", "nome", "email", "whatsapp", "especialidade", "cidade",
  "arquetipo", "faixa", "score", "n_alertas", "alertas", "respostas",
  "consentimento", "origem"
];

function doPost(e) {
  try {
    var dados = JSON.parse(e.postData.contents);
    var planilha = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];

    // Cria o cabeçalho na primeira vez
    if (planilha.getLastRow() === 0) {
      planilha.appendRow(CABECALHO);
    }

    var linha = CABECALHO.map(function (col) {
      return dados[col] !== undefined ? dados[col] : "";
    });
    planilha.appendRow(linha);

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, erro: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService
    .createTextOutput("Webhook do Raio-X ativo.")
    .setMimeType(ContentService.MimeType.TEXT);
}
