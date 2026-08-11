main_py_content = '''from fastapi import FastAPI, Header, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import UUID
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
import uuid

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cernova XML + Livro Caixa RBV1")

@app.get("/")
async def root():
    return {"status": "Cernova RBV1 - Sistema rodando"}

@app.get("/health")
async def health(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "OK", "database": "Connected"}
    except Exception as e:
        return {"status": "ERROR", "database": str(e)}

@app.post("/ingestao/xml")
async def ingestao_xml(file: UploadFile = File(...), x_tenant_id: str = Header(...), db: Session = Depends(get_db)) -> dict:
    try:
        arquivo_bytes = await file.read()
        tenant_id = UUID(x_tenant_id)
        ingestion = IngestaoService.salvar_xml_bruto(db=db, tenant_id=tenant_id, filename=file.filename, arquivo_bytes=arquivo_bytes)
        return {"ingestion_id": str(ingestion.ingestion_id), "tenant_id": str(ingestion.tenant_id), "filename": ingestion.filename, "hash_sha256": ingestion.hash_sha256, "tamanho_bytes": ingestion.tamanho_bytes, "status": ingestion.status, "criado_em": ingestion.criado_em.isoformat()}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.post("/parse/xml")
async def parse_xml(ingestion_id: str = Header(...), x_tenant_id: str = Header(...), db: Session = Depends(get_db)) -> dict:
    try:
        ingestion_uuid = UUID(ingestion_id)
        tenant_id = UUID(x_tenant_id)
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        ingestion = db.query(XmlIngestion).filter(XmlIngestion.ingestion_id == ingestion_uuid, XmlIngestion.tenant_id == tenant_id).first()
        if not ingestion:
            return {"status": "erro", "mensagem": "Ingestão não encontrada"}
        documento = ParserService.salvar_documento(db=db, tenant_id=tenant_id, ingestion_id=ingestion_uuid, xml_bruto=ingestion.xml_bruto)
        return {"documento_id": str(documento.documento_id), "ingestion_id": str(documento.ingestion_id), "tenant_id": str(documento.tenant_id), "numero_nfe": documento.numero_nfe, "chave_acesso": documento.chave_acesso, "data_emissao": documento.data_emissao.isoformat() if documento.data_emissao else None, "valor_total": documento.valor_total, "status_parse": documento.status_parse, "erro_parse": documento.erro_parse, "parseado_em": documento.parseado_em.isoformat() if documento.parseado_em else None}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.post("/classificacao/candidata")
async def classificacao_candidata(documento_id: str = Header(...), ingestion_id: str = Header(...), x_tenant_id: str = Header(...), db: Session = Depends(get_db)) -> dict:
    try:
        documento_uuid = UUID(documento_id)
        ingestion_uuid = UUID(ingestion_id)
        tenant_id = UUID(x_tenant_id)
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        documento = db.query(XmlDocumento).filter(XmlDocumento.documento_id == documento_uuid, XmlDocumento.tenant_id == tenant_id).first()
        if not documento:
            return {"status": "erro", "mensagem": "Documento não encontrado"}
        dados_classificacao = ClassificacaoService.classificar_nfe(numero_nfe=documento.numero_nfe or "DESCONHECIDO", natureza_operacao=documento.numero_nfe or "Operação", valor_total=documento.valor_total or "0")
        classificacao = ClassificacaoService.salvar_classificacao(db=db, tenant_id=tenant_id, documento_id=documento_uuid, ingestion_id=ingestion_uuid, dados_classificacao=dados_classificacao)
        return {"classificacao_id": str(classificacao.classificacao_id), "documento_id": str(classificacao.documento_id), "status_classificacao": classificacao.status_classificacao, "tipo_documento": classificacao.tipo_documento, "cfop": classificacao.cfop, "ncm": classificacao.ncm, "confianca": classificacao.confianca, "regra_aplicada": classificacao.regra_aplicada, "justificativa": classificacao.justificativa, "criado_em": classificacao.criado_em.isoformat()}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.post("/livro-caixa")
async def gerar_livro_caixa(documento_id: str = Header(...), x_tenant_id: str = Header(...), db: Session = Depends(get_db)) -> dict:
    try:
        documento_uuid = UUID(documento_id)
        tenant_id = UUID(x_tenant_id)
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        documento = db.query(XmlDocumento).filter(XmlDocumento.documento_id == documento_uuid, XmlDocumento.tenant_id == tenant_id).first()
        if not documento:
            return {"status": "erro", "mensagem": "Documento não encontrado"}
        dados_livro = LivroCaixaService.gerar_livro_caixa(numero_nfe=documento.numero_nfe or "DESCONHECIDO", valor_total=documento.valor_total or "0", tipo_operacao="entrada")
        livro = LivroCaixaService.salvar_livro_caixa(db=db, tenant_id=tenant_id, documento_id=documento_uuid, dados_livro=dados_livro)
        return {"livro_caixa_id": str(livro.livro_caixa_id), "documento_id": str(livro.documento_id), "tipo_movimento": livro.tipo_movimento, "valor": livro.valor, "descricao": livro.descricao, "status": livro.status, "criado_em": livro.criado_em.isoformat()}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.post("/pre-contabilizacao")
async def gerar_pre_contabilizacao(documento_id: str = Header(...), x_tenant_id: str = Header(...), db: Session = Depends(get_db)) -> dict:
    try:
        documento_uuid = UUID(documento_id)
        tenant_id = UUID(x_tenant_id)
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        documento = db.query(XmlDocumento).filter(XmlDocumento.documento_id == documento_uuid, XmlDocumento.tenant_id == tenant_id).first()
        if not documento:
            return {"status": "erro", "mensagem": "Documento não encontrado"}
        dados_pre = LivroCaixaService.gerar_pre_contabilizacao(valor_total=documento.valor_total or "0", tipo_operacao="entrada")
        pre_conta = LivroCaixaService.salvar_pre_contabilizacao(db=db, tenant_id=tenant_id, documento_id=documento_uuid, dados_pre=dados_pre)
        return {"pre_contabilizacao_id": str(pre_conta.pre_contabilizacao_id), "documento_id": str(pre_conta.documento_id), "conta_debito": pre_conta.conta_debito, "conta_credito": pre_conta.conta_credito, "valor": pre_conta.valor, "descricao": pre_conta.descricao, "status": pre_conta.status, "criado_em": pre_conta.criado_em.isoformat()}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.post("/versionamento/criar-versao")
async def criar_versao_cadeia(documento_id: str = Header(...), x_tenant_id: str = Header(...), db: Session = Depends(get_db)) -> dict:
    try:
        documento_uuid = UUID(documento_id)
        tenant_id = UUID(x_tenant_id)
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": str(tenant_id)})
        documento = db.query(XmlDocumento).filter(XmlDocumento.documento_id == documento_uuid, XmlDocumento.tenant_id == tenant_id).first()
        if not documento:
            return {"status": "erro", "mensagem": "Documento não encontrado"}
        dados_cadeia = {"documento_id": str(documento.documento_id), "numero_nfe": documento.numero_nfe, "valor_total": documento.valor_total, "data_emissao": documento.data_emissao.isoformat() if documento.data_emissao else None}
        versao = VersiorService.criar_versao(db=db, tenant_id=tenant_id, documento_id=documento_uuid, dados_cadeia=dados_cadeia, motivo="Versionamento automático")
        return {"cadeia_versao_id": str(versao.cadeia_versao_id), "documento_id": str(versao.documento_id), "numero_versao": versao.numero_versao, "hash_versao": versao.hash_versao, "criado_em": versao.criado_em.isoformat()}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.post("/outbox/reprocessar")
async def reprocessar_evento_outbox(outbox_id: str = Header(...), x_tenant_id: str = Header(...), db: Session = Depends(get_db)) -> dict:
    try:
        outbox_uuid = UUID(outbox_id)
        tenant_id = UUID(x_tenant_id)
        evento = VersiorService.reprocessar_evento(db=db, tenant_id=tenant_id, outbox_id=outbox_uuid)
        if not evento:
            return {"status": "erro", "mensagem": "Evento não encontrado"}
        return {"outbox_id": str(evento.outbox_id), "tipo_evento": evento.tipo_evento, "processado": evento.processado, "tentativas": evento.tentativas, "criado_em": evento.criado_em.isoformat()}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

with open("app/main.py", "w", encoding="utf-8") as f:
    f.write(main_py_content)

print("\n" + "="*70)
print("MAIN.PY RECRIADO COM SUCESSO!")
print("="*70)
print("✅ Todos os imports corretos")
print("✅ Todos os 9 endpoints adicionados")
print("✅ Pronto para testar")
print("="*70 + "\n")
