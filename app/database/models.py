from sqlalchemy import Column, String, DateTime, TIMESTAMP, ForeignKey, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from enum import Enum as PyEnum

Base = declarative_base()


# ============ ENUM PARA IDEMPOTÊNCIA ============
class IdempotencyKeyStatus(PyEnum):
    """Status da chave de idempotência"""
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"


# ============ MODELOS EXISTENTES ============
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


# ============ NOVO MODELO - IDEMPOTÊNCIA ============
class IdempotencyKey(Base):
    """
    Armazena chaves de idempotência para evitar duplicação
    Garante que mesma operação 2x = resultado igual
    """
    
    __tablename__ = "idempotency_keys"
    
    # ID único
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Chave enviada pelo cliente
    key = Column(String(255), unique=True, nullable=False, index=True)
    
    # Endpoint da requisição
    endpoint = Column(String(255), nullable=False)
    
    # Status: processing, success, failed
    status = Column(String(20), nullable=False, default="processing")
    
    # Resposta cacheada (JSON)
    response = Column(String, nullable=True)
    
    # Mensagem de erro (se falhou)
    error = Column(String(1000), nullable=True)
    
    # Timestamps
    criado_em = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<IdempotencyKey {self.key} - {self.status}>"