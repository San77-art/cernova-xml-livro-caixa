# ═══════════════════════════════════════════════════════════════════════════════
# CERNOVA RBV1 v2.0 - DEPLOYMENT AUTOMÁTICO COM MÓDULO MEDICINA
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host "
╔═══════════════════════════════════════════════════════════════════════════════╗
║                   CERNOVA RBV1 v2.0 - DEPLOYMENT AUTOMÁTICO                  ║
║              Integração Módulo Medicina com XML + Livro Caixa                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

# ───────────────────────────────────────────────────────────────────────────────
# PASSO 1: Restaurar Ambiente
# ───────────────────────────────────────────────────────────────────────────────

Write-Host "`n[1/8] Restaurando ambiente..." -ForegroundColor Yellow
cd C:\Users\User\cernova-xml-livro-caixa
if (-not (Test-Path "venv\Scripts\activate")) {
    Write-Host "❌ Ambiente virtual não encontrado!" -ForegroundColor Red
    exit 1
}

& venv\Scripts\activate
Write-Host "✅ Ambiente ativado" -ForegroundColor Green

# ───────────────────────────────────────────────────────────────────────────────
# PASSO 2: Copiar Arquivos
# ───────────────────────────────────────────────────────────────────────────────

Write-Host "`n[2/8] Copiando arquivos..." -ForegroundColor Yellow

# Backup do main.py antigo
Copy-Item app\main.py app\main.py.backup -Force
Write-Host "   ✅ Backup de main.py criado"

# Criar arquivo main.py completo com Medicina
@'
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

# Database
from app.database.session import Base, engine, get_db

# Modulos
from app.modulos.ingestao import routes as ingestao_routes
from app.modulos.parser import routes as parser_routes
from app.modulos.classificacao import routes as classificacao_routes
from app.modulos.livro_caixa import routes as livro_caixa_routes
from app.modulos.medicina import routes as medicina_routes

# Config
from app.config.emails import EmailService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
    logger.info("🚀 Iniciando Cernova RBV1 v2.0...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database criado/validado")
    yield
    # Shutdown
    logger.info("🔴 Encerrando Cernova RBV1...")

app = FastAPI(
    title="Cernova RBV1",
    description="Motor Documental Transversal - XML, Livro Caixa, Medicina & Agro",
    version="2.0.0",
    lifespan=lifespan
)

# ============ HEALTH CHECK ============

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check com status do banco"""
    try:
        db = next(get_db())
        db.execute("SELECT 1")
        db.close()
        return {
            "status": "OK",
            "database": "Connected",
            "version": "2.0.0",
            "modulos": ["xml", "livro_caixa", "medicina"]
        }
    except Exception as e:
        logger.error(f"❌ Health check falhou: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "ERROR", "database": "Disconnected"}
        )

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "status": "Cernova RBV1 - Sistema rodando",
        "versao": "2.0.0",
        "modulos": ["ingestao", "parser", "classificacao", "livro_caixa", "medicina"],
        "docs": "/docs",
        "emails": {
            "suporte": "suporte@cernova.com.br",
            "admin": "admin@cernova.com.br",
            "suporte_medicina": "suporte-medicina@cernova.com.br"
        }
    }

# ============ REGISTRAR ROUTERS ============

app.include_router(ingestao_routes.router)
app.include_router(parser_routes.router)
app.include_router(classificacao_routes.router)
app.include_router(livro_caixa_routes.router)
app.include_router(medicina_routes.router)

# ============ ERROR HANDLERS ============

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint não encontrado", "path": str(request.url)}
    )

@app.exception_handler(500)
async def server_error_handler(request, exc):
    logger.error(f"❌ Erro no servidor: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )

# ============ STARTUP EVENTS ============

@app.on_event("startup")
async def startup_event():
    """Executado ao iniciar"""
    logger.info("✅ Cernova RBV1 v2.0 iniciado com sucesso!")
    logger.info("📊 Endpoints disponíveis:")
    logger.info("   - GET /health (Health Check)")
    logger.info("   - GET / (Info)")
    logger.info("   - POST /ingestao/xml (Upload XML)")
    logger.info("   - GET /classificacoes (Classificações)")
    logger.info("   - GET /livro-caixa (Livro Caixa)")
    logger.info("   - POST /medicina/consultorios (Novo Consultório)")
    logger.info("   - POST /medicina/medicos (Novo Médico)")
    logger.info("   - POST /medicina/pacientes (Novo Paciente)")
    logger.info("   - POST /medicina/consultas (Agendar Consulta)")
    logger.info("   - GET /docs (Swagger UI)")

@app.on_event("shutdown")
async def shutdown_event():
    """Executado ao desligar"""
    logger.info("🔴 Cernova RBV1 encerrado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
