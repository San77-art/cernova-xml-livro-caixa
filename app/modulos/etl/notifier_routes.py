from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modulos.etl.notifier_factory import NotificadorFactory

router = APIRouter(prefix="/api/etl/notificadores", tags=["Notificadores"])


# ============ GET: Listar tipos de notificadores ============
@router.get("/tipos-suportados")
async def listar_notificadores():
    """
    Listar todos os notificadores disponíveis
    
    Retorna: ["EMAIL", "SMS", "WHATSAPP", "PUSH"]
    """
    tipos = NotificadorFactory.obter_tipos_suportados()
    print(f"[ROUTES] 🔔 Notificadores disponíveis: {tipos}")
    return {"notificadores": tipos}


# ============ POST: Notificar via EMAIL ============
@router.post("/notificar/email")
async def notificar_email(
    email: str,
    assunto: str,
    mensagem: str,
    tipo_documento: str = "NF-e",
    db: Session = Depends(get_db)
):
    """
    Enviar notificação por Email
    
    Exemplo:
    - email: "cliente@example.com"
    - assunto: "Nota Fiscal Emitida"
    - mensagem: "Sua NF-e foi processada com sucesso"
    """
    dados = {
        "email": email,
        "tipo_documento": tipo_documento
    }
    
    resultado = NotificadorFactory.notificar("EMAIL", dados, mensagem)
    return {
        "tipo": "EMAIL",
        "enviado": resultado["enviado"],
        "canal": resultado["canal"],
        "destinatario": resultado["destinatario"],
        "status": resultado["status"]
    }


# ============ POST: Notificar via SMS ============
@router.post("/notificar/sms")
async def notificar_sms(
    telefone: str,
    mensagem: str,
    tipo_documento: str = "NF-e",
    db: Session = Depends(get_db)
):
    """
    Enviar notificação por SMS
    
    Exemplo:
    - telefone: "(11) 99999-9999"
    - mensagem: "Nota fiscal emitida com sucesso"
    """
    dados = {
        "telefone": telefone,
        "tipo_documento": tipo_documento
    }
    
    resultado = NotificadorFactory.notificar("SMS", dados, mensagem)
    return {
        "tipo": "SMS",
        "enviado": resultado["enviado"],
        "canal": resultado["canal"],
        "destinatario": resultado["destinatario"],
        "status": resultado["status"],
        "caracteres": resultado.get("caracteres", 0)
    }


# ============ POST: Notificar via WHATSAPP ============
@router.post("/notificar/whatsapp")
async def notificar_whatsapp(
    whatsapp: str,
    mensagem: str,
    tipo_documento: str = "NF-e",
    db: Session = Depends(get_db)
):
    """
    Enviar notificação por WhatsApp
    
    Exemplo:
    - whatsapp: "(11) 99999-9999"
    - mensagem: "Sua nota foi processada"
    """
    dados = {
        "whatsapp": whatsapp,
        "tipo_documento": tipo_documento
    }
    
    resultado = NotificadorFactory.notificar("WHATSAPP", dados, mensagem)
    return {
        "tipo": "WHATSAPP",
        "enviado": resultado["enviado"],
        "canal": resultado["canal"],
        "destinatario": resultado["destinatario"],
        "status": resultado["status"],
        "tipo_mensagem": resultado.get("tipo_mensagem", "texto")
    }


# ============ POST: Notificar via PUSH ============
@router.post("/notificar/push")
async def notificar_push(
    device_id: str,
    user_id: str,
    mensagem: str,
    tipo_documento: str = "NF-e",
    db: Session = Depends(get_db)
):
    """
    Enviar Push Notification (App Mobile)
    
    Exemplo:
    - device_id: "device_abc123xyz"
    - user_id: "user_123"
    - mensagem: "Nota fiscal disponível"
    """
    dados = {
        "device_id": device_id,
        "user_id": user_id,
        "tipo_documento": tipo_documento
    }
    
    resultado = NotificadorFactory.notificar("PUSH", dados, mensagem)
    return {
        "tipo": "PUSH",
        "enviado": resultado["enviado"],
        "canal": resultado["canal"],
        "destinatario": resultado["destinatario"],
        "user_id": resultado.get("user_id"),
        "status": resultado["status"],
        "titulo": resultado.get("titulo", "Notificação importante")
    }


# ============ POST: Notificar via TODOS os canais ============
@router.post("/notificar/multicanal")
async def notificar_multicanal(
    email: str,
    telefone: str,
    whatsapp: str,
    device_id: str,
    user_id: str,
    mensagem: str,
    tipo_documento: str = "NF-e",
    db: Session = Depends(get_db)
):
    """
    Notificar em TODOS os canais: EMAIL + SMS + WHATSAPP + PUSH
    
    Retorna resultado de cada notificador
    """
    # Dados para EMAIL
    dados_email = {"email": email, "tipo_documento": tipo_documento}
    
    # Dados para SMS
    dados_sms = {"telefone": telefone, "tipo_documento": tipo_documento}
    
    # Dados para WHATSAPP
    dados_whatsapp = {"whatsapp": whatsapp, "tipo_documento": tipo_documento}
    
    # Dados para PUSH
    dados_push = {"device_id": device_id, "user_id": user_id, "tipo_documento": tipo_documento}
    
    # Notificar em todos os canais
    resultado_email = NotificadorFactory.notificar("EMAIL", dados_email, mensagem)
    resultado_sms = NotificadorFactory.notificar("SMS", dados_sms, mensagem)
    resultado_whatsapp = NotificadorFactory.notificar("WHATSAPP", dados_whatsapp, mensagem)
    resultado_push = NotificadorFactory.notificar("PUSH", dados_push, mensagem)
    
    # Contar quantos foram enviados com sucesso
    sucesso_count = sum([
        resultado_email["enviado"],
        resultado_sms["enviado"],
        resultado_whatsapp["enviado"],
        resultado_push["enviado"]
    ])
    
    return {
        "multicanal": True,
        "total_canais": 4,
        "canais_sucesso": sucesso_count,
        "notificadores": {
            "EMAIL": {
                "enviado": resultado_email["enviado"],
                "status": resultado_email["status"]
            },
            "SMS": {
                "enviado": resultado_sms["enviado"],
                "status": resultado_sms["status"]
            },
            "WHATSAPP": {
                "enviado": resultado_whatsapp["enviado"],
                "status": resultado_whatsapp["status"]
            },
            "PUSH": {
                "enviado": resultado_push["enviado"],
                "status": resultado_push["status"]
            }
        }
    }