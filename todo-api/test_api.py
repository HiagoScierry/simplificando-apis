#!/usr/bin/env python3
"""
Testes para a Todo API usando pytest
"""

import pytest
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

# Fixture para dados de teste
@pytest.fixture
def todo_data():
    return [
        {
            "title": "Estudar FastAPI",
            "description": "Aprender sobre desenvolvimento de APIs REST com FastAPI"
        },
        {
            "title": "Implementar autenticação",
            "description": "Adicionar sistema de login e JWT"
        },
        {
            "title": "Deploy da aplicação"
        }
    ]

@pytest.fixture
def created_todos():
    """Fixture que cria algumas tarefas e as remove após o teste"""
    todos = []
    yield todos
    # Cleanup - remover todas as tarefas criadas durante o teste
    for todo_id in todos:
        try:
            requests.delete(f"{BASE_URL}/todos/{todo_id}")
        except:
            pass

class TestTodoAPI:
    """Classe de testes para a Todo API"""
    
    def test_root_endpoint(self):
        """Testa o endpoint raiz"""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        
    def test_list_empty_todos(self):
        """Testa listagem de tarefas quando vazia"""
        response = requests.get(f"{BASE_URL}/todos")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
    def test_create_todo_with_description(self, todo_data, created_todos):
        """Testa criação de tarefa com descrição"""
        todo_info = todo_data[0]
        response = requests.post(f"{BASE_URL}/todos", json=todo_info)
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["title"] == todo_info["title"]
        assert data["description"] == todo_info["description"]
        assert data["completed"] is False
        
        created_todos.append(data["id"])
        
    def test_create_todo_without_description(self, todo_data, created_todos):
        """Testa criação de tarefa sem descrição"""
        todo_info = todo_data[2]  # Tarefa sem descrição
        response = requests.post(f"{BASE_URL}/todos", json=todo_info)
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["title"] == todo_info["title"]
        assert data.get("description") in [None, ""]
        assert data["completed"] is False
        
        created_todos.append(data["id"])
        
    def test_get_specific_todo(self, todo_data, created_todos):
        """Testa obtenção de tarefa específica"""
        # Primeiro criar uma tarefa
        todo_info = todo_data[0]
        create_response = requests.post(f"{BASE_URL}/todos", json=todo_info)
        assert create_response.status_code == 201
        todo_id = create_response.json()["id"]
        created_todos.append(todo_id)
        
        # Agora buscar a tarefa
        response = requests.get(f"{BASE_URL}/todos/{todo_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == todo_info["title"]
        
    def test_get_nonexistent_todo(self):
        """Testa obtenção de tarefa inexistente"""
        response = requests.get(f"{BASE_URL}/todos/999")
        assert response.status_code == 404
        
    def test_update_todo(self, todo_data, created_todos):
        """Testa atualização de tarefa"""
        # Primeiro criar uma tarefa
        todo_info = todo_data[1]
        create_response = requests.post(f"{BASE_URL}/todos", json=todo_info)
        assert create_response.status_code == 201
        todo_id = create_response.json()["id"]
        created_todos.append(todo_id)
        
        # Atualizar a tarefa
        update_data = {
            "title": "Implementar autenticação JWT",
            "description": "Adicionar sistema completo de autenticação com JWT e refresh tokens",
            "completed": True
        }
        response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
        assert data["completed"] == update_data["completed"]
        
    def test_toggle_todo_status(self, todo_data, created_todos):
        """Testa alternância de status de conclusão"""
        # Primeiro criar uma tarefa
        todo_info = todo_data[0]
        create_response = requests.post(f"{BASE_URL}/todos", json=todo_info)
        assert create_response.status_code == 201
        todo_id = create_response.json()["id"]
        created_todos.append(todo_id)
        
        # Alternar status
        response = requests.patch(f"{BASE_URL}/todos/{todo_id}/toggle")
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True
        
        # Alternar novamente
        response = requests.patch(f"{BASE_URL}/todos/{todo_id}/toggle")
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is False
        
    def test_delete_todo(self, todo_data, created_todos):
        """Testa exclusão de tarefa"""
        # Primeiro criar uma tarefa
        todo_info = todo_data[2]
        create_response = requests.post(f"{BASE_URL}/todos", json=todo_info)
        assert create_response.status_code == 201
        todo_id = create_response.json()["id"]
        
        # Deletar a tarefa
        response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
        assert response.status_code == 200
        
        # Verificar que foi deletada
        get_response = requests.get(f"{BASE_URL}/todos/{todo_id}")
        assert get_response.status_code == 404
        
    def test_get_stats(self, todo_data, created_todos):
        """Testa obtenção de estatísticas"""
        # Criar algumas tarefas
        for todo_info in todo_data[:2]:
            create_response = requests.post(f"{BASE_URL}/todos", json=todo_info)
            if create_response.status_code == 201:
                created_todos.append(create_response.json()["id"])
        
        # Marcar uma como concluída
        if created_todos:
            requests.patch(f"{BASE_URL}/todos/{created_todos[0]}/toggle")
        
        # Obter estatísticas
        response = requests.get(f"{BASE_URL}/todos/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "completed" in data
        assert "pending" in data
        assert isinstance(data["total"], int)
        assert isinstance(data["completed"], int)
        assert isinstance(data["pending"], int)
        
    def test_list_todos_after_operations(self, todo_data, created_todos):
        """Testa listagem após várias operações"""
        # Criar várias tarefas
        for todo_info in todo_data:
            create_response = requests.post(f"{BASE_URL}/todos", json=todo_info)
            if create_response.status_code == 201:
                created_todos.append(create_response.json()["id"])
        
        # Listar todas
        response = requests.get(f"{BASE_URL}/todos")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= len(created_todos)
        
    def test_connection_error_handling(self):
        """Testa tratamento de erro de conexão"""
        try:
            response = requests.get("http://localhost:9999/", timeout=1)
        except requests.exceptions.ConnectionError:
            # Este é o comportamento esperado quando o servidor não está rodando
            assert True
        except requests.exceptions.Timeout:
            assert True
        else:
            # Se chegou aqui, algo inesperado aconteceu
            pytest.fail("Esperava uma exceção de conexão")

@pytest.mark.integration
class TestTodoAPIIntegration:
    """Testes de integração mais complexos"""
    
    def test_full_workflow(self, todo_data):
        """Testa um fluxo completo de operações"""
        created_ids = []
        
        try:
            # 1. Criar múltiplas tarefas
            for todo_info in todo_data:
                response = requests.post(f"{BASE_URL}/todos", json=todo_info)
                assert response.status_code == 201
                created_ids.append(response.json()["id"])
            
            # 2. Listar e verificar
            response = requests.get(f"{BASE_URL}/todos")
            assert response.status_code == 200
            todos = response.json()
            assert len([t for t in todos if t["id"] in created_ids]) == len(created_ids)
            
            # 3. Atualizar uma tarefa
            if created_ids:
                update_data = {"title": "Tarefa Atualizada", "completed": True}
                response = requests.put(f"{BASE_URL}/todos/{created_ids[0]}", json=update_data)
                assert response.status_code == 200
            
            # 4. Verificar estatísticas
            response = requests.get(f"{BASE_URL}/todos/stats")
            assert response.status_code == 200
            stats = response.json()
            assert stats["total"] >= len(created_ids)
            assert stats["completed"] >= 1
            
        finally:
            # Cleanup
            for todo_id in created_ids:
                try:
                    requests.delete(f"{BASE_URL}/todos/{todo_id}")
                except:
                    pass

if __name__ == "__main__":
    # Executar testes se o arquivo for chamado diretamente
    pytest.main([__file__, "-v"])
