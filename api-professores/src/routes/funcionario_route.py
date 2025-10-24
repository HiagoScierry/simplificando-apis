from fastapi import APIRouter, HTTPException
from typing import List

from src.models.funcionario import Funcionario, FuncionarioCreate
from src.config.database.connection import get_connection
from src.repository.funcionario_repository import funcionario_repository
from src.repository.cargo_repository import cargo_repository

router = APIRouter()

# add api section on swagger
router.tags = ["Funcionários"]

@router.get("/funcionarios", response_model=List[Funcionario])
def listar_funcionarios():
    return funcionario_repository.list_funcionarios()

@router.get("/funcionarios/{funcionario_id}", response_model=Funcionario)
def obter_funcionario(funcionario_id: int):
    funcionario = funcionario_repository.get_funcionario_by_id(funcionario_id)
    if funcionario is None:
        return {"error": "Funcionário não encontrado"}
    return funcionario

@router.post("/funcionarios", response_model=Funcionario)
def criar_funcionario(funcionario: FuncionarioCreate):
    try:
        if funcionario.cargo_id:
            if not cargo_repository.get_cargo_by_id(funcionario.cargo_id):
                raise HTTPException(status_code=400, detail="Cargo não encontrado")

        new_funcionario = funcionario_repository.create_funcionario(funcionario.nome, funcionario.cargo_id)
        return new_funcionario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/funcionarios/{funcionario_id}", response_model=Funcionario)
def atualizar_funcionario(funcionario_id: int, funcionario: FuncionarioCreate):
    if funcionario.cargo_id:
        if not cargo_repository.get_cargo_by_id(funcionario.cargo_id):
            raise HTTPException(status_code=400, detail="Cargo não encontrado")

    updated = funcionario_repository.edit_funcionario(funcionario_id, funcionario.nome, funcionario.cargo_id)
    if not updated:
        return {"error": "Funcionário não encontrado"}
    return { "id": funcionario_id, "nome": funcionario.nome, "cargo_id": funcionario.cargo_id}

@router.delete("/funcionarios/{funcionario_id}")
def deletar_funcionario(funcionario_id: int):
    deleted = funcionario_repository.delete_funcionario(funcionario_id)
    if not deleted:
        return {"error": "Funcionário não encontrado"}
    return {"message": "Funcionário deletado com sucesso"}