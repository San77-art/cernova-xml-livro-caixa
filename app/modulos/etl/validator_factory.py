from app.modulos.etl.interfaces import ValidadorNota
from app.modulos.etl.validadores import ValidadorSEFAZ, ValidadorDatabase, ValidadorAssinatura


class ValidadorFactory:
    """Factory para criar validadores"""
    
    _validadores = {}
    
    @classmethod
    def registrar(cls, tipo: str, validador_class):
        """Registrar novo validador"""
        cls._validadores[tipo] = validador_class
        print(f"[FACTORY] ✅ Validador '{tipo}' registrado!")
    
    @classmethod
    def criar(cls, tipo: str) -> ValidadorNota:
        """Criar instância de validador"""
        if tipo not in cls._validadores:
            raise ValueError(f"Validador '{tipo}' não encontrado")
        
        print(f"[FACTORY] 🔍 Criando validador: {tipo}")
        return cls._validadores[tipo]()
    
    @classmethod
    def obter_tipos_suportados(cls) -> list:
        """Listar validadores disponíveis"""
        return list(cls._validadores.keys())
    
    @classmethod
    def validar(cls, tipo: str, dados: dict) -> dict:
        """
        Validar dados usando validador específico
        
        Retorna:
        {
            "valido": bool,
            "erros": [str],
            "avisos": [str],
            "tipo_validador": str
        }
        """
        try:
            validador = cls.criar(tipo)
            resultado = validador.validar(dados)
            print(f"[FACTORY] ✅ Validação {tipo} concluída: {resultado['valido']}")
            return resultado
        except Exception as e:
            print(f"[FACTORY] ❌ Erro na validação: {str(e)}")
            return {
                "valido": False,
                "erros": [str(e)],
                "avisos": [],
                "tipo_validador": tipo
            }


# ============ REGISTRAR VALIDADORES ============
ValidadorFactory.registrar("SEFAZ", ValidadorSEFAZ)
ValidadorFactory.registrar("DATABASE", ValidadorDatabase)
ValidadorFactory.registrar("ASSINATURA", ValidadorAssinatura)