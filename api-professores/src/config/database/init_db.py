from src.config.database.connection import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Criar tabela cargos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cargos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)

    # Criar tabela funcionarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cargo_id INTEGER,
            FOREIGN KEY(cargo_id) REFERENCES cargos(id)
        )
    """)

    conn.commit()
    conn.close()

