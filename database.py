## conexão ao banco de dados
from sqlalchemy import create_engine, Column, Integer, String, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Configuração do banco de dados
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:NovaSenha@localhost/banco-de-dados-api"

# Criação do engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool  # Evitar o uso de múltiplas conexões no SQLite
)

# Criando a sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Definindo o modelo para a tabela tarefas
class Tarefa(Base):
    __tablename__ = "tarefas_api"
    
    id = Column(Integer, primary_key=True, index=True)
    nome_tarefa = Column(String, index=True)
    status_tarefa = Column(SmallInteger)  # Usando SmallInteger para o status

# Função para criar a tabela no banco de dados
def create_tables():
    Base.metadata.create_all(bind=engine)

# Função para obter a sessão
def get_db():
    db = SessionLocal()  # Cria a sessão
    try:
        yield db  # Faz a sessão disponível
    finally:
        db.close()  # Fecha a sessão quando terminar


