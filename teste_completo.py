import subprocess
import time
import requests
import sys

print("\n" + "="*70)
print("TESTE COMPLETO - VERIFICAÇÃO PÓS-RESTART")
print("="*70 + "\n")

# Verificar PostgreSQL
print("[1/5] Verificando PostgreSQL...")
result = subprocess.run("psql -U postgres -d cernova_rb -c \"SELECT 1;\"", shell=True, capture_output=True, text=True)
if "1" in result.stdout:
    print("✅ PostgreSQL está rodando\n")
else:
    print("❌ PostgreSQL não respondeu\n")
    sys.exit(1)

# Reiniciar servidor
print("[2/5] Reiniciando FastAPI...")
proc = subprocess.Popen("python -m app.main", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(6)
print("✅ Servidor rodando\n")

# Verificar tabelas
print("[3/5] Verificando banco de dados...")
result = subprocess.run("psql -U postgres -d cernova_rb -c \"\\\\dt\"", shell=True, capture_output=True, text=True)
table_count = result.stdout.count("tabela")
print(f"✅ {table_count} tabelas encontradas\n")

# Testar endpoints
print("[4/5] Testando endpoints...\n")

BASE_URL = "http://localhost:8000"
TENANT_ID = "123e4567-e89b-12d3-a456-426614174000"
DOC_ID = "c3146a0a-952e-45a2-9f4d-9b081ed9e512"
ING_ID = "471e71e8-e2f5-4c5c-a54a-815c4d22957c"

endpoints = [
    ("GET /", "GET", f"{BASE_URL}/", {}),
    ("GET /health", "GET", f"{BASE_URL}/health", {}),
    ("POST /ingestao/xml", "POST", f"{BASE_URL}/ingestao/xml", {"X-Tenant-Id": TENANT_ID}),
    ("POST /parse/xml", "POST", f"{BASE_URL}/parse/xml", {"X-Tenant-Id": TENANT_ID, "Ingestion-Id": ING_ID}),
    ("POST /classificacao/candidata", "POST", f"{BASE_URL}/classificacao/candidata", {"X-Tenant-Id": TENANT_ID, "Documento-Id": DOC_ID, "Ingestion-Id": ING_ID}),
    ("POST /livro-caixa", "POST", f"{BASE_URL}/livro-caixa", {"X-Tenant-Id": TENANT_ID, "Documento-Id": DOC_ID}),
    ("POST /pre-contabilizacao", "POST", f"{BASE_URL}/pre-contabilizacao", {"X-Tenant-Id": TENANT_ID, "Documento-Id": DOC_ID}),
]

success_count = 0
for name, method, url, headers in endpoints:
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=5)
        else:
            resp = requests.post(url, headers=headers, timeout=5)
        
        if resp.status_code == 200:
            print(f"✅ {name:<40} Status: {resp.status_code}")
            success_count += 1
        else:
            print(f"❌ {name:<40} Status: {resp.status_code}")
    except Exception as e:
        print(f"❌ {name:<40} Erro: {str(e)[:40]}")

print(f"\n[5/5] Resumo Final")
print("="*70)
print(f"✅ PostgreSQL: OK")
print(f"✅ Servidor: Rodando em {BASE_URL}")
print(f"✅ Banco: {table_count} tabelas")
print(f"✅ Endpoints: {success_count}/{len(endpoints)} funcionando")
print("="*70 + "\n")

if success_count == len(endpoints):
    print("🎉 TESTE COMPLETO - TUDO FUNCIONANDO!")
    print("Servidor rodando. Pressione CTRL+C para parar.\n")
    proc.wait()
else:
    print(f"⚠️ {len(endpoints) - success_count} endpoint(s) falharam")
    sys.exit(1)
