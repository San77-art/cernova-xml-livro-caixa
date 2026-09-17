from app.modulos.etl.interfaces import ParserXML
import xml.etree.ElementTree as ET
from datetime import datetime
import json


class ParseadorNFe(ParserXML):
    """Parser para NF-e (Nota Fiscal Eletrônica)"""
    
    def parsear(self, xml: str) -> dict:
        """Parsear XML de NF-e"""
        try:
            root = ET.fromstring(xml)
            
            # Extrair dados da NF-e
            dados = {
                "tipo_documento": "NF-e",
                "numero": self._extrair_campo(root, "ide/nNF"),
                "serie": self._extrair_campo(root, "ide/serie"),
                "data_emissao": self._extrair_campo(root, "ide/dhEmi"),
                "valor_total": self._extrair_campo(root, "total/ICMSTot/vNF"),
                "cnpj_emitente": self._extrair_campo(root, "emit/CNPJ"),
                "cnpj_destinatario": self._extrair_campo(root, "dest/CNPJ"),
            }
            
            campos_extraidos = len([v for v in dados.values() if v])
            
            print(f"[PARSER] 📄 Parseando NF-e...")
            print(f"[PARSER] Número: {dados.get('numero')}")
            print(f"[PARSER] Campos extraídos: {campos_extraidos}")
            
            return {
                "parseado": True,
                "tipo": "NFe",
                "dados": dados,
                "campos_extraidos": campos_extraidos,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "parseado": False,
                "tipo": "NFe",
                "erro": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _extrair_campo(self, root, caminho: str):
        """Extrai valor de campo XML por caminho"""
        try:
            partes = caminho.split("/")
            elemento = root
            for parte in partes:
                elemento = elemento.find(parte)
                if elemento is None:
                    return None
            return elemento.text
        except:
            return None
    
    @property
    def tipo_parser(self) -> str:
        return "NFe"


class ParseadorNFCe(ParserXML):
    """Parser para NFC-e (Nota Fiscal de Consumidor Eletrônica)"""
    
    def parsear(self, xml: str) -> dict:
        """Parsear XML de NFC-e"""
        try:
            root = ET.fromstring(xml)
            
            # Extrair dados da NFC-e
            dados = {
                "tipo_documento": "NFC-e",
                "numero": self._extrair_campo(root, "ide/nNF"),
                "serie": self._extrair_campo(root, "ide/serie"),
                "data_emissao": self._extrair_campo(root, "ide/dhEmi"),
                "valor_total": self._extrair_campo(root, "total/ICMSTot/vNF"),
                "cnpj_emitente": self._extrair_campo(root, "emit/CNPJ"),
                "serie_sat": self._extrair_campo(root, "infSat/assinaturaQRCode"),
            }
            
            campos_extraidos = len([v for v in dados.values() if v])
            
            print(f"[PARSER] 📱 Parseando NFC-e...")
            print(f"[PARSER] Número: {dados.get('numero')}")
            print(f"[PARSER] Campos extraídos: {campos_extraidos}")
            
            return {
                "parseado": True,
                "tipo": "NFCe",
                "dados": dados,
                "campos_extraidos": campos_extraidos,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "parseado": False,
                "tipo": "NFCe",
                "erro": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _extrair_campo(self, root, caminho: str):
        """Extrai valor de campo XML por caminho"""
        try:
            partes = caminho.split("/")
            elemento = root
            for parte in partes:
                elemento = elemento.find(parte)
                if elemento is None:
                    return None
            return elemento.text
        except:
            return None
    
    @property
    def tipo_parser(self) -> str:
        return "NFCe"


class ParseadorCTe(ParserXML):
    """Parser para CT-e (Conhecimento de Transporte Eletrônico)"""
    
    def parsear(self, xml: str) -> dict:
        """Parsear XML de CT-e"""
        try:
            root = ET.fromstring(xml)
            
            # Extrair dados do CT-e
            dados = {
                "tipo_documento": "CT-e",
                "numero": self._extrair_campo(root, "ide/nCT"),
                "serie": self._extrair_campo(root, "ide/serie"),
                "data_emissao": self._extrair_campo(root, "ide/dhEmi"),
                "valor_total": self._extrair_campo(root, "total/vRec"),
                "cnpj_emitente": self._extrair_campo(root, "emit/CNPJ"),
                "cnpj_transportador": self._extrair_campo(root, "infCte/transp/CNPJ"),
            }
            
            campos_extraidos = len([v for v in dados.values() if v])
            
            print(f"[PARSER] 🚚 Parseando CT-e...")
            print(f"[PARSER] Número: {dados.get('numero')}")
            print(f"[PARSER] Campos extraídos: {campos_extraidos}")
            
            return {
                "parseado": True,
                "tipo": "CTe",
                "dados": dados,
                "campos_extraidos": campos_extraidos,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "parseado": False,
                "tipo": "CTe",
                "erro": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _extrair_campo(self, root, caminho: str):
        """Extrai valor de campo XML por caminho"""
        try:
            partes = caminho.split("/")
            elemento = root
            for parte in partes:
                elemento = elemento.find(parte)
                if elemento is None:
                    return None
            return elemento.text
        except:
            return None
    
    @property
    def tipo_parser(self) -> str:
        return "CTe"


class ParseadorGenerico(ParserXML):
    """Parser genérico para qualquer estrutura XML"""
    
    def parsear(self, xml: str) -> dict:
        """Parsear XML genérico"""
        try:
            root = ET.fromstring(xml)
            
            # Extrair estrutura completa
            dados = self._xml_para_dict(root)
            campos_extraidos = self._contar_campos(dados)
            
            print(f"[PARSER] 📋 Parseando XML genérico...")
            print(f"[PARSER] Root tag: {root.tag}")
            print(f"[PARSER] Campos extraídos: {campos_extraidos}")
            
            return {
                "parseado": True,
                "tipo": "GENERICO",
                "dados": dados,
                "campos_extraidos": campos_extraidos,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "parseado": False,
                "tipo": "GENERICO",
                "erro": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _xml_para_dict(self, elemento):
        """Converte elemento XML para dicionário"""
        resultado = {}
        
        # Adicionar atributos
        if elemento.attrib:
            resultado["@atributos"] = elemento.attrib
        
        # Adicionar texto
        if elemento.text and elemento.text.strip():
            resultado["#texto"] = elemento.text.strip()
        
        # Adicionar filhos
        for filho in elemento:
            chave = filho.tag
            valor = self._xml_para_dict(filho)
            
            if chave in resultado:
                if not isinstance(resultado[chave], list):
                    resultado[chave] = [resultado[chave]]
                resultado[chave].append(valor)
            else:
                resultado[chave] = valor
        
        return resultado
    
    def _contar_campos(self, dados, profundidade=0):
        """Conta número de campos extraídos"""
        count = 0
        if isinstance(dados, dict):
            count = len(dados)
            for v in dados.values():
                count += self._contar_campos(v, profundidade + 1)
        elif isinstance(dados, list):
            for item in dados:
                count += self._contar_campos(item, profundidade + 1)
        return count
    
    @property
    def tipo_parser(self) -> str:
        return "GENERICO"