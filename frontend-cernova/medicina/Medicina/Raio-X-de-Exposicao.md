# Raio-X de Exposição — Degrau 0 (isca / lead magnet)

> Auto-diagnóstico gratuito que **faz o convencimento**: mostra ao médico/clínica os riscos que ele não via e gera o "preciso resolver isso". Capta lead qualificado e abre a venda do **Diagnóstico Essencial/Executivo** (degraus 1–2). Ver `Estrutura-de-produtos.md`.
>
> **Cada alerta é fundamentado numa ficha de `base-conhecimento/`** — é isso que dá credibilidade e diferencia de um quiz genérico.

## Princípios de design (best practices de lead magnet)
1. **Curto e sem atrito:** ~10–13 perguntas por pessoa (graças à ramificação por arquétipo). 3–5 minutos.
2. **Linguagem de decisão, não jurídica:** pergunta-se o sintoma, não o artigo de lei.
3. **Saída personalizada e tangível:** score de exposição (velocímetro) + 3–5 alertas com impacto traduzido.
4. **Cria urgência honesta:** mostra o risco real; não promete economia.
5. **CTA claro:** do alerta para o diagnóstico pago.
6. **Disclaimer:** é uma triagem preliminar automatizada, **não é parecer**; a confirmação vem no diagnóstico.

---

## Fluxo
```
[Bloco A: Identificação + Segmentação]  → define arquétipo
        │
        ├─ Médico liberal            → Blocos: TRIB-PF, PATRIM, GOV-min
        ├─ Clínica em crescimento    → Blocos: TRIB-PJ, PATRIM, GOV, REFORMA
        ├─ Clínica de convênio       → Blocos: TRIB-PJ, CONV, GOV, REFORMA
        └─ Grupo/família multi-CNPJ  → Blocos: TRIB-PJ, PATRIM, SUCESS, GOV
        │
[Cálculo do Score de Exposição]  → faixa Verde/Amarelo/Vermelho
        │
[Mini-relatório + CTA]
```

---

## Bloco A — Identificação e segmentação (todos respondem)

| # | Pergunta | Opções | Uso |
|---|---|---|---|
| A1 | Como você atua hoje? | (a) Só pessoa física · (b) Tenho 1 PJ/clínica · (c) Tenho 2+ CNPJs / grupo · (d) Clínica com sócios | Roteia arquétipo |
| A2 | De onde vem a maior parte da sua receita? | (a) Particular/reembolso · (b) Convênios/planos · (c) Hospital/PJ contratante · (d) Misto | Roteia (convênio→bloco CONV) |
| A3 | Faixa de faturamento anual | <R$360k · R$360k–1M · R$1–4,8M · >R$4,8M | Porte/ticket; regime |
| A4 | Regime tributário atual | PF (carnê-leão) · Simples · Lucro Presumido · Lucro Real · Não sei | Dispara trilhas fiscais |

**Regra de arquétipo:** A1=a → *Médico liberal*; A1=b + A2≠b → *Clínica em crescimento*; A2=b → *Clínica de convênio*; A1=c/d → *Grupo/família*.

---

## Banco de perguntas por bloco
Cada pergunta tem **flag de risco** (severidade) e a **ficha-fundamento** (id em `base-conhecimento/`). A flag dispara quando a resposta indica exposição.

### TRIB-PF — Médico pessoa física
| Pergunta | Resposta que dispara flag | Sev. | Fundamento |
|---|---|---|---|
| Você emite **recibo eletrônico (Receita Saúde)** de todos os atendimentos? | "Não/parcialmente/não sei" | Alto | `receita-saude` |
| Você usa **Carnê-Leão e Livro Caixa** para deduzir despesas e apurar o IR mensal? | "Não/não sei" | Médio | `livro-caixa-carne-leao` |
| Recebe por **plano de saúde** como PF e sabe quem recolhe a contribuição previdenciária? | "Não sei / acho que a operadora" | Médio | `irrf-servicos-medicos` |
| Já recebeu **carta da malha, intimação ou aviso** da Receita? | "Sim" | Alto | `carf-sumula-241-irrf-glosa` |

### TRIB-PJ — Clínica / grupo
| Pergunta | Dispara flag | Sev. | Fundamento |
|---|---|---|---|
| Sua clínica usa (ou quer usar) a tributação reduzida de **"serviços hospitalares"**? | "Sim" **e** não é sociedade empresária / sem prova Anvisa | Alto | `stj-tema-217-servicos-hospitalares`, `carf-sumula-142-servicos-hospitalares`, `parecer-sei-7689-2021-servicos-hospitalares` |
| Vocês separam receita de **consulta simples** das demais? | "Não/não sei" | Médio | `stj-resp-1877568-anestesiologia` |
| A clínica está **registrada/licenciada na Anvisa/vigilância** e em dia? | "Não/não sei" | Médio | `anvisa-rdc-63-2011-rdc-50-2002` |
| Se faz **análises clínicas/laboratório**, conhece a norma vigente (RDC 978/2025)? | "Não" | Baixo | `anvisa-rdc-978-2025-analises-clinicas` |

### PATRIM — Patrimonial / societário
| Pergunta | Dispara flag | Sev. | Fundamento |
|---|---|---|---|
| O **pró-labore** e a **distribuição de lucros** seguem exatamente o contrato social? | "Não/não sei" | Alto | `carf-acordao-2401-002873-prolabore` |
| A empresa paga alguma **despesa pessoal do sócio** (cartão, carro, condomínio, casa)? | "Sim/às vezes" | Alto | `carf-acordao-2401-002873-prolabore`, `lei-13874-2019-liberdade-economica` |
| O **imóvel** da clínica está no **mesmo CNPJ** da operação? | "Sim/não sei" | Médio | `lei-13874-2019-liberdade-economica` |
| Existe **cessão de imóvel/bem** da empresa a sócio sem contrato a valor de mercado? | "Sim" | Alto | `carf-acordao-2401-002873-prolabore` |

