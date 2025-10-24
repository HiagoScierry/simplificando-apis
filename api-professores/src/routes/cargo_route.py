from fastapi import APIRouter
from src.models.cargo import Cargo, CargoCreate
from typing import List
from src.config.database.connection import get_connection
from src.repository.cargo_repository import cargo_repository

router = APIRouter()

# add api section on swagger
router.tags = ["Cargos"]

@router.get("/cargos", response_model=List[Cargo])
def listar_cargos():
    return cargo_repository.list_cargos()

@router.get("/cargos/{cargo_id}", response_model=Cargo)
def obter_cargo(cargo_id: int):
    cargo = cargo_repository.get_cargo(cargo_id)
    if cargo is None:
        return {"error": "Cargo not found"}
    return cargo

@router.post("/cargos", response_model=Cargo)
def criar_cargo(cargo: CargoCreate):
    id = cargo_repository.create_cargo(cargo.nome)
    return {"id": id, "nome": cargo.nome}

@router.put("/cargos/{cargo_id}", response_model=Cargo)
def atualizar_cargo(cargo_id: int, cargo: CargoCreate):
    updated = cargo_repository.update_cargo(cargo_id, cargo.nome)
    if not updated:
        return {"error": "Cargo not found"}
    return {"id": cargo_id, "nome": cargo.nome}

@router.delete("/cargos/{cargo_id}")
def deletar_cargo(cargo_id: int):
    deleted = cargo_repository.delete_cargo(cargo_id)
    if not deleted:
        return {"error": "Cargo not found"}
    return {"message": "Cargo deleted successfully"}
