from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.session import get_db, engine, Base

# Importar modelos de Medicina
from app.modulos.medicina.models import Consultorio, Medico, Paciente, Consulta, Prontuario, Procedimento

# Importar modelos de Juridico
from app.modulos.juridico.models import Norma

# Importar rotas
from app.modulos.juridico.routes import router as juridico_router

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Criar app
app = FastAPI(
    title="Cernova RBV1 v2.0",
    description="Motor Documental + XML + Livro Caixa + Medicina + Base Jurídica",
    version="2.0.0"
)

# Registrar routers
app.include_router(juridico_router)

# ============ HEALTH CHECK ============
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "OK",
            "database": "Connected",
            "version": "2.0.0",
            "modulos": ["xml", "livro_caixa", "medicina", "juridico"]
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "database": "Disconnected",
            "erro": str(e)
        }

# ============ ROOT ============
@app.get("/")
async def root():
    return {
        "status": "Cernova RBV1 v2.0 - Sistema rodando",
        "versao": "2.0.0",
        "modulos": ["xml", "livro_caixa", "medicina", "juridico"],
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "medicina": "/medicina/consultorios",
            "juridico": "/juridico/normas"
        }
    }

# ============ MEDICINA: CONSULTÓRIOS ============
@app.post("/medicina/consultorios")
async def criar_consultorio(nome: str, cnpj: str, db: Session = Depends(get_db)):
    """Criar novo consultório"""
    try:
        consultorio = Consultorio(
            nome=nome,
            cnpj=cnpj,
            empresa_id="default"
        )
        db.add(consultorio)
        db.commit()
        db.refresh(consultorio)
        return {
            "id": str(consultorio.id),
            "nome": consultorio.nome,
            "cnpj": consultorio.cnpj,
            "status": "criado"
        }
    except Exception as e:
        db.rollback()
        return {"status": "erro", "mensagem": str(e)}

@app.get("/medicina/consultorios")
async def listar_consultorios(db: Session = Depends(get_db)):
    """Listar consultórios"""
    try:
        consultorios = db.query(Consultorio).all()
        return [
            {
                "id": str(c.id),
                "nome": c.nome,
                "cnpj": c.cnpj,
                "ativo": c.ativo
            }
            for c in consultorios
        ]
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

# ============ MEDICINA: MÉDICOS ============
@app.post("/medicina/medicos")
async def criar_medico(
    nome_completo: str,
    cpf: str,
    crm: str,
    especialidade: str,
    consultorio_id: str,
    db: Session = Depends(get_db)
):
    """Cadastrar novo médico"""
    try:
        medico = Medico(
            nome_completo=nome_completo,
            cpf=cpf,
            crm=crm,
            especialidade=especialidade,
            consultorio_id=consultorio_id
        )
        db.add(medico)
        db.commit()
        db.refresh(medico)
        return {
            "id": str(medico.id),
            "nome": medico.nome_completo,
            "crm": medico.crm,
            "especialidade": medico.especialidade,
            "status": "criado"
        }
    except Exception as e:
        db.rollback()
        return {"status": "erro", "mensagem": str(e)}

@app.get("/medicina/medicos")
async def listar_medicos(consultorio_id: str = None, db: Session = Depends(get_db)):
    """Listar médicos"""
    try:
        query = db.query(Medico)
        if consultorio_id:
            query = query.filter(Medico.consultorio_id == consultorio_id)
        medicos = query.all()
        return [
            {
                "id": str(m.id),
                "nome": m.nome_completo,
                "crm": m.crm,
                "especialidade": m.especialidade
            }
            for m in medicos
        ]
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

# ============ MEDICINA: PACIENTES ============
@app.post("/medicina/pacientes")
async def criar_paciente(
    nome_completo: str,
    cpf: str,
    data_nascimento: str,
    consultorio_id: str,
    db: Session = Depends(get_db)
):
    """Registrar novo paciente"""
    try:
        from datetime import datetime
        data = datetime.fromisoformat(data_nascimento)
        paciente = Paciente(
            nome_completo=nome_completo,
            cpf=cpf,
            data_nascimento=data,
            consultorio_id=consultorio_id
        )
        db.add(paciente)
        db.commit()
        db.refresh(paciente)
        return {
            "id": str(paciente.id),
            "nome": paciente.nome_completo,
            "cpf": paciente.cpf,
            "status": "criado"
        }
    except Exception as e:
        db.rollback()
        return {"status": "erro", "mensagem": str(e)}

@app.get("/medicina/pacientes")
async def listar_pacientes(consultorio_id: str = None, db: Session = Depends(get_db)):
    """Listar pacientes"""
    try:
        query = db.query(Paciente)
        if consultorio_id:
            query = query.filter(Paciente.consultorio_id == consultorio_id)
        pacientes = query.all()
        return [
            {
                "id": str(p.id),
                "nome": p.nome_completo,
                "cpf": p.cpf
            }
            for p in pacientes
        ]
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
