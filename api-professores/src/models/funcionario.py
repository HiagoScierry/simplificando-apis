from pydantic import BaseModel

class FuncionarioCreate(BaseModel):
    nome: str
    cargo_id: int

class Funcionario(BaseModel):
    id: int
    nome: str
    cargo_id: int
    cargo_nome: str | None = None