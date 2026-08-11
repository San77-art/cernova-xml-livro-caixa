from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database.models import Base
from datetime import datetime
import uuid

class ClassificacaoCandidata(Base):
    __tablename__ = "classificacao_candidata"
    
    classificacao_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    documento_id = Column(UUID(as_uuid=True), ForeignKey("xml_documento.documento_id"), nullable=False)
    ingestion_id = Column(UUID(as_uuid=True), ForeignKey("xml_ingestao.ingestion_id"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=False)
    
    # Versionamento (R6 da ADR-001)
    versao = Column(Integer, default=1)
    classificacao_version = Column(String(50), nullable=False)  # v1, v2, etc
    
    # Classificação CANDIDATA (não definitiva!)
    tipo_documento = Column(String(50))  # NF-e, NF-e suplementar, etc
    natureza_operacao = Column(String(255))
    cfop = Column(String(4))  # Código Fiscal de Operação
    ncm = Column(String(8))   # Nomenclatura Comum do Mercosul
    
    # Status (R4: NENHUMA classificação é definitiva sem validação humana!)
    status_classificacao = Column(String(50), default="candidata")  # candidata, validada, rejeitada
    confianca = Column(String(20))  # alto, médio, baixo
    
    # Rastreabilidade
    regra_aplicada = Column(String(255))  # Qual regra gerou essa classificação
    justificativa = Column(Text)
    
    criado_em = Column(DateTime, default=datetime.utcnow)
    validado_em = Column(DateTime, nullable=True)
    validado_por = Column(String(255), nullable=True)  # Usuário que validou