
## conexão ao banco de dados


from sqlalchemy import create_engine, Column, Integer, String, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados (substitua com suas credenciais)
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:NovaSenha@localhost/banco-de-dados-api"

# Criação do motor de conexão (engine)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Criando uma base para o modelo (mapeamento ORM)
Base = declarative_base()

# Definindo o modelo para a tabela tarefas
class Tarefa(Base):
    __tablename__ = 'tarefas_api'  # Nome da tabela no banco de dados, alterei para 'tarefas_api'

    idtarefas_api = Column(Integer, primary_key=True, autoincrement=True)
    nome_tarefa = Column(String(200), nullable=False)
    status_tarefa = Column(SmallInteger, nullable=False)

# Criando uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para criar a tabela no banco de dados
def create_tables():
    Base.metadata.create_all(bind=engine)


from sqlalchemy.orm import Session

# Função para criar uma nova tarefa
def create_task(nome_tarefa, status_tarefa):
    db = SessionLocal()
    tarefa = Tarefa(nome_tarefa=nome_tarefa, status_tarefa=status_tarefa)
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    db.close()
    return tarefa











# Teste de inserção de dados
#if __name__ == "__main__":
 #   create_tables()
 #   print("Tabela criada com sucesso!")
    
    # Teste de inserção
#    nova_tarefa = create_task("Estudar para a prova", 1)
#    print(f"Tarefa criada: {nova_tarefa.nome_tarefa} com status {nova_tarefa.status_tarefa}")



## teste para ver se a conexão está funcioando
#try:
#    with engine.connect() as connection:
#        print("Conexão bem-sucedida ao banco de dados!")
#except Exception as e:
#    print(f"Erro na conexão: {e}")