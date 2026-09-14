# Especificação do Agente — Raio-X de Exposição (degrau 0, gratuito)

> Documento-guia para construir o agente. Consolida o processo ideal em requisitos acionáveis.
> **Insumos:** roteiro em [`Raio-X-de-Exposicao.md`](Raio-X-de-Exposicao.md) · cérebro em [`base-conhecimento/`](base-conhecimento/README.md) · contexto comercial em [`Estrutura-de-produtos.md`](Estrutura-de-produtos.md) · perfil em [`ICP-medicos.md`](ICP-medicos.md).
> **Tecnologia:** Claude Developer Platform (platform.claude.com) via API, Sonnet 4.6+ (ver §11). Persona/UX inspiradas nas Alice (Agro Inteligente), mas **sem AIRIA**.

---

## 1. Objetivo e definição de sucesso
**Objetivo:** triagem gratuita que revela a exposição jurídico-fiscal do médico/clínica, gera o "preciso resolver isso" e captura lead qualificado para o diagnóstico pago (degraus 1–2).

**Sucesso = 6 critérios simultâneos:**
1. **Não alucina** — só afirma o que está na base validada.
2. **Roteia certo** — identifica o arquétipo e faz só o que importa.
3. **Conversa bem** — tom de decisão; lida com "não sei" e ambiguidade.
4. **Entrega valor** — relatório personalizado e honesto.
5. **Captura e encaminha** — lead com contexto + handoff.
6. **É responsável** — disclaimer, não promete economia, é LGPD-compliant.

**Métricas (definir metas após baseline):** taxa de conclusão do quiz · % conclusão→lead · % lead→agendamento · % agendamento→venda · tempo médio de sessão · taxa de abandono por etapa.

---

## 2. Arquitetura
```
 Aquisição → [Motor de Conversa] → [Motor de Score] → [Gerador de Relatório] → [Captura/CRM] → [Handoff]
                     │                                          │
                     └────────── CÉREBRO: base-conhecimento/ ───┘  (grounding / fonte de verdade)
```
| Componente | Responsabilidade | Fonte/insumo |
|---|---|---|
| Cérebro | Fonte de verdade; impede alucinação | `base-conhecimento/` (36 fichas validadas) |
| Motor de conversa | Persona + roteiro + ramificação | `Raio-X-de-Exposicao.md` (Bloco A + blocos) |
| Motor de score | Severidade → velocímetro | regra de pontuação (§6) |
| Gerador de relatório | Saída personalizada | template (§7) |
| Captura/CRM | Lead + respostas | integração a definir (§11) |
| Handoff | Roteia lead quente p/ comercial | regra por faixa (§8) |

---

## 3. Persona do agente
- **Nome:** **Alice**.
- **Papel:** especialista em **estruturação fiscal, patrimonial e de governança** para médicos e clínicas. **Alice NÃO é médica** (não dá orientação clínica) **nem advogada** (não faz parecer/defesa jurídica) — ela faz a triagem e aponta exposição; a parte jurídica fica com parceiros (degrau 3).
- **Tom:** consultivo, direto, linguagem de decisão (sem juridiquês), acolhedor com quem responde "não sei".
- **Limite:** triagem, **não** parecer; nunca dá a recomendação final nem promete economia.

---

## 4. Jornada end-to-end (estados do agente)
1. **Boas-vindas + consentimento LGPD** (antes de qualquer pergunta).
2. **Triagem (Bloco A)** → define arquétipo, regime, porte.
3. **Diagnóstico conversacional** → blocos condicionais por arquétipo; cada resposta acende/não uma flag.
4. **Cálculo do score** (silencioso).
5. **Entrega do relatório** (na hora).
6. **Captura do lead.**
7. **Nutrição/follow-up** (sequência curta).
8. **Handoff** (por faixa do velocímetro).
9. **Loop de melhoria** (dados → ajustes).

**Roteamento de arquétipo (do Bloco A):** A1=a → *Médico liberal*; A1=b e A2≠convênio → *Clínica em crescimento*; A2=convênio → *Clínica de convênio*; A1=c/d → *Grupo/família*. Blocos por arquétipo conforme `Raio-X-de-Exposicao.md`.

---

## 5. Roteiro de perguntas
Fonte única: **[`Raio-X-de-Exposicao.md`](Raio-X-de-Exposicao.md)** (Bloco A + blocos TRIB-PF, TRIB-PJ, PATRIM, SUCESS, CONV, GOV, REFORMA). Cada pergunta tem **flag**, **severidade** e **ficha-fundamento**. Manter ~10–13 perguntas por trajeto. *Não duplicar o roteiro aqui — alterações vão no arquivo-fonte.*

---

## 6. Motor de score
- Flag disparada pontua: **Alto = 3 · Médio = 2 · Baixo = 1**. Score = soma.

| Faixa | Velocímetro | Leitura |
|---|---|---|
| 0–4 | 🟢 Verde | Exposição baixa |
| 5–10 | 🟡 Amarelo | Exposição relevante |
| 11+ | 🔴 Vermelho | Exposição alta |

- **Override:** qualquer flag **Alto** isolada puxa a leitura para ≥ 🟡 e vira destaque.

---

## 7. Gerador de relatório (template de saída)
1. **Velocímetro + faixa** + 1 frase de leitura.
2. **3–5 maiores alertas**, cada um com: título em linguagem de decisão · impacto traduzido · fundamento ("base: STJ Tema 217 + Súmula CARF 142" — sem expor o id interno).
3. **O que NÃO foi avaliado** (1 linha honesta).
4. **CTA** para o Diagnóstico Essencial/Executivo.
5. **Disclaimer** (§9).
> O relatório usa o teor das fichas; **nunca** cita número/artigo que não esteja na base.

---

## 8. Handoff comercial
- 🔴 **Vermelho** → lead quente, comercial contata em 24h com resumo dos alertas.
- 🟡 **Amarelo** → lead morno, follow-up + oferta de conversa.
- 🟢 **Verde** → nutrição (conteúdo educativo), sem pressão.
- Todo handoff carrega: arquétipo, regime, porte, alertas disparados, contato.

---

## 9. Guardrails (regras do system prompt)
- **Grounding estrito:** se não está na base, responde *"isso a gente confirma no diagnóstico"*. Nunca improvisa lei/número/prazo.
- **Triagem, não parecer:** não dá recomendação definitiva nem indica estrutura específica.
- **Nunca promete economia** — fala em exposição/risco.
- **Tom:** decisão, frases curtas, sem juridiquês.
- **"Não sei" = sinal de risco** (falta de visibilidade já é exposição), sem constranger.
- **Privacidade:** coleta o mínimo; **não pede dado clínico de paciente** — só estrutura do negócio.
- **Honestidade na saída:** mostra o que não avaliou.
- **Encerramento elegante:** se a pessoa desiste, agradece e captura lead parcial.
- **Sem aconselhamento fora de escopo** (operacional/clínico/glosa): remete a parceiro.

---

## 10. LGPD e consentimento (o agente precisa ser o que ele cobra)
- Aviso de privacidade + consentimento **antes** da 1ª pergunta.
- Base legal e finalidade explícitas (triagem + contato comercial).
- Coleta mínima; sem dado sensível de paciente.
- Canal para o titular exercer direitos; retenção definida.
- Plano de incidente (coerente com `anpd-res-15-2024-incidentes` — 3 dias úteis).

---

## 11. Decisões de plataforma ✅ (decididas)
- [x] **Tecnologia:** **Claude Developer Platform** (platform.claude.com) via **API**, modelo **Sonnet 4.6 ou superior** quando disponível. **Não usar AIRIA.**
- [x] **Canal primário:** **página web / landing** com o agente embarcado. WhatsApp fica para fase 2 (distribuição).
- [x] **Formato:** **guiado com tom conversacional** — perguntas fechadas (previsíveis e testáveis) com a persona da "Alice médica" na superfície.
- [x] **Captura do lead:** **depois, com gate de relatório** — responde → vê o velocímetro (teaser) → informa contato para destravar os alertas detalhados.
- [x] **Preço:** **gratuito 100%** (degrau 0 é isca; preço só a partir do degrau 1).
- [x] **Destino dos leads:** **simples** — planilha (ex.: Google Sheets) e/ou e-mail ao comercial. Migrar para CRM quando escalar.

### Implicações técnicas dessa escolha
- **Stack:** frontend web (landing + UI do quiz) → backend chamando a **API da Anthropic** (Sonnet 4.6+).
- **Base como contexto:** carregar `base-conhecimento/` no contexto do sistema e usar **prompt caching** (a base é grande e estática → cache reduz custo/latência a cada turno). Ver skill `claude-api`.
- **Roteiro como estado controlado:** a ramificação (Bloco A → blocos) e o score vivem na **lógica da aplicação**, não na "boa vontade" do modelo — o modelo cuida do tom e da redação dos alertas a partir das fichas. Isso garante previsibilidade e testabilidade.
- **Captura de lead:** formulário do gate (frontend) grava na planilha/e-mail; não precisa ser uma *tool* do modelo.
- **Geração do relatório:** o modelo redige os alertas ancorado nas fichas disparadas; a aplicação injeta apenas as fichas relevantes ao trajeto (menos contexto, menos risco).

---

## 12. Plano de testes (antes do ar) — eval via API
> Método dos avatares + gabarito (inspirado no `testar-agro-inteligente`), mas executado como **harness de avaliação chamando a API** (não AIRIA). Ver skills `claude-api` e `skill-creator` (evals).
1. **Avatares de teste** (1 por arquétipo): Dr. liberal alta renda · clínica em crescimento · clínica de convênio · família multi-CNPJ — com respostas roteirizadas.
2. **Gabarito por avatar:** alertas que DEVEM disparar + faixa correta do velocímetro.
3. **Bateria:**
   - **Roteamento** — cada avatar cai no trajeto certo.
   - **Score** — faixa bate com o gabarito.
   - **Anti-alucinação** — armadilhas ("qual o artigo exato?", "quanto economizo?") → resiste.
   - **Tom/objeções** — "já tenho contador", "medo de mexer" → responde no script.
   - **Borda** — "não sei" em tudo; abandono no meio.
4. **Regressão:** rodar a bateria a cada mudança de roteiro/base, comparando com gabarito.

---

## 13. Operação e manutenção
- **Sincronia com a base:** ficha muda (lei nova) → alerta correspondente é ajustado. A base é o cérebro.
- **Métricas vivas** (§1) revisadas periodicamente.
- **Feedback do comercial** vira ajuste de pergunta/alerta.
- **Reteste de regressão** após cada atualização.

---

## 14. Definição de "pronto para o ar" (launch checklist)
- [ ] Roteiro final revisado e ramificação testada.
- [ ] Todos os alertas com ficha-fundamento existente na base.
- [ ] Guardrails no system prompt + teste anti-alucinação aprovado.
- [ ] Consentimento LGPD implementado.
- [ ] Score e velocímetro batendo com o gabarito dos 4 avatares.
- [ ] Template de relatório aprovado (tom + honestidade + CTA).
- [ ] Captura de lead + handoff funcionando ponta a ponta.
- [ ] Métricas instrumentadas.
- [ ] Decisões de plataforma (§11) fechadas.
