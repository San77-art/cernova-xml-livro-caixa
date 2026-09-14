// =============================================================================
// app.js — Frontend do Raio-X de Exposição. A lógica de fluxo e score vem do
// módulo compartilhado roteiro.mjs (mesma fonte de verdade do backend/eval).
// =============================================================================
import {
  BLOCO_A,
  getQuestionsForArchetype,
  routeArchetype,
  computeResult,
  FAIXA_META,
  trajectoryLength,
} from "./shared/roteiro.mjs";

// ---- Configuração editável -------------------------------------------------
const CONFIG = {
  // Preencha com o WhatsApp do comercial (só dígitos, com DDI 55) para o CTA
  // abrir a conversa. Ex.: "5567999999999". Se vazio, o CTA mostra confirmação.
  comercialWhatsApp: "",
};

// ---- Estado ----------------------------------------------------------------
const answers = {};
let questions = [...BLOCO_A]; // diagnóstico é anexado após o Bloco A
let idx = 0;
let archetype = null;
let chatHistory = [];
let lastResult = null;

// ---- Helpers de tela -------------------------------------------------------
const $ = (id) => document.getElementById(id);
function show(screen) {
  document.querySelectorAll(".screen").forEach((s) => s.classList.remove("active"));
  $(screen).classList.add("active");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// ---- Velocímetro (SVG) -----------------------------------------------------
function pointAt(deg, r = 80, cx = 100, cy = 100) {
  const t = (deg * Math.PI) / 180;
  return [cx + r * Math.cos(t), cy - r * Math.sin(t)];
}
function arc(a1, a2, color) {
  const [x1, y1] = pointAt(a1);
  const [x2, y2] = pointAt(a2);
  return `<path d="M ${x1.toFixed(1)} ${y1.toFixed(1)} A 80 80 0 0 1 ${x2.toFixed(1)} ${y2.toFixed(1)}" stroke="${color}" stroke-width="16" fill="none" stroke-linecap="round"/>`;
}
function drawGauge(elId, faixa, score) {
  const ang = 180 - (Math.min(score, 16) / 16) * 180; // 0pts=180°(esq) .. 16pts=0°(dir)
  const [nx, ny] = pointAt(ang, 62);
  const cols = { verde: "#5a8f6e", amarelo: "#bb9a44", vermelho: "#a8543f" };
  const dim = (z) => (z === faixa ? cols[z] : cols[z] + "55");
  const svg = `
  <svg viewBox="0 0 200 118" xmlns="http://www.w3.org/2000/svg" style="width:100%;">
    ${arc(180, 121, dim("verde"))}
    ${arc(119, 61, dim("amarelo"))}
    ${arc(59, 0, dim("vermelho"))}
    <line x1="100" y1="100" x2="${nx.toFixed(1)}" y2="${ny.toFixed(1)}" stroke="#0e2a47" stroke-width="4" stroke-linecap="round"/>
    <circle cx="100" cy="100" r="7" fill="#0e2a47"/>
  </svg>`;
  $(elId).innerHTML = svg;
}

// ---- Quiz ------------------------------------------------------------------
function totalQuestions() {
  return archetype ? BLOCO_A.length + trajectoryLength(archetype) : BLOCO_A.length + 10;
}
function updateProgress() {
  const pct = Math.min(100, Math.round((idx / totalQuestions()) * 100));
  $("bar").style.width = pct + "%";
}

const ALICE_INTROS = {
  A: "Vamos começar entendendo sua estrutura.",
  "TRIB-PF": "Agora, sobre o seu imposto de renda como pessoa física.",
  "TRIB-PJ": "Vamos olhar a parte tributária da clínica.",
  PATRIM: "Sobre a separação entre o patrimônio da empresa e o seu.",
  SUCESS: "Agora, o tema sucessão e patrimônio da família.",
  CONV: "Sobre a sua relação com os convênios.",
  GOV: "Quase lá. Sobre dados de pacientes e governança.",
  REFORMA: "Por fim, a transição tributária de 2026.",
};
let lastBlockShown = null;

function renderQuestion() {
  const q = questions[idx];
  updateProgress();

  if (q.block !== lastBlockShown && ALICE_INTROS[q.block]) {
    $("alice-says").textContent = ALICE_INTROS[q.block];
    lastBlockShown = q.block;
  }
  $("q-text").textContent = q.text;
  const box = $("q-options");
  box.innerHTML = "";
  for (const opt of q.options) {
    const b = document.createElement("button");
    b.className = "opt" + (answers[q.id] === opt.value ? " sel" : "");
    b.textContent = opt.label;
    b.onclick = () => choose(q, opt.value);
    box.appendChild(b);
  }
  $("q-back").style.display = idx > 0 ? "block" : "none";
  $("free-input").value = "";
}

function choose(q, value) {
  answers[q.id] = value;

  // Ao terminar o Bloco A, define arquétipo e anexa o trajeto de diagnóstico.
  if (q.id === "A4" && !archetype) {
    archetype = routeArchetype(answers);
    questions = [...BLOCO_A, ...getQuestionsForArchetype(archetype)];
  }

  idx++;
  if (idx >= questions.length) return finishQuiz();
  renderQuestion();
}

function finishQuiz() {
  lastResult = computeResult(answers);
  const meta = FAIXA_META[lastResult.faixa];
  drawGauge("gauge", lastResult.faixa, lastResult.score);
  $("gband").textContent = `${meta.emoji} ${meta.rotulo}`;
  $("gband").className = "gband " + lastResult.faixa;
  $("gleitura").textContent = meta.frase;
  const n = lastResult.firedFlags.length;
  const txt = n > 0 ? `${n} ${n === 1 ? "alerta" : "alertas"}` : "seu resultado completo";
  $("lock-n").textContent = txt;
  $("lock-n2").textContent = n > 0 ? "alertas" : "detalhes";
  show("s-gate");
}

// ---- Conversa livre (digitar em vez de clicar) -----------------------------
async function sendFree() {
  const v = $("free-input").value.trim();
  if (!v) return;
  const q = questions[idx];
  chatHistory.push({ role: "user", content: v });
  $("alice-says").textContent = "…";
  $("free-input").value = "";
  try {
    const r = await fetch("/api/chat", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ messages: chatHistory, currentQuestionText: q.text }),
    });
    const data = await r.json();
    const reply = data.reply || "Boa pergunta — isso a gente confirma no diagnóstico. Voltando à pergunta:";
    chatHistory.push({ role: "assistant", content: reply });
    $("alice-says").innerHTML = fmtAlice(reply);
  } catch (e) {
    $("alice-says").textContent = "Tive um probleminha de conexão, mas seguimos. Voltando à pergunta:";
  }
}

