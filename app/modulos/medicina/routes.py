from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.session import get_db
from app.modulos.medicina import models, schemas
from app.config.emails import EmailService

router = APIRouter(prefix="/medicina", tags=["Medicina"])

# ============ CONSULTÓRIO ============

@router.post("/consultorios", response_model=schemas.ConsultorioResponse)
async def criar_consultorio(
    consultorio: schemas.ConsultorioCreate,
    db: Session = Depends(get_db)
):
    """Cria novo consultório"""
    db_consultorio = models.Consultorio(
        **consultorio.dict(),
        empresa_id="default"  # Você pode mudar isso para multi-tenant
    )
    db.add(db_consultorio)
    db.commit()
    db.refresh(db_consultorio)
    
    # Enviar email de boas-vindas
    await EmailService.notificar_novo_consultorio(
        consultorio.email_contato,
        consultorio.nome
    )
    
    return db_consultorio

@router.get("/consultorios")
async def listar_consultorios(db: Session = Depends(get_db)):
    """Lista todos os consultórios"""
    return db.query(models.Consultorio).all()

@router.get("/consultorios/{consultorio_id}", response_model=schemas.ConsultorioResponse)
async def obter_consultorio(consultorio_id: str, db: Session = Depends(get_db)):
    """Obtém um consultório específico"""
    consultorio = db.query(models.Consultorio).filter(
        models.Consultorio.id == consultorio_id
    ).first()
    if not consultorio:
        raise HTTPException(status_code=404, detail="Consultório não encontrado")
    return consultorio

# ============ MÉDICO ============

@router.post("/medicos", response_model=schemas.MedicoResponse)
async def criar_medico(
    medico: schemas.MedicoCreate,
    db: Session = Depends(get_db)
):
    """Cria novo médico"""
    # Verificar se consultório existe
    consultorio = db.query(models.Consultorio).filter(
        models.Consultorio.id == medico.consultorio_id
    ).first()
    if not consultorio:
        raise HTTPException(status_code=404, detail="Consultório não encontrado")
    
    db_medico = models.Medico(**medico.dict())
    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    
    # Enviar email
    if medico.email:
        await EmailService.notificar_novo_medico(
            medico.email,
            medico.nome_completo,
            medico.especialidade
        )
    
    return db_medico

@router.get("/medicos")
async def listar_medicos(consultorio_id: str = None, db: Session = Depends(get_db)):
    """Lista médicos (filtrar por consultório)"""
    query = db.query(models.Medico)
    if consultorio_id:
        query = query.filter(models.Medico.consultorio_id == consultorio_id)
    return query.all()

@router.get("/medicos/{medico_id}", response_model=schemas.MedicoResponse)
async def obter_medico(medico_id: str, db: Session = Depends(get_db)):
    """Obtém um médico específico"""
    medico = db.query(models.Medico).filter(models.Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return medico

# ============ PACIENTE ============

@router.post("/pacientes", response_model=schemas.PacienteResponse)
async def criar_paciente(
    paciente: schemas.PacienteCreate,
    db: Session = Depends(get_db)
):
    """Cria novo paciente"""
    # Verificar se consultório existe
    consultorio = db.query(models.Consultorio).filter(
        models.Consultorio.id == paciente.consultorio_id
    ).first()
    if not consultorio:
        raise HTTPException(status_code=404, detail="Consultório não encontrado")
    
    db_paciente = models.Paciente(**paciente.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    
    return db_paciente

@router.get("/pacientes")
async def listar_pacientes(consultorio_id: str = None, db: Session = Depends(get_db)):
    """Lista pacientes (filtrar por consultório)"""
    query = db.query(models.Paciente)
    if consultorio_id:
        query = query.filter(models.Paciente.consultorio_id == consultorio_id)
    return query.all()

@router.get("/pacientes/{paciente_id}", response_model=schemas.PacienteResponse)
async def obter_paciente(paciente_id: str, db: Session = Depends(get_db)):
    """Obtém um paciente específico"""
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente

# ============ CONSULTA ============

@router.post("/consultas", response_model=schemas.ConsultaResponse)
async def criar_consulta(
    consulta: schemas.ConsultaCreate,
    db: Session = Depends(get_db)
):
    """Agenda nova consulta"""
    # Verificar se paciente e médico existem
    paciente = db.query(models.Paciente).filter(models.Paciente.id == consulta.paciente_id).first()
    medico = db.query(models.Medico).filter(models.Medico.id == consulta.medico_id).first()
    
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    
    db_consulta = models.Consulta(**consulta.dict())
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    
    # Enviar email de confirmação
    if paciente.email:
        await EmailService.enviar_email(
            paciente.email,
            "Confirmação de Consulta Agendada",
            f"Sua consulta com Dr(a). {medico.nome_completo} está marcada para {consulta.data_hora}"
        )
    
    return db_consulta

@router.get("/consultas")
async def listar_consultas(medico_id: str = None, paciente_id: str = None, db: Session = Depends(get_db)):
    """Lista consultas"""
    query = db.query(models.Consulta)
    if medico_id:
        query = query.filter(models.Consulta.medico_id == medico_id)
    if paciente_id:
        query = query.filter(models.Consulta.paciente_id == paciente_id)
    return query.all()

# ============ PRONTUÁRIO ============

@router.post("/prontuarios", response_model=schemas.ProntuarioResponse)
async def criar_prontuario(
    prontuario: schemas.ProntuarioCreate,
    db: Session = Depends(get_db)
):
    """Cria novo prontuário (registro de atendimento)"""
    paciente = db.query(models.Paciente).filter(models.Paciente.id == prontuario.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    db_prontuario = models.Prontuario(**prontuario.dict())
    db.add(db_prontuario)
    db.commit()
    db.refresh(db_prontuario)
    
    return db_prontuario

@router.get("/prontuarios/{paciente_id}")
async def listar_prontuarios_paciente(paciente_id: str, db: Session = Depends(get_db)):
    """Lista prontuários de um paciente"""
    return db.query(models.Prontuario).filter(models.Prontuario.paciente_id == paciente_id).all()

# ============ PROCEDIMENTO ============

@router.post("/procedimentos", response_model=schemas.ProcedimentoResponse)
async def criar_procedimento(
    procedimento: schemas.ProcedimentoCreate,
    db: Session = Depends(get_db)
):
    """Cria novo procedimento"""
    consultorio = db.query(models.Consultorio).filter(
        models.Consultorio.id == procedimento.consultorio_id
    ).first()
    if not consultorio:
        raise HTTPException(status_code=404, detail="Consultório não encontrado")
    
    db_procedimento = models.Procedimento(**procedimento.dict())
    db.add(db_procedimento)
    db.commit()
    db.refresh(db_procedimento)
    
    return db_procedimento

@router.get("/procedimentos")
async def listar_procedimentos(consultorio_id: str = None, db: Session = Depends(get_db)):
    """Lista procedimentos"""
    query = db.query(models.Procedimento)
    if consultorio_id:
        query = query.filter(models.Procedimento.consultorio_id == consultorio_id)
    return query.all()
