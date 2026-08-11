import psycopg2
try:
    conn = psycopg2.connect(host="cernova-rb-db.c61cukey2jxy.us-east-1.rds.amazonaws.com", user="postgres", password="CernovaRB2026!", dbname="cernova_rb", port=5432)
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(" CONECTADO COM SUCESSO!")
    print(f"PostgreSQL: {version[0]}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f" ERRO: {e}")
