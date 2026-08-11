from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.database.models import Base
from datetime import datetime
import uuid

class CadeiaVersao(Base):
    __tablename__ = "cadeia_versao"
    
    cadeia_versao_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    documento_id = Column(UUID(as_uuid=True), ForeignKey("xml_documento.documento_id"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=False)
    
    # Versionamento (R6)
    numero_versao = Column(Integer, nullable=False)
    hash_versao = Column(String(64), nullable=False, unique=True)
    
    # Dados da versão
    dados_versao = Column(JSONB)
    motivo_alteracao = Column(Text)
    
    # Rastreabilidade
    criado_por = Column(String(255))
    criado_em = Column(DateTime, default=datetime.utcnow)
    ativo = Column(Boolean, default=True)

class Outbox(Base):
    __tablename__ = "outbox"
    
    outbox_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=False)
    documento_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Evento para reprocessamento (R10)
    tipo_evento = Column(String(50), nullable=False)
    evento_id = Column(String(255), nullable=False)
    dados_evento = Column(JSONB, nullable=False)
    
    # Status
    processado = Column(Boolean, default=False)
    tentativas = Column(Integer, default=0)
    erro_ultimo = Column(Text, nullable=True)
    
    # Timestamps
    criado_em = Column(DateTime, default=datetime.utcnow)
    processado_em = Column(DateTime, nullable=True)
