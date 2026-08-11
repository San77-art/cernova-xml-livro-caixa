import requests

# URL e headers
url = "http://localhost:8000/classificacao/candidata"
tenant_id = "123e4567-e89b-12d3-a456-426614174000"
documento_id = "c3146a0a-952e-45a2-9f4d-9b081ed9e512"
ingestion_id = "471e71e8-e2f5-4c5c-a54a-815c4d22957c"

headers = {
    "X-Tenant-Id": tenant_id,
    "Documento-Id": documento_id,
    "Ingestion-Id": ingestion_id
}

# POST
response = requests.post(url, headers=headers)

# Resultado
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")