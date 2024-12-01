from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, create_tables
from crud import get_tarefas, get_tarefa_por_id, criar_tarefa, atualizar_tarefa, deletar_tarefa
from schemas import TarefaCreate, TarefaUpdate, TarefaOut

#inicializa a aplicação FastAPI
app = FastAPI()

#cria as tabelas no banco de dados
create_tables()

#dependência do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#rotas da API
@app.get("/tarefas", response_model=list[TarefaOut])
def listar_tarefas(db: Session = Depends(get_db)):
    return get_tarefas(db)

@app.get("/tarefas/{tarefa_id}", response_model=TarefaOut)
def obter_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = get_tarefa_por_id(db, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@app.post("/tarefas", response_model=TarefaOut)
def criar_nova_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    return criar_tarefa(db, tarefa)

@app.put("/tarefas/{tarefa_id}", response_model=TarefaOut)
def editar_tarefa(tarefa_id: int, tarefa: TarefaUpdate, db: Session = Depends(get_db)):
    tarefa_atualizada = atualizar_tarefa(db, tarefa_id, tarefa)
    if not tarefa_atualizada:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa_atualizada

@app.delete("/tarefas/{tarefa_id}")
def excluir_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa_deletada = deletar_tarefa(db, tarefa_id)
    if not tarefa_deletada:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa excluída com sucesso"}
