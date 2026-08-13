@'
from typing import List
from pydantic import BaseModel

class EmailConfig(BaseModel):
    """Configuração de emails da Cernova"""
    
    # Emails principais
    SUPORTE_EMAIL = "suporte@cernova.com.br"
    ADMIN_EMAIL = "admin@cernova.com.br"
    
    # Por área
    SUPORTE_MEDICINA = "suporte-medicina@cernova.com.br"
    SUPORTE_AGRO = "suporte-agro@cernova.com.br"
    SUPORTE_LIVRO_CAIXA = "suporte-livro-caixa@cernova.com.br"
    
    # Configurações SMTP (usar variáveis de ambiente em produção)
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USER = "seu-email@cernova.com.br"
    SMTP_PASSWORD = "sua-senha-app"
    
    # Templates de assuntos
    TEMPLATES = {
        "novo_consultorio": "Bem-vindo ao Cernova Medicina - Consultório Registrado",
        "novo_medico": "Novo Médico Cadastrado",
        "nova_consulta": "Confirmação de Consulta Agendada",
        "novo_paciente": "Novo Paciente Registrado",
        "prescricao_criada": "Prescrição Médica Emitida",
        "alerta_segurança": "Alerta de Segurança - Cernova",
        "suporte": "Resposta do Suporte Cernova",
    }

class EmailService:
    """Serviço de envio de emails"""
    
    @staticmethod
    async def enviar_email(
        destinatario: str,
        assunto: str,
        corpo: str,
        tipo_email: str = "texto"
    ) -> bool:
        """Envia email"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            config = EmailConfig()
            
            msg = MIMEMultipart("alternative")
            msg["Subject"] = assunto
            msg["From"] = config.SMTP_USER
            msg["To"] = destinatario
            
            if tipo_email == "html":
                msg.attach(MIMEText(corpo, "html"))
            else:
                msg.attach(MIMEText(corpo, "plain"))
            
            with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
                server.starttls()
                server.login(config.SMTP_USER, config.SMTP_PASSWORD)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False
    
    @staticmethod
    async def notificar_novo_consultorio(email: str, nome_consultorio: str):
        corpo = f"Bem-vindo ao Cernova Medicina!\n\nSeu consultório {nome_consultorio} foi registrado.\n\nSuporte: suporte-medicina@cernova.com.br"
        return await EmailService.enviar_email(
            email,
            EmailConfig.TEMPLATES["novo_consultorio"],
            corpo
        )
    
    @staticmethod
    async def notificar_novo_medico(email: str, nome_medico: str, especialidade: str):
        corpo = f"Novo Médico Registrado\n\nNome: {nome_medico}\nEspecialidade: {especialidade}\n\nSuporte: suporte-medicina@cernova.com.br"
        return await EmailService.enviar_email(
            email,
            EmailConfig.TEMPLATES["novo_medico"],
            corpo
        )
    
    @staticmethod
    async def notificar_suporte(assunto: str, corpo: str):
        return await EmailService.enviar_email(
            EmailConfig.SUPORTE_EMAIL,
            assunto,
            corpo
        )
'@ | Out-File -FilePath app/config/emails.py -Encoding UTF8