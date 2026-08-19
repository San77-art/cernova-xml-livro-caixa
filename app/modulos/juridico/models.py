# app/modulos/juridico/models.py
from sqlalchemy import Column, String, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import enum

from app.database.session import Base

class TipoNorma(str, enum.Enum):
    LGPD = "LGPD"
    CFM = "CFM"
    ANVISA = "ANVISA"
    CARF = "CARF"
    STJ = "STJ"
    STF = "STF"
    OUTROS = "OUTROS"

class Norma(Base):
    __tablename__ = "normas_juridicas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(String(255), nullable=False)
    tipo = Column(Enum(TipoNorma), nullable=False)
    numero = Column(String(50))  # Art. 5º, Resolução 123, etc
    descricao = Column(Text)
    conteudo = Column(Text)
    data_publicacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    link_oficial = Column(String(500))
    tags = Column(String(500))  # Comma-separated tags
    
    def __repr__(self):
        return f"<Norma {self.tipo} - {self.titulo}>"
