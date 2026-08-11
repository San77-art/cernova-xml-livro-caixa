from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID
from app.modulos.classificacao.models import ClassificacaoCandidata
from datetime import datetime

class ClassificacaoService:
    
    @staticmethod
    def classificar_nfe(
        numero_nfe: str,
        natureza_operacao: str,
        valor_total: str
    ) -> dict:
        """
        Classificação DETERMINÍSTICA (SEM LLM).
        Retorna classificação CANDIDATA.
        Segue R4: Nenhuma classificação é definitiva sem validação humana!
        Segue R8: Nenhum LLM em classificação.
        """
        
        # Regras determinísticas simples (exemplo)
        classificacao = {
            "tipo_documento": "NF-e",
            "natureza_operacao": natureza_operacao or "Operação interna",
            "cfop": "5102",  # Venda de mercadoria adquirida ou recebida
            "ncm": "0000000",  # Padrão quando não identificado
            "confianca": "médio",
            "regra_aplicada": "REGRA_BASICA_NFE",
            "justificativa": f"Classificação candidata automática. Número NF-e: {numero_nfe}"
        }
        
        return classificacao
    
    @staticmethod
    def salvar_classificacao(
        db: Session,
        tenant_id: UUID,
        documento_id: UUID,
        ingestion_id: UUID,
        dados_classificacao: dict
    ) -> ClassificacaoCandidata:
        """Salva classificação CANDIDATA com RLS"""
        
        # Set RLS context
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        
        # Criar classificação
        classificacao = ClassificacaoCandidata(
            documento_id=documento_id,
            ingestion_id=ingestion_id,
            tenant_id=tenant_id,
            versao=1,
            classificacao_version="v1",
            tipo_documento=dados_classificacao.get("tipo_documento"),
            natureza_operacao=dados_classificacao.get("natureza_operacao"),
            cfop=dados_classificacao.get("cfop"),
            ncm=dados_classificacao.get("ncm"),
            status_classificacao="candidata",  # NUNCA é definitiva!
            confianca=dados_classificacao.get("confianca"),
            regra_aplicada=dados_classificacao.get("regra_aplicada"),
            justificativa=dados_classificacao.get("justificativa")
        )
        
        db.add(classificacao)
        db.commit()
        db.refresh(classificacao)
        
        return classificacao