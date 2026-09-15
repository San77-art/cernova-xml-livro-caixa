from fastapi import Request
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import IdempotencyKey
import json
from datetime import datetime


async def idempotency_middleware(request: Request, call_next):
    """
    Middleware de Idempotência
    
    Verifica se requisição já foi processada.
    Se sim, retorna resultado anterior.
    Se não, processa e salva resultado.
    """
    
    # Pegar chave de idempotência do header
    idempotency_key = request.headers.get("Idempotency-Key")
    
    # Se não tem chave, processa normalmente
    if not idempotency_key:
        response = await call_next(request)
        return response
    
    # Pegar database
    db = next(get_db())
    
    try:
        # Buscar se já foi processado
        existing_key = db.query(IdempotencyKey).filter(
            IdempotencyKey.key == idempotency_key
        ).first()
        
        # Se já foi processado com SUCESSO
        if existing_key and existing_key.status == "success":
            print(f"[IDEMPOTENCY] ✅ Chave {idempotency_key} já processada! Retornando resultado anterior...")
            
            # Retornar resposta cacheada
            response_data = json.loads(existing_key.response) if existing_key.response else {}
            return JSONResponse(
                status_code=200,
                content=response_data,
                headers={"X-Idempotency-Replayed": "true"}
            )
        
        # Se está processando, aguarde
        elif existing_key and existing_key.status == "processing":
            print(f"[IDEMPOTENCY] ⏳ Chave {idempotency_key} ainda processando...")
            return JSONResponse(
                status_code=409,
                content={"erro": "Requisição já está sendo processada"}
            )
        
        # Se falhou antes, pode tentar novamente
        elif existing_key and existing_key.status == "failed":
            print(f"[IDEMPOTENCY] 🔄 Chave {idempotency_key} falhou antes, processando novamente...")
            db.delete(existing_key)
            db.commit()
        
        # CRIAR ENTRADA COMO "PROCESSING"
        if not existing_key:
            print(f"[IDEMPOTENCY] 📝 Nova chave {idempotency_key} - marcando como PROCESSING...")
            idempotency_entry = IdempotencyKey(
                key=idempotency_key,
                endpoint=str(request.url.path),
                status="processing"
            )
            db.add(idempotency_entry)
            db.commit()
        
        # PROCESSAR REQUISIÇÃO
        print(f"[IDEMPOTENCY] ⚙️ Processando {idempotency_key}...")
        response = await call_next(request)
        
        # Ler corpo da resposta
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        
        # SALVAR RESULTADO SE SUCESSO (200-299)
        if 200 <= response.status_code < 300:
            try:
                response_json = json.loads(response_body)
            except:
                response_json = {"status": "sucesso"}
            
            idempotency_entry = db.query(IdempotencyKey).filter(
                IdempotencyKey.key == idempotency_key
            ).first()
            
            if idempotency_entry:
                idempotency_entry.status = "success"
                idempotency_entry.response = json.dumps(response_json)
                idempotency_entry.atualizado_em = datetime.utcnow()
                db.commit()
                print(f"[IDEMPOTENCY] ✅ Chave {idempotency_key} - SUCESSO salvo!")
        
        # SE ERRO, MARCAR COMO FAILED
        else:
            idempotency_entry = db.query(IdempotencyKey).filter(
                IdempotencyKey.key == idempotency_key
            ).first()
            
            if idempotency_entry:
                idempotency_entry.status = "failed"
                idempotency_entry.error = response_body.decode()[:1000]
                idempotency_entry.atualizado_em = datetime.utcnow()
                db.commit()
                print(f"[IDEMPOTENCY] ❌ Chave {idempotency_key} - FALHOU")
        
        # Retornar resposta com streaming
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
    
    except Exception as e:
        print(f"[IDEMPOTENCY] 🚨 Erro no middleware: {str(e)}")
        response = await call_next(request)
        return response
    
    finally:
        db.close()