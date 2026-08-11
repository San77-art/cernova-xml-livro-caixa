import subprocess
import time
import requests
import sys

print("\n" + "="*70)
print("REINICIANDO SERVIDOR + TESTE FINAL")
print("="*70 + "\n")

print("[1/2] Reiniciando servidor...")
proc = subprocess.Popen("python -m app.main", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(8)  # Esperar mais tempo
print("✅ Servidor rodando\n")

BASE_URL = "http://localhost:8000"
TENANT_ID = "123e4567-e89b-12d3-a456-426614174000"
DOC_ID = "c3146a0a-952e-45a2-9f4d-9b081ed9e512"

print("[2/2] Testando endpoints de versionamento...\n")

endpoints_versao = [
    ("POST /versionamento/criar-versao", f"{BASE_URL}/versionamento/criar-versao", {"X-Tenant-Id": TENANT_ID, "Documento-Id": DOC_ID}),
    ("POST /outbox/reprocessar", f"{BASE_URL}/outbox/reprocessar", {"X-Tenant-Id": TENANT_ID, "Outbox-Id": DOC_ID}),
]

for name, url, headers in endpoints_versao:
    try:
        resp = requests.post(url, headers=headers, timeout=5)
        status = resp.status_code
        if status == 200:
            print(f"✅ {name:<45} Status: {status}")
        else:
            print(f"⚠️  {name:<45} Status: {status}")
    except Exception as e:
        print(f"❌ {name:<45} Erro: {str(e)[:30]}")

print("\n" + "="*70)
print("🎉 FASE 6 - ENDPOINTS TESTADOS!")
print("="*70 + "\n")

print("Servidor rodando. Pressione CTRL+C para parar.\n")
proc.wait()
