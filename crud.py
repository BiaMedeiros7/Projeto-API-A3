from sqlalchemy.orm import Session
from models import Tarefa, StatusEnum
from schemas import TarefaCreate, TarefaUpdate

def get_tarefas(db: Session):
    return db.query(Tarefa).all()

def get_tarefa_por_id(db: Session, tarefa_id: int):
    return db.query(Tarefa).filter(Tarefa.idtarefas_api == tarefa_id).first()

def criar_tarefa(db: Session, tarefa: TarefaCreate):
    nova_tarefa = Tarefa(nome_tarefa=tarefa.nome_tarefa, status_tarefa=tarefa.status_tarefa)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

def atualizar_tarefa(db: Session, tarefa_id: int, tarefa: TarefaUpdate):
    tarefa_existente = db.query(Tarefa).filter(Tarefa.idtarefas_api == tarefa_id).first()
    if not tarefa_existente:
        return None
    if tarefa.nome_tarefa:
        tarefa_existente.nome_tarefa = tarefa.nome_tarefa
    if tarefa.status_tarefa:
        tarefa_existente.status_tarefa = tarefa.status_tarefa
    db.commit()
    db.refresh(tarefa_existente)
    return tarefa_existente

def deletar_tarefa(db: Session, tarefa_id: int):
    tarefa = db.query(Tarefa).filter(Tarefa.idtarefas_api == tarefa_id).first()
    if tarefa:
        db.delete(tarefa)
        db.commit()
    return tarefa
