# Estrutura de Produtos — Diagnóstico Jurídico-Fiscal para Médicos & Clínicas (Junior)

> Documento de arquitetura comercial. Base: `ICP-medicos.md`, `Pesquisa analítica do ICP de médicos e clínicas.md` e a base de conhecimento validada em `base-conhecimento/`.

## Decisões que orientam este desenho
- **Escopo da Junior:** **só diagnóstico** (mapeamento, cenários, recomendação). A **execução** (reorganização societária, dossiê de defesa, implementação) é **encaminhada a parceiros** — a Junior não executa.
- **Motor de receita:** **recorrente** (assinatura de governança/monitoramento).
- **Segmentação:** por **estrutura/arquétipo** do negócio, não por especialidade médica.

### Como "só diagnóstico" + "recorrente" se encaixam (a chave do modelo)
A Junior não vende execução, mas vende **diagnóstico contínuo**: *"eu vigio sua exposição e a lei que muda."* O produto recorrente é diagnóstico vivo — não execução. É isso que transforma a [base de conhecimento validada](base-conhecimento/README.md) em **produto vivo** (a lei muda o tempo todo; a base é atualizada; o cliente paga para estar sempre coberto).

---

## Por que escada de valor (e não 1 produto fixo)
O mercado é majoritariamente **inconsciente do problema** — o médico não sabe que está exposto. Vender um diagnóstico caro direto para quem não sabe que tem a dor é nadar contra a corrente. A solução de mercado é uma **escada de valor**: degraus do baixo atrito (que *faz o convencimento por você*) ao alto valor. É o mesmo modelo que já funciona no **Agro Inteligente** (Alice P01 grátis → P02 pago → ...). Aqui, adaptado para "só diagnóstico + recorrente".

---

## A escada de valor

| Degrau | Produto | Formato | Preço (hipótese¹) | Função no funil |
|---|---|---|---|---|
| **0 — Isca** | **Raio-X de Exposição** | Auto-diagnóstico guiado (10–15 perguntas) → mini-relatório de alertas | Grátis / simbólico | **Faz o convencimento.** Mostra os buracos que o médico não via. Gera o "preciso resolver isso". Capta lead qualificado. |
| **1 — Entrada** | **Diagnóstico Essencial** | Productized, escopo fixo, ~1–2 semanas | Fixo baixo — **R$ 2–5k** | Tripwire. Prova método, entrega valor real, revela problemas maiores. Para médico liberal/consultório. |
| **2 — Core** | **Diagnóstico Executivo** | Productized, escopo fixo, ~3–4 semanas | Fixo-âncora — **R$ 8–20k** | Carro-chefe. Matriz de risco + cenários + roadmap + plano de encaminhamento. Para clínica/multi-CNPJ/família. |
| **3 — Ponte** | **Plano de Implementação + Encaminhamento** | Entregue *dentro* do diagnóstico + curadoria de parceiros | Incluso no degrau 2 (+ fee de indicação opcional) | A Junior não executa; entrega o roadmap e conecta a advogado/contador/societário parceiro. Mantém a Junior como "maestro" sem assumir execução. |
| **4 — Motor** | **Assinatura de Governança** | Recorrente | Mensal/anual — **R$ 1–5k/mês** (por porte) | **A receita previsível.** Monitora exposição e mudanças de lei; mantém o dossiê e os cenários vivos. Retém o cliente. |

¹ **Preços são hipóteses a validar** — não temos benchmark proprietário nem custo-base aqui, e a própria pesquisa marcou confiança "média/baixa" em pricing. Ancorar em **risco evitado** (autuação de serviço hospitalar mal defendido = 6–7 dígitos), não em horas.

---

## O degrau 4 em detalhe (precisa justificar a assinatura)
Como a Junior para no diagnóstico, o recorrente **não pode ser "executamos pra você"** — tem que ser vigilância de alto valor. O que entra:

