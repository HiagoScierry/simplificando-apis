from fastapi import APIRouter
from src.models.cargo import Cargo, CargoCreate
from typing import List
from src.services.cargo_service import cargo_service

router = APIRouter()

# add api section on swagger
router.tags = ["Cargos"]

@router.get("/cargos", response_model=List[Cargo])
def listar_cargos():
    """Lista todos os cargos disponíveis"""
    return cargo_service.listar_todos_cargos()

@router.get("/cargos/{cargo_id}", response_model=Cargo)
def obter_cargo(cargo_id: int):
    """Obtém um cargo específico pelo ID"""
    return cargo_service.obter_cargo_por_id(cargo_id)

@router.post("/cargos", response_model=Cargo)
def criar_cargo(cargo: CargoCreate):
    """Cria um novo cargo"""
    return cargo_service.criar_novo_cargo(cargo)

@router.put("/cargos/{cargo_id}", response_model=Cargo)
def atualizar_cargo(cargo_id: int, cargo: CargoCreate):
    """Atualiza um cargo existente"""
    return cargo_service.atualizar_cargo(cargo_id, cargo)

@router.delete("/cargos/{cargo_id}")
def deletar_cargo(cargo_id: int):
    """Deleta um cargo"""
    return cargo_service.deletar_cargo(cargo_id)
