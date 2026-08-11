from sqlalchemy import Column, String, DateTime, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"
    
    tenant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False)
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)

class Usuario(Base):
    __tablename__ = "usuarios"
    
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id"), primary_key=True)
    usuario_id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)