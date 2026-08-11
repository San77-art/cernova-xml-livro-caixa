import os
import sys

print("\n" + "="*70)
print("CRIANDO FASE 6 - VERSIONAMENTO + IDEMPOTÊNCIA + OUTBOX")
print("="*70 + "\n")

# Criar pasta
os.makedirs("app/modulos/versionamento", exist_ok=True)
print("✅ Pasta criada: app/modulos/versionamento/\n")

# 1. __init__.py
with open("app/modulos/versionamento/__init__.py", "w") as f:
    f.write("")
print("✅ Criado: __init__.py")

# 2. models.py
models_content = '''from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, Boolean
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
'''

with open("app/modulos/versionamento/models.py", "w") as f:
    f.write(models_content)
print("✅ Criado: models.py")

# 3. schemas.py
schemas_content = '''from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class CadeiaVersaoResponse(BaseModel):
    cadeia_versao_id: UUID
    documento_id: UUID
    numero_versao: int
    hash_versao: str
    motivo_alteracao: str | None
    criado_em: datetime
    
    class Config:
        from_attributes = True

class OutboxResponse(BaseModel):
    outbox_id: UUID
    documento_id: UUID | None
    tipo_evento: str
    evento_id: str
    processado: bool
    tentativas: int
    criado_em: datetime
    
    class Config:
        from_attributes = True
'''

with open("app/modulos/versionamento/schemas.py", "w") as f:
    f.write(schemas_content)
print("✅ Criado: schemas.py")

# 4. service.py
service_content = '''import hashlib
import json
from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID
from app.modulos.versionamento.models import CadeiaVersao, Outbox
from datetime import datetime

class VersiorService:
    
    @staticmethod
    def calcular_hash_cadeia(dados: dict) -> str:
        """Calcula hash SHA-256 da cadeia (R6)"""
        json_str = json.dumps(dados, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    @staticmethod
    def criar_versao(
        db: Session,
        tenant_id: UUID,
        documento_id: UUID,
        dados_cadeia: dict,
        motivo: str
    ) -> CadeiaVersao:
        """Cria nova versão da cadeia (R6)"""
        
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        
        # Obter última versão
        ultima_versao = db.query(CadeiaVersao).filter(
            CadeiaVersao.documento_id == documento_id,
            CadeiaVersao.ativo == True
        ).order_by(CadeiaVersao.numero_versao.desc()).first()
        
        novo_numero = (ultima_versao.numero_versao if ultima_versao else 0) + 1
        hash_cadeia = VersiorService.calcular_hash_cadeia(dados_cadeia)
        
        # Desativar versão anterior
        if ultima_versao:
            ultima_versao.ativo = False
        
        # Criar nova versão
        versao = CadeiaVersao(
            documento_id=documento_id,
            tenant_id=tenant_id,
            numero_versao=novo_numero,
            hash_versao=hash_cadeia,
            dados_versao=dados_cadeia,
            motivo_alteracao=motivo,
            ativo=True
        )
        
        db.add(versao)
        db.commit()
        db.refresh(versao)
        
        return versao
    
    @staticmethod
    def registrar_evento_outbox(
        db: Session,
        tenant_id: UUID,
        tipo_evento: str,
        evento_id: str,
        dados: dict,
        documento_id: UUID = None
    ) -> Outbox:
        """Registra evento no Outbox (R10 - Idempotência)"""
        
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        
        evento = Outbox(
            tenant_id=tenant_id,
            documento_id=documento_id,
            tipo_evento=tipo_evento,
            evento_id=evento_id,
            dados_evento=dados,
            processado=False,
            tentativas=0
        )
        
        db.add(evento)
        db.commit()
        db.refresh(evento)
        
        return evento
    
    @staticmethod
    def reprocessar_evento(
        db: Session,
        tenant_id: UUID,
        outbox_id: UUID
    ) -> Outbox:
        """Marca evento para reprocessamento (R10)"""
        
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        
        evento = db.query(Outbox).filter(
            Outbox.outbox_id == outbox_id,
            Outbox.tenant_id == tenant_id
        ).first()
        
        if evento:
            evento.processado = False
            evento.tentativas = 0
            evento.erro_ultimo = None
            db.commit()
            db.refresh(evento)
        
        return evento
'''

with open("app/modulos/versionamento/service.py", "w") as f:
    f.write(service_content)
print("✅ Criado: service.py")

print("\n" + "="*70)
print("FASE 6 - ESTRUTURA CRIADA COM SUCESSO!")
print("="*70 + "\n")
print("Próximo: Atualizar main.py com endpoints de versionamento\n")
