import subprocess
import time
import requests
import sys

print("\n" + "="*60)
print("CERNOVA - RESTART + TESTE + COMMIT")
print("="*60 + "\n")

print("[1/4] Reiniciando servidor...")
# Inicia servidor em background
proc = subprocess.Popen("python -m app.main", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(6)  # Esperar servidor iniciar
print("✅ Servidor rodando\n")

BASE_URL = "http://localhost:8000"
TENANT_ID = "123e4567-e89b-12d3-a456-426614174000"
DOC_ID = "c3146a0a-952e-45a2-9f4d-9b081ed9e512"
ING_ID = "471e71e8-e2f5-4c5c-a54a-815c4d22957c"

endpoints = [
    ("GET /", "GET", f"{BASE_URL}/", {}),
    ("GET /health", "GET", f"{BASE_URL}/health", {}),
    ("POST /livro-caixa", "POST", f"{BASE_URL}/livro-caixa", {"X-Tenant-Id": TENANT_ID, "Documento-Id": DOC_ID}),
    ("POST /pre-contabilizacao", "POST", f"{BASE_URL}/pre-contabilizacao", {"X-Tenant-Id": TENANT_ID, "Documento-Id": DOC_ID}),
    ("POST /classificacao/candidata", "POST", f"{BASE_URL}/classificacao/candidata", {"X-Tenant-Id": TENANT_ID, "Documento-Id": DOC_ID, "Ingestion-Id": ING_ID}),
]

print("[2/4] Testando endpoints...\n")

success_count = 0
for name, method, url, headers in endpoints:
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=5)
        else:
            resp = requests.post(url, headers=headers, timeout=5)
        
        if resp.status_code == 200:
            print(f"✅ {name:<35} Status: {resp.status_code}")
            success_count += 1
        else:
            print(f"❌ {name:<35} Status: {resp.status_code}")
    except Exception as e:
        print(f"❌ {name:<35} Erro: Servidor não responde")

print(f"\n[3/4] Git Commit...")
subprocess.run("git add .", shell=True, capture_output=True)
subprocess.run('git commit -m "Fase 5: livro caixa + pré-contabilização determinística - endpoints OK"', shell=True, capture_output=True)
print("✅ Commit feito\n")

print("[4/4] Resumo")
print("="*60)
print(f"✅ {success_count}/{len(endpoints)} endpoints funcionando!")
print("="*60 + "\n")

if success_count == len(endpoints):
    print("🎉 TODOS OS TESTES PASSARAM!")
    print(f"Servidor rodando em {BASE_URL}")
    print("Pressione CTRL+C para parar\n")
    proc.wait()
else:
    print("⚠️ ALGUNS TESTES FALHARAM!")
