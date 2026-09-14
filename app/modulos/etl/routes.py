from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.modulos.etl.factory import ProcessadorFactory

router = APIRouter(prefix="/api/etl", tags=["etl"])

class ProcessarDocumentoRequest(BaseModel):
    tipo: str
    xml: str

class ProcessarDocumentoResponse(BaseModel):
    status: str
    tipo: str
    mensagem: str
    rb_id: int = None

@router.post("/processar", response_model=ProcessarDocumentoResponse)
async def processar_documento(request: ProcessarDocumentoRequest):
    """Endpoint para processar documentos fiscais"""
    
    try:
        print(f"[LOG] Requisicao recebida: tipo={request.tipo}")
        
        processador = ProcessadorFactory.criar(request.tipo)
        print(f"[LOG] Processador criado: {processador.tipo_documento}")
        
        validado = processador.validar_assinatura(request.xml)
        if not validado:
            raise HTTPException(status_code=400, detail="Assinatura invalida")
        print(f"[LOG] Assinatura validada")
        
        dados = processador.extrair_dados(request.xml)
        print(f"[LOG] Dados extraidos")
        
        rb_id = processador.inserir_no_rb(dados)
        print(f"[LOG] Inserido no RB com ID: {rb_id}")
        
        return ProcessarDocumentoResponse(
            status="sucesso",
            tipo=processador.tipo_documento,
            mensagem=f"Documento {processador.tipo_documento} processado com sucesso",
            rb_id=rb_id
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Tipo invalido: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar: {str(e)}")

@router.get("/tipos-suportados")
async def tipos_suportados():
    """Endpoint para listar tipos de documentos suportados"""
    tipos = ProcessadorFactory.obter_tipos_suportados()
    return {"tipos": tipos, "total": len(tipos)}

@router.post("/validar")
async def validar_documento(request: ProcessarDocumentoRequest):
    """Endpoint so para validar assinatura"""
    try:
        processador = ProcessadorFactory.criar(request.tipo)
        validado = processador.validar_assinatura(request.xml)
        return {
            "tipo": processador.tipo_documento,
            "valido": validado,
            "mensagem": "Assinatura valida" if validado else "Assinatura invalida"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
