from fastapi import APIRouter
from typing import List

from src.models.funcionario import Funcionario, FuncionarioCreate
from src.services.funcionario_service import funcionario_service

router = APIRouter()

# add api section on swagger
router.tags = ["Funcionários"]

@router.get("/funcionarios", response_model=List[Funcionario])
def listar_funcionarios():
    """Lista todos os funcionários"""
    return funcionario_service.listar_todos_funcionarios()

@router.get("/funcionarios/{funcionario_id}", response_model=Funcionario)
def obter_funcionario(funcionario_id: int):
    """Obtém um funcionário específico pelo ID"""
    return funcionario_service.obter_funcionario_por_id(funcionario_id)

@router.post("/funcionarios", response_model=Funcionario)
def criar_funcionario(funcionario: FuncionarioCreate):
    """Cria um novo funcionário"""
    return funcionario_service.criar_novo_funcionario(funcionario)

@router.put("/funcionarios/{funcionario_id}", response_model=Funcionario)
def atualizar_funcionario(funcionario_id: int, funcionario: FuncionarioCreate):
    """Atualiza um funcionário existente"""
    return funcionario_service.atualizar_funcionario(funcionario_id, funcionario)

@router.delete("/funcionarios/{funcionario_id}")
def deletar_funcionario(funcionario_id: int):
    """Deleta um funcionário"""
    return funcionario_service.deletar_funcionario(funcionario_id)