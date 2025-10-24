# Todo API

Uma API simples para gerenciar tarefas (todos) usando FastAPI com armazenamento em memória.

## Funcionalidades

- ✅ Criar tarefas
- ✅ Listar todas as tarefas
- ✅ Obter tarefa por ID
- ✅ Atualizar tarefas
- ✅ Deletar tarefas
- ✅ Alternar status de conclusão
- ✅ Estatísticas das tarefas

## Como executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o servidor:
```bash
python app.py
```

Ou usando uvicorn diretamente:
```bash
uvicorn app:app --reload
```

3. Acesse a documentação da API em: http://localhost:8000/docs

## Endpoints

### GET /
- Endpoint raiz da API

### GET /todos
- Lista todas as tarefas

### GET /todos/{todo_id}
- Obtém uma tarefa específica por ID

### POST /todos
- Cria uma nova tarefa
- Body: `{"title": "string", "description": "string (opcional)"}`

### PUT /todos/{todo_id}
- Atualiza uma tarefa existente
- Body: `{"title": "string (opcional)", "description": "string (opcional)", "completed": "boolean (opcional)"}`

### DELETE /todos/{todo_id}
- Deleta uma tarefa

### PATCH /todos/{todo_id}/toggle
- Alterna o status de conclusão de uma tarefa

### GET /todos/stats
- Retorna estatísticas das tarefas (total, concluídas, pendentes, taxa de conclusão)

## Exemplo de uso

```python
import requests

# Criar uma tarefa
response = requests.post("http://localhost:8000/todos", 
                        json={"title": "Estudar FastAPI", "description": "Aprender sobre APIs REST"})

# Listar tarefas
response = requests.get("http://localhost:8000/todos")

# Marcar como concluída
response = requests.patch("http://localhost:8000/todos/1/toggle")
```

## Modelos de dados

### TodoCreate
```json
{
  "title": "string",
  "description": "string (opcional)"
}
```

### TodoUpdate
```json
{
  "title": "string (opcional)",
  "description": "string (opcional)",
  "completed": "boolean (opcional)"
}
```

### Todo
```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```
