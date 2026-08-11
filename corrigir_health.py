with open("app/main.py", "r", encoding="utf-8") as f:
    content = f.read()

old = 'db.execute("SELECT 1")'
new = 'db.execute(text("SELECT 1"))'

if old in content:
    content = content.replace(old, new)
    with open("app/main.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Corrigido!")
else:
    print("Já estava correto")
