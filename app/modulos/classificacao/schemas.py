from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ClassificacaoCandidataResponse(BaseModel):
    classificacao_id: UUID
    documento_id: UUID
    ingestion_id: UUID
    tenant_id: UUID
    versao: int
    classificacao_version: str
    tipo_documento: str | None
    natureza_operacao: str | None
    cfop: str | None
    ncm: str | None
    status_classificacao: str
    confianca: str | None
    regra_aplicada: str | None
    criado_em: datetime
    
    class Config:
        from_attributes = True