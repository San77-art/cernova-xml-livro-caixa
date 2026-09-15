from app.modulos.etl.interfaces import NotificadorNota
from app.modulos.etl.notificadores import NotificadorEmail, NotificadorSMS, NotificadorWhatsApp, NotificadorPush


class NotificadorFactory:
    """Factory para criar notificadores"""
    
    _notificadores = {}
    
    @classmethod
    def registrar(cls, tipo: str, notificador_class):
        """Registrar novo notificador"""
        cls._notificadores[tipo] = notificador_class
        print(f"[FACTORY] ✅ Notificador '{tipo}' registrado!")
    
    @classmethod
    def criar(cls, tipo: str) -> NotificadorNota:
        """Criar instância de notificador"""
        if tipo not in cls._notificadores:
            raise ValueError(f"Notificador '{tipo}' não encontrado")
        
        print(f"[FACTORY] 🔔 Criando notificador: {tipo}")
        return cls._notificadores[tipo]()
    
    @classmethod
    def obter_tipos_suportados(cls) -> list:
        """Listar notificadores disponíveis"""
        return list(cls._notificadores.keys())
    
    @classmethod
    def notificar(cls, tipo: str, dados: dict, mensagem: str) -> dict:
        """
        Notificar usando notificador específico
        
        Retorna:
        {
            "enviado": bool,
            "canal": str,
            "destinatario": str,
            "status": str
        }
        """
        try:
            notificador = cls.criar(tipo)
            resultado = notificador.notificar(dados, mensagem)
            print(f"[FACTORY] ✅ Notificação {tipo} concluída: {resultado['enviado']}")
            return resultado
        except Exception as e:
            print(f"[FACTORY] ❌ Erro na notificação: {str(e)}")
            return {
                "enviado": False,
                "canal": tipo,
                "destinatario": "",
                "status": f"erro - {str(e)}"
            }


# ============ REGISTRAR NOTIFICADORES ============
NotificadorFactory.registrar("EMAIL", NotificadorEmail)
NotificadorFactory.registrar("SMS", NotificadorSMS)
NotificadorFactory.registrar("WHATSAPP", NotificadorWhatsApp)
NotificadorFactory.registrar("PUSH", NotificadorPush)