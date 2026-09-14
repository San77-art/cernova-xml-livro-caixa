from app.modulos.etl.interfaces import ProcessadorNota
from app.modulos.etl.processadores import (
    ProcessadorNFe,
    ProcessadorNFCe,
    ProcessadorCTe
)

class ProcessadorFactory:
    """FACTORY METHOD!"""
    
    _processadores = {
        "NF-e": ProcessadorNFe,
        "NFC-e": ProcessadorNFCe,
        "CT-e": ProcessadorCTe,
    }
    
    @staticmethod
    def criar(tipo: str) -> ProcessadorNota:
        """Factory Method - O Metodo Factory!"""
        
        if tipo not in ProcessadorFactory._processadores:
            tipos_disponiveis = list(ProcessadorFactory._processadores.keys())
            raise ValueError(
                f"Tipo '{tipo}' nao suportado! Use: {tipos_disponiveis}"
            )
        
        classe_processador = ProcessadorFactory._processadores[tipo]
        return classe_processador()
    
    @staticmethod
    def registrar(tipo: str, classe):
        """Registrar novo tipo dinamicamente"""
        if not issubclass(classe, ProcessadorNota):
            raise TypeError(f"Classe {classe} deve herdar de ProcessadorNota")
        ProcessadorFactory._processadores[tipo] = classe
    
    @staticmethod
    def obter_tipos_suportados():
        """Retorna lista de tipos suportados"""
        return list(ProcessadorFactory._processadores.keys())
