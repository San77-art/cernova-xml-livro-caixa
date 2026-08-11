import sys
sys.path.insert(0, ".")

print("\n" + "="*70)
print("VERIFICAR ENDPOINTS REGISTRADOS NO FASTAPI")
print("="*70 + "\n")

try:
    from app.main import app
    
    print("✅ main.py importado com sucesso\n")
    
    print("Endpoints registrados:\n")
    for route in app.routes:
        if hasattr(route, 'path'):
            methods = getattr(route, 'methods', [])
            print(f"  {methods} {route.path}")
    
    print("\n" + "="*70)
    
except Exception as e:
    print(f"❌ ERRO ao importar main.py:")
    print(f"   {str(e)}")
    print("\n" + "="*70)
