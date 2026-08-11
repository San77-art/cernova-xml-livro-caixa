from sqlalchemy import Column, String, LargeBinary, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.database.models import Base
from datetime import datetime
import uuid

class XmlIngestion(Base):
    __tablename__ = "xml_ingestao"
    
    ingestion_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=False)
    filename = Column(String(500), nullable=False)
    xml_bruto = Column(LargeBinary, nullable=False)  # IMUTÁVEL
    hash_sha256 = Column(String(64), nullable=False, index=True)
    tamanho_bytes = Column(Integer, nullable=False)
    status = Column(String(50), default="recebido")  # recebido, processando, processado, erro
    criado_em = Column(DateTime, default=datetime.utcnow)
    processado_em = Column(DateTime, nullable=True)
    
    __table_args__ = (
        # RLS Policy
        # tenant_id = CAST(current_setting('app.tenant_id') AS UUID)
    )