# Ler main.py atual
with open("app/main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Verificar se já tem imports de versionamento
if "from app.modulos.versionamento" not in content:
    # Adicionar imports ANTES de "# Criar tabelas"
    new_imports = '''from app.modulos.versionamento.models import CadeiaVersao, Outbox
from app.modulos.versionamento.schemas import CadeiaVersaoResponse, OutboxResponse
from app.modulos.versionamento.service import VersiorService
'''
    
    content = content.replace(
        "import uuid\n\n# Criar",
        f"import uuid\n{new_imports}\n# Criar"
    )

# Adicionar endpoints ANTES do "if __name__"
new_endpoints = '''

@app.post("/versionamento/criar-versao")
async def criar_versao_cadeia(
    documento_id: str = Header(...),
    x_tenant_id: str = Header(...),
    db: Session = Depends(get_db)
) -> dict:
    """
    Cria nova versão da cadeia (R6 - Versionamento).
    Versionamento automático de todas as alterações.
    Segue R6 da ADR-001.
    """
    
    try:
        documento_uuid = UUID(documento_id)
        tenant_id = UUID(x_tenant_id)
        
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        documento = db.query(XmlDocumento).filter(
            XmlDocumento.documento_id == documento_uuid,
            XmlDocumento.tenant_id == tenant_id
        ).first()
        
        if not documento:
            return {"status": "erro", "mensagem": "Documento não encontrado"}
        
        # Dados da cadeia
        dados_cadeia = {
            "documento_id": str(documento.documento_id),
            "numero_nfe": documento.numero_nfe,
            "valor_total": documento.valor_total,
            "data_emissao": documento.data_emissao.isoformat() if documento.data_emissao else None
        }
        
        # Criar versão
        versao = VersiorService.criar_versao(
            db=db,
            tenant_id=tenant_id,
            documento_id=documento_uuid,
            dados_cadeia=dados_cadeia,
            motivo="Versionamento automático"
        )
        
        return {
            "cadeia_versao_id": str(versao.cadeia_versao_id),
            "documento_id": str(versao.documento_id),
            "numero_versao": versao.numero_versao,
            "hash_versao": versao.hash_versao,
            "criado_em": versao.criado_em.isoformat()
        }
        
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.post("/outbox/reprocessar")
async def reprocessar_evento_outbox(
    outbox_id: str = Header(...),
    x_tenant_id: str = Header(...),
    db: Session = Depends(get_db)
) -> dict:
    """
    Reprocessa evento do Outbox (R10 - Idempotência).
    Marca evento para reprocessamento garantindo idempotência.
    Segue R10 da ADR-001.
    """
    
    try:
        outbox_uuid = UUID(outbox_id)
        tenant_id = UUID(x_tenant_id)
        
        evento = VersiorService.reprocessar_evento(
            db=db,
            tenant_id=tenant_id,
            outbox_id=outbox_uuid
        )
        
        if not evento:
            return {"status": "erro", "mensagem": "Evento não encontrado"}
        
        return {
            "outbox_id": str(evento.outbox_id),
            "tipo_evento": evento.tipo_evento,
            "processado": evento.processado,
            "tentativas": evento.tentativas,
            "criado_em": evento.criado_em.isoformat()
        }
        
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
'''

content = content.replace(
    "if __name__ == \"__main__\":",
    f"{new_endpoints}\n\nif __name__ == \"__main__\":"
)

# Salvar main.py atualizado
with open("app/main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("\n" + "="*70)
print("MAIN.PY ATUALIZADO COM SUCESSO!")
print("="*70)
print("✅ Imports adicionados")
print("✅ Endpoint /versionamento/criar-versao adicionado")
print("✅ Endpoint /outbox/reprocessar adicionado")
print("="*70 + "\n")
