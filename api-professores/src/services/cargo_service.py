from typing import List, Optional
from fastapi import HTTPException

from src.models.cargo import Cargo, CargoCreate
from src.repository.cargo_repository import cargo_repository


class CargoService:
    """Serviço responsável pela lógica de negócio relacionada aos cargos"""
    
    def __init__(self):
        self.cargo_repository = cargo_repository
    
    def listar_todos_cargos(self) -> List[Cargo]:
        try:
            return self.cargo_repository.list_cargos()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
    def obter_cargo_por_id(self, cargo_id: int) -> Cargo:
        if cargo_id <= 0:
            raise HTTPException(status_code=400, detail="ID do cargo deve ser um número positivo")
        
        cargo = self.cargo_repository.get_cargo(cargo_id)
        if cargo is None:
            raise HTTPException(status_code=404, detail="Cargo não encontrado")
        
        return cargo
    
    def criar_novo_cargo(self, cargo_data: CargoCreate) -> Cargo:
        if not cargo_data.nome or cargo_data.nome.strip() == "":
            raise HTTPException(status_code=400, detail="Nome do cargo é obrigatório")
        
        # Validar se o nome não está muito longo
        if len(cargo_data.nome.strip()) > 100:
            raise HTTPException(status_code=400, detail="Nome do cargo não pode ter mais de 100 caracteres")
        
        try:
            cargo_id = self.cargo_repository.create_cargo(cargo_data.nome.strip())
            return Cargo(id=cargo_id, nome=cargo_data.nome.strip())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar cargo: {str(e)}")
    
    def atualizar_cargo(self, cargo_id: int, cargo_data: CargoCreate) -> Cargo:
        if cargo_id <= 0:
            raise HTTPException(status_code=400, detail="ID do cargo deve ser um número positivo")
        
        if not cargo_data.nome or cargo_data.nome.strip() == "":
            raise HTTPException(status_code=400, detail="Nome do cargo é obrigatório")
        
        if len(cargo_data.nome.strip()) > 100:
            raise HTTPException(status_code=400, detail="Nome do cargo não pode ter mais de 100 caracteres")
        
        try:
            # Verificar se o cargo existe
            cargo_existente = self.cargo_repository.get_cargo(cargo_id)
            if cargo_existente is None:
                raise HTTPException(status_code=404, detail="Cargo não encontrado")
            
            updated = self.cargo_repository.update_cargo(cargo_id, cargo_data.nome.strip())
            if not updated:
                raise HTTPException(status_code=500, detail="Erro ao atualizar cargo")
            
            return Cargo(id=cargo_id, nome=cargo_data.nome.strip())
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar cargo: {str(e)}")
    
    def deletar_cargo(self, cargo_id: int) -> dict:
        if cargo_id <= 0:
            raise HTTPException(status_code=400, detail="ID do cargo deve ser um número positivo")
        
        try:
            # Verificar se o cargo existe
            cargo_existente = self.cargo_repository.get_cargo(cargo_id)
            if cargo_existente is None:
                raise HTTPException(status_code=404, detail="Cargo não encontrado")
            
            deleted = self.cargo_repository.delete_cargo(cargo_id)
            if not deleted:
                raise HTTPException(status_code=500, detail="Erro ao deletar cargo")
            
            return {"message": "Cargo deletado com sucesso"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao deletar cargo: {str(e)}")


# Instância única do serviço
cargo_service = CargoService()
