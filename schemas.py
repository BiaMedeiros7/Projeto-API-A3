# arq de validação de dados

from pydantic import BaseModel
from enum import Enum
from typing import Optional


class StatusEnum(str, Enum):
    PENDENTE = "pendente"
    CONCLUIDO = "concluido"


class TarefaCreate(BaseModel):
    nome_tarefa: str
    status_tarefa: StatusEnum = StatusEnum.PENDENTE  

    class Config:
        from_attributes = True 


class TarefaOut(BaseModel):
    idtarefas_api: int
    nome_tarefa: str
    status_tarefa: StatusEnum

    class Config:
       from_attributes = True 


class TarefaUpdate(BaseModel):
    nome_tarefa: Optional[str] = None
    status_tarefa: Optional[StatusEnum] = None

    class Config:
        from_attributes = True 