// ---- Gate + Relatório ------------------------------------------------------
function validEmail(s) {
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(s);
}
async function submitGate() {
  const lead = {
    nome: $("f-nome").value.trim(),
    email: $("f-email").value.trim(),
    whatsapp: $("f-whats").value.trim(),
    especialidade: $("f-esp").value.trim(),
    cidade: $("f-cidade").value.trim(),
    consentimento: true,
    origem: "raio-x-web",
  };
  const err = $("gate-err");
  if (!lead.nome) return (err.textContent = "Por favor, informe seu nome.");
  if (!validEmail(lead.email)) return (err.textContent = "Informe um e-mail válido.");
  if (lead.whatsapp.replace(/\D/g, "").length < 10) return (err.textContent = "Informe um WhatsApp válido.");
  err.textContent = "";

  show("s-report");
  $("report-loading").style.display = "block";
  $("report-body").style.display = "none";

  // 1) Grava o lead (não bloqueia a geração do relatório).
  fetch("/api/lead", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ lead, answers }),
  }).catch(() => {});

  // 2) Gera o relatório a partir das fichas disparadas.
  try {
    const r = await fetch("/api/report", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ answers }),
    });
    const data = await r.json();
    if (data.error) throw new Error(data.error);
    renderReport(data, lead);
  } catch (e) {
    $("report-loading").innerHTML =
      '<p class="muted">Não consegui montar o relatório agora. Seu contato foi registrado e nosso time vai te enviar o resultado. 🙏</p>';
  }
}

function renderReport(data, lead) {
  drawGauge("gauge2", data.faixa, data.score);
  $("gband2").textContent = `${data.faixaMeta.emoji} ${data.faixaMeta.rotulo}`;
  $("gband2").className = "gband " + data.faixa;
  $("r-leitura").textContent = data.report.leitura || data.faixaMeta.frase;

  const box = $("r-alertas");
  box.innerHTML = "";
  const alertas = data.report.alertas || [];
  if (alertas.length === 0) {
    box.innerHTML = '<p class="muted">Não encontramos alertas de exposição relevante nas áreas avaliadas. Bom sinal — mas vale confirmar no diagnóstico.</p>';
  }
  for (const a of alertas) {
    const sev = (a.severidade || "medio").toLowerCase();
    const div = document.createElement("div");
    div.className = "alert " + sev;
    div.innerHTML = `<span class="sev-tag ${sev}">${sev}</span>
      <h3>${esc(a.titulo)}</h3>
      <div class="imp">${esc(a.impacto)}</div>
      <div class="fund">${esc(a.fundamento || "")}</div>`;
    box.appendChild(div);
  }
  $("r-naoaval").textContent = data.report.naoAvaliado || "";
  $("r-cta").textContent = data.cta || "";
  $("r-disclaimer").textContent = data.disclaimer || "";

  $("r-cta-btn").onclick = () => {
    if (CONFIG.comercialWhatsApp) {
      const msg = encodeURIComponent(
        `Olá! Fiz o Raio-X de Exposição (resultado: ${data.faixaMeta.rotulo}) e quero falar sobre o diagnóstico. Meu nome é ${lead.nome}.`
      );
      window.open(`https://wa.me/${CONFIG.comercialWhatsApp}?text=${msg}`, "_blank");
    } else {
      $("r-cta-btn").textContent = "✓ Recebemos seu contato — nosso time vai falar com você!";
      $("r-cta-btn").disabled = true;
    }
  };

  $("report-loading").style.display = "none";
  $("report-body").style.display = "block";
}

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}
// Remove markdown das respostas da Alice (asteriscos) e converte **x** em negrito.
function fmtAlice(s) {
  return esc(s)
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*/g, "")
    .replace(/\n/g, "<br>");
}

// ---- Bindings --------------------------------------------------------------
$("go-consent").onclick = () => show("s-consent");
$("back-landing").onclick = () => show("s-landing");
$("consent-check").onchange = (e) => ($("go-quiz").disabled = !e.target.checked);
$("go-quiz").onclick = () => {
  show("s-quiz");
  renderQuestion();
};
$("q-back").onclick = () => {
  if (idx > 0) {
    idx--;
    renderQuestion();
  }
};
$("free-send").onclick = sendFree;
$("free-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendFree();
});
$("go-report").onclick = submitGate;
