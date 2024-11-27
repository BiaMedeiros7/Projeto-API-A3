from schemas import TarefaCreate, TarefaUpdate, StatusEnum
from pydantic import ValidationError
import pytest
from schemas import TarefaOut


def test_tarefa_create_nome_tarefa_obrigatorio():
    with pytest.raises(ValidationError):
        TarefaCreate(nome_tarefa=None)  # Espera um erro, pois nome_tarefa não pode ser None



def test_tarefa_create_valida():
    tarefa = TarefaCreate(nome_tarefa="Estudar Python")
    assert tarefa.nome_tarefa == "Estudar Python"
    assert tarefa.status_tarefa == StatusEnum.PENDENTE

def test_tarefa_create_invalida():
    try:
        TarefaCreate(nome_tarefa=None)  # Nome da tarefa não pode ser None
    except ValidationError as e:
        assert "Input should be a valid string" in str(e)

def test_tarefa_update():
    tarefa = TarefaUpdate(nome_tarefa="Atualizar Teste")
    assert tarefa.nome_tarefa == "Atualizar Teste"
    assert tarefa.status_tarefa is None


def test_status_enum_valido():
    # Testa se um valor válido é aceito
    tarefa = TarefaCreate(nome_tarefa="Testar Enum", status_tarefa=StatusEnum.PENDENTE)
    assert tarefa.status_tarefa == StatusEnum.PENDENTE

def test_status_enum_invalido():
    # Testa se um valor inválido gera erro
    with pytest.raises(ValueError):
        TarefaCreate(nome_tarefa="Testar Enum", status_tarefa="invalid_status")


def test_tarefa_update_status_opcional():
    tarefa = TarefaUpdate(nome_tarefa="Atualizar Tarefa")
    assert tarefa.status_tarefa is None  # Espera que status_tarefa seja None, pois não foi informado


def test_tarefa_update_nome_opcional():
    tarefa = TarefaUpdate(status_tarefa=StatusEnum.CONCLUIDO)
    assert tarefa.nome_tarefa is None  # Espera que nome_tarefa seja None, pois não foi informado


def test_tarefa_out():
    tarefa = TarefaOut(idtarefas_api=1, nome_tarefa="Tarefa de Teste", status_tarefa=StatusEnum.CONCLUIDO)
    assert tarefa.idtarefas_api == 1
    assert tarefa.nome_tarefa == "Tarefa de Teste"
    assert tarefa.status_tarefa == StatusEnum.CONCLUIDO

def test_tarefa_create_valida():
    tarefa = TarefaCreate(nome_tarefa="Estudar Pydantic", status_tarefa=StatusEnum.PENDENTE)
    assert tarefa.nome_tarefa == "Estudar Pydantic"
    assert tarefa.status_tarefa == StatusEnum.PENDENTE

def test_tarefa_create_nome_tarefa_tipo_incorreto():
    with pytest.raises(ValidationError):
        TarefaCreate(nome_tarefa=12345)  # Deve lançar erro, pois nome_tarefa deve ser uma string

def test_tarefa_create_com_valor_default():
    tarefa = TarefaCreate(nome_tarefa="Tarefa sem status")
    assert tarefa.status_tarefa == StatusEnum.PENDENTE  # Valor padrão deve ser 'pendente'

def test_tarefa_to_json():
    tarefa = TarefaOut(idtarefas_api=2, nome_tarefa="Tarefa para exportar", status_tarefa=StatusEnum.CONCLUIDO)
    tarefa_json = tarefa.dict()  # Converte para dicionário
    assert "idtarefas_api" in tarefa_json
    assert "nome_tarefa" in tarefa_json
    assert "status_tarefa" in tarefa_json