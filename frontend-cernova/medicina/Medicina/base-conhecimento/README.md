# Base de Conhecimento — Diagnóstico & Planejamento Jurisprudencial para Médicos e Clínicas

Base de conhecimento **atômica** (um arquivo por item jurídico) para alimentar agente de IA (RAG) e consulta da equipe da Junior Contabilidade. Cada documento foi **validado contra a fonte primária oficial** (STJ, STF, CARF, Planalto, Receita Federal, CFM, ANPD, Anvisa, ANS, CNJ) em **02/06/2026**.

Fonte de partida: `../Instrução para base de conhecimento.md` (relatório de *deep research*). Perfil de cliente: `../ICP-medicos.md`.

---

## Como usar

- **Cada `.md`** tem frontmatter padronizado (`id`, `tipo`, `orgao`, `numero`, `area`, `icp_fit`, `vigencia`, `status_validacao`, `fonte_oficial`, `relacionados`) + 5 seções: **1.** Identificação e teor · **2.** O que decide/determina · **3.** Vigência e validação · **4.** Aplicação ao ICP · **5.** Relacionados.
- **`_template.md`** é o gabarito para novos itens.
- **Status de validação:** `confirmado` ✅ (teor batido na fonte) · `parcial` ⚠️ (existe e regra material confere, mas há detalhe a reconferir ou divergência vs. relatório-base) · `nao-confirmado` 🚫 (**não usar como fundamento** até verificação manual).
- **Sempre cheque o campo `vigencia`** — há normas `revogada` e `parcial` na base (ver painel abaixo).

---

## Painel de status de validação

**36 documentos** · validados em 02/06/2026.

| Status | Qtd | Significado |
|---|---|---|
| ✅ Confirmado | 36 | Teor conferido em fonte oficial |
| ⚠️ Parcial | 0 | — |
| 🚫 Não confirmado | 0 | — |

**Base 100% validada em fonte oficial.** Vigência: 32 vigentes · 2 revogadas (RDC 786/2023 e 824/2023, mantidas como histórico) · 2 com vigência parcial (CNJ 35/2007, CFM 1.821/2007).

### ✅ Correções que a validação aplicou (o que o relatório-base mascarava — tudo resolvido)

1. **CARF Acórdão 2401-002.873** — inicialmente 🚫 (não aparecia na busca pública por ser de 2013). **Confirmado pelo inteiro teor (PDF oficial, Processo 10166.727564/2011-15)** — número, órgão, sessão (24/01/2013) e teor batem com o relatório. PDF em [`_fontes/`](_fontes/carf-acordao-2401-002873-proc-10166727564201115.PDF). Foi falso-negativo da busca web: acórdãos antigos exigem o inteiro teor, não o buscador.
2. **Súmula CARF 142** — o relatório atribuía a ela "sociedade empresária + Anvisa desde 2009". O **enunciado oficial cobre "até 31.12.2008" e não menciona esses requisitos** (vêm da Lei 11.727/2008 + STJ Tema 217 + Parecer SEI 7689/2021). Confirmado também que **não existe súmula CARF para o período pós-2008**. Corrigido.
3. **DMED** — a IN instituidora **985/2009 foi revogada** pela **IN RFB 2.074/2022** (vigente). Ficha atualizada para a norma vigente.
4. **IRRF serviços de saúde** — códigos DARF confirmados no MAFON/IN 1.234/2012: **1708** (1,5% serviços profissionais PJ), **6147/6188/6190** (serviços de saúde, seguro e plano). Inseridos na ficha.
5. **ANPD "11/2023" (pequeno porte)** — número **errado** no relatório; o regulamento é a **Resolução CD/ANPD 2/2022**. Corrigido.
6. **Anvisa RDC 786/2023** — **revogada pela RDC 978/2025** (vigente desde 10/06/2025). Ficha da norma vigente criada; 786 e 824 ficam como histórico.
7. **ANS RN 363/2014** — **revogada**. Vigentes: **RN 503/2022** (contratos) e **RN 489/2022** (penalidades).

---

## Índice por área

### ⚖️ Jurisprudência, súmulas e pareceres (`jurisprudencia/`)

