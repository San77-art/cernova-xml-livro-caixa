from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modulos.etl.validator_factory import ValidadorFactory

router = APIRouter(prefix="/api/etl/validadores", tags=["Validadores"])


# ============ GET: Listar tipos de validadores ============
@router.get("/tipos-suportados")
async def listar_validadores():
    """
    Listar todos os validadores disponíveis
    
    Retorna: ["SEFAZ", "DATABASE", "ASSINATURA"]
    """
    tipos = ValidadorFactory.obter_tipos_suportados()
    print(f"[ROUTES] 📋 Validadores disponíveis: {tipos}")
    return {"validadores": tipos}


# ============ POST: Validar com SEFAZ ============
@router.post("/validar/sefaz")
async def validar_sefaz(
    cnpj: str,
    serie: str,
    numero: str,
    data_emissao: str,
    valor_total: float,
    db: Session = Depends(get_db)
):
    """
    Validar nota para SEFAZ (Receita Federal)
    
    Exemplo:
    - cnpj: "12.345.678/0001-99"
    - serie: "001"
    - numero: "000001"
    - data_emissao: "2026-09-15"
    - valor_total: 1500.50
    """
    dados = {
        "cnpj": cnpj,
        "serie": serie,
        "numero": numero,
        "data_emissao": data_emissao,
        "valor_total": valor_total
    }
    
    resultado = ValidadorFactory.validar("SEFAZ", dados)
    return {
        "tipo": "SEFAZ",
        "valido": resultado["valido"],
        "erros": resultado["erros"],
        "avisos": resultado["avisos"]
    }


# ============ POST: Validar com DATABASE ============
@router.post("/validar/database")
async def validar_database(
    consultorio_id: str,
    tipo_documento: str,
    empresa_id: str = "default",
    medico_id: str = None,
    status: str = "pendente",
    db: Session = Depends(get_db)
):
    """
    Validar dados para o banco de dados
    
    Exemplo:
    - consultorio_id: "c437c115-35ea-4140-bab8-698bb950dc6e"
    - tipo_documento: "NF-e"
    - empresa_id: "default"
    """
    dados = {
        "consultorio_id": consultorio_id,
        "tipo_documento": tipo_documento,
        "empresa_id": empresa_id,
        "medico_id": medico_id,
        "status": status
    }
    
    resultado = ValidadorFactory.validar("DATABASE", dados)
    return {
        "tipo": "DATABASE",
        "valido": resultado["valido"],
        "erros": resultado["erros"],
        "avisos": resultado["avisos"],
        "dados_ajustados": dados
    }


# ============ POST: Validar ASSINATURA ============
@router.post("/validar/assinatura")
async def validar_assinatura(
    xml: str,
    assinatura: str,
    certificado: str = None,
    db: Session = Depends(get_db)
):
    """
    Validar assinatura digital do documento
    
    Exemplo:
    - xml: "<nota>...</nota>"
    - assinatura: "-----BEGIN PKCS7-----..."
    - certificado: "cert_path"
    """
    dados = {
        "xml": xml,
        "assinatura": assinatura,
        "certificado": certificado
    }
    
    resultado = ValidadorFactory.validar("ASSINATURA", dados)
    return {
        "tipo": "ASSINATURA",
        "valido": resultado["valido"],
        "erros": resultado["erros"],
        "avisos": resultado["avisos"]
    }


# ============ POST: Validar TODAS as camadas ============
@router.post("/validar/completo")
async def validar_completo(
    cnpj: str,
    serie: str,
    numero: str,
    data_emissao: str,
    valor_total: float,
    consultorio_id: str,
    tipo_documento: str,
    xml: str,
    assinatura: str,
    db: Session = Depends(get_db)
):
    """
    Validar com TODAS as 3 camadas: SEFAZ + DATABASE + ASSINATURA
    
    Retorna resultado de cada validador
    """
    dados_sefaz = {
        "cnpj": cnpj,
        "serie": serie,
        "numero": numero,
        "data_emissao": data_emissao,
        "valor_total": valor_total
    }
    
    dados_db = {
        "consultorio_id": consultorio_id,
        "tipo_documento": tipo_documento,
        "empresa_id": "default"
    }
    
    dados_assinatura = {
        "xml": xml,
        "assinatura": assinatura
    }
    
    # Validar com todas as camadas
    resultado_sefaz = ValidadorFactory.validar("SEFAZ", dados_sefaz)
    resultado_db = ValidadorFactory.validar("DATABASE", dados_db)
    resultado_assinatura = ValidadorFactory.validar("ASSINATURA", dados_assinatura)
    
    # Validação completa = todos válidos
    valido_completo = (
        resultado_sefaz["valido"] and 
        resultado_db["valido"] and 
        resultado_assinatura["valido"]
    )
    
    return {
        "valido": valido_completo,
        "validadores": {
            "SEFAZ": {
                "valido": resultado_sefaz["valido"],
                "erros": resultado_sefaz["erros"],
                "avisos": resultado_sefaz["avisos"]
            },
            "DATABASE": {
                "valido": resultado_db["valido"],
                "erros": resultado_db["erros"],
                "avisos": resultado_db["avisos"]
            },
            "ASSINATURA": {
                "valido": resultado_assinatura["valido"],
                "erros": resultado_assinatura["erros"],
                "avisos": resultado_assinatura["avisos"]
            }
        }
    }