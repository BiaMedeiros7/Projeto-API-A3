from sqlalchemy.orm import Session
from models import Tarefa
from schemas import TarefaUpdate  # Certifique-se de ter o esquema importado

def get_tarefas(db: Session):
    """Retorna todas as tarefas do banco de dados."""
    return db.query(Tarefa).all()

def get_tarefa_por_id(db: Session, tarefa_id: int):
    """Retorna uma tarefa específica pelo ID."""
    tarefa = db.query(Tarefa).filter(Tarefa.idtarefas_api == tarefa_id).first()
    if not tarefa:
        raise ValueError(f"Tarefa com ID {tarefa_id} não encontrada.")
    return tarefa

def criar_tarefa(db: Session, nome_tarefa: str, status_tarefa: int):
    """Cria uma nova tarefa no banco de dados."""
    if not nome_tarefa or status_tarefa is None:
        raise ValueError("Os campos nome_tarefa e status_tarefa são obrigatórios.")
    nova_tarefa = Tarefa(nome_tarefa=nome_tarefa, status_tarefa=status_tarefa)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

def atualizar_tarefa(db: Session, tarefa_id: int, tarefa: TarefaUpdate):
    """Atualiza uma tarefa existente pelo ID."""
    db_tarefa = db.query(Tarefa).filter(Tarefa.idtarefas_api == tarefa_id).first()
    if not db_tarefa:
        raise ValueError(f"Tarefa com ID {tarefa_id} não encontrada.")
    db_tarefa.nome_tarefa = tarefa.nome_tarefa
    db_tarefa.status_tarefa = tarefa.status_tarefa
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

def deletar_tarefa(db: Session, tarefa_id: int):
    """Remove uma tarefa do banco de dados pelo ID."""
    tarefa = db.query(Tarefa).filter(Tarefa.idtarefas_api == tarefa_id).first()
    if not tarefa:
        raise ValueError(f"Tarefa com ID {tarefa_id} não encontrada.")
    db.delete(tarefa)
    db.commit()
    return tarefa
