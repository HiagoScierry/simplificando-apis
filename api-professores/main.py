from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.database.init_db import init_db

from src.routes.cargo_route import router as cargo_router
from src.routes.funcionario_route import router as funcionario_router

init_db()

app = FastAPI(title="API Empresa - Funcionários e Cargos")

# permitir o front local acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cargo_router)
app.include_router(funcionario_router)