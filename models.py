from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

class StatusEnum(PyEnum):
    PENDENTE = "pendente"
    CONCLUIDO = "concluido"

class Tarefa(Base):
    __tablename__ = "tarefas_api"
    __table_args__ = {"extend_existing": True}  # Evita conflito se a tabela já existir

    idtarefas_api = Column(Integer, primary_key=True, index=True)
    nome_tarefa = Column(String(200), index=True)
    status_tarefa = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.PENDENTE)
