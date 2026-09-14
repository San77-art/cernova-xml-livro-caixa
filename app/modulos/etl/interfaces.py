from abc import ABC, abstractmethod
from typing import Dict, Any

class ProcessadorNota(ABC):
    """Interface - todos os processadores devem implementar isto"""
    
    @abstractmethod
    def validar_assinatura(self, xml: str) -> bool:
        """Valida assinatura do documento"""
        pass
    
    @abstractmethod
    def extrair_dados(self, xml: str) -> Dict[str, Any]:
        """Extrai dados do XML"""
        pass
    
    @abstractmethod
    def inserir_no_rb(self, dados: Dict) -> int:
        """Insere no banco de dados"""
        pass
    
    @property
    @abstractmethod
    def tipo_documento(self) -> str:
        """Que tipo de documento sou?"""
        pass
