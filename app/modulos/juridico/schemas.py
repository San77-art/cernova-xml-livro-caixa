# app/modulos/juridico/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class TipoNormaSchema(str, Enum):
    LGPD = "LGPD"
    CFM = "CFM"
    ANVISA = "ANVISA"
    CARF = "CARF"
    STJ = "STJ"
    STF = "STF"
    OUTROS = "OUTROS"

class NormaCreate(BaseModel):
    titulo: str
    tipo: TipoNormaSchema
    numero: Optional[str] = None
    descricao: Optional[str] = None
    conteudo: Optional[str] = None
    link_oficial: Optional[str] = None
    tags: Optional[str] = None

class NormaResponse(NormaCreate):
    id: str
    data_publicacao: datetime
    data_atualizacao: datetime
    
    class Config:
        from_attributes = True