### SUCESS — Sucessório (grupo/família)
| Pergunta | Dispara flag | Sev. | Fundamento |
|---|---|---|---|
| Existe **plano de sucessão** (quem comanda/vota/recebe se o sócio-chave faltar)? | "Não" | Alto | `lc-227-2026-itcmd-trusts` |
| Já estimaram o **ITCMD** e de onde sairia a liquidez para pagá-lo? | "Não" | Médio | `lc-227-2026-itcmd-trusts`, `ec-132-2023-reforma` |
| Têm **offshore/trust** no exterior montado antes de 2024? | "Sim" | Alto | `lei-14754-2023-offshores-trusts`, `lc-227-2026-itcmd-trusts` |
| Já pensaram em **holding / inventário extrajudicial**? | "Não/não sei" | Baixo | `cnj-571-2024-inventario-extrajudicial` |

### CONV — Convênio
| Pergunta | Dispara flag | Sev. | Fundamento |
|---|---|---|---|
| Há **contrato escrito** com todas as operadoras com quem trabalham? | "Não/parcial" | Alto | `ans-contrato-tiss-glosa` |
| Têm trilha formal de **recurso de glosa** (TISS)? | "Não/não sei" | Médio | `ans-contrato-tiss-glosa` |

### GOV — Governança / dados (versão -min para médico liberal: só as 2 primeiras)
| Pergunta | Dispara flag | Sev. | Fundamento |
|---|---|---|---|
| Vocês tratam **dados de pacientes** com base legal, controle de acesso e plano de incidente? | "Não/não sei" | Alto | `lgpd-lei-13709-2018`, `anpd-res-15-2024-incidentes` |
| Sabem que incidente relevante deve ser comunicado à ANPD em **3 dias úteis**? | "Não" | Médio | `anpd-res-15-2024-incidentes` |
| Atendem por **telemedicina** com registro em prontuário? | "Sim, sem registro formal" | Médio | `cfm-2314-2022-telemedicina` |
| A **publicidade/redes sociais** seguem a Resolução CFM 2.336/2023 (CRM/RQE, preços)? | "Não/não sei" | Médio | `cfm-2336-2023-publicidade` |

### REFORMA — Transição 2026 (clínicas)
| Pergunta | Dispara flag | Sev. | Fundamento |
|---|---|---|---|
| Se é do **Simples**, já está pronto para a **NFS-e nacional** (obrigatória set/2026)? | "Não/não sei" | Alto | `simples-nacional-nfse-2026` |
| Seu sistema já emite documento com destaque de **CBS/IBS** (desde jan/2026)? | "Não/não sei" | Médio | `lc-214-2025-ibs-cbs` |

---

## Score de Exposição
- Cada flag pontua pela severidade: **Alto = 3 · Médio = 2 · Baixo = 1**.
- **Score = soma das flags disparadas.** (Normalizar por nº de perguntas do trajeto para comparar arquétipos.)

| Faixa | Velocímetro | Leitura |
|---|---|---|
| 0–4 pts | 🟢 Verde | Exposição baixa — alguns ajustes pontuais |
| 5–10 pts | 🟡 Amarelo | Exposição relevante — há buracos que custam caro |
| 11+ pts | 🔴 Vermelho | Exposição alta — risco concreto de autuação/perda patrimonial |

> Qualquer flag **Alto** isolada (ex.: paga despesa pessoal do sócio; usa "serviço hospitalar" sem requisitos) já puxa a leitura para pelo menos 🟡 e vira destaque no relatório.

---

## Mini-relatório de saída (o que o médico recebe)
1. **Velocímetro + faixa** (🟢🟡🔴) com 1 frase de leitura.
2. **Seus 3–5 maiores alertas**, cada um com:
   - título em linguagem de decisão ("A clínica pode estar pagando imposto sobre 'serviço hospitalar' sem cumprir os requisitos");
   - **impacto** ("risco de glosa do benefício + autuação retroativa");
   - **fundamento** ("base: STJ Tema 217 + Súmula CARF 142") — *sem* citar o número da ficha interna ao cliente, mas usando o lastro.
3. **O que NÃO está sinalizado** (1 linha honesta: "isto é uma triagem; só o diagnóstico confirma").
4. **CTA:** "Quer saber o tamanho real e como blindar? O **Diagnóstico [Essencial/Executivo]** quantifica cada alerta e entrega o plano." → agenda/contato.
5. **Captura:** nome, e-mail, WhatsApp, especialidade, cidade (lead).

---

## Notas de implementação
- **Vira agente** no padrão Alice P01: o Bloco A roteia, os blocos condicionais rodam, o score gera o velocímetro, o relatório usa as fichas como fonte. A `base-conhecimento/` já é o "cérebro".
- **Disclaimer fixo:** "Triagem preliminar automatizada com base em normas e jurisprudência vigentes (validadas em 06/2026). Não constitui parecer jurídico-contábil; a confirmação ocorre no diagnóstico."
- **Atualização:** quando uma ficha muda (lei nova), o alerta correspondente é ajustado — o Raio-X acompanha a base.
- **Métrica de sucesso do degrau 0:** taxa de conclusão do quiz · % que vira lead · % de lead que agenda diagnóstico.

## Decisões em aberto (suas)
- [ ] Canal do Raio-X: página web/quiz, WhatsApp, ou agente conversacional?
- [ ] Grátis 100% ou simbólico (filtra curioso)?
- [ ] Captura de lead **antes** de ver o resultado (mais leads, mais atrito) ou **depois** (menos leads, mais qualificados)?
