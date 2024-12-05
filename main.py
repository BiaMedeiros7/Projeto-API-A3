from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal  
from schemas import TarefaCreate, TarefaUpdate, TarefaOut
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from crud import criar_tarefa, atualizar_tarefa, deletar_tarefa, obter_tarefas_por_box  


def get_db():
    db = SessionLocal()  
    try:
        yield db  
    finally:
        db.close()  


app = FastAPI()


origins = [
    "http://127.0.0.1:5500",  
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.get("/tarefas/{box_id}", response_model=List[TarefaOut])
def obter_tarefas_por_box_id(box_id: int, db: Session = Depends(get_db)):
    tarefas = obter_tarefas_por_box(db, box_id)
    if not tarefas:
        raise HTTPException(status_code=404, detail="Nenhuma tarefa encontrada para este Box.")
    return tarefas


@app.post("/tarefas", response_model=TarefaOut)
def criar_nova_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    return criar_tarefa(db, tarefa.nome_tarefa, tarefa.status_tarefa, tarefa.box_id)


@app.put("/tarefas/{id}", response_model=TarefaOut)
def update_tarefa(id: int, tarefa: TarefaUpdate, db: Session = Depends(get_db)):
    db_tarefa = atualizar_tarefa(db, id, tarefa)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa


@app.delete("/tarefas/{id}")
def delete_tarefa(id: int, db: Session = Depends(get_db)):
    tarefa = deletar_tarefa(db, id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa excluída"}

