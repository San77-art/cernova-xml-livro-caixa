from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID
from app.modulos.livro_caixa.models import LivroCaixa, PreContabilizacao
from datetime import datetime

class LivroCaixaService:
    
    @staticmethod
    def gerar_livro_caixa(
        numero_nfe: str,
        valor_total: str,
        tipo_operacao: str
    ) -> dict:
        """
        Gera entrada de livro caixa DETERMINÍSTICA (SEM LLM).
        Segue R8 da ADR-001.
        """
        
        # Regras determinísticas
        if "entrada" in tipo_operacao.lower():
            tipo_movimento = "entrada"
            descricao = f"Entrada NF-e {numero_nfe}"
        else:
            tipo_movimento = "saida"
            descricao = f"Saída NF-e {numero_nfe}"
        
        return {
            "tipo_movimento": tipo_movimento,
            "valor": valor_total,
            "descricao": descricao
        }
    
    @staticmethod
    def salvar_livro_caixa(
        db: Session,
        tenant_id: UUID,
        documento_id: UUID,
        dados_livro: dict
    ) -> LivroCaixa:
        """Salva livro caixa com RLS"""
        
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        
        livro = LivroCaixa(
            documento_id=documento_id,
            tenant_id=tenant_id,
            tipo_movimento=dados_livro.get("tipo_movimento"),
            data_movimento=datetime.utcnow(),
            valor=dados_livro.get("valor"),
            descricao=dados_livro.get("descricao"),
            status="processado"
        )
        
        db.add(livro)
        db.commit()
        db.refresh(livro)
        
        return livro
    
    @staticmethod
    def gerar_pre_contabilizacao(
        valor_total: str,
        tipo_operacao: str
    ) -> dict:
        """
        Gera pré-contabilização DETERMINÍSTICA (SEM LLM).
        Contas padrão (exemplo simplificado).
        Segue R8 da ADR-001.
        """
        
        if "entrada" in tipo_operacao.lower():
            conta_debito = "1.1.1.01"  # Caixa
            conta_credito = "4.1.1.01"  # Receita de Vendas
        else:
            conta_debito = "5.1.1.01"  # CMV
            conta_credito = "1.1.1.01"  # Caixa
        
        return {
            "conta_debito": conta_debito,
            "conta_credito": conta_credito,
            "valor": valor_total,
            "descricao": f"Lançamento contábil automático"
        }
    
    @staticmethod
    def salvar_pre_contabilizacao(
        db: Session,
        tenant_id: UUID,
        documento_id: UUID,
        dados_pre: dict
    ) -> PreContabilizacao:
        """Salva pré-contabilização com RLS"""
        
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        
        pre_conta = PreContabilizacao(
            documento_id=documento_id,
            tenant_id=tenant_id,
            conta_debito=dados_pre.get("conta_debito"),
            conta_credito=dados_pre.get("conta_credito"),
            valor=dados_pre.get("valor"),
            descricao=dados_pre.get("descricao"),
            status="rascunho"  # Nunca é contabilizado automaticamente!
        )
        
        db.add(pre_conta)
        db.commit()
        db.refresh(pre_conta)
        
        return pre_conta