from pydantic import BaseModel
from typing import Optional

class TarefaCreate(BaseModel):
    nome_tarefa: str
    status_tarefa: int = 0  
    box_id: int  

    class Config:
        orm_mode = True  

class TarefaUpdate(BaseModel):
    nome_tarefa: str
    status_tarefa: int
    box_id: int  

    class Config:
        orm_mode = True

class TarefaOut(BaseModel):
    idtarefas_api: int
    nome_tarefa: str
    status_tarefa: int
    box_id: int  

    class Config:
        orm_mode = True
