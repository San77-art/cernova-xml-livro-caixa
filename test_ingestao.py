import requests
from uuid import uuid4

# URL e headers
url = "http://localhost:8000/ingestao/xml"
tenant_id = "123e4567-e89b-12d3-a456-426614174000"
headers = {"X-Tenant-Id": tenant_id}

# Arquivo
with open("test.xml", "rb") as f:
    files = {"file": ("test.xml", f, "application/xml")}
    
    # POST
    response = requests.post(url, files=files, headers=headers)
    
    # Resultado
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")