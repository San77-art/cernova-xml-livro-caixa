from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modulos.etl.exporter_factory import ExportadorFactory

router = APIRouter(
    prefix="/api/etl/exportadores",
    tags=["Exportadores"]
)


# ============ TIPOS SUPORTADOS ============
@router.get("/tipos-suportados")
async def listar_exportadores():
    """Lista exportadores disponíveis"""
    tipos = ExportadorFactory.obter_tipos_suportados()
    return {
        "exportadores": tipos,
        "total": len(tipos)
    }


# ============ EXPORTAR PARA JSON ============
@router.post("/exportar/json")
async def exportar_json(
    numero: str,
    serie: str,
    valor: float,
    cnpj: str,
    db: Session = Depends(get_db)
):
    """Exportar nota em formato JSON"""
    dados = {
        "numero": numero,
        "serie": serie,
        "valor": valor,
        "cnpj": cnpj,
        "timestamp": "2026-09-16T10:00:00"
    }
    
    resultado = ExportadorFactory.exportar("JSON", dados)
    return resultado


# ============ EXPORTAR PARA XML ============
@router.post("/exportar/xml")
async def exportar_xml(
    numero: str,
    serie: str,
    valor: float,
    cnpj: str,
    db: Session = Depends(get_db)
):
    """Exportar nota em formato XML"""
    dados = {
        "numero": numero,
        "serie": serie,
        "valor": valor,
        "cnpj": cnpj,
        "timestamp": "2026-09-16T10:00:00"
    }
    
    resultado = ExportadorFactory.exportar("XML", dados)
    return resultado


# ============ EXPORTAR PARA PDF ============
@router.post("/exportar/pdf")
async def exportar_pdf(
    numero: str,
    serie: str,
    valor: float,
    cnpj: str,
    db: Session = Depends(get_db)
):
    """Exportar nota em formato PDF"""
    dados = {
        "numero": numero,
        "serie": serie,
        "valor": valor,
        "cnpj": cnpj,
        "timestamp": "2026-09-16T10:00:00"
    }
    
    resultado = ExportadorFactory.exportar("PDF", dados)
    return resultado


# ============ EXPORTAR PARA EXCEL ============
@router.post("/exportar/excel")
async def exportar_excel(
    numero: str,
    serie: str,
    valor: float,
    cnpj: str,
    db: Session = Depends(get_db)
):
    """Exportar nota em formato Excel/CSV"""
    dados = {
        "numero": numero,
        "serie": serie,
        "valor": valor,
        "cnpj": cnpj,
        "timestamp": "2026-09-16T10:00:00"
    }
    
    resultado = ExportadorFactory.exportar("EXCEL", dados)
    return resultado


# ============ EXPORTAR PARA MÚLTIPLOS FORMATOS ============
@router.post("/exportar/multicanal")
async def exportar_multicanal(
    numero: str,
    serie: str,
    valor: float,
    cnpj: str,
    formatos: list = None,
    db: Session = Depends(get_db)
):
    """Exportar nota para múltiplos formatos simultaneamente"""
    if formatos is None:
        formatos = ["JSON", "XML", "EXCEL"]
    
    dados = {
        "numero": numero,
        "serie": serie,
        "valor": valor,
        "cnpj": cnpj,
        "timestamp": "2026-09-16T10:00:00"
    }
    
    resultados = {}
    for formato in formatos:
        try:
            resultado = ExportadorFactory.exportar(formato, dados)
            resultados[formato] = resultado
        except Exception as e:
            resultados[formato] = {
                "exportado": False,
                "erro": str(e)
            }
    
    return {
        "multicanal": True,
        "exportacoes": resultados,
        "total_sucesso": sum(1 for r in resultados.values() if r.get("exportado"))
    }