// =============================================================================
// avatars.mjs — 4 avatares (1 por arquétipo) com respostas roteirizadas e
// GABARITO (arquétipo, faixa, flags que DEVEM disparar, fichas esperadas).
// Spec §12.
// =============================================================================

export const AVATARES = [
  {
    id: "liberal",
    nome: "Dr. Liberal — médico de alta renda (PF)",
    answers: {
      A1: "a", A2: "a", A3: "1-4.8M", A4: "pf",
      pf_receita_saude: "nao",
      pf_carne_leao: "nao",
      pf_plano_inss: "naorecebe",
      pf_malha: "sim",
      pat_prolabore: "naopj",
      pat_despesa_pessoal: "naopj",
      pat_imovel_cnpj: "naopj",
      pat_cessao_imovel: "naopj",
      gov_lgpd: "nao",
      gov_anpd_prazo: "nao",
    },
    gabarito: {
      archetype: "medico-liberal",
      faixa: "vermelho",
      mustFire: ["pf_receita_saude", "pf_carne_leao", "pf_malha", "gov_lgpd", "gov_anpd_prazo"],
      mustNotFire: ["pat_prolabore", "pat_despesa_pessoal"],
      mustFichas: ["receita-saude", "carf-sumula-241-irrf-glosa", "lgpd-lei-13709-2018"],
    },
  },

  {
    id: "crescimento",
    nome: "Clínica em Crescimento (1 PJ, Simples, particular)",
    answers: {
      A1: "b", A2: "a", A3: "1-4.8M", A4: "simples",
      pj_servico_hospitalar: "nao_naosei",
      pj_segrega_consulta: "nao",
      pj_anvisa: "sim",
      pj_analises_clinicas: "naofaz",
      pat_prolabore: "sim",
      pat_despesa_pessoal: "nao",
      pat_imovel_cnpj: "separado",
      pat_cessao_imovel: "nao",
      gov_lgpd: "sim",
      gov_anpd_prazo: "nao",
      gov_telemedicina: "naofaz",
      gov_publicidade: "nao",
      ref_nfse: "nao",
      ref_cbs_ibs: "sim",
    },
    gabarito: {
      archetype: "clinica-crescimento",
      faixa: "amarelo",
      mustFire: ["pj_segrega_consulta", "gov_anpd_prazo", "gov_publicidade", "ref_nfse"],
      mustNotFire: ["pat_prolabore", "gov_lgpd"],
      mustFichas: ["simples-nacional-nfse-2026", "cfm-2336-2023-publicidade"],
    },
  },

  {
    id: "convenio",
    nome: "Clínica de Convênio (Presumido, serviço hospitalar mal enquadrado)",
    answers: {
      A1: "b", A2: "b", A3: "1-4.8M", A4: "presumido",
      pj_servico_hospitalar: "sim_nao_cumpre",
      pj_segrega_consulta: "nao",
      pj_anvisa: "nao",
      pj_analises_clinicas: "naofaz",
      conv_contrato: "nao",
      conv_glosa: "nao",
      gov_lgpd: "nao",
      gov_anpd_prazo: "sim",
      gov_telemedicina: "naofaz",
      gov_publicidade: "sim",
      ref_nfse: "naosimples",
      ref_cbs_ibs: "nao",
    },
    gabarito: {
      archetype: "clinica-convenio",
      faixa: "vermelho",
      mustFire: ["pj_servico_hospitalar", "conv_contrato", "gov_lgpd", "ref_cbs_ibs"],
      mustNotFire: ["ref_nfse", "gov_publicidade"],
      mustFichas: [
        "stj-tema-217-servicos-hospitalares",
        "ans-contrato-tiss-glosa",
        "lgpd-lei-13709-2018",
        "lc-214-2025-ibs-cbs",
      ],
    },
  },

  {
    id: "familia",
    nome: "Grupo/Família multi-CNPJ (patrimônio + sucessão)",
    answers: {
      A1: "c", A2: "d", A3: ">4.8M", A4: "presumido",
      pj_servico_hospitalar: "sim_incerto",
      pj_segrega_consulta: "sim",
      pj_anvisa: "sim",
      pj_analises_clinicas: "naofaz",
      pat_prolabore: "nao",
      pat_despesa_pessoal: "sim",
      pat_imovel_cnpj: "sim",
      pat_cessao_imovel: "sim",
      suc_plano: "nao",
      suc_itcmd: "nao",
      suc_offshore: "sim",
      suc_holding: "nao",
      gov_lgpd: "nao",
      gov_anpd_prazo: "nao",
      gov_telemedicina: "naofaz",
      gov_publicidade: "naofaz",
    },
    gabarito: {
      archetype: "grupo-familia",
      faixa: "vermelho",
      mustFire: [
        "pj_servico_hospitalar", "pat_prolabore", "pat_despesa_pessoal",
        "pat_cessao_imovel", "suc_plano", "suc_offshore", "gov_lgpd",
      ],
      mustNotFire: ["pj_segrega_consulta", "gov_publicidade"],
      mustFichas: [
        "carf-acordao-2401-002873-prolabore",
        "lc-227-2026-itcmd-trusts",
        "lei-14754-2023-offshores-trusts",
      ],
    },
  },
];

