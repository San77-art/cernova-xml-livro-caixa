from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database.models import Base
from datetime import datetime
import uuid

class LivroCaixa(Base):
    __tablename__ = "livro_caixa"
    
    livro_caixa_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    documento_id = Column(UUID(as_uuid=True), ForeignKey("xml_documento.documento_id"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=False)
    
    # Dados do livro caixa
    tipo_movimento = Column(String(50))  # entrada, saida
    data_movimento = Column(DateTime)
    valor = Column(String(20))  # Decimal como STRING (R9)
    descricao = Column(Text)
    
    # Versionamento (R6)
    versao = Column(Integer, default=1)
    
    # Status
    status = Column(String(50), default="processado")
    
    criado_em = Column(DateTime, default=datetime.utcnow)

class PreContabilizacao(Base):
    __tablename__ = "pre_contabilizacao"
    
    pre_contabilizacao_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    documento_id = Column(UUID(as_uuid=True), ForeignKey("xml_documento.documento_id"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=False)
    
    # Lançamento contábil
    conta_debito = Column(String(50))
    conta_credito = Column(String(50))
    valor = Column(String(20))  # Decimal como STRING (R9)
    descricao = Column(Text)
    
    # Versionamento (R6)
    versao = Column(Integer, default=1)
    
    # Status
    status = Column(String(50), default="rascunho")  # rascunho, validado, contabilizado
    
    criado_em = Column(DateTime, default=datetime.utcnow)
    contabilizado_em = Column(DateTime, nullable=True)