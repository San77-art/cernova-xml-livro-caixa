import pytest
import requests

BASE_URL = "http://localhost:8000"
TENANT_ID = "123e4567-e89b-12d3-a456-426614174000"

def test_health():
    resp = requests.get(f"{BASE_URL}/health")
    assert resp.status_code == 200

def test_root():
    resp = requests.get(f"{BASE_URL}/")
    assert resp.status_code == 200

def test_endpoints():
    headers = {"X-Tenant-Id": TENANT_ID, "Ingestion-Id": "471e71e8-e2f5-4c5c-a54a-815c4d22957c"}
    resp = requests.post(f"{BASE_URL}/parse/xml", headers=headers)
    assert resp.status_code == 200
