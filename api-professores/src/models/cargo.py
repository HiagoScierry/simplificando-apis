from pydantic import BaseModel

class CargoCreate(BaseModel):
    nome: str

class Cargo(BaseModel):  # usado no GET / retorno
    id: int
    nome: str