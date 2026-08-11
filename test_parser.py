import requests
from uuid import uuid4

# Dados de teste
url_parse = "http://localhost:8000/parse/xml"
tenant_id = "123e4567-e89b-12d3-a456-426614174000"

# Use a ingestion_id do teste anterior
ingestion_id = "471e71e8-e2f5-4c5c-a54a-815c4d22957c"

headers = {
    "X-Tenant-Id": tenant_id,
    "Ingestion-Id": ingestion_id
}

# POST
response = requests.post(url_parse, headers=headers)

# Resultado
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")