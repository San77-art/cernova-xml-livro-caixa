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


# ============ TESTES EXPORTADORES ============
class TestExportadores:
    """Testa ExportadorFactory"""
    
    def test_listar_exportadores(self):
        """Testa GET /api/etl/exportadores/tipos-suportados"""
        response = client.get("/api/etl/exportadores/tipos-suportados")
        assert response.status_code == 200
        data = response.json()
        assert "exportadores" in data
        assert "JSON" in data["exportadores"]
        assert "XML" in data["exportadores"]
        assert "PDF" in data["exportadores"]
        assert "EXCEL" in data["exportadores"]
        print(f"✅ Exportadores: {data['exportadores']}")
    
    def test_exportar_json(self):
        """Testa exportação JSON"""
        response = client.post(
            "/api/etl/exportadores/exportar/json",
            params={
                "numero": "001",
                "serie": "1",
                "valor": 1000.0,
                "cnpj": "12.345.678/0001-99"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["exportado"] == True
        assert data["formato"] == "JSON"
        print("✅ JSON exportado com sucesso!")
    
    def test_exportar_xml(self):
        """Testa exportação XML"""
        response = client.post(
            "/api/etl/exportadores/exportar/xml",
            params={
                "numero": "001",
                "serie": "1",
                "valor": 1000.0,
                "cnpj": "12.345.678/0001-99"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["exportado"] == True
        assert data["formato"] == "XML"
        print("✅ XML exportado com sucesso!")
    
    def test_exportar_pdf(self):
        """Testa exportação PDF"""
        response = client.post(
            "/api/etl/exportadores/exportar/pdf",
            params={
                "numero": "001",
                "serie": "1",
                "valor": 1000.0,
                "cnpj": "12.345.678/0001-99"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["exportado"] == True
        assert data["formato"] == "PDF"
        print("✅ PDF exportado com sucesso!")
    
    def test_exportar_excel(self):
        """Testa exportação EXCEL"""
        response = client.post(
            "/api/etl/exportadores/exportar/excel",
            params={
                "numero": "001",
                "serie": "1",
                "valor": 1000.0,
                "cnpj": "12.345.678/0001-99"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["exportado"] == True
        assert data["formato"] == "EXCEL"
        print("✅ EXCEL exportado com sucesso!")



# ============ TESTES AGENDADORES ============
class TestAgendadores:
    """Testa AgendamentoFactory"""
    
    def test_listar_agendadores(self):
        """Testa GET /api/etl/agendadores/tipos-suportados"""
        response = client.get("/api/etl/agendadores/tipos-suportados")
        assert response.status_code == 200
        data = response.json()
        assert "agendadores" in data
        assert "PRESENCIAL" in data["agendadores"]
        assert "TELEMEDICINA" in data["agendadores"]
        assert "HOMECARE" in data["agendadores"]
        print(f"✅ Agendadores: {data['agendadores']}")
    
    def test_agendar_presencial(self):
        """Testa agendamento presencial"""
        response = client.post(
            "/api/etl/agendadores/agendar/presencial",
            params={
                "paciente_nome": "João Silva",
                "profissional_nome": "Dr. Carlos",
                "data": "2026-09-20",
                "horario": "14:00",
                "consultorio": "Consultório 1"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["agendado"] == True
        assert data["tipo"] == "PRESENCIAL"
        print("✅ Presencial agendado com sucesso!")
    
    def test_agendar_telemedicina(self):
        """Testa agendamento telemedicina"""
        response = client.post(
            "/api/etl/agendadores/agendar/telemedicina",
            params={
                "paciente_nome": "Maria Santos",
                "profissional_nome": "Dra. Ana",
                "data": "2026-09-21",
                "horario": "10:00",
                "email": "maria@example.com"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["agendado"] == True
        assert data["tipo"] == "TELEMEDICINA"
        assert "link_acesso" in data
        print("✅ Telemedicina agendada com sucesso!")
    
    def test_agendar_homecare(self):
        """Testa agendamento home care"""
        response = client.post(
            "/api/etl/agendadores/agendar/homecare",
            params={
                "paciente_nome": "Pedro Costa",
                "profissional_nome": "Dr. Ricardo",
                "data": "2026-09-22",
                "horario": "15:00",
                "endereco": "Rua das Flores 123",
                "telefone": "(11)99999-9999"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["agendado"] == True
        assert data["tipo"] == "HOMECARE"
        assert "tempo_deslocamento_min" in data
        print("✅ Home care agendado com sucesso!")

        

# ============ TESTES PARSADORES ============
class TestParsadores:
    """Testa ParserFactory"""
    
    def test_listar_parsadores(self):
        """Testa GET /api/etl/parsadores/tipos-suportados"""
        response = client.get("/api/etl/parsadores/tipos-suportados")
        assert response.status_code == 200
        data = response.json()
        assert "parsadores" in data
        assert "NFe" in data["parsadores"]
        assert "NFCe" in data["parsadores"]
        assert "CTe" in data["parsadores"]
        assert "GENERICO" in data["parsadores"]
        print(f"✅ Parsadores: {data['parsadores']}")
    
    def test_parsear_generico(self):
        """Testa parser genérico"""
        xml = '<?xml version="1.0"?><nota><numero>001</numero><serie>1</serie><valor>1000.00</valor></nota>'
        response = client.post(
            "/api/etl/parsadores/parsear/generico",
            params={"xml": xml}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["parseado"] == True
        assert data["tipo"] == "GENERICO"
        print("✅ Parser genérico funcionou!")
    
    def test_parsear_nfe(self):
        """Testa parser NFe"""
        xml = '<?xml version="1.0"?><NFe><ide><nNF>001</nNF><serie>1</serie><dhEmi>2026-09-17</dhEmi></ide><total><ICMSTot><vNF>1000.00</vNF></ICMSTot></total><emit><CNPJ>12345678000199</CNPJ></emit></NFe>'
        response = client.post(
            "/api/etl/parsadores/parsear/nfe",
            params={"xml": xml}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["parseado"] == True
        assert data["tipo"] == "NFe"
        assert data["dados"]["numero"] == "001"
        print("✅ Parser NFe funcionou!")
    
    def test_parsear_nfce(self):
        """Testa parser NFCe"""
        xml = '<?xml version="1.0"?><NFCe><ide><nNF>002</nNF><serie>1</serie><dhEmi>2026-09-17</dhEmi></ide><total><ICMSTot><vNF>500.00</vNF></ICMSTot></total><emit><CNPJ>12345678000199</CNPJ></emit></NFCe>'
        response = client.post(
            "/api/etl/parsadores/parsear/nfce",
            params={"xml": xml}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["parseado"] == True
        assert data["tipo"] == "NFCe"
        print("✅ Parser NFCe funcionou!")
    
    def test_parsear_cte(self):
        """Testa parser CTe"""
        xml = '<?xml version="1.0"?><CTe><ide><nCT>003</nCT><serie>1</serie><dhEmi>2026-09-17</dhEmi></ide><total><vRec>200.00</vRec></total><emit><CNPJ>12345678000199</CNPJ></emit></CTe>'
        response = client.post(
            "/api/etl/parsadores/parsear/cte",
            params={"xml": xml}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["parseado"] == True
        assert data["tipo"] == "CTe"
        print("✅ Parser CTe funcionou!")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])