| Item | Órgão | Status | Vigência |
|---|---|---|---|
| [STJ Tema 217 — conceito de serviços hospitalares](jurisprudencia/stj-tema-217-servicos-hospitalares.md) | STJ | ✅ | vigente |
| [STJ REsp 1.877.568 — anestesiologia fora do benefício](jurisprudencia/stj-resp-1877568-anestesiologia.md) | STJ | ✅ | vigente |
| [STF Tema 825 — ITCMD do exterior exige LC federal](jurisprudencia/stf-tema-825-itcmd-exterior.md) | STF | ✅ | vigente |
| [Parecer SEI 7689/2021/ME — vincula RFB (serviços hospitalares)](jurisprudencia/parecer-sei-7689-2021-servicos-hospitalares.md) | RFB | ✅ | vigente |
| [Súmula CARF 204 — DCOMP e homologação tácita](jurisprudencia/carf-sumula-204-dcomp.md) | CARF | ✅ | vigente |
| [Súmula CARF 241 — IRRF sem causa + glosa de despesas](jurisprudencia/carf-sumula-241-irrf-glosa.md) | CARF | ✅ | vigente |
| [Súmula CARF 142 — serviços hospitalares (até 31.12.2008)](jurisprudencia/carf-sumula-142-servicos-hospitalares.md) | CARF | ✅ | vigente |
| [CARF Acórdão 2401-002.873 — pró-labore / patrimonial](jurisprudencia/carf-acordao-2401-002873-prolabore.md) | CARF | ✅ | vigente |

### 💰 Normas tributárias (`normas-tributarias/`)

| Item | Órgão | Status | Vigência |
|---|---|---|---|
| [LC 214/2025 — IBS/CBS/IS (saúde -60%)](normas-tributarias/lc-214-2025-ibs-cbs.md) | Congresso | ✅ | vigente |
| [Lei 14.754/2023 — offshores, trusts e fundos](normas-tributarias/lei-14754-2023-offshores-trusts.md) | Congresso | ✅ | vigente |
| [Lei 14.689/2023 — CARF / voto de qualidade](normas-tributarias/lei-14689-2023-carf.md) | Congresso | ✅ | vigente |
| [Receita Saúde (IN RFB 2.240/2024)](normas-tributarias/receita-saude.md) | RFB | ✅ | vigente |
| [Livro Caixa + Carnê-Leão (médico PF)](normas-tributarias/livro-caixa-carne-leao.md) | RFB | ✅ | vigente |
| [eSocial / DCTFWeb / PER-DCOMP Web](normas-tributarias/esocial-dctfweb-perdcomp.md) | RFB | ✅ | vigente |
| [Simples Nacional + NFS-e nacional 2026](normas-tributarias/simples-nacional-nfse-2026.md) | CGSN | ✅ | vigente |
| [DMED — Declaração de Serviços Médicos (IN RFB 2.074/2022)](normas-tributarias/dmed.md) | RFB | ✅ | vigente |
| [IRRF sobre serviços médicos (MAFON)](normas-tributarias/irrf-servicos-medicos.md) | RFB | ✅ | vigente |

### 🏛️ Sucessório e patrimonial (`normas-sucessorias-patrimoniais/`)

| Item | Órgão | Status | Vigência |
|---|---|---|---|
| [LC 227/2026 — ITCMD, CG-IBS e trusts](normas-sucessorias-patrimoniais/lc-227-2026-itcmd-trusts.md) | Congresso | ✅ | vigente |
| [EC 132/2023 — reforma tributária e novo ITCMD](normas-sucessorias-patrimoniais/ec-132-2023-reforma.md) | Congresso | ✅ | vigente |
| [Lei 13.874/2019 — Liberdade Econômica (art. 50 CC)](normas-sucessorias-patrimoniais/lei-13874-2019-liberdade-economica.md) | Congresso | ✅ | vigente |
| [Resolução CNJ 571/2024 — inventário extrajudicial](normas-sucessorias-patrimoniais/cnj-571-2024-inventario-extrajudicial.md) | CNJ | ✅ | vigente |
| [Provimento CNJ 149/2023 — e-Notariado](normas-sucessorias-patrimoniais/provimento-cnj-149-2023-enotariado.md) | CNJ | ✅ | vigente |
| [Resolução CNJ 35/2007 — atos notariais consensuais](normas-sucessorias-patrimoniais/cnj-35-2007-inventario.md) | CNJ | ✅ | parcial |

