from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tarefa(Base):
    __tablename__ = "tarefas_api"
    __table_args__ = {"extend_existing": True}  # Evita conflito se a tabela já existir

    idtarefas_api = Column(Integer, primary_key=True, index=True)
    nome_tarefa = Column(String(200), index=True)
    status_tarefa = Column(Integer, nullable=False, default=0)  # 0 para PENDENTE, 1 para CONCLUÍDO
