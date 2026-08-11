import os
import subprocess

print("\n" + "="*70)
print("INSPEÇÃO COMPLETA DO PROJETO CERNOVA")
print("="*70 + "\n")

# 1. Estrutura de pastas
print("[1] ESTRUTURA DE PASTAS")
print("-"*70)
for root, dirs, files in os.walk("app"):
    level = root.replace("app", "").count(os.sep)
    indent = " " * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = " " * 2 * (level + 1)
    for file in files:
        if file.endswith(".py"):
            print(f"{subindent}{file}")

# 2. Arquivos Python
print("\n[2] ARQUIVOS PYTHON")
print("-"*70)
result = subprocess.run("ls -Recurse app -Include '*.py' | Measure-Object", shell=True, capture_output=True, text=True)
py_files = subprocess.run("ls -Recurse app -Include '*.py' -File", shell=True, capture_output=True, text=True)
print(py_files.stdout)

# 3. Git Status
print("[3] GIT STATUS")
print("-"*70)
result = subprocess.run("git status --short", shell=True, capture_output=True, text=True)
if result.stdout.strip():
    print(result.stdout)
else:
    print("✅ Tudo commitado (sem mudanças pendentes)")

# 4. Git Log (últimos 8 commits)
print("\n[4] GIT LOG (últimas 8 versões)")
print("-"*70)
result = subprocess.run("git log --oneline -8", shell=True, capture_output=True, text=True)
print(result.stdout)

# 5. Banco de dados
print("[5] BANCO DE DADOS")
print("-"*70)
result = subprocess.run("psql -U postgres -d cernova_rb -c \"\\\\dt\"", shell=True, capture_output=True, text=True)
print(result.stdout)

# 6. Tamanho do projeto
print("[6] TAMANHO DO PROJETO")
print("-"*70)
result = subprocess.run("du -sh app", shell=True, capture_output=True, text=True)
print(f"Pasta app: {result.stdout.strip()}")

result = subprocess.run("du -sh .", shell=True, capture_output=True, text=True)
print(f"Projeto total: {result.stdout.strip()}")

print("\n" + "="*70)
print("INSPEÇÃO COMPLETA")
print("="*70 + "\n")
