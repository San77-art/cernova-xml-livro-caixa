import hashlib
from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID
from app.modulos.ingestao.models import XmlIngestion

class IngestaoService:
    
    @staticmethod
    def calcular_hash_sha256(arquivo_bytes: bytes) -> str:
        """Calcula hash SHA-256 do arquivo (ANTES de qualquer processamento)"""
        return hashlib.sha256(arquivo_bytes).hexdigest()
    
    @staticmethod
    def salvar_xml_bruto(
        db: Session,
        tenant_id: UUID,
        filename: str,
        arquivo_bytes: bytes
    ) -> XmlIngestion:
        """
        Salva arquivo XML bruto (IMUTÁVEL).
        Hash é calculado ANTES da inserção.
        Segue R5 da ADR-001: XML bruto imutável + hash ANTES de qualquer parse
        """
        
        # 1. Calcular hash ANTES de qualquer processamento
        hash_sha256 = IngestaoService.calcular_hash_sha256(arquivo_bytes)
        
        # 2. Setar tenant context (RLS)
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        
        # 3. Criar registro
        ingestion = XmlIngestion(
            tenant_id=tenant_id,
            filename=filename,
            xml_bruto=arquivo_bytes,
            hash_sha256=hash_sha256,
            tamanho_bytes=len(arquivo_bytes),
            status="recebido"
        )
        
        db.add(ingestion)
        db.commit()
        db.refresh(ingestion)
        
        return ingestion
    
    @staticmethod
    def obter_ingestion(
        db: Session,
        tenant_id: UUID,
        ingestion_id: UUID
    ) -> XmlIngestion:
        """Obtém ingestão com RLS"""
        
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        
        return db.query(XmlIngestion).filter(
            XmlIngestion.ingestion_id == ingestion_id,
            XmlIngestion.tenant_id == tenant_id
        ).first()