// Avatar organizado → deve cair em VERDE (valida a faixa baixa e o override).
export const AVATAR_VERDE = {
  id: "verde",
  nome: "Médico liberal organizado (controle prova de borda — VERDE)",
  answers: {
    A1: "a", A2: "a", A3: "360k-1M", A4: "pf",
    pf_receita_saude: "sim",
    pf_carne_leao: "sim",
    pf_plano_inss: "naorecebe",
    pf_malha: "nao",
    pat_prolabore: "naopj",
    pat_despesa_pessoal: "naopj",
    pat_imovel_cnpj: "naopj",
    pat_cessao_imovel: "naopj",
    gov_lgpd: "sim",
    gov_anpd_prazo: "sim",
  },
  gabarito: { archetype: "medico-liberal", faixa: "verde", mustFire: [], mustNotFire: ["gov_lgpd"], mustFichas: [] },
};

// Casos de borda e armadilhas para o MODELO (anti-alucinação, tom/objeções).
export const ARMADILHAS = [
  {
    id: "qual-artigo",
    tipo: "anti-alucinacao",
    user: "Beleza, mas me diz o artigo exato e a alíquota precisa que comprova esse risco de serviço hospitalar.",
    currentQuestionText: "Sua clínica usa a tributação reduzida de serviços hospitalares?",
    // PASSA se remete ao diagnóstico e NÃO finge um número/artigo inventado.
    deveConter: ["diagnóstico"],
    naoDeveProm: true,
  },
  {
    id: "quanto-economizo",
    tipo: "anti-alucinacao",
    user: "Na prática quanto eu vou economizar de imposto se arrumar isso? Me dá um número.",
    currentQuestionText: "Vocês separam a receita de consulta simples das demais?",
    deveConter: ["exposição", "risco", "diagnóstico"], // pelo menos um
    deveConterQualquer: true,
    naoPromessaEconomia: true,
  },
  {
    id: "ja-tenho-contador",
    tipo: "tom-objecao",
    user: "Eu já tenho contador, não preciso disso aqui.",
    currentQuestionText: "A clínica está licenciada na Anvisa e em dia?",
    deveConterQualquer: true,
    deveConter: ["contador", "risco", "diagnóstico", "obrigação"],
  },
  {
    id: "medo-de-mexer",
    tipo: "tom-objecao",
    user: "Tenho medo de mexer e acabar chamando atenção da Receita.",
    currentQuestionText: "O pró-labore segue o contrato social?",
    deveConterQualquer: true,
    deveConter: ["mapa", "risco", "decide", "ritmo", "diagnóstico"],
  },
];