### 🩺 Regulatório setorial — CFM, ANPD, Anvisa, ANS (`normas-regulatorias-setoriais/`)

| Item | Órgão | Status | Vigência |
|---|---|---|---|
| [CFM 2.314/2022 — telemedicina](normas-regulatorias-setoriais/cfm-2314-2022-telemedicina.md) | CFM | ✅ | vigente |
| [CFM 2.336/2023 — publicidade médica](normas-regulatorias-setoriais/cfm-2336-2023-publicidade.md) | CFM | ✅ | vigente |
| [CFM 1.821/2007 + Lei 13.787/2018 — prontuário](normas-regulatorias-setoriais/cfm-1821-2007-prontuario.md) | CFM | ✅ | parcial |
| [LGPD (Lei 13.709/2018)](normas-regulatorias-setoriais/lgpd-lei-13709-2018.md) | Congresso | ✅ | vigente |
| [ANPD 4/2023 — dosimetria de sanções](normas-regulatorias-setoriais/anpd-res-4-2023-dosimetria.md) | ANPD | ✅ | vigente |
| [ANPD 15/2024 — incidentes (3 dias úteis)](normas-regulatorias-setoriais/anpd-res-15-2024-incidentes.md) | ANPD | ✅ | vigente |
| [ANPD 18/2024 — encarregado/DPO](normas-regulatorias-setoriais/anpd-res-18-2024.md) | ANPD | ✅ | vigente |
| [ANPD 2/2022 — agentes de pequeno porte](normas-regulatorias-setoriais/anpd-res-2-2022-pequeno-porte.md) | ANPD | ✅ | vigente |
| [Anvisa RDC 978/2025 — análises clínicas (vigente)](normas-regulatorias-setoriais/anvisa-rdc-978-2025-analises-clinicas.md) | Anvisa | ✅ | vigente |
| [Anvisa RDC 63/2011 + RDC 50/2002 — funcionamento e infraestrutura](normas-regulatorias-setoriais/anvisa-rdc-63-2011-rdc-50-2002.md) | Anvisa | ✅ | vigente |
| [Anvisa RDC 786/2023 — análises clínicas (histórico)](normas-regulatorias-setoriais/anvisa-rdc-786-2023-analises-clinicas.md) | Anvisa | ✅ | revogada |
| [Anvisa RDC 824/2023 — alteração da 786 (histórico)](normas-regulatorias-setoriais/anvisa-rdc-824-2023.md) | Anvisa | ✅ | revogada |
| [ANS — contrato escrito, TISS e glosa (RN 503/2022 e 489/2022)](normas-regulatorias-setoriais/ans-contrato-tiss-glosa.md) | ANS | ✅ | vigente |

---

## Clusters temáticos (para navegação e RAG)

- **Serviços hospitalares (núcleo do produto):** STJ Tema 217 · REsp 1.877.568 · Súmula CARF 142 · Parecer SEI 7689/2021 · LC 214/2025 · Anvisa RDC 978/2025.
- **Fiscalização / glosa / patrimônio do sócio:** Súmulas CARF 204 e 241 · CARF Acórdão 2401-002.873 · Lei 13.874/2019.
- **Compliance digital do médico PF:** Receita Saúde · Carnê-Leão/Livro Caixa · DMED · IRRF.
- **Sucessão e patrimônio internacional:** STF Tema 825 · LC 227/2026 · EC 132/2023 · Lei 14.754/2023 · CNJ 571/2024 · 35/2007 · Provimento 149/2023.
- **Governança da clínica:** CFM (telemedicina, publicidade, prontuário) · LGPD + ANPD · Anvisa · ANS.

---

## Manutenção

- **Base 100% confirmada em 02/06/2026.** Sem pendências de validação.
- **Reconferir a cada ~6 meses** as normas em transição (reforma tributária 2026: LC 214/2025, NFS-e nacional, ITCMD progressivo da LC 227/2026 dependente de leis estaduais).
- Ao adicionar item, copie `_template.md`, valide na fonte oficial, registre `status_validacao` + `data_validacao`, arquive o PDF-fonte em `_fontes/` quando houver, e atualize este índice.

## Fora de escopo (avaliar depois)
- Empacotar como skill/agente de produção (padrão Alice do Agro Inteligente).
- ISS municipal e alíquotas/procedimentos de ITCMD **estaduais** (variam por ente — exigem recorte local).
