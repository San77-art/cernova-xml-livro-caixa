from app.modulos.etl.interfaces import AgendamentoNota
from app.modulos.etl.agendadores import AgendamentoPresencial, AgendamentoTelemedicina, AgendamentoHomeCare


class AgendamentoFactory:
    """Factory para criar agendadores"""
    
    _agendadores = {}
    
    @classmethod
    def registrar(cls, tipo: str, agendador_class):
        """Registrar novo agendador"""
        cls._agendadores[tipo] = agendador_class
        print(f"[FACTORY] ✅ Agendador '{tipo}' registrado!")
    
    @classmethod
    def criar(cls, tipo: str) -> AgendamentoNota:
        """Criar instância de agendador"""
        if tipo not in cls._agendadores:
            raise ValueError(f"Agendador '{tipo}' não encontrado")
        
        print(f"[FACTORY] 📅 Criando agendador: {tipo}")
        return cls._agendadores[tipo]()
    
    @classmethod
    def obter_tipos_suportados(cls) -> list:
        """Listar agendadores disponíveis"""
        return list(cls._agendadores.keys())
    
    @classmethod
    def agendar(cls, tipo: str, dados: dict) -> dict:
        """
        Agendar consulta usando agendador específico
        
        Retorna:
        {
            "agendado": bool,
            "tipo": str,
            "paciente": str,
            "data": str,
            "horario": str
        }
        """
        try:
            agendador = cls.criar(tipo)
            resultado = agendador.agendar(dados)
            print(f"[FACTORY] ✅ Agendamento {tipo} concluído: {resultado['agendado']}")
            return resultado
        except Exception as e:
            print(f"[FACTORY] ❌ Erro no agendamento: {str(e)}")
            return {
                "agendado": False,
                "tipo": tipo,
                "erro": str(e)
            }


# ============ REGISTRAR AGENDADORES ============
AgendamentoFactory.registrar("PRESENCIAL", AgendamentoPresencial)
AgendamentoFactory.registrar("TELEMEDICINA", AgendamentoTelemedicina)
AgendamentoFactory.registrar("HOMECARE", AgendamentoHomeCare)