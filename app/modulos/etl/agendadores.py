from app.modulos.etl.interfaces import AgendamentoNota
from datetime import datetime, timedelta
import random


class AgendamentoPresencial(AgendamentoNota):
    """Agendamento de consulta presencial"""
    
    def agendar(self, dados: dict) -> dict:
        """Agendar consulta presencial"""
        try:
            paciente = dados.get("paciente_nome", "Desconhecido")
            profissional = dados.get("profissional_nome", "Médico")
            data = dados.get("data", datetime.now().isoformat())
            horario = dados.get("horario", "09:00")
            consultorio = dados.get("consultorio", "Consultório 1")
            
            # Gerar ID único de agendamento
            agenda_id = f"PRES-{random.randint(10000, 99999)}"
            
            print(f"[AGENDADOR] 📅 Agendando presencial para {paciente}")
            print(f"[AGENDADOR] Data: {data} às {horario}")
            print(f"[AGENDADOR] Local: {consultorio}")
            
            return {
                "agendado": True,
                "tipo": "PRESENCIAL",
                "agenda_id": agenda_id,
                "paciente": paciente,
                "profissional": profissional,
                "data": data,
                "horario": horario,
                "local": consultorio,
                "status": "confirmado",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "agendado": False,
                "tipo": "PRESENCIAL",
                "erro": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    @property
    def tipo_agendamento(self) -> str:
        return "PRESENCIAL"


class AgendamentoTelemedicina(AgendamentoNota):
    """Agendamento de consulta por telemedicina"""
    
    def agendar(self, dados: dict) -> dict:
        """Agendar consulta telemedicina"""
        try:
            paciente = dados.get("paciente_nome", "Desconhecido")
            profissional = dados.get("profissional_nome", "Médico")
            data = dados.get("data", datetime.now().isoformat())
            horario = dados.get("horario", "09:00")
            email_paciente = dados.get("email", "paciente@example.com")
            
            # Gerar link de acesso único
            link_acesso = f"https://telemedicina.cernova.com/consulta/{random.randint(100000, 999999)}"
            agenda_id = f"TELE-{random.randint(10000, 99999)}"
            
            print(f"[AGENDADOR] 📱 Agendando telemedicina para {paciente}")
            print(f"[AGENDADOR] Data: {data} às {horario}")
            print(f"[AGENDADOR] Link: {link_acesso}")
            
            return {
                "agendado": True,
                "tipo": "TELEMEDICINA",
                "agenda_id": agenda_id,
                "paciente": paciente,
                "profissional": profissional,
                "data": data,
                "horario": horario,
                "email": email_paciente,
                "link_acesso": link_acesso,
                "status": "link enviado",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "agendado": False,
                "tipo": "TELEMEDICINA",
                "erro": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    @property
    def tipo_agendamento(self) -> str:
        return "TELEMEDICINA"


class AgendamentoHomeCare(AgendamentoNota):
    """Agendamento de atendimento home care"""
    
    def agendar(self, dados: dict) -> dict:
        """Agendar atendimento home care"""
        try:
            paciente = dados.get("paciente_nome", "Desconhecido")
            profissional = dados.get("profissional_nome", "Médico")
            data = dados.get("data", datetime.now().isoformat())
            horario = dados.get("horario", "09:00")
            endereco = dados.get("endereco", "Endereço não informado")
            telefone = dados.get("telefone", "(11) 99999-9999")
            
            # Gerar ID único de visita
            visita_id = f"HOME-{random.randint(10000, 99999)}"
            
            # Calcular tempo de deslocamento (simulado)
            tempo_deslocamento = random.randint(15, 45)
            
            print(f"[AGENDADOR] 🏥 Agendando home care para {paciente}")
            print(f"[AGENDADOR] Data: {data} às {horario}")
            print(f"[AGENDADOR] Endereço: {endereco}")
            print(f"[AGENDADOR] Tempo estimado de deslocamento: {tempo_deslocamento}min")
            
            return {
                "agendado": True,
                "tipo": "HOMECARE",
                "visita_id": visita_id,
                "paciente": paciente,
                "profissional": profissional,
                "data": data,
                "horario": horario,
                "endereco": endereco,
                "telefone": telefone,
                "tempo_deslocamento_min": tempo_deslocamento,
                "status": "visita agendada",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "agendado": False,
                "tipo": "HOMECARE",
                "erro": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    @property
    def tipo_agendamento(self) -> str:
        return "HOMECARE"