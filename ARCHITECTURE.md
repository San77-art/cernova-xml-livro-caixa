# ARQUITETURA TÉCNICA - CERNOVA RBV1

## Diagrama da Solução

\\\
┌─────────────────────────────────────────────────────────────┐
│                     CAMADA APRESENTAÇÃO                      │
│  Frontend (React/Vue) - Dashboard + Upload de NF-e          │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│                    CAMADA API (FastAPI)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ GET  /health                                         │   │
│  │ POST /ingestao/xml                                   │   │
│  │ POST /parse/xml                                      │   │
│  │ POST /classificacao/candidata                        │   │
│  │ POST /livro-caixa                                    │   │
│  │ POST /pre-contabilizacao                             │   │
│  │ POST /versionamento/criar-versao                     │   │
│  │ POST /outbox/reprocessar                             │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│                 CAMADA LÓGICA (Módulos)                      │
│  ┌────────────┬────────────┬────────────┬─────────────┐    │
│  │ Ingestão   │ Parser     │Classificação│ Livro Caixa│    │
│  ├────────────┼────────────┼────────────┼─────────────┤    │
│  │ Hash SHA256│ XML Extract│ Regras Det.│ Movimentos  │    │
│  │ Imutável   │ SEM LLM    │ Status:    │ Contas      │    │
│  │            │            │ Candidata  │             │    │
│  └────────────┴────────────┴────────────┴─────────────┘    │
│  ┌────────────┬─────────────────────────┐                  │
│  │Versionamento│ Outbox + Idempotência  │                  │
│  ├────────────┼─────────────────────────┤                  │
│  │Cadeias     │ Reprocessamento        │                  │
│  │Auditoria   │ Garantia Entrega       │                  │
│  └────────────┴─────────────────────────┘                  │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│              CAMADA DADOS (PostgreSQL 18.3)                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Tabelas:                                             │   │
│  │ • tenants              (multiempresa)                │   │
│  │ • usuarios             (RLS: tenant_id)              │   │
│  │ • xml_ingestao         (XML bruto + hash)            │   │
│  │ • xml_documento        (Parsed data)                 │   │
│  │ • classificacao_candidata (Nunca definitiva)        │   │
│  │ • livro_caixa          (Movimentos)                  │   │
│  │ • pre_contabilizacao   (Lançamentos)                 │   │
│  │ • cadeia_versao        (Auditoria)                   │   │
│  │ • outbox               (Idempotência)                │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│                    CAMADA CLOUD (AWS)                        │
│  ┌──────────────┬──────────────┬──────────────┐             │
│  │ RDS          │ ECS          │ CloudWatch   │             │
│  │ PostgreSQL   │ FastAPI      │ Logs + Monitoring
│  └──────────────┴──────────────┴──────────────┘             │
└─────────────────────────────────────────────────────────────┘
\\\

---

## Fluxo de Dados

### 1. Upload NF-e
\\\
Usuario → POST /ingestao/xml → FastAPI
  ↓
XML armazenado BRUTO (imutável)
  ↓
SHA-256 calculado
  ↓
Salvo em xml_ingestao
\\\

### 2. Parse
\\\
POST /parse/xml → FastAPI
  ↓
Extração XML DETERMINÍSTICA (SEM IA)
  ↓
Dados salvos em xml_documento
  ↓
status_parse = 'processado'
\\\

### 3. Classificação
\\\
POST /classificacao/candidata → FastAPI
  ↓
Regras DETERMINÍSTICAS aplicadas
  ↓
Classificação CANDIDATA criada
  ↓
status_classificacao = 'candidata' (NUNCA definitiva!)
\\\

### 4. Livro Caixa
\\\
POST /livro-caixa → FastAPI
  ↓
Movimento contábil criado
  ↓
Registrado em livro_caixa
\\\

### 5. Versionamento
\\\
POST /versionamento/criar-versao → FastAPI
  ↓
Hash SHA-256 da cadeia
  ↓
Versão armazenada (v1, v2, v3...)
  ↓
Auditoria completa
\\\

### 6. Idempotência
\\\
Qualquer erro → Evento registrado em Outbox
  ↓
Reprocessamento automático (POST /outbox/reprocessar)
  ↓
Garantia de entrega (exatamente uma vez)
\\\

---

## Segurança

### RLS Dupla
\\\
Nível 1: Tenant isolamento
  └─ Tenant A só vê seus dados

Nível 2: Usuário isolamento  
  └─ Usuário só vê seu tenant
\\\

### LGPD
- ✅ Dados pessoais criptografados
- ✅ Auditoria append-only
- ✅ Direito ao esquecimento implementado
- ✅ Consentimento registrado

### Compliance
- ✅ ADR-001: 100%
- ✅ Sigilo fiscal: Garantido
- ✅ Auditoria: Ativada

---

## Escalabilidade

### Horizontal
- Múltiplas instâncias FastAPI
- Load balancer AWS
- RDS replicado

### Vertical
- Database indexação
- Caching automático
- Connection pooling

---

