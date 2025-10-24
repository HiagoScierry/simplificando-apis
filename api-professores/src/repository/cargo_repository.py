from src.config.database.connection import get_connection

class CargoRepository:
    def __init__(self, connection):
        self.connection = connection

    def create_cargo(self, nome: str) -> int:
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO cargos (nome) VALUES (?)", (nome,))
        self.connection.commit()
        return cursor.lastrowid

    def list_cargos(self) -> list:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM cargos")
        cargos = cursor.fetchall()
        return [dict(c) for c in cargos]

    def get_cargo_by_id(self, cargo_id: int) -> dict | None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM cargos WHERE id=?", (cargo_id,))
        cargo = cursor.fetchone()
        return dict(cargo) if cargo else None

    def edit_cargo(self, cargo_id: int, nome: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("UPDATE cargos SET nome=? WHERE id=?", (nome, cargo_id))
        self.connection.commit()
        return cursor.rowcount > 0

    def delete_cargo(self, cargo_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM cargos WHERE id=?", (cargo_id,))
        self.connection.commit()
        return cursor.rowcount > 0

cargo_repository = CargoRepository(get_connection())