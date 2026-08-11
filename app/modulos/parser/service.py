import xml.etree.ElementTree as ET
from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID
from app.modulos.parser.models import XmlDocumento
from datetime import datetime

class ParserService:
    
    @staticmethod
    def extrair_dados_nfe(xml_bruto: bytes) -> dict:
        """
        Parse XML de NF-e (determinístico, SEM LLM).
        Segue R8 da ADR-001: Nenhum LLM em parser.
        Retorna dict com dados extraídos ou erro.
        """
        
        try:
            # Parse XML
            root = ET.fromstring(xml_bruto)
            
            # Namespaces NFe
            ns = {
                'nfe': 'http://www.portalfiscal.inf.br/nfe',
                'default': 'http://www.portalfiscal.inf.br/nfe'
            }
            
            # Extração (DETERMINÍSTICA)
            infNFe = root.find('.//nfe:infNFe', ns)
            if infNFe is None:
                infNFe = root.find('.//infNFe')
            
            ide = infNFe.find('.//nfe:ide', ns) if infNFe else None
            if ide is None and infNFe:
                ide = infNFe.find('.//ide')
            
            total = infNFe.find('.//nfe:total', ns) if infNFe else None
            if total is None and infNFe:
                total = infNFe.find('.//total')
            
            # Dados extraídos
            dados = {
                "numero_nfe": ide.find('.//nfe:nNF', ns).text if ide and ide.find('.//nfe:nNF', ns) is not None else ide.find('.//nNF').text if ide else None,
                "chave_acesso": infNFe.get('Id', '').replace('NFe', '') if infNFe is not None else None,
                "data_emissao": ide.find('.//nfe:dhEmi', ns).text if ide and ide.find('.//nfe:dhEmi', ns) is not None else ide.find('.//dhEmi').text if ide else None,
                "valor_total": total.find('.//nfe:vNF', ns).text if total and total.find('.//nfe:vNF', ns) is not None else total.find('.//vNF').text if total else None,
                "erro": None
            }
            
            return dados
            
        except Exception as e:
            return {
                "numero_nfe": None,
                "chave_acesso": None,
                "data_emissao": None,
                "valor_total": None,
                "erro": str(e)
            }
    
    @staticmethod
    def salvar_documento(
        db: Session,
        tenant_id: UUID,
        ingestion_id: UUID,
        xml_bruto: bytes
    ) -> XmlDocumento:
        """Salva documento parseado com RLS"""
        
        # Set RLS context
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        
        # Parse XML
        dados = ParserService.extrair_dados_nfe(xml_bruto)
        
        # Criar documento
        documento = XmlDocumento(
            ingestion_id=ingestion_id,
            tenant_id=tenant_id,
            numero_nfe=dados.get("numero_nfe"),
            chave_acesso=dados.get("chave_acesso"),
            data_emissao=dados.get("data_emissao"),
            valor_total=dados.get("valor_total"),
            status_parse="erro" if dados.get("erro") else "sucesso",
            erro_parse=dados.get("erro"),
            parseado_em=datetime.utcnow()
        )
        
        db.add(documento)
        db.commit()
        db.refresh(documento)
        
        return documento