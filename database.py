## conexão ao banco de dados
from sqlalchemy import create_engine, Column, Integer, String, Enum, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from enum import Enum as PyEnum

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:sql070105@localhost/banco-de-dados-api"


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


Base = declarative_base()

class StatusEnum(PyEnum):
    PENDENTE = "pendente"
    CONCLUIDO = "concluido"


class Tarefa(Base):
    __tablename__ = 'tarefas_api'  

    idtarefas_api = Column(Integer, primary_key=True, autoincrement=True)
    nome_tarefa = Column(String(200), nullable=False)
    status_tarefa = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.PENDENTE)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)


def create_task(nome_tarefa, status_tarefa):
    db = SessionLocal()
    tarefa = Tarefa(nome_tarefa=nome_tarefa, status_tarefa=status_tarefa)
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    db.close()
    return tarefa



