from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modulos.etl.conector_factory import ConectorFactory

router = APIRouter(
    prefix="/api/etl/conectores",
    tags=["Conectores"]
)


# ============ ESTADOS SUPORTADOS ============
@router.get("/estados-suportados")
async def listar_estados():
    """Lista estados com conectores SEFAZ disponíveis"""
    estados = ConectorFactory.obter_estados_suportados()
    return {
        "estados": estados,
        "total": len(estados),
        "descricao": "Conectores SEFAZ por estado - RS, SP, MG"
    }


# ============ CONECTAR COM SEFAZ-RS ============
@router.post("/conectar/rs")
async def conectar_rs(
    cnpj: str,
    numero_nfe: str,
    serie: str = "1",
    db: Session = Depends(get_db)
):
    """Conectar e validar NF-e com SEFAZ-RS"""
    dados = {
        "cnpj": cnpj,
        "numero_nfe": numero_nfe,
        "serie": serie
    }
    
    resultado = ConectorFactory.conectar("RS", dados)
    return resultado


# ============ CONECTAR COM SEFAZ-SP ============
@router.post("/conectar/sp")
async def conectar_sp(
    cnpj: str,
    numero_nfe: str,
    serie: str = "1",
    db: Session = Depends(get_db)
):
    """Conectar e validar NF-e com SEFAZ-SP"""
    dados = {
        "cnpj": cnpj,
        "numero_nfe": numero_nfe,
        "serie": serie
    }
    
    resultado = ConectorFactory.conectar("SP", dados)
    return resultado


# ============ CONECTAR COM SEFAZ-MG ============
@router.post("/conectar/mg")
async def conectar_mg(
    cnpj: str,
    numero_nfe: str,
    serie: str = "1",
    db: Session = Depends(get_db)
):
    """Conectar e validar NF-e com SEFAZ-MG"""
    dados = {
        "cnpj": cnpj,
        "numero_nfe": numero_nfe,
        "serie": serie
    }
    
    resultado = ConectorFactory.conectar("MG", dados)
    return resultado


# ============ CONECTAR GENERICO (AUTO-DETECT ESTADO) ============
@router.post("/conectar/auto")
async def conectar_auto(
    cnpj: str,
    numero_nfe: str,
    estado: str = "SP",
    serie: str = "1",
    db: Session = Depends(get_db)
):
    """
    Conectar e validar NF-e com SEFAZ (estado definido pelo usuário)
    Estados suportados: RS, SP, MG
    """
    estado_upper = estado.upper()
    
    if estado_upper not in ConectorFactory.obter_estados_suportados():
        return {
            "conectado": False,
            "erro": f"Estado '{estado_upper}' não suportado. Suportados: {', '.join(ConectorFactory.obter_estados_suportados())}"
        }
    
    dados = {
        "cnpj": cnpj,
        "numero_nfe": numero_nfe,
        "serie": serie
    }
    
    resultado = ConectorFactory.conectar(estado_upper, dados)
    return resultado


# ============ CONECTAR COM MÚLTIPLOS ESTADOS ============
@router.post("/conectar/multicanal")
async def conectar_multicanal(
    cnpj: str,
    numero_nfe: str,
    serie: str = "1",
    db: Session = Depends(get_db)
):
    """
    Conectar com MÚLTIPLOS SEFAZ simultaneamente
    Útil para empresas multi-estado
    """
    estados = ConectorFactory.obter_estados_suportados()
    
    dados = {
        "cnpj": cnpj,
        "numero_nfe": numero_nfe,
        "serie": serie
    }
    
    resultados = {}
    for estado in estados:
        try:
            resultado = ConectorFactory.conectar(estado, dados)
            resultados[estado] = resultado
        except Exception as e:
            resultados[estado] = {
                "conectado": False,
                "erro": str(e)
            }
    
    return {
        "multicanal": True,
        "nfe": f"{numero_nfe}/{serie}",
        "cnpj": cnpj,
        "conectores": resultados,
        "total_conectados": sum(1 for r in resultados.values() if r.get("conectado"))
    }


# ============ VALIDAR URL SEFAZ ============
@router.get("/validar-url/{estado}")
async def validar_url_sefaz(estado: str):
    """
    Validar URL do webservice SEFAZ para um estado
    Útil para testes de conectividade
    """
    estado_upper = estado.upper()
    
    if estado_upper not in ConectorFactory.obter_estados_suportados():
        return {
            "valido": False,
            "erro": f"Estado '{estado_upper}' não suportado"
        }
    
    conector = ConectorFactory.criar(estado_upper)
    
    return {
        "valido": True,
        "estado": conector.estado,
        "url_sefaz": conector.url_sefaz,
        "tipo": "webservice SOAP/XML"
    }