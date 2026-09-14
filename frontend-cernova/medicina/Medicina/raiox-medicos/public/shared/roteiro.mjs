// =============================================================================
// Raio-X de Exposição — Roteiro + Motor de Score (lógica determinística)
// Fonte de verdade: Raio-X-de-Exposicao.md  · Spec-Agente-RaioX.md §6
//
// IMPORTANTE: a ramificação (arquétipo) e o score vivem AQUI, na lógica da
// aplicação — não na "boa vontade" do modelo. O modelo só redige o tom e os
// alertas a partir das fichas. Isto garante previsibilidade e testabilidade.
//
// Este módulo é importado pelo frontend (browser), pelo backend (Cloudflare
// Functions) e pelo harness de eval (Node). Mantém-se sem dependências.
// =============================================================================

// Pesos de severidade (Spec §6)
export const PESO = { alto: 3, medio: 2, baixo: 1 };

// -----------------------------------------------------------------------------
// BLOCO A — Identificação e segmentação (todos respondem). Não pontua.
// -----------------------------------------------------------------------------
export const BLOCO_A = [
  {
    id: "A1",
    block: "A",
    text: "Como você atua hoje?",
    options: [
      { value: "a", label: "Só pessoa física (sem empresa)" },
      { value: "b", label: "Tenho 1 PJ / clínica" },
      { value: "e", label: "Atuo como PF e PJ ao mesmo tempo" },
      { value: "c", label: "Tenho 2+ CNPJs / grupo" },
      { value: "d", label: "Clínica com sócios" },
    ],
  },
  {
    id: "A2",
    block: "A",
    text: "De onde vem a maior parte da sua receita?",
    options: [
      { value: "a", label: "Particular / reembolso" },
      { value: "b", label: "Convênios / planos de saúde" },
      { value: "c", label: "Hospital / PJ que me contrata" },
      { value: "d", label: "Misto" },
    ],
  },
  {
    id: "A3",
    block: "A",
    text: "Faixa de faturamento anual (somando tudo):",
    options: [
      { value: "ate360k", label: "Até R$ 360 mil" },
      { value: "360k-1M", label: "R$ 360 mil – 1 milhão" },
      { value: "1-4.8M", label: "R$ 1 – 4,8 milhões" },
      { value: ">4.8M", label: "Acima de R$ 4,8 milhões" },
    ],
  },
  {
    id: "A4",
    block: "A",
    text: "Regime tributário atual:",
    options: [
      { value: "pf", label: "Pessoa física (carnê-leão)" },
      { value: "simples", label: "Simples Nacional" },
      { value: "presumido", label: "Lucro Presumido" },
      { value: "real", label: "Lucro Real" },
      { value: "naosei", label: "Não sei" },
    ],
  },
];

// Helper para opções "neutras" (não disparam flag)
const ok = (value, label) => ({ value, label, fires: false });
// Helper para opções que disparam flag
const flag = (value, label, severity, fichas) => ({
  value,
  label,
  fires: true,
  severity,
  fichas,
});

// -----------------------------------------------------------------------------
// Banco de perguntas por bloco. Cada opção de risco carrega severidade + fichas.
// -----------------------------------------------------------------------------
export const BLOCKS = {
  // ---- TRIB-PF — Médico pessoa física --------------------------------------
  "TRIB-PF": [
    {
      id: "pf_receita_saude",
      block: "TRIB-PF",
      text: "Você emite recibo eletrônico (Receita Saúde) de todos os atendimentos particulares?",
      options: [
        ok("sim", "Sim, de todos"),
        flag("nao", "Não / só de parte deles", "alto", ["receita-saude"]),
        flag("naosei", "Não sei o que é Receita Saúde", "alto", ["receita-saude"]),
      ],
    },
    {
      id: "pf_carne_leao",
      block: "TRIB-PF",
      text: "Você usa Carnê-Leão e Livro Caixa para deduzir despesas e apurar o IR mês a mês?",
      options: [
        ok("sim", "Sim, com Livro Caixa"),
        flag("nao", "Não / pago sobre a receita cheia", "medio", ["livro-caixa-carne-leao"]),
        flag("naosei", "Não sei", "medio", ["livro-caixa-carne-leao"]),
      ],
    },
    {
      id: "pf_plano_inss",
      block: "TRIB-PF",
      text: "Recebe de plano de saúde como pessoa física e sabe quem recolhe a contribuição previdenciária?",
      options: [
        ok("naorecebe", "Não recebo de plano como PF"),
        ok("sei", "Recebo e sei quem recolhe"),
        flag("naosei", "Recebo, mas não sei / acho que é a operadora", "medio", ["irrf-servicos-medicos"]),
      ],
    },
    {
      id: "pf_malha",
      block: "TRIB-PF",
      text: "Já recebeu carta da malha, intimação ou aviso da Receita?",
      options: [
        ok("nao", "Não"),
        flag("sim", "Sim", "alto", ["carf-sumula-241-irrf-glosa"]),
      ],
    },
  ],

  // ---- TRIB-PJ — Clínica / grupo -------------------------------------------
  "TRIB-PJ": [
    {
      id: "pj_servico_hospitalar",
      block: "TRIB-PJ",
      text: "Sua clínica usa (ou quer usar) a tributação reduzida de \"serviços hospitalares\" (presunção de 8% IRPJ / 12% CSLL)?",
      options: [
        ok("sim_ok", "Sim, e somos sociedade empresária com licença Anvisa em dia"),
        flag("sim_incerto", "Sim, mas não tenho certeza se cumprimos sociedade empresária + Anvisa", "alto", [
          "stj-tema-217-servicos-hospitalares",
          "carf-sumula-142-servicos-hospitalares",
          "parecer-sei-7689-2021-servicos-hospitalares",
        ]),
        flag("sim_nao_cumpre", "Sim, e NÃO somos sociedade empresária / sem licença Anvisa", "alto", [
          "stj-tema-217-servicos-hospitalares",
          "carf-sumula-142-servicos-hospitalares",
          "stj-resp-1877568-anestesiologia",
        ]),
        flag("nao_naosei", "Não usamos / não sei o que é isso", "baixo", ["stj-tema-217-servicos-hospitalares"]),
      ],
    },
    {
      id: "pj_segrega_consulta",
      block: "TRIB-PJ",
      text: "Vocês separam a receita de consulta simples das demais (procedimentos, exames, terapias)?",
      options: [
        ok("sim", "Sim, é separado"),
        flag("nao", "Não / não sei", "medio", ["stj-resp-1877568-anestesiologia"]),
      ],
    },
    {
      id: "pj_anvisa",
      block: "TRIB-PJ",
      text: "A clínica está registrada/licenciada na Anvisa/vigilância sanitária e em dia?",
      options: [
        ok("sim", "Sim, licença em dia"),
        flag("nao", "Não / não sei", "medio", ["anvisa-rdc-63-2011-rdc-50-2002"]),
      ],
    },
    {
      id: "pj_analises_clinicas",
      block: "TRIB-PJ",
      text: "Se faz análises clínicas/laboratório (inclusive testes rápidos), conhece a norma vigente (RDC 978/2025)?",
      options: [
        ok("naofaz", "Não fazemos análises clínicas"),
        ok("conhece", "Fazemos e conhecemos a norma"),
        flag("naoconhece", "Fazemos, mas não conheço a norma", "baixo", ["anvisa-rdc-978-2025-analises-clinicas"]),
      ],
    },
  ],

  // ---- PATRIM — Patrimonial / societário -----------------------------------
  PATRIM: [
    {
      id: "pat_prolabore",
      block: "PATRIM",
      text: "O pró-labore e a distribuição de lucros seguem exatamente o que está no contrato social?",
      options: [
        ok("naopj", "Não tenho PJ"),
        ok("sim", "Sim, seguem o contrato"),
        flag("nao", "Não / não sei", "alto", ["carf-acordao-2401-002873-prolabore"]),
      ],
    },
    {
      id: "pat_despesa_pessoal",
      block: "PATRIM",
      text: "A empresa paga alguma despesa pessoal do sócio (cartão, carro, condomínio, casa)?",
      options: [
        ok("naopj", "Não tenho PJ"),
        ok("nao", "Não, é tudo separado"),
        flag("sim", "Sim / às vezes", "alto", [
          "carf-acordao-2401-002873-prolabore",
          "lei-13874-2019-liberdade-economica",
        ]),
      ],
    },
    {
      id: "pat_imovel_cnpj",
      block: "PATRIM",
      text: "O imóvel da clínica está no mesmo CNPJ da operação?",
      options: [
        ok("naopj", "Não tenho PJ / imóvel próprio"),
        ok("separado", "Não, está separado (outra PJ ou PF)"),
        flag("sim", "Sim / não sei", "medio", ["lei-13874-2019-liberdade-economica"]),
      ],
    },
    {
      id: "pat_cessao_imovel",
      block: "PATRIM",
      text: "Existe cessão de imóvel ou bem da empresa a sócio sem contrato a valor de mercado?",
      options: [
        ok("naopj", "Não tenho PJ"),
        ok("nao", "Não"),
        flag("sim", "Sim", "alto", ["carf-acordao-2401-002873-prolabore"]),
      ],
    },
  ],

  // ---- SUCESS — Sucessório (grupo/família) ---------------------------------
  SUCESS: [
    {
      id: "suc_plano",
      block: "SUCESS",
      text: "Existe um plano de sucessão (quem comanda, quem vota e quem recebe se o sócio-chave faltar)?",
      options: [
        ok("sim", "Sim, está desenhado"),
        flag("nao", "Não", "alto", ["lc-227-2026-itcmd-trusts"]),
      ],
    },
    {
      id: "suc_itcmd",
      block: "SUCESS",
      text: "Já estimaram o ITCMD da sucessão e de onde sairia a liquidez para pagá-lo?",
      options: [
        ok("sim", "Sim"),
        flag("nao", "Não", "medio", ["lc-227-2026-itcmd-trusts", "ec-132-2023-reforma"]),
      ],
    },
    {
      id: "suc_offshore",
      block: "SUCESS",
      text: "Têm offshore ou trust no exterior montado antes de 2024?",
      options: [
        ok("nao", "Não"),
        flag("sim", "Sim", "alto", ["lei-14754-2023-offshores-trusts", "lc-227-2026-itcmd-trusts"]),
      ],
    },
    {
      id: "suc_holding",
      block: "SUCESS",
      text: "Já pensaram em holding familiar ou inventário extrajudicial?",
      options: [
        ok("sim", "Sim, já estudamos"),
        flag("nao", "Não / não sei", "baixo", ["cnj-571-2024-inventario-extrajudicial"]),
      ],
    },
  ],

  // ---- CONV — Convênio ------------------------------------------------------
  CONV: [
    {
      id: "conv_contrato",
      block: "CONV",
      text: "Há contrato escrito com todas as operadoras com quem vocês trabalham?",
      options: [
        ok("sim", "Sim, com todas"),
        flag("nao", "Não / só com algumas", "alto", ["ans-contrato-tiss-glosa"]),
      ],
    },
    {
      id: "conv_glosa",
      block: "CONV",
      text: "Têm uma rotina formal de recurso de glosa (faturamento em TISS, prazos, contestação)?",
      options: [
        ok("sim", "Sim"),
        flag("nao", "Não / não sei", "medio", ["ans-contrato-tiss-glosa"]),
      ],
    },
  ],

  // ---- GOV — Governança / dados (GOV-min = só as 2 primeiras) ---------------
  GOV: [
    {
      id: "gov_lgpd",
      block: "GOV",
      text: "Vocês tratam dados de pacientes com base legal definida, controle de acesso e plano de incidente?",
      options: [
        ok("sim", "Sim"),
        flag("nao", "Não / não sei", "alto", ["lgpd-lei-13709-2018", "anpd-res-15-2024-incidentes"]),
      ],
    },
    {
      id: "gov_anpd_prazo",
      block: "GOV",
      text: "Sabem que um incidente relevante (vazamento) precisa ser comunicado à ANPD em 3 dias úteis?",
      options: [
        ok("sim", "Sim, sabíamos"),
        flag("nao", "Não", "medio", ["anpd-res-15-2024-incidentes"]),
      ],
    },
    {
      id: "gov_telemedicina",
      block: "GOV",
      text: "Atendem por telemedicina com registro em prontuário?",
      options: [
        ok("naofaz", "Não fazemos telemedicina"),
        ok("sim", "Sim, com registro em prontuário"),
        flag("semregistro", "Sim, sem registro formal", "medio", ["cfm-2314-2022-telemedicina"]),
      ],
    },
    {
      id: "gov_publicidade",
      block: "GOV",
      text: "A publicidade e as redes sociais seguem a Resolução CFM 2.336/2023 (CRM/RQE, regras de imagem e preço)?",
      options: [
        ok("naofaz", "Não fazemos publicidade"),
        ok("sim", "Sim, seguem as regras"),
        flag("nao", "Não / não sei", "medio", ["cfm-2336-2023-publicidade"]),
      ],
    },
  ],

  // ---- REFORMA — Transição 2026 (clínicas) ---------------------------------
  REFORMA: [
    {
      id: "ref_nfse",
      block: "REFORMA",
      text: "Se a clínica é do Simples, já está pronta para a NFS-e nacional (obrigatória desde set/2026)?",
      options: [
        ok("naosimples", "Não somos do Simples"),
        ok("pronto", "Sim, já estamos prontos"),
        flag("nao", "Não / não sei", "alto", ["simples-nacional-nfse-2026"]),
      ],
    },
    {
      id: "ref_cbs_ibs",
      block: "REFORMA",
      text: "Seu sistema já emite documento com destaque de CBS/IBS (vigente desde jan/2026)?",
      options: [
        ok("sim", "Sim"),
        flag("nao", "Não / não sei", "medio", ["lc-214-2025-ibs-cbs"]),
      ],
    },
  ],
};

