from app.modulos.etl.interfaces import NotificadorNota
import re
from datetime import datetime


class NotificadorEmail(NotificadorNota):
    """Notifica via Email"""
    
    def notificar(self, dados: dict, mensagem: str) -> dict:
        """Enviar notificação por email"""
        email = dados.get("email", "")
        
        # Validar email
        if not self._validar_email(email):
            return {
                "enviado": False,
                "canal": "EMAIL",
                "destinatario": email,
                "status": "erro - email inválido",
                "erro": "Formato de email inválido"
            }
        
        # Simular envio de email
        print(f"[EMAIL] 📧 Enviando para {email}")
        print(f"[EMAIL] Assunto: Notificação - {dados.get('tipo_documento', 'Nota')}")
        print(f"[EMAIL] Mensagem: {mensagem}")
        
        return {
            "enviado": True,
            "canal": "EMAIL",
            "destinatario": email,
            "status": "enviado com sucesso",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _validar_email(self, email: str) -> bool:
        """Valida formato do email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @property
    def tipo_notificador(self) -> str:
        return "EMAIL"


class NotificadorSMS(NotificadorNota):
    """Notifica via SMS"""
    
    def notificar(self, dados: dict, mensagem: str) -> dict:
        """Enviar notificação por SMS"""
        telefone = dados.get("telefone", "")
        
        # Validar telefone
        if not self._validar_telefone(telefone):
            return {
                "enviado": False,
                "canal": "SMS",
                "destinatario": telefone,
                "status": "erro - telefone inválido",
                "erro": "Formato de telefone inválido"
            }
        
        # Limitar mensagem a 160 caracteres (SMS)
        mensagem_sms = mensagem[:160]
        
        # Simular envio de SMS
        print(f"[SMS] 📱 Enviando para {telefone}")
        print(f"[SMS] Mensagem: {mensagem_sms}")
        
        return {
            "enviado": True,
            "canal": "SMS",
            "destinatario": telefone,
            "status": "enviado com sucesso",
            "caracteres": len(mensagem_sms),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _validar_telefone(self, telefone: str) -> bool:
        """Valida formato do telefone (Brasil)"""
        telefone_limpo = re.sub(r'\D', '', telefone)
        # Telefone deve ter 10 ou 11 dígitos
        return len(telefone_limpo) in [10, 11]
    
    @property
    def tipo_notificador(self) -> str:
        return "SMS"


class NotificadorWhatsApp(NotificadorNota):
    """Notifica via WhatsApp"""
    
    def notificar(self, dados: dict, mensagem: str) -> dict:
        """Enviar notificação por WhatsApp"""
        whatsapp = dados.get("whatsapp", "")
        
        # Validar WhatsApp (mesmo formato de telefone)
        if not self._validar_whatsapp(whatsapp):
            return {
                "enviado": False,
                "canal": "WHATSAPP",
                "destinatario": whatsapp,
                "status": "erro - whatsapp inválido",
                "erro": "Formato de WhatsApp inválido"
            }
        
        # Simular envio via WhatsApp
        print(f"[WHATSAPP] 💬 Enviando para {whatsapp}")
        print(f"[WHATSAPP] Mensagem: {mensagem}")
        
        return {
            "enviado": True,
            "canal": "WHATSAPP",
            "destinatario": whatsapp,
            "status": "enviado com sucesso",
            "tipo_mensagem": "texto",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _validar_whatsapp(self, whatsapp: str) -> bool:
        """Valida número de WhatsApp"""
        whatsapp_limpo = re.sub(r'\D', '', whatsapp)
        # WhatsApp deve ter 10 ou 11 dígitos
        return len(whatsapp_limpo) in [10, 11]
    
    @property
    def tipo_notificador(self) -> str:
        return "WHATSAPP"


class NotificadorPush(NotificadorNota):
    """Notifica via Push Notification (App Mobile)"""
    
    def notificar(self, dados: dict, mensagem: str) -> dict:
        """Enviar push notification"""
        device_id = dados.get("device_id", "")
        user_id = dados.get("user_id", "")
        
        # Validar device_id
        if not device_id or not user_id:
            return {
                "enviado": False,
                "canal": "PUSH",
                "destinatario": device_id,
                "status": "erro - device_id ou user_id inválido",
                "erro": "Device ID ou User ID não informado"
            }
        
        # Simular envio de Push
        print(f"[PUSH] 🔔 Enviando para device_id: {device_id}")
        print(f"[PUSH] User ID: {user_id}")
        print(f"[PUSH] Título: Notificação importante")
        print(f"[PUSH] Mensagem: {mensagem}")
        
        return {
            "enviado": True,
            "canal": "PUSH",
            "destinatario": device_id,
            "user_id": user_id,
            "status": "enviado com sucesso",
            "titulo": "Notificação importante",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @property
    def tipo_notificador(self) -> str:
        return "PUSH"