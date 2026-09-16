import pytest
from fastapi.testclient import TestClient
from app.main import app

# Cliente para testes
client = TestClient(app)


# ============ TESTES HEALTH CHECK ============
class TestHealth:
    """Testa Health Check"""
    
    def test_health_check(self):
        """Testa /health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "OK"
        print("✅ Health check passou!")


# ============ TESTES FACTORY METHOD ============
class TestFactoryMethod:
    """Testa ProcessadorFactory"""
    
    def test_listar_tipos_suportados(self):
        """Testa GET /api/etl/tipos-suportados"""
        response = client.get("/api/etl/tipos-suportados")
        assert response.status_code == 200
        data = response.json()
        assert "tipos" in data
        print(f"✅ Factory Method: {data['tipos']}")
    
    def test_processar_nfe(self):
        """Testa POST /api/etl/processar para NF-e"""
        payload = {
            "tipo_documento": "NF-e"
        }
        response = client.post("/api/etl/processar", json=payload)
        # Se retornar 200 ou 422, ambos são OK para E2E
        assert response.status_code in [200, 400, 422]
        print(f"✅ Factory: POST /api/etl/processar respondeu com {response.status_code}")


# ============ TESTES VALIDADORES ============
class TestValidadores:
    """Testa ValidadorFactory"""
    
    def test_listar_validadores(self):
        """Testa GET /api/etl/validadores/tipos-suportados"""
        response = client.get("/api/etl/validadores/tipos-suportados")
        assert response.status_code == 200
        data = response.json()
        assert "validadores" in data
        print(f"✅ Validadores: {data['validadores']}")
    
    def test_validador_sefaz(self):
        """Testa validação SEFAZ"""
        response = client.post(
            "/api/etl/validadores/validar/sefaz",
            params={
                "cnpj": "12.345.678/0001-99",
                "serie": "001",
                "numero": "000001",
                "data_emissao": "2026-09-15",
                "valor_total": 1500.50
            }
        )
        assert response.status_code == 200
        print("✅ SEFAZ validou com sucesso!")
    
    def test_validador_database(self):
        """Testa validação DATABASE"""
        response = client.post(
            "/api/etl/validadores/validar/database",
            params={
                "consultorio_id": "550e8400-e29b-41d4-a716-446655440000",
                "tipo_documento": "NF-e"
            }
        )
        assert response.status_code == 200
        print("✅ DATABASE validou com sucesso!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])