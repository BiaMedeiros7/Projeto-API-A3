# arq de validação de dados
from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class TarefaCreate(BaseModel):
    nome_tarefa: str
    status_tarefa: int = 0  # Padrão para PENDENTE

    class Config:
        from_attributes = True

class TarefaOut(BaseModel):
    idtarefas_api: int
    nome_tarefa: str
    status_tarefa: int

    class Config:
        from_attributes = True


class TarefaUpdate(BaseModel):
    nome_tarefa: str
    status_tarefa: int


    class Config:
        from_attributes = True

