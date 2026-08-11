import subprocess
import time
import requests
import sys
import os

print("\n" + "="*60)
print("CERNOVA - TESTE DE ENDPOINTS")
print("="*60 + "\n")

print("[1/3] Esperando servidor ficar pronto...")
time.sleep(3)

BASE_URL = "http://localhost:8000"
TENANT_ID = "123e4567-e89b-12d3-a456-426614174000"
DOC_ID = "c3146a0a-952e-45a2-9f4d-9b081ed9e512"
ING_ID = "471e71e8-e2f5-4c5c-a54a-815c4d22957c"

endpoints = [
    ("GET /", "GET", f"{BASE_URL}/", {}),
    ("GET /health", "GET", f"{BASE_URL}/health", {}),
    ("POST /livro-caixa", "POST", f"{BASE_URL}/livro-caixa", {"X-Tenant-Id": TENANT_ID, "Documento-Id": DOC_ID}),
    ("POST /pre-contabilizacao", "POST", f"{BASE_URL}/pre-contabilizacao", {"X-Tenant-Id": TENANT_ID, "Documento-Id": DOC_ID}),
]

print("\n[2/3] Testando endpoints...\n")

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
        print(f"❌ {name:<35} Erro: {str(e)}")

print(f"\n[3/3] Resumo")
print("="*60)
print(f"✅ {success_count}/{len(endpoints)} endpoints funcionando!")
print("="*60 + "\n")

if success_count == len(endpoints):
    print("🎉 TODOS OS TESTES PASSARAM!")
    sys.exit(0)
else:
    print("⚠️ ALGUNS TESTES FALHARAM!")
    sys.exit(1)
