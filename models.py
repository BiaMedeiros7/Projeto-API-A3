from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tarefa(Base):
    __tablename__ = "tarefas_api"

    idtarefas_api = Column(Integer, primary_key=True, index=True)
    nome_tarefa = Column(String(200), index=True)
    status_tarefa = Column(SmallInteger, nullable=False, default=0)  
    box_id = Column(Integer, nullable=False)  
