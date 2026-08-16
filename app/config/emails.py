from typing import List
from pydantic import BaseModel

class EmailConfig(BaseModel):
    """Configuração de emails da Cernova"""
    SUPORTE_EMAIL = "suporte@cernova.com.br"
    ADMIN_EMAIL = "admin@cernova.com.br"

class EmailService:
    @staticmethod
    def enviar_email(destinatario: str, assunto: str, corpo: str) -> bool:
        try:
            return True
        except Exception as e:
            return False
