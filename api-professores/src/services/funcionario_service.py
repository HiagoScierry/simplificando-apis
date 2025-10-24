from typing import List, Optional
from fastapi import HTTPException

from src.models.funcionario import Funcionario, FuncionarioCreate
from src.repository.funcionario_repository import funcionario_repository
from src.repository.cargo_repository import cargo_repository


class FuncionarioService:
    def __init__(self):
        self.funcionario_repository = funcionario_repository
        self.cargo_repository = cargo_repository
    
    def listar_todos_funcionarios(self) -> List[Funcionario]:
        try:
            return self.funcionario_repository.list_funcionarios()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
    def obter_funcionario_por_id(self, funcionario_id: int) -> Funcionario:
        if funcionario_id <= 0:
            raise HTTPException(status_code=400, detail="ID do funcionário deve ser um número positivo")
        
        funcionario = self.funcionario_repository.get_funcionario_by_id(funcionario_id)
        if funcionario is None:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")
        
        return funcionario
    
    def criar_novo_funcionario(self, funcionario_data: FuncionarioCreate) -> Funcionario:
        # Validações de entrada
        if not funcionario_data.nome or funcionario_data.nome.strip() == "":
            raise HTTPException(status_code=400, detail="Nome do funcionário é obrigatório")
        
        if len(funcionario_data.nome.strip()) > 100:
            raise HTTPException(status_code=400, detail="Nome do funcionário não pode ter mais de 100 caracteres")
        
        # Validar cargo se fornecido
        if funcionario_data.cargo_id is not None:
            if funcionario_data.cargo_id <= 0:
                raise HTTPException(status_code=400, detail="ID do cargo deve ser um número positivo")
            
            cargo_existe = self.cargo_repository.get_cargo_by_id(funcionario_data.cargo_id)
            if not cargo_existe:
                raise HTTPException(status_code=400, detail="Cargo não encontrado")
        
        try:
            novo_funcionario = self.funcionario_repository.create_funcionario(
                funcionario_data.nome.strip(), 
                funcionario_data.cargo_id
            )
            return novo_funcionario
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar funcionário: {str(e)}")
    
    def atualizar_funcionario(self, funcionario_id: int, funcionario_data: FuncionarioCreate) -> Funcionario:
        if funcionario_id <= 0:
            raise HTTPException(status_code=400, detail="ID do funcionário deve ser um número positivo")
        
        if not funcionario_data.nome or funcionario_data.nome.strip() == "":
            raise HTTPException(status_code=400, detail="Nome do funcionário é obrigatório")
        
        if len(funcionario_data.nome.strip()) > 100:
            raise HTTPException(status_code=400, detail="Nome do funcionário não pode ter mais de 100 caracteres")
        
        # Validar cargo se fornecido
        if funcionario_data.cargo_id is not None:
            if funcionario_data.cargo_id <= 0:
                raise HTTPException(status_code=400, detail="ID do cargo deve ser um número positivo")
            
            cargo_existe = self.cargo_repository.get_cargo_by_id(funcionario_data.cargo_id)
            if not cargo_existe:
                raise HTTPException(status_code=400, detail="Cargo não encontrado")
        
        try:
            # Verificar se o funcionário existe
            funcionario_existente = self.funcionario_repository.get_funcionario_by_id(funcionario_id)
            if funcionario_existente is None:
                raise HTTPException(status_code=404, detail="Funcionário não encontrado")
            
            updated = self.funcionario_repository.edit_funcionario(
                funcionario_id, 
                funcionario_data.nome.strip(), 
                funcionario_data.cargo_id
            )
            
            if not updated:
                raise HTTPException(status_code=500, detail="Erro ao atualizar funcionário")
            
            return Funcionario(
                id=funcionario_id, 
                nome=funcionario_data.nome.strip(), 
                cargo_id=funcionario_data.cargo_id
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar funcionário: {str(e)}")
    
    def deletar_funcionario(self, funcionario_id: int) -> dict:
        if funcionario_id <= 0:
            raise HTTPException(status_code=400, detail="ID do funcionário deve ser um número positivo")
        
        try:
            # Verificar se o funcionário existe
            funcionario_existente = self.funcionario_repository.get_funcionario_by_id(funcionario_id)
            if funcionario_existente is None:
                raise HTTPException(status_code=404, detail="Funcionário não encontrado")
            
            deleted = self.funcionario_repository.delete_funcionario(funcionario_id)
            if not deleted:
                raise HTTPException(status_code=500, detail="Erro ao deletar funcionário")
            
            return {"message": "Funcionário deletado com sucesso"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao deletar funcionário: {str(e)}")


# Instância única do serviço
funcionario_service = FuncionarioService()
