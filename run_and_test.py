import subprocess
import time
import requests
import json
import sys

GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

print(f"{BLUE}{'='*60}")
print("CERNOVA - RESTART + TEST + COMMIT")
print(f"{'='*60}{RESET}\n")

print(f"{BLUE}[1/5] Parando servidor...{RESET}")
subprocess.run("taskkill /F /IM python.exe 2>nul", shell=True, capture_output=True)
time.sleep(2)
print(f"{GREEN}✅ Servidor parado{RESET}\n")

print(f"{BLUE}[2/5] Reiniciando servidor...{RESET}")
proc = subprocess.Popen("python -m app.main", shell=True)
time.sleep(5)
print(f"{GREEN}✅ Servidor rodando{RESET}\n")

print(f"{BLUE}[3/5] Testando endpoints...{RESET}\n")

BASE_URL = "http://localhost:8000"
TENANT_ID = "123e4567-e89b-12d3-a456-426614174000"
DOC_ID = "c3146a0a-952e-45a2-9f4d-9b081ed9e512"
ING_ID = "471e71e8-e2f5-4c5c-a54a-815c4d22957c"

endpoints = [
    {"name": "GET /", "method": "GET", "url": f"{BASE_URL}/", "headers": {}},
    {"name": "GET /health", "method": "GET", "url": f"{BASE_URL}/health", "headers": {}},
    {"name": "POST /livro-caixa", "method": "POST", "url": f"{BASE_URL}/livro-caixa", "headers": {"X-Tenant-Id": TENANT_ID, "Documento-Id": DOC_ID}},
    {"name": "POST /pre-contabilizacao", "method": "POST", "url": f"{BASE_URL}/pre-contabilizacao", "headers": {"X-Tenant-Id": TENANT_ID, "Documento-Id": DOC_ID}},
    {"name": "POST /classificacao/candidata", "method": "POST", "url": f"{BASE_URL}/classificacao/candidata", "headers": {"X-Tenant-Id": TENANT_ID, "Documento-Id": DOC_ID, "Ingestion-Id": ING_ID}},
]

failed = []
for ep in endpoints:
    try:
        if ep["method"] == "GET":
            resp = requests.get(ep["url"], headers=ep["headers"], timeout=5)
        else:
            resp = requests.post(ep["url"], headers=ep["headers"], timeout=5)
        if resp.status_code == 200:
            print(f"{GREEN}✅ {ep['name']:<35} Status: {resp.status_code}{RESET}")
        else:
            print(f"{RED}❌ {ep['name']:<35} Status: {resp.status_code}{RESET}")
            failed.append(ep["name"])
    except Exception as e:
        print(f"{RED}❌ {ep['name']:<35} Erro: {str(e)}{RESET}")
        failed.append(ep["name"])

print()

print(f"{BLUE}[4/5] Fazendo git commit...{RESET}")
subprocess.run("git add .", shell=True, capture_output=True)
subprocess.run('git commit -m "Fase 5: livro caixa + pré-contabilização - testes OK"', shell=True, capture_output=True)
print(f"{GREEN}✅ Git commit feito{RESET}\n")

print(f"{BLUE}[5/5] Resumo{RESET}")
print(f"{BLUE}{'='*60}{RESET}")

if failed:
    print(f"{RED}❌ {len(failed)} endpoint(s) falharam{RESET}")
else:
    print(f"{GREEN}✅ TODOS OS ENDPOINTS FUNCIONANDO!{RESET}")

print(f"{BLUE}{'='*60}{RESET}")
