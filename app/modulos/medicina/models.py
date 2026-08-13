from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Text, Date, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base
import uuid

class Consultorio(Base):
    __tablename__ = "consultorios"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    empresa_id = Column(String(36), nullable=False)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(18), nullable=False, unique=True)
    email_contato = Column(String(255))
    telefone = Column(String(20))
    endereco = Column(Text)
    cep = Column(String(10))
    cidade = Column(String(100))
    estado = Column(String(2))
    especialidades = Column(JSON, default=[])
    crm_responsavel = Column(String(20))
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    medicos = relationship("Medico", back_populates="consultorio")
    pacientes = relationship("Paciente", back_populates="consultorio")
    procedimentos = relationship("Procedimento", back_populates="consultorio")

class Medico(Base):
    __tablename__ = "medicos"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    consultorio_id = Column(String(36), ForeignKey("consultorios.id"), nullable=False)
    nome_completo = Column(String(255), nullable=False)
    cpf = Column(String(14), nullable=False, unique=True)
    crm = Column(String(20), nullable=False, unique=True)
    especialidade = Column(String(100), nullable=False)
    email = Column(String(255), unique=True)
    telefone = Column(String(20))
    data_nascimento = Column(Date)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    consultorio = relationship("Consultorio", back_populates="medicos")
    consultas = relationship("Consulta", back_populates="medico")

class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    consultorio_id = Column(String(36), ForeignKey("consultorios.id"), nullable=False)
    nome_completo = Column(String(255), nullable=False)
    cpf = Column(String(14), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    sexo = Column(String(1))
    email = Column(String(255))
    telefone = Column(String(20))
    endereco = Column(Text)
    convenio = Column(String(100))
    numero_cartao_convenio = Column(String(50))
    alergias = Column(JSON, default=[])
    comorbidades = Column(JSON, default=[])
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    consultorio = relationship("Consultorio", back_populates="pacientes")
    consultas = relationship("Consulta", back_populates="paciente")

class Consulta(Base):
    __tablename__ = "consultas"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    paciente_id = Column(String(36), ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(String(36), ForeignKey("medicos.id"), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    tipo = Column(String(50), default="presencial")
    motivo = Column(Text)
    status = Column(String(20), default="agendada")
    criado_em = Column(DateTime, default=datetime.utcnow)
    
    paciente = relationship("Paciente", back_populates="consultas")
    medico = relationship("Medico", back_populates="consultas")

class Prontuario(Base):
    __tablename__ = "prontuarios"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    paciente_id = Column(String(36), ForeignKey("pacientes.id"), nullable=False)
    data_atendimento = Column(DateTime, nullable=False)
    queixa_principal = Column(Text)
    anamnese = Column(Text)
    exame_fisico = Column(Text)
    diagnostico = Column(Text)
    conduta = Column(Text)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    paciente = relationship("Paciente", back_populates="prontuarios")

class Procedimento(Base):
    __tablename__ = "procedimentos"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    consultorio_id = Column(String(36), ForeignKey("consultorios.id"), nullable=False)
    nome = Column(String(255), nullable=False)
    codigo_tiss = Column(String(10))
    descricao = Column(Text)
    valor_particular = Column(Integer)
    valor_convenio = Column(Integer)
    tempo_estimado = Column(Integer)
    criado_em = Column(DateTime, default=datetime.utcnow)
    
    consultorio = relationship("Consultorio", back_populates="procedimentos")

# Adicionar relacionamento que faltava
Paciente.prontuarios = relationship("Prontuario", back_populates="paciente")
