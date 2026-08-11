# Cernova XML + Livro Caixa RBV1

Backoffice web interno multiempresa para processamento de NF-e.

## Fases Implementadas

- Fase 1: Setup + Database (PostgreSQL 18.3)
- Fase 2: Ingestao XML (hash SHA-256)
- Fase 3: Parser XML (determinístico)
- Fase 4: Classificação Candidata
- Fase 5: Livro Caixa + Pre-contabilização
- Fase 6: Versionamento + Idempotência + Outbox
- Fase 7: Deploy AWS + Testes

## Stack

- FastAPI 0.141.1
- PostgreSQL 18.3
- Python 3.12
- AWS (RDS + ECS)
- Terraform

## Endpoints

GET  /health
POST /parse/xml
POST /classificacao/candidata
POST /livro-caixa
POST /pre-contabilizacao
POST /versionamento/criar-versao
POST /outbox/reprocessar

## Compliance

- ADR-001 completo
- LGPD ready
- RLS multiempresa
- Zero LLM
