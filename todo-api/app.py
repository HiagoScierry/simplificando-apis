from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os

app = FastAPI(
    title="Todo API",
    description="Uma API simples para gerenciar tarefas",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados para Todo
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime
    updated_at: datetime

# Armazenamento em memória
todo_example = Todo(
    id=1,
    title="Exemplo de Tarefa",
    description="Esta é uma tarefa de exemplo.",
    completed=False,
    created_at=datetime.now(),
    updated_at=datetime.now()
)

todos_db: List[Todo] = [
]
next_id = 1

# Rotas da API
@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {"message": "Todo API está funcionando!"}

@app.get("/app")
async def serve_app():
    """Servir a aplicação web"""
    return FileResponse("index.html")

@app.get("/todos", response_model=List[Todo])
async def get_todos():
    """Listar todas as tarefas"""
    return todos_db

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    """Obter uma tarefa específica por ID"""
    todo = next((todo for todo in todos_db if todo.id == todo_id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return todo

@app.post("/todos", response_model=Todo, status_code=201)
async def create_todo(todo_data: TodoCreate):
    """Criar uma nova tarefa"""
    global next_id

    now = datetime.now()
    new_todo = Todo(
        id=next_id,
        title=todo_data.title,
        description=todo_data.description,
        completed=False,
        created_at=now,
        updated_at=now
    )

    todos_db.append(new_todo)
    next_id += 1

    return new_todo

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_data: TodoUpdate):
    """Atualizar uma tarefa existente"""
    todo_index = next((i for i, todo in enumerate(todos_db) if todo.id == todo_id), None)

    if todo_index is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    todo = todos_db[todo_index]

    # Atualizar apenas os campos fornecidos
    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.description is not None:
        todo.description = todo_data.description
    if todo_data.completed is not None:
        todo.completed = todo_data.completed

    todo.updated_at = datetime.now()
    todos_db[todo_index] = todo

    return todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    """Deletar uma tarefa"""
    todo_index = next((i for i, todo in enumerate(todos_db) if todo.id == todo_id), None)

    if todo_index is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    deleted_todo = todos_db.pop(todo_index)
    return {"message": f"Tarefa '{deleted_todo.title}' deletada com sucesso"}

@app.patch("/todos/{todo_id}/toggle", response_model=Todo)
async def toggle_todo_completed(todo_id: int):
    """Alternar o status de conclusão de uma tarefa"""
    todo_index = next((i for i, todo in enumerate(todos_db) if todo.id == todo_id), None)

    if todo_index is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    todo = todos_db[todo_index]
    todo.completed = not todo.completed
    todo.updated_at = datetime.now()
    todos_db[todo_index] = todo

    return todo

@app.get("/todos/stats")
async def get_todos_stats():
    """Obter estatísticas das tarefas"""
    total = len(todos_db)
    completed = sum(1 for todo in todos_db if todo.completed)
    pending = total - completed

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": round((completed / total * 100) if total > 0 else 0, 2)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)