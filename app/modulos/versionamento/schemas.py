from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class CadeiaVersaoResponse(BaseModel):
    cadeia_versao_id: UUID
    documento_id: UUID
    numero_versao: int
    hash_versao: str
    motivo_alteracao: str | None
    criado_em: datetime
    
    class Config:
        from_attributes = True

class OutboxResponse(BaseModel):
    outbox_id: UUID
    documento_id: UUID | None
    tipo_evento: str
    evento_id: str
    processado: bool
    tentativas: int
    criado_em: datetime
    
    class Config:
        from_attributes = True
