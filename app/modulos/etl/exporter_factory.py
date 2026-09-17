from app.modulos.etl.interfaces import ExportadorNota
from app.modulos.etl.exportadores import ExportadorJSON, ExportadorXML, ExportadorPDF, ExportadorExcel


class ExportadorFactory:
    """Factory para criar exportadores"""
    
    _exportadores = {}
    
    @classmethod
    def registrar(cls, tipo: str, exportador_class):
        """Registrar novo exportador"""
        cls._exportadores[tipo] = exportador_class
        print(f"[FACTORY] ✅ Exportador '{tipo}' registrado!")
    
    @classmethod
    def criar(cls, tipo: str) -> ExportadorNota:
        """Criar instância de exportador"""
        if tipo not in cls._exportadores:
            raise ValueError(f"Exportador '{tipo}' não encontrado")
        
        print(f"[FACTORY] 📊 Criando exportador: {tipo}")
        return cls._exportadores[tipo]()
    
    @classmethod
    def obter_tipos_suportados(cls) -> list:
        """Listar exportadores disponíveis"""
        return list(cls._exportadores.keys())
    
    @classmethod
    def exportar(cls, tipo: str, dados: dict) -> dict:
        """
        Exportar dados usando exportador específico
        
        Retorna:
        {
            "exportado": bool,
            "formato": str,
            "tamanho": int,
            "conteudo": string ou bytes
        }
        """
        try:
            exportador = cls.criar(tipo)
            resultado = exportador.exportar(dados)
            print(f"[FACTORY] ✅ Exportação {tipo} concluída: {resultado['exportado']}")
            return resultado
        except Exception as e:
            print(f"[FACTORY] ❌ Erro na exportação: {str(e)}")
            return {
                "exportado": False,
                "formato": tipo,
                "tamanho": 0,
                "erro": str(e)
            }


# ============ REGISTRAR EXPORTADORES ============
ExportadorFactory.registrar("JSON", ExportadorJSON)
ExportadorFactory.registrar("XML", ExportadorXML)
ExportadorFactory.registrar("PDF", ExportadorPDF)
ExportadorFactory.registrar("EXCEL", ExportadorExcel)