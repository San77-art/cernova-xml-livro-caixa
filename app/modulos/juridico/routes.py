# app/modulos/juridico/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modulos.juridico.models import Norma, TipoNorma
from app.modulos.juridico.schemas import NormaCreate, NormaResponse

router = APIRouter(prefix="/juridico", tags=["juridico"])

@router.get("/normas")
async def listar_normas(tipo: str = None, db: Session = Depends(get_db)):
    query = db.query(Norma)
    if tipo:
        query = query.filter(Norma.tipo == tipo)
    return query.all()

@router.get("/normas/{norma_id}")
async def obter_norma(norma_id: str, db: Session = Depends(get_db)):
    norma = db.query(Norma).filter(Norma.id == norma_id).first()
    if not norma:
        return {"erro": "Norma não encontrada"}
    return norma

@router.post("/normas")
async def criar_norma(norma: NormaCreate, db: Session = Depends(get_db)):
    nova_norma = Norma(**norma.dict())
    db.add(nova_norma)
    db.commit()
    db.refresh(nova_norma)
    return nova_norma

@router.get("/tipos")
async def listar_tipos():
    return [tipo.value for tipo in TipoNorma]
