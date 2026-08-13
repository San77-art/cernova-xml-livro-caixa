from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List

# CONSULTÓRIO
class ConsultorioBase(BaseModel):
    nome: str
    cnpj: str
    email_contato: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cep: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    especialidades: Optional[List[str]] = None
    crm_responsavel: Optional[str] = None

class ConsultorioCreate(ConsultorioBase):
    pass

class ConsultorioResponse(ConsultorioBase):
    id: str
    empresa_id: str
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime
    class Config:
        from_attributes = True

# MÉDICO
class MedicoBase(BaseModel):
    nome_completo: str
    cpf: str
    crm: str
    especialidade: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None

class MedicoCreate(MedicoBase):
    consultorio_id: str

class MedicoResponse(MedicoBase):
    id: str
    consultorio_id: str
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime
    class Config:
        from_attributes = True

# PACIENTE
class PacienteBase(BaseModel):
    nome_completo: str
    cpf: str
    data_nascimento: date
    sexo: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    convenio: Optional[str] = None
    numero_cartao_convenio: Optional[str] = None
    alergias: Optional[List[str]] = None
    comorbidades: Optional[List[str]] = None

class PacienteCreate(PacienteBase):
    consultorio_id: str

class PacienteResponse(PacienteBase):
    id: str
    consultorio_id: str
    criado_em: datetime
    atualizado_em: datetime
    class Config:
        from_attributes = True

# CONSULTA
class ConsultaBase(BaseModel):
    data_hora: datetime
    tipo: str = "presencial"
    motivo: Optional[str] = None
    status: str = "agendada"

class ConsultaCreate(ConsultaBase):
    paciente_id: str
    medico_id: str

class ConsultaResponse(ConsultaBase):
    id: str
    paciente_id: str
    medico_id: str
    criado_em: datetime
    class Config:
        from_attributes = True

# PRONTUÁRIO
class ProntuarioBase(BaseModel):
    data_atendimento: datetime
    queixa_principal: Optional[str] = None
    anamnese: Optional[str] = None
    exame_fisico: Optional[str] = None
    diagnostico: Optional[str] = None
    conduta: Optional[str] = None

class ProntuarioCreate(ProntuarioBase):
    paciente_id: str

class ProntuarioResponse(ProntuarioBase):
    id: str
    paciente_id: str
    criado_em: datetime
    atualizado_em: datetime
    class Config:
        from_attributes = True

# PROCEDIMENTO
class ProcedimentoBase(BaseModel):
    nome: str
    codigo_tiss: Optional[str] = None
    descricao: Optional[str] = None
    valor_particular: Optional[int] = None
    valor_convenio: Optional[int] = None
    tempo_estimado: Optional[int] = None

class ProcedimentoCreate(ProcedimentoBase):
    consultorio_id: str

class ProcedimentoResponse(ProcedimentoBase):
    id: str
    consultorio_id: str
    criado_em: datetime
    class Config:
        from_attributes = True
