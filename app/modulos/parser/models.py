from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database.models import Base
from datetime import datetime
import uuid

class XmlDocumento(Base):
    __tablename__ = "xml_documento"
    
    documento_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ingestion_id = Column(UUID(as_uuid=True), ForeignKey("xml_ingestao.ingestion_id"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=False)
    
    # Dados extraídos do XML (estruturado)
    numero_nfe = Column(String(50), nullable=True)
    chave_acesso = Column(String(44), nullable=True)
    data_emissao = Column(DateTime, nullable=True)
    valor_total = Column(String(20), nullable=True)  # Decimal como STRING (R9)
    
    # Resultado do parse
    status_parse = Column(String(50), default="pendente")  # pendente, sucesso, erro
    erro_parse = Column(Text, nullable=True)
    
    criado_em = Column(DateTime, default=datetime.utcnow)
    parseado_em = Column(DateTime, nullable=True)