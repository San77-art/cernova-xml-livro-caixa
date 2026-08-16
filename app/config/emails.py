from typing import List

class EmailConfig:
    """Configuração de emails da Cernova"""
    SUPORTE_EMAIL: str = "suporte@cernova.com.br"
    ADMIN_EMAIL: str = "admin@cernova.com.br"

class EmailService:
    @staticmethod
    def enviar_email(destinatario: str, assunto: str, corpo: str) -> bool:
        try:
            return True
        except Exception as e:
            return False
