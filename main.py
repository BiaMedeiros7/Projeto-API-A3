from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, create_tables
from crud import get_tarefas, get_tarefa_por_id, criar_tarefa, atualizar_tarefa, deletar_tarefa
from schemas import TarefaCreate, TarefaUpdate, TarefaOut  # Importando os esquemas necessários
from fastapi.middleware.cors import CORSMiddleware

# inicializa a aplicação FastAPI
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Permite todas as origens, você pode mudar para ['http://127.0.0.1:5500'] para permitir apenas o seu front-end
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os headers
)












# cria as tabelas no banco de dados
create_tables()

# dependência do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# rotas da API

# Listar todas as tarefas
@app.get("/tarefas", response_model=list[TarefaOut])
def listar_tarefas(db: Session = Depends(get_db)):
    return get_tarefas(db)

# Obter uma tarefa específica pelo ID
@app.get("/tarefas/{tarefa_id}", response_model=TarefaOut)
def obter_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = get_tarefa_por_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

# Criar uma nova tarefa
@app.post("/tarefas", response_model=TarefaOut)
def criar_nova_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    return criar_tarefa(db, tarefa.nome_tarefa, tarefa.status_tarefa)

# Atualizar uma tarefa existente
@app.put("/tarefas/{id}", response_model=TarefaOut)
def update_tarefa(id: int, tarefa: TarefaUpdate, db: Session = Depends(get_db)):
    db_tarefa = atualizar_tarefa(db, id, tarefa)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa

# Deletar uma tarefa
@app.delete("/tarefas/{id}")
def delete_tarefa(id: int, db: Session = Depends(get_db)):
    tarefa = deletar_tarefa(db, id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa excluída"}
