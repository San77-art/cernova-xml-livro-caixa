from app.modulos.etl.interfaces import ConectorSEFAZ
from app.modulos.etl.conectores import ConectorRS, ConectorSP, ConectorMG


class ConectorFactory:
    """Factory para criar conectores SEFAZ por estado"""
    
    _conectores = {}
    
    @classmethod
    def registrar(cls, estado: str, conector_class):
        """Registrar novo conector por estado"""
        cls._conectores[estado] = conector_class
        print(f"[FACTORY] ✅ Conector SEFAZ '{estado}' registrado!")
    
    @classmethod
    def criar(cls, estado: str) -> ConectorSEFAZ:
        """Criar instância de conector por estado"""
        if estado not in cls._conectores:
            raise ValueError(f"Conector SEFAZ '{estado}' não encontrado")
        
        print(f"[FACTORY] 🔗 Criando conector SEFAZ: {estado}")
        return cls._conectores[estado]()
    
    @classmethod
    def obter_estados_suportados(cls) -> list:
        """Listar estados com conectores disponíveis"""
        return list(cls._conectores.keys())
    
    @classmethod
    def conectar(cls, estado: str, dados: dict) -> dict:
        """
        Conectar e validar com SEFAZ do estado
        
        Retorna:
        {
            "conectado": bool,
            "estado": str,
            "protocolo": str,
            "status_sefaz": str
        }
        """
        try:
            conector = cls.criar(estado)
            resultado = conector.conectar(dados)
            print(f"[FACTORY] ✅ Conexão SEFAZ {estado} concluída: {resultado['conectado']}")
            return resultado
        except Exception as e:
            print(f"[FACTORY] ❌ Erro na conexão SEFAZ: {str(e)}")
            return {
                "conectado": False,
                "estado": estado,
                "erro": str(e)
            }


# ============ REGISTRAR CONECTORES ============
ConectorFactory.registrar("RS", ConectorRS)
ConectorFactory.registrar("SP", ConectorSP)
ConectorFactory.registrar("MG", ConectorMG)