- **Monitoramento jurídico-regulatório** filtrado para a estrutura do cliente (novas súmulas CARF, marcos da reforma 2026, ITCMD estadual, mudanças CFM/ANPD/Anvisa/ANS). Alimentado pela base de conhecimento.
- **Alerta dirigido:** quando algo muda e afeta *aquele* cliente, ele é avisado com o impacto traduzido.
- **Re-diagnóstico periódico** (trimestral/semestral): a exposição é reavaliada — nada fica desatualizado.
- **Dossiê vivo:** a documentação de defesa é mantida atualizada (ex.: tese de serviço hospitalar).
- **Acesso consultivo** (office hours / canal de dúvida).

Isso é defensável, recorrente e usa a base como ativo — coisa que "contabilidade online" não tem.

---

## Segmentação por estrutura (4 arquétipos) × produtos
A mensagem e a lente do diagnóstico mudam por arquétipo, mas o **esqueleto do produto é o mesmo** (escala melhor).

| Arquétipo | Dor dominante | Degrau de entrada típico | Gancho do recorrente |
|---|---|---|---|
| **Médico liberal de alta renda** (particular/reembolso) | Mistura PF/PJ, retirada desorganizada, medo de malha, Receita Saúde | Essencial (1) | Acompanhar cruzamento eletrônico e teses de PF |
| **Clínica em crescimento** | Cresce sem backoffice; emissão/NFS-e, LGPD, precificação | Essencial→Executivo (1–2) | Conformidade contínua na transição 2026 (CBS/IBS, NFS-e) |
| **Clínica dependente de convênio** | Margem, glosa, contrato, indicadores | Executivo (2) | Vigilância contratual/regulatória (ANS) — *execução de glosa fica fora; é software/parceiro* |
| **Grupo/família multi-CNPJ** | Estrutura opaca, patrimônio misturado, sucessão sem desenho | Executivo (2) | Governança patrimonial-sucessória viva (ITCMD, holding, confusão patrimonial) |

> **Nota crítica de escopo:** glosa/TISS e KPIs operacionais (no-show, ocupação de agenda) **não são competência da Junior** — são de software (Feegow/iClinic). No arquétipo de convênio, vender *vigilância jurídico-contratual*, não *gestão de glosa*. Não prometa o que não entrega.

---

## O moat (por que conseguem cobrar premium)
A [base de conhecimento validada](base-conhecimento/README.md) (36 fichas, 100% confirmadas em fonte oficial) é o ativo proprietário que:
- dá **credibilidade jurisprudencial real** (resolve o ponto fraco que a própria pesquisa apontava: "confiança média/baixa em tese jurisprudencial");
- alimenta o **Raio-X (degrau 0)** e o **recorrente (degrau 4)**;
- diferencia da contabilidade generalista e do software.

---

## Funil
```
Raio-X grátis (convence)  →  Diagnóstico Essencial/Executivo (one-shot)  →  Assinatura de Governança (recorrente)
        ▲ lead                         ▲ caixa + qualifica                          ▲ retém + previsível
                                        └─ Plano + encaminhamento a parceiro (Junior = maestro, não executor)
```

---

## Riscos e o que validar antes de lançar (sendo crítico)
1. **Pricing é chute fundamentado** — validar com 5–10 entrevistas/ofertas reais antes de fixar tabela.
2. **Dados de mercado da pesquisa não validados** (52,9 mi beneficiários etc.) — conferir na ANS/Receita antes de usar em material de venda.
3. **Risco do recorrente:** assinatura sem entregável tangível mensal cancela rápido. O degrau 4 precisa de **cadência visível** (alerta/relatório periódico), senão vira "seguro que ninguém sente".
4. **Encaminhamento sem governança vira perda de cliente** — definir a rede de parceiros e o padrão de handoff (e se há fee de indicação).
5. **Não inflar escopo** para operacional/clínico — fica fora.

## Próximos passos sugeridos
- [ ] Validar faixas de preço e a tese do recorrente com alguns clientes-alvo.
- [ ] Detalhar o **Raio-X (degrau 0)** — é o que destrava o funil; pode virar o próximo agente (estilo Alice P01).
- [ ] Definir entregáveis e SLA de cada degrau (escopo fixo de productized service).
- [ ] Desenhar a cadência do recorrente (o que o cliente recebe a cada mês/trimestre).
