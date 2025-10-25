from src.config.database.connection import get_connection

class FuncionarioRepository:
    def __init__(self, connection):
        self.connection = connection

    def create_funcionario(self, nome: str, cargo_id: int) -> int:
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO funcionarios (nome, cargo_id) VALUES (?, ?)", (nome, cargo_id))
        self.connection.commit()
        return cursor.lastrowid

    def list_funcionarios(self) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT
                f.id,
                f.nome,
                f.cargo_id,
                c.nome as cargo_nome
            FROM funcionarios f
            INNER JOIN cargos c ON f.cargo_id = c.id
        """)
        funcionarios = cursor.fetchall()
        return [dict(f) for f in funcionarios]

    def get_funcionario_by_id(self, funcionario_id: int) -> dict | None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM funcionarios WHERE id=?", (funcionario_id,))
        funcionario = cursor.fetchone()
        return dict(funcionario) if funcionario else None

    def edit_funcionario(self, funcionario_id: int, nome: str, cargo_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("UPDATE funcionarios SET nome=?, cargo_id=? WHERE id=?", (nome, cargo_id, funcionario_id))
        self.connection.commit()
        return cursor.rowcount > 0

    def delete_funcionario(self, funcionario_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM funcionarios WHERE id=?", (funcionario_id,))
        self.connection.commit()
        return cursor.rowcount > 0

funcionario_repository = FuncionarioRepository(get_connection())