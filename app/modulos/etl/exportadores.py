from app.modulos.etl.interfaces import ExportadorNota
import json
from datetime import datetime


class ExportadorJSON(ExportadorNota):
    """Exporta dados em formato JSON"""
    
    def exportar(self, dados: dict) -> dict:
        """Exportar para JSON"""
        try:
            # Converter dados para JSON
            json_str = json.dumps(dados, indent=2, default=str)
            json_bytes = json_str.encode('utf-8')
            
            print(f"[EXPORTADOR] 📄 Exportando para JSON...")
            print(f"[EXPORTADOR] Tamanho: {len(json_bytes)} bytes")
            
            return {
                "exportado": True,
                "formato": "JSON",
                "tamanho": len(json_bytes),
                "conteudo": json_str,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "exportado": False,
                "formato": "JSON",
                "tamanho": 0,
                "erro": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    @property
    def tipo_exportador(self) -> str:
        return "JSON"


class ExportadorXML(ExportadorNota):
    """Exporta dados em formato XML"""
    
    def exportar(self, dados: dict) -> dict:
        """Exportar para XML"""
        try:
            # Construir XML
            xml_str = self._dict_to_xml(dados, "nota")
            xml_bytes = xml_str.encode('utf-8')
            
            print(f"[EXPORTADOR] 📋 Exportando para XML...")
            print(f"[EXPORTADOR] Tamanho: {len(xml_bytes)} bytes")
            
            return {
                "exportado": True,
                "formato": "XML",
                "tamanho": len(xml_bytes),
                "conteudo": xml_str,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "exportado": False,
                "formato": "XML",
                "tamanho": 0,
                "erro": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _dict_to_xml(self, data: dict, root_name: str) -> str:
        """Converte dicionário para XML"""
        xml = f'<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += f'<{root_name}>\n'
        
        for key, value in data.items():
            if isinstance(value, dict):
                xml += f'  <{key}>\n'
                for k, v in value.items():
                    xml += f'    <{k}>{v}</{k}>\n'
                xml += f'  </{key}>\n'
            else:
                xml += f'  <{key}>{value}</{key}>\n'
        
        xml += f'</{root_name}>'
        return xml
    
    @property
    def tipo_exportador(self) -> str:
        return "XML"


class ExportadorPDF(ExportadorNota):
    """Exporta dados em formato PDF"""
    
    def exportar(self, dados: dict) -> dict:
        """Exportar para PDF (simulado)"""
        try:
            # Simular PDF gerado
            pdf_content = self._gerar_pdf_simulado(dados)
            pdf_bytes = pdf_content.encode('utf-8')
            
            print(f"[EXPORTADOR] 📕 Exportando para PDF...")
            print(f"[EXPORTADOR] Tamanho: {len(pdf_bytes)} bytes")
            
            return {
                "exportado": True,
                "formato": "PDF",
                "tamanho": len(pdf_bytes),
                "conteudo": pdf_content,
                "timestamp": datetime.utcnow().isoformat(),
                "nota": "PDF simulado - use ReportLab para PDF real"
            }
        except Exception as e:
            return {
                "exportado": False,
                "formato": "PDF",
                "tamanho": 0,
                "erro": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _gerar_pdf_simulado(self, dados: dict) -> str:
        """Gera conteúdo PDF simulado"""
        pdf = "%PDF-1.4\n"
        pdf += "1 0 obj\n"
        pdf += "<< /Type /Catalog /Pages 2 0 R >>\n"
        pdf += "endobj\n"
        pdf += f"% Dados: {json.dumps(dados)}\n"
        pdf += "%%EOF\n"
        return pdf
    
    @property
    def tipo_exportador(self) -> str:
        return "PDF"


class ExportadorExcel(ExportadorNota):
    """Exporta dados em formato Excel (CSV)"""
    
    def exportar(self, dados: dict) -> dict:
        """Exportar para Excel/CSV"""
        try:
            # Converter para CSV
            csv_str = self._dict_to_csv(dados)
            csv_bytes = csv_str.encode('utf-8')
            
            print(f"[EXPORTADOR] 📊 Exportando para Excel/CSV...")
            print(f"[EXPORTADOR] Tamanho: {len(csv_bytes)} bytes")
            
            return {
                "exportado": True,
                "formato": "EXCEL",
                "tamanho": len(csv_bytes),
                "conteudo": csv_str,
                "timestamp": datetime.utcnow().isoformat(),
                "nota": "Formato CSV - abrir com Excel"
            }
        except Exception as e:
            return {
                "exportado": False,
                "formato": "EXCEL",
                "tamanho": 0,
                "erro": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _dict_to_csv(self, data: dict) -> str:
        """Converte dicionário para CSV"""
        csv = "Campo,Valor\n"
        
        for key, value in data.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    csv += f'"{key}.{k}","{v}"\n'
            else:
                csv += f'"{key}","{value}"\n'
        
        return csv
    
    @property
    def tipo_exportador(self) -> str:
        return "EXCEL"