import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Tarefa, StatusEnum
from sqlalchemy import text
from database import engine, SessionLocal
import pytest
from pydantic import ValidationError
from schemas import TarefaCreate, TarefaOut, StatusEnum
from pydantic import BaseModel
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from schemas import TarefaUpdate, StatusEnum  # Ajuste o caminho conforme necessário


DATABASE_URL = "mysql+pymysql://root:NovaSenha@localhost/banco-de-dados-api"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def setup_database_fixture():
    # Criação das tabelas no banco de dados
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db  
    db.close()
    Base.metadata.drop_all(bind=engine)  # Remove as tabelas após os testes


#verificar a operação de inserção de uma tarefa no banco de dados
def test_insert_tarefa(setup_database_fixture):
    db = setup_database_fixture  
    try:
        nova_tarefa = {"nome_tarefa": "Tarefa de Teste", "status_tarefa": 1}
        db.execute(
            text("INSERT INTO tarefas_api (nome_tarefa, status_tarefa) VALUES (:nome_tarefa, :status_tarefa)"),
            nova_tarefa
        )
        db.commit()
        result = db.execute(
            text("SELECT * FROM tarefas_api WHERE nome_tarefa=:nome_tarefa"),
            {"nome_tarefa": "Tarefa de Teste"}
        ).fetchone()  # Usando fetchone() pois esperamos um único resultado

        # Asserções
        assert result is not None 
        assert result[1] == "Tarefa de Teste"  
    finally:
        db.rollback()  


#verificar o comportamento da operação de exclusão (delete) de uma tarefa no banco de dados
def test_update_tarefa(setup_database_fixture):
    db = setup_database_fixture
    tarefa = Tarefa(nome_tarefa="Tarefa de Teste", status_tarefa=StatusEnum.PENDENTE)
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)

    # Atualizando a tarefa
    update_data = TarefaUpdate(nome_tarefa="Tarefa Atualizada", status_tarefa=StatusEnum.CONCLUIDO)
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(tarefa, key, value)
    db.commit()
    db.refresh(tarefa)

    # Verificando se a tarefa foi atualizada corretamente
    assert tarefa.nome_tarefa == "Tarefa Atualizada"
    assert tarefa.status_tarefa == StatusEnum.CONCLUIDO





# TESTE BANCO DE DADOS EM MEMÓRIA (MODELS.PY)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # Banco em memória

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_create_table(setup_database_fixture):
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='tarefas_api';"))
        table_exists = result.fetchone() is not None
        assert table_exists, "A tabela 'tarefas_api' não foi criada."
    finally:
        db.close()








# Teste de criação de tarefa (validação de entrada)
def test_tarefa_create_valid():
    # Dados válidos
    tarefa_data = {"nome_tarefa": "Tarefa válida", "status_tarefa": StatusEnum.PENDENTE}
    
    # Cria o schema de entrada
    tarefa = TarefaCreate(**tarefa_data)
    
    # Verifica se os dados foram atribuídos corretamente
    assert tarefa.nome_tarefa == "Tarefa válida"
    assert tarefa.status_tarefa == StatusEnum.PENDENTE

def test_tarefa_create_invalid_status():
    # Dados com status inválido
    tarefa_data = {"nome_tarefa": "Tarefa inválida", "status_tarefa": "invalido"}
    
    # Testa se o Pydantic lança erro de validação quando o status é inválido
    with pytest.raises(ValidationError):
        TarefaCreate(**tarefa_data)

# Teste de saída (leitura)
def test_tarefa_out():
    # Dados válidos
    tarefa_data = {
        "idtarefas_api": 1,
        "nome_tarefa": "Tarefa de Exemplo",
        "status_tarefa": StatusEnum.CONCLUIDO,
    }

    # Cria o schema de saída
    tarefa_out = TarefaOut(**tarefa_data)

    # Verifica se os dados de saída estão corretos
    assert tarefa_out.idtarefas_api == 1
    assert tarefa_out.nome_tarefa == "Tarefa de Exemplo"
    assert tarefa_out.status_tarefa == StatusEnum.CONCLUIDO




# Teste de atualização de tarefa
class StatusEnum(str, Enum):
    PENDENTE = "pendente"
    CONCLUIDO = "concluido"

# Esquema de atualização de tarefa
class TarefaUpdate(BaseModel):
    nome_tarefa: Optional[str] = None
    status_tarefa: Optional[StatusEnum] = None

    class Config:
        orm_mode = True  # Permite a conversão do modelo SQLAlchemy para o esquema Pydantic