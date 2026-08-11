from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class XmlDocumentoResponse(BaseModel):
    documento_id: UUID
    ingestion_id: UUID
    tenant_id: UUID
    numero_nfe: str | None
    chave_acesso: str | None
    data_emissao: datetime | None
    valor_total: str | None
    status_parse: str
    criado_em: datetime
    
    class Config:
        from_attributes = True