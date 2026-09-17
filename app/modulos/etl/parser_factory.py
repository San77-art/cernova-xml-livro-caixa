from app.modulos.etl.interfaces import ParserXML
from app.modulos.etl.parsadores import ParseadorNFe, ParseadorNFCe, ParseadorCTe, ParseadorGenerico


class ParserFactory:
    """Factory para criar parsers de XML"""
    
    _parsadores = {}
    
    @classmethod
    def registrar(cls, tipo: str, parsador_class):
        """Registrar novo parser"""
        cls._parsadores[tipo] = parsador_class
        print(f"[FACTORY] ✅ Parser '{tipo}' registrado!")
    
    @classmethod
    def criar(cls, tipo: str) -> ParserXML:
        """Criar instância de parser"""
        if tipo not in cls._parsadores:
            raise ValueError(f"Parser '{tipo}' não encontrado")
        
        print(f"[FACTORY] 📄 Criando parser: {tipo}")
        return cls._parsadores[tipo]()
    
    @classmethod
    def obter_tipos_suportados(cls) -> list:
        """Listar parsers disponíveis"""
        return list(cls._parsadores.keys())
    
    @classmethod
    def parsear(cls, tipo: str, xml: str) -> dict:
        """
        Parsear XML usando parser específico
        
        Retorna:
        {
            "parseado": bool,
            "tipo": str,
            "dados": dict,
            "campos_extraidos": int
        }
        """
        try:
            parsador = cls.criar(tipo)
            resultado = parsador.parsear(xml)
            print(f"[FACTORY] ✅ Parse {tipo} concluído: {resultado['parseado']}")
            return resultado
        except Exception as e:
            print(f"[FACTORY] ❌ Erro no parse: {str(e)}")
            return {
                "parseado": False,
                "tipo": tipo,
                "erro": str(e)
            }


# ============ REGISTRAR PARSERS ============
ParserFactory.registrar("NFe", ParseadorNFe)
ParserFactory.registrar("NFCe", ParseadorNFCe)
ParserFactory.registrar("CTe", ParseadorCTe)
ParserFactory.registrar("GENERICO", ParseadorGenerico)