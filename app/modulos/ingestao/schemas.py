from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class XmlIngestionResponse(BaseModel):
    ingestion_id: UUID
    tenant_id: UUID
    filename: str
    hash_sha256: str
    tamanho_bytes: int
    status: str
    criado_em: datetime
    
    class Config:
        from_attributes = True