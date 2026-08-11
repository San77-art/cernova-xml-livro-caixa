# coding: utf-8
import hashlib
import json
from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID
from app.modulos.versionamento.models import CadeiaVersao, Outbox
from datetime import datetime

class VersiorService:
    
    @staticmethod
    def calcular_hash_cadeia(dados: dict) -> str:
        json_str = json.dumps(dados, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    @staticmethod
    def criar_versao(db: Session, tenant_id: UUID, documento_id: UUID, dados_cadeia: dict, motivo: str) -> CadeiaVersao:
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        ultima_versao = db.query(CadeiaVersao).filter(CadeiaVersao.documento_id == documento_id, CadeiaVersao.ativo == True).order_by(CadeiaVersao.numero_versao.desc()).first()
        novo_numero = (ultima_versao.numero_versao if ultima_versao else 0) + 1
        hash_cadeia = VersiorService.calcular_hash_cadeia(dados_cadeia)
        if ultima_versao:
            ultima_versao.ativo = False
        versao = CadeiaVersao(documento_id=documento_id, tenant_id=tenant_id, numero_versao=novo_numero, hash_versao=hash_cadeia, dados_versao=dados_cadeia, motivo_alteracao=motivo, ativo=True)
        db.add(versao)
        db.commit()
        db.refresh(versao)
        return versao
    
    @staticmethod
    def registrar_evento_outbox(db: Session, tenant_id: UUID, tipo_evento: str, evento_id: str, dados: dict, documento_id: UUID = None) -> Outbox:
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        evento = Outbox(tenant_id=tenant_id, documento_id=documento_id, tipo_evento=tipo_evento, evento_id=evento_id, dados_evento=dados, processado=False, tentativas=0)
        db.add(evento)
        db.commit()
        db.refresh(evento)
        return evento
    
    @staticmethod
    def reprocessar_evento(db: Session, tenant_id: UUID, outbox_id: UUID) -> Outbox:
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        evento = db.query(Outbox).filter(Outbox.outbox_id == outbox_id, Outbox.tenant_id == tenant_id).first()
        if evento:
            evento.processado = False
            evento.tentativas = 0
            evento.erro_ultimo = None
            db.commit()
            db.refresh(evento)
        return evento
