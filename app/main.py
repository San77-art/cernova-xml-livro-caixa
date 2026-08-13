from fastapi import FastAPI, Header, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID
from datetime import datetime
from app.database.session import get_db, engine
from app.database.models import Base
from app.modulos.ingestao.models import XmlIngestion
from app.modulos.ingestao.service import IngestaoService
from app.modulos.parser.models import XmlDocumento
from app.modulos.parser.service import ParserService
from app.modulos.classificacao.models import ClassificacaoCandidata
from app.modulos.classificacao.service import ClassificacaoService
from app.modulos.livro_caixa.models import LivroCaixa, PreContabilizacao
from app.modulos.livro_caixa.service import LivroCaixaService
from app.modulos.versionamento.models import CadeiaVersao, Outbox
from app.modulos.versionamento.service import VersiorService

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cernova XML + Livro Caixa + Medicina RBV1 v2.0")

@app.get("/")
async def root():
    return {"status": "Cernova RBV1 v2.0 - Sistema rodando", "modulos": ["xml", "livro_caixa", "medicina"]}

@app.get("/health")
async def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "OK", "database": "Connected", "version": "2.0.0"}
    except:
        return {"status": "ERROR", "database": "Disconnected"}

# ============ MEDICINA ENDPOINTS ============

@app.post("/medicina/consultorios")
async def criar_consultorio(nome: str, cnpj: str, db: Session = Depends(get_db)):
    try:
        from app.modulos.medicina.models import Consultorio
        consultorio = Consultorio(nome=nome, cnpj=cnpj, empresa_id="default")
        db.add(consultorio)
        db.commit()
        db.refresh(consultorio)
        return {"id": str(consultorio.id), "nome": consultorio.nome, "status": "criado"}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.get("/medicina/consultorios")
async def listar_consultorios(db: Session = Depends(get_db)):
    try:
        from app.modulos.medicina.models import Consultorio
        consultorios = db.query(Consultorio).all()
        return [{"id": str(c.id), "nome": c.nome, "cnpj": c.cnpj} for c in consultorios]
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.post("/medicina/medicos")
async def criar_medico(nome_completo: str, cpf: str, crm: str, especialidade: str, consultorio_id: str, db: Session = Depends(get_db)):
    try:
        from app.modulos.medicina.models import Medico
        medico = Medico(nome_completo=nome_completo, cpf=cpf, crm=crm, especialidade=especialidade, consultorio_id=consultorio_id)
        db.add(medico)
        db.commit()
        db.refresh(medico)
        return {"id": str(medico.id), "nome": medico.nome_completo, "status": "criado"}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.get("/medicina/medicos")
async def listar_medicos(consultorio_id: str = None, db: Session = Depends(get_db)):
    try:
        from app.modulos.medicina.models import Medico
        query = db.query(Medico)
        if consultorio_id:
            query = query.filter(Medico.consultorio_id == consultorio_id)
        medicos = query.all()
        return [{"id": str(m.id), "nome": m.nome_completo, "crm": m.crm} for m in medicos]
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.post("/medicina/pacientes")
async def criar_paciente(nome_completo: str, cpf: str, data_nascimento: str, consultorio_id: str, db: Session = Depends(get_db)):
    try:
        from app.modulos.medicina.models import Paciente
        paciente = Paciente(nome_completo=nome_completo, cpf=cpf, data_nascimento=datetime.fromisoformat(data_nascimento), consultorio_id=consultorio_id)
        db.add(paciente)
        db.commit()
        db.refresh(paciente)
        return {"id": str(paciente.id), "nome": paciente.nome_completo, "status": "criado"}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.get("/medicina/pacientes")
async def listar_pacientes(consultorio_id: str = None, db: Session = Depends(get_db)):
    try:
        from app.modulos.medicina.models import Paciente
        query = db.query(Paciente)
        if consultorio_id:
            query = query.filter(Paciente.consultorio_id == consultorio_id)
        pacientes = query.all()
        return [{"id": str(p.id), "nome": p.nome_completo, "cpf": p.cpf} for p in pacientes]
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