// -----------------------------------------------------------------------------
// Trajetos por arquétipo (Raio-X-de-Exposicao.md · fluxo).
// mode:"min" para GOV = só as 2 primeiras perguntas (médico liberal).
// -----------------------------------------------------------------------------
export const TRAJETOS = {
  "medico-liberal": {
    rotulo: "Médico liberal",
    blocos: [
      { block: "TRIB-PF" },
      { block: "PATRIM" },
      { block: "GOV", mode: "min" },
    ],
  },
  "medico-misto": {
    rotulo: "Médico PF + PJ",
    blocos: [
      { block: "TRIB-PF" },
      { block: "TRIB-PJ" },
      { block: "PATRIM" },
      { block: "GOV", mode: "min" },
    ],
  },
  "clinica-crescimento": {
    rotulo: "Clínica em crescimento",
    blocos: [
      { block: "TRIB-PJ" },
      { block: "PATRIM" },
      { block: "GOV" },
      { block: "REFORMA" },
    ],
  },
  "clinica-convenio": {
    rotulo: "Clínica de convênio",
    blocos: [
      { block: "TRIB-PJ" },
      { block: "CONV" },
      { block: "GOV" },
      { block: "REFORMA" },
    ],
  },
  "grupo-familia": {
    rotulo: "Grupo / família multi-CNPJ",
    blocos: [
      { block: "TRIB-PJ" },
      { block: "PATRIM" },
      { block: "SUCESS" },
      { block: "GOV" },
    ],
  },
};

// -----------------------------------------------------------------------------
// Roteamento de arquétipo (Spec §4 · Raio-X "Regra de arquétipo").
// Precedência (para tornar determinístico em casos de sobreposição):
//   1. A1=a                        -> Médico liberal (é pessoa física)
//   2. A1=c ou A1=d                -> Grupo/família (estrutura multi-entidade domina)
//   3. A2=b (convênio)             -> Clínica de convênio
//   4. caso contrário (A1=b)       -> Clínica em crescimento
// -----------------------------------------------------------------------------
export function routeArchetype(aAnswers) {
  const a1 = aAnswers.A1;
  const a2 = aAnswers.A2;
  if (a1 === "a") return "medico-liberal";
  if (a1 === "e") return "medico-misto"; // PF + PJ ao mesmo tempo
  if (a1 === "c" || a1 === "d") return "grupo-familia";
  if (a2 === "b") return "clinica-convenio";
  return "clinica-crescimento";
}

// Devolve a lista ordenada de perguntas de diagnóstico para um arquétipo
export function getQuestionsForArchetype(archetype) {
  const traj = TRAJETOS[archetype];
  if (!traj) throw new Error("Arquétipo desconhecido: " + archetype);
  const out = [];
  for (const b of traj.blocos) {
    let perguntas = BLOCKS[b.block];
    if (b.mode === "min") perguntas = perguntas.slice(0, 2);
    out.push(...perguntas);
  }
  return out;
}

// Mapa rápido id-pergunta -> pergunta (todas as perguntas de diagnóstico)
const ALL_QUESTIONS = (() => {
  const m = {};
  for (const arr of Object.values(BLOCKS)) for (const q of arr) m[q.id] = q;
  return m;
})();

export function getQuestionById(id) {
  return ALL_QUESTIONS[id];
}

export function faixaFromScore(score) {
  if (score <= 4) return "verde";
  if (score <= 10) return "amarelo";
  return "vermelho";
}

export const FAIXA_META = {
  verde: {
    emoji: "🟢",
    rotulo: "Exposição baixa",
    frase: "Sua estrutura aparenta estar relativamente organizada — alguns ajustes pontuais resolvem.",
  },
  amarelo: {
    emoji: "🟡",
    rotulo: "Exposição relevante",
    frase: "Há buracos que podem custar caro. Vale entender o tamanho real antes que vire autuação.",
  },
  vermelho: {
    emoji: "🔴",
    rotulo: "Exposição alta",
    frase: "Há risco concreto de autuação ou de perda patrimonial. Isto pede atenção prioritária.",
  },
};

// -----------------------------------------------------------------------------
// Motor de score (Spec §6). Recebe TODAS as respostas (Bloco A + diagnóstico).
// Retorna arquétipo, flags disparadas, score, faixa e fichas do trajeto.
//
// answers = { A1:"b", A2:"a", ..., pj_servico_hospitalar:"sim_incerto", ... }
// -----------------------------------------------------------------------------
export function computeResult(answers) {
  const archetype = routeArchetype(answers);
  const perguntas = getQuestionsForArchetype(archetype);

  const firedFlags = [];
  let score = 0;
  let temAlto = false;
  const fichaIds = new Set();

  for (const q of perguntas) {
    const chosen = answers[q.id];
    if (chosen == null) continue; // sem resposta (abandono / parcial)
    const opt = q.options.find((o) => o.value === chosen);
    if (!opt || !opt.fires) continue;
    score += PESO[opt.severity];
    if (opt.severity === "alto") temAlto = true;
    for (const f of opt.fichas) fichaIds.add(f);
    firedFlags.push({
      questionId: q.id,
      block: q.block,
      pergunta: q.text,
      respostaLabel: opt.label,
      severity: opt.severity,
      fichas: opt.fichas,
    });
  }

  let faixa = faixaFromScore(score);
  // Override: qualquer flag Alto isolada puxa a leitura para pelo menos 🟡
  if (temAlto && faixa === "verde") faixa = "amarelo";

  return {
    archetype,
    archetypeLabel: TRAJETOS[archetype].rotulo,
    firedFlags,
    score,
    faixa,
    fichaIds: [...fichaIds],
    totalPerguntas: perguntas.length,
  };
}

// Quantas perguntas de diagnóstico cada arquétipo tem (para barra de progresso)
export function trajectoryLength(archetype) {
  return getQuestionsForArchetype(archetype).length;
}
