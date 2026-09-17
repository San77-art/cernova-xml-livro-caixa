from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modulos.etl.parser_factory import ParserFactory

router = APIRouter(
    prefix="/api/etl/parsadores",
    tags=["Parsadores"]
)


# ============ TIPOS SUPORTADOS ============
@router.get("/tipos-suportados")
async def listar_parsadores():
    """Lista parsers disponíveis"""
    tipos = ParserFactory.obter_tipos_suportados()
    return {
        "parsadores": tipos,
        "total": len(tipos)
    }


# ============ PARSEAR NFe ============
@router.post("/parsear/nfe")
async def parsear_nfe(
    xml: str,
    db: Session = Depends(get_db)
):
    """Parsear XML de NF-e"""
    resultado = ParserFactory.parsear("NFe", xml)
    return resultado


# ============ PARSEAR NFCe ============
@router.post("/parsear/nfce")
async def parsear_nfce(
    xml: str,
    db: Session = Depends(get_db)
):
    """Parsear XML de NFC-e"""
    resultado = ParserFactory.parsear("NFCe", xml)
    return resultado


# ============ PARSEAR CTe ============
@router.post("/parsear/cte")
async def parsear_cte(
    xml: str,
    db: Session = Depends(get_db)
):
    """Parsear XML de CT-e"""
    resultado = ParserFactory.parsear("CTe", xml)
    return resultado


# ============ PARSEAR GENERICO ============
@router.post("/parsear/generico")
async def parsear_generico(
    xml: str,
    db: Session = Depends(get_db)
):
    """Parsear XML genérico (qualquer estrutura)"""
    resultado = ParserFactory.parsear("GENERICO", xml)
    return resultado


# ============ PARSEAR AUTOMÁTICO ============
@router.post("/parsear/auto")
async def parsear_automatico(
    xml: str,
    db: Session = Depends(get_db)
):
    """
    Parsear XML e detectar tipo automaticamente
    Tenta NFe -> NFCe -> CTe -> GENERICO
    """
    tipos_tentar = ["NFe", "NFCe", "CTe", "GENERICO"]
    
    for tipo in tipos_tentar:
        try:
            resultado = ParserFactory.parsear(tipo, xml)
            if resultado.get("parseado"):
                print(f"[ROUTES] ✅ Detectado tipo: {tipo}")
                return resultado
        except:
            continue
    
    # Se nenhum funcionou, retorna genérico
    return {
        "parseado": False,
        "tipo": "DESCONHECIDO",
        "erro": "Não foi possível parsear o XML",
        "tentativas": tipos_tentar
    }


# ============ PARSEAR MÚLTIPLOS TIPOS ============
@router.post("/parsear/multicanal")
async def parsear_multicanal(
    xml: str,
    db: Session = Depends(get_db)
):
    """Parsear XML com todos os tipos de parser"""
    tipos = ["NFe", "NFCe", "CTe", "GENERICO"]
    
    resultados = {}
    for tipo in tipos:
        try:
            resultado = ParserFactory.parsear(tipo, xml)
            resultados[tipo] = resultado
        except Exception as e:
            resultados[tipo] = {
                "parseado": False,
                "erro": str(e)
            }
    
    return {
        "multicanal": True,
        "parsadores": resultados,
        "total_sucesso": sum(1 for r in resultados.values() if r.get("parseado"))
    }