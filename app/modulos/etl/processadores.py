from typing import Dict, Any
from app.modulos.etl.interfaces import ProcessadorNota

class ProcessadorNFe(ProcessadorNota):
    """Processa NF-e (Nota Fiscal Eletrônica)"""
    
    def validar_assinatura(self, xml: str) -> bool:
        print(f"Validando assinatura NF-e...")
        return True
    
    def extrair_dados(self, xml: str) -> Dict[str, Any]:
        print(f"Extraindo dados NF-e...")
        return {
            "chave": "35240812345678901234567890123456",
            "numero": "123456",
            "serie": "1",
            "valor": 1000.00,
            "natureza_operacao": "VENDA",
            "tipo": "NF-e",
            "emitente": "EMPRESA XYZ",
            "destinatario": "CLIENTE ABC"
        }
    
    def inserir_no_rb(self, dados: Dict) -> int:
        print(f"Inserindo NF-e no banco de dados...")
        return 1001
    
    @property
    def tipo_documento(self) -> str:
        return "NF-e"

class ProcessadorNFCe(ProcessadorNota):
    """Processa NFC-e (Nota Fiscal de Consumidor Eletrônica)"""
    
    def validar_assinatura(self, xml: str) -> bool:
        print(f"Validando assinatura NFC-e...")
        return True
    
    def extrair_dados(self, xml: str) -> Dict[str, Any]:
        print(f"Extraindo dados NFC-e...")
        return {
            "chave": "35240812345678901234567890123456",
            "numero": "654321",
            "serie": "1",
            "valor": 50.00,
            "natureza_operacao": "CONSUMIDOR",
            "tipo": "NFC-e",
            "emitente": "LOJA ABC",
            "pdv": "001"
        }
    
    def inserir_no_rb(self, dados: Dict) -> int:
        print(f"Inserindo NFC-e no banco de dados...")
        return 1002
    
    @property
    def tipo_documento(self) -> str:
        return "NFC-e"

class ProcessadorCTe(ProcessadorNota):
    """Processa CT-e (Conhecimento de Transporte Eletrônico)"""
    
    def validar_assinatura(self, xml: str) -> bool:
        print(f"Validando assinatura CT-e...")
        return True
    
    def extrair_dados(self, xml: str) -> Dict[str, Any]:
        print(f"Extraindo dados CT-e...")
        return {
            "chave": "35240812345678901234567890123456",
            "numero_cte": "98765",
            "serie": "1",
            "valor": 500.00,
            "natureza_operacao": "TRANSPORTE",
            "tipo": "CT-e",
            "origem": "SAO PAULO",
            "destino": "RIO DE JANEIRO",
            "peso_bruto": 1000.00
        }
    
    def inserir_no_rb(self, dados: Dict) -> int:
        print(f"Inserindo CT-e no banco de dados...")
        return 1003
    
    @property
    def tipo_documento(self) -> str:
        return "CT-e"
