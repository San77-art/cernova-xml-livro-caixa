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


# ============ VALIDADORES ============
class ValidadorNota(ABC):
    """Interface para validadores de notas fiscais"""
    
    @abstractmethod
    def validar(self, dados: dict) -> dict:
        """
        Validar dados da nota
        
        Retorna:
        {
            "valido": bool,
            "erros": [str],
            "avisos": [str]
        }
        """
        pass
    
    @property
    @abstractmethod
    def tipo_validador(self) -> str:
        """Tipo: SEFAZ, DATABASE, ASSINATURA"""
        pass


# ============ NOTIFICADORES ============
class NotificadorNota(ABC):
    """Interface para notificadores de notas fiscais"""
    
    @abstractmethod
    def notificar(self, dados: dict, mensagem: str) -> dict:
        """
        Enviar notificação
        
        Retorna:
        {
            "enviado": bool,
            "canal": str,
            "destinatario": str,
            "status": str
        }
        """
        pass
    
    @property
    @abstractmethod
    def tipo_notificador(self) -> str:
        """Tipo: EMAIL, SMS, WHATSAPP, PUSH"""
        pass


# ============ EXPORTADORES ============
class ExportadorNota(ABC):
    """Interface para exportadores de notas fiscais"""
    
    @abstractmethod
    def exportar(self, dados: dict) -> dict:
        """
        Exportar dados em formato específico
        
        Retorna:
        {
            "exportado": bool,
            "formato": str,
            "tamanho": int,
            "conteudo": bytes ou string
        }
        """
        pass
    
    @property
    @abstractmethod
    def tipo_exportador(self) -> str:
        """Tipo: PDF, XML, JSON, EXCEL"""
        pass


# ============ AGENDAMENTOS ============
class AgendamentoNota(ABC):
    """Interface para tipos de agendamento"""
    
    @abstractmethod
    def agendar(self, dados: dict) -> dict:
        """
        Agendar consulta/serviço
        
        Retorna:
        {
            "agendado": bool,
            "tipo": str,
            "data": str,
            "horario": str,
            "paciente": str,
            "profissional": str
        }
        """
        pass
    
    @property
    @abstractmethod
    def tipo_agendamento(self) -> str:
        """Tipo: PRESENCIAL, TELEMEDICINA, HOMECARE"""
        pass