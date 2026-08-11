from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class LivroCaixaResponse(BaseModel):
    livro_caixa_id: UUID
    documento_id: UUID
    tenant_id: UUID
    tipo_movimento: str | None
    data_movimento: datetime | None
    valor: str | None
    descricao: str | None
    status: str
    criado_em: datetime
    
    class Config:
        from_attributes = True

class PreContabilizacaoResponse(BaseModel):
    pre_contabilizacao_id: UUID
    documento_id: UUID
    tenant_id: UUID
    conta_debito: str | None
    conta_credito: str | None
    valor: str | None
    descricao: str | None
    status: str
    criado_em: datetime
    
    class Config:
        from_attributes = True