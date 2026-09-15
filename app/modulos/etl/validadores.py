from app.modulos.etl.interfaces import ValidadorNota
from datetime import datetime
import re


class ValidadorSEFAZ(ValidadorNota):
    """Valida dados para comunicação com SEFAZ"""
    
    def validar(self, dados: dict) -> dict:
        """Valida formato e regras SEFAZ"""
        erros = []
        avisos = []
        
        # Validar CNPJ
        if not self._validar_cnpj(dados.get("cnpj", "")):
            erros.append("CNPJ inválido para SEFAZ")
        
        # Validar série e número da nota
        if not dados.get("serie"):
            erros.append("Série da nota é obrigatória")
        if not dados.get("numero"):
            erros.append("Número da nota é obrigatória")
        
        # Validar data
        try:
            datetime.fromisoformat(dados.get("data_emissao", ""))
        except:
            erros.append("Data de emissão inválida")
        
        # Validar valor
        try:
            valor = float(dados.get("valor_total", 0))
            if valor <= 0:
                erros.append("Valor total deve ser maior que zero")
        except:
            erros.append("Valor total inválido")
        
        return {
            "valido": len(erros) == 0,
            "erros": erros,
            "avisos": avisos,
            "tipo_validador": self.tipo_validador
        }
    
    def _validar_cnpj(self, cnpj: str) -> bool:
        """Valida CNPJ"""
        # Remove caracteres não numéricos
        cnpj_limpo = re.sub(r'\D', '', cnpj)
        
        # CNPJ deve ter 14 dígitos
        return len(cnpj_limpo) == 14
    
    @property
    def tipo_validador(self) -> str:
        return "SEFAZ"


class ValidadorDatabase(ValidadorNota):
    """Valida constraints do banco de dados"""
    
    def validar(self, dados: dict) -> dict:
        """Valida regras de negócio do banco"""
        erros = []
        avisos = []
        
        # Validar consultório_id
        if not dados.get("consultorio_id"):
            erros.append("Consultório ID é obrigatório")
        
        # Validar medico_id
        if not dados.get("medico_id"):
            avisos.append("Médico ID não informado")
        
        # Validar empresa_id
        if not dados.get("empresa_id"):
            dados["empresa_id"] = "default"
            avisos.append("Empresa ID não informado, usando 'default'")
        
        # Validar tipo_documento
        tipos_validos = ["NF-e", "NFC-e", "CT-e"]
        if dados.get("tipo_documento") not in tipos_validos:
            erros.append(f"Tipo de documento inválido. Válidos: {tipos_validos}")
        
        # Validar status
        status_validos = ["pendente", "processado", "erro"]
        if dados.get("status") not in status_validos:
            dados["status"] = "pendente"
            avisos.append("Status não informado, usando 'pendente'")
        
        return {
            "valido": len(erros) == 0,
            "erros": erros,
            "avisos": avisos,
            "tipo_validador": self.tipo_validador
        }
    
    @property
    def tipo_validador(self) -> str:
        return "DATABASE"


class ValidadorAssinatura(ValidadorNota):
    """Valida assinatura digital do documento"""
    
    def validar(self, dados: dict) -> dict:
        """Valida assinatura digital"""
        erros = []
        avisos = []
        
        # Validar se tem XML
        if not dados.get("xml"):
            erros.append("XML do documento é obrigatório")
        
        # Validar se tem assinatura
        if not dados.get("assinatura"):
            erros.append("Documento não possui assinatura digital")
        
        # Validar se tem certificado
        if not dados.get("certificado"):
            avisos.append("Certificado digital não informado")
        
        # Validar estrutura básica da assinatura
        if dados.get("assinatura"):
            assinatura = dados.get("assinatura", "")
            if not assinatura.startswith("-----BEGIN"):
                avisos.append("Formato de assinatura parece incorreto")
        
        return {
            "valido": len(erros) == 0,
            "erros": erros,
            "avisos": avisos,
            "tipo_validador": self.tipo_validador
        }
    
    @property
    def tipo_validador(self) -> str:
        return "ASSINATURA"