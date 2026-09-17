from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modulos.etl.agendamento_factory import AgendamentoFactory

router = APIRouter(
    prefix="/api/etl/agendadores",
    tags=["Agendadores"]
)


# ============ TIPOS SUPORTADOS ============
@router.get("/tipos-suportados")
async def listar_agendadores():
    """Lista agendadores disponíveis"""
    tipos = AgendamentoFactory.obter_tipos_suportados()
    return {
        "agendadores": tipos,
        "total": len(tipos)
    }


# ============ AGENDAR PRESENCIAL ============
@router.post("/agendar/presencial")
async def agendar_presencial(
    paciente_nome: str,
    profissional_nome: str,
    data: str,
    horario: str,
    consultorio: str = "Consultório 1",
    db: Session = Depends(get_db)
):
    """Agendar consulta presencial"""
    dados = {
        "paciente_nome": paciente_nome,
        "profissional_nome": profissional_nome,
        "data": data,
        "horario": horario,
        "consultorio": consultorio
    }
    
    resultado = AgendamentoFactory.agendar("PRESENCIAL", dados)
    return resultado


# ============ AGENDAR TELEMEDICINA ============
@router.post("/agendar/telemedicina")
async def agendar_telemedicina(
    paciente_nome: str,
    profissional_nome: str,
    data: str,
    horario: str,
    email: str,
    db: Session = Depends(get_db)
):
    """Agendar consulta por telemedicina"""
    dados = {
        "paciente_nome": paciente_nome,
        "profissional_nome": profissional_nome,
        "data": data,
        "horario": horario,
        "email": email
    }
    
    resultado = AgendamentoFactory.agendar("TELEMEDICINA", dados)
    return resultado


# ============ AGENDAR HOME CARE ============
@router.post("/agendar/homecare")
async def agendar_homecare(
    paciente_nome: str,
    profissional_nome: str,
    data: str,
    horario: str,
    endereco: str,
    telefone: str,
    db: Session = Depends(get_db)
):
    """Agendar atendimento home care"""
    dados = {
        "paciente_nome": paciente_nome,
        "profissional_nome": profissional_nome,
        "data": data,
        "horario": horario,
        "endereco": endereco,
        "telefone": telefone
    }
    
    resultado = AgendamentoFactory.agendar("HOMECARE", dados)
    return resultado


# ============ AGENDAR EM MÚLTIPLOS CANAIS ============
@router.post("/agendar/multicanal")
async def agendar_multicanal(
    paciente_nome: str,
    profissional_nome: str,
    data: str,
    horario: str,
    email: str,
    endereco: str,
    telefone: str,
    consultorio: str = "Consultório 1",
    db: Session = Depends(get_db)
):
    """Agendar em múltiplos tipos de agendamento"""
    
    dados_presencial = {
        "paciente_nome": paciente_nome,
        "profissional_nome": profissional_nome,
        "data": data,
        "horario": horario,
        "consultorio": consultorio
    }
    
    dados_tele = {
        "paciente_nome": paciente_nome,
        "profissional_nome": profissional_nome,
        "data": data,
        "horario": horario,
        "email": email
    }
    
    dados_home = {
        "paciente_nome": paciente_nome,
        "profissional_nome": profissional_nome,
        "data": data,
        "horario": horario,
        "endereco": endereco,
        "telefone": telefone
    }
    
    resultado_presencial = AgendamentoFactory.agendar("PRESENCIAL", dados_presencial)
    resultado_tele = AgendamentoFactory.agendar("TELEMEDICINA", dados_tele)
    resultado_home = AgendamentoFactory.agendar("HOMECARE", dados_home)
    
    return {
        "multicanal": True,
        "agendamentos": {
            "PRESENCIAL": resultado_presencial,
            "TELEMEDICINA": resultado_tele,
            "HOMECARE": resultado_home
        },
        "total_agendados": sum([
            resultado_presencial.get("agendado", False),
            resultado_tele.get("agendado", False),
            resultado_home.get("agendado", False)
        ])
    }