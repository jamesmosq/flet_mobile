import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from modelos import Gasto, Categoria, CATEGORIAS_DEFAULT


class BaseDatos:
    """Repositorio central de la app — maneja todas las operaciones SQLite."""

    def __init__(self):
        ruta = Path(__file__).parent / "gastos.db"
        self.conn = sqlite3.connect(str(ruta), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._inicializar()

    def _inicializar(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS categorias (
                id      INTEGER PRIMARY KEY,
                nombre  TEXT NOT NULL,
                icono   TEXT,
                color   TEXT
            );

            CREATE TABLE IF NOT EXISTS gastos (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion   TEXT NOT NULL,
                monto         REAL NOT NULL,
                categoria_id  INTEGER REFERENCES categorias(id),
                fecha         TEXT NOT NULL
            );
        """)
        self.conn.commit()
        self._sembrar_categorias()

    def _sembrar_categorias(self):
        """Inserta las categorías por defecto si la tabla está vacía."""
        cantidad = self.conn.execute("SELECT COUNT(*) FROM categorias").fetchone()[0]
        if cantidad == 0:
            self.conn.executemany(
                "INSERT INTO categorias (id, nombre, icono, color) VALUES (?, ?, ?, ?)",
                [(c.id, c.nombre, c.icono, c.color) for c in CATEGORIAS_DEFAULT]
            )
            self.conn.commit()

    # ─── Categorías ───────────────────────────────────────────────

    def obtener_categorias(self) -> List[Categoria]:
        rows = self.conn.execute("SELECT * FROM categorias ORDER BY nombre").fetchall()
        return [Categoria(**dict(r)) for r in rows]

    # ─── Gastos ───────────────────────────────────────────────────

    def obtener_gastos(self, mes: Optional[str] = None) -> List[Gasto]:
        if mes:
            sql = """
                SELECT g.*, c.nombre AS categoria_nombre, c.color AS categoria_color
                FROM gastos g LEFT JOIN categorias c ON g.categoria_id = c.id
                WHERE strftime('%Y-%m', g.fecha) = ?
                ORDER BY g.fecha DESC
            """
            rows = self.conn.execute(sql, (mes,)).fetchall()
        else:
            sql = """
                SELECT g.*, c.nombre AS categoria_nombre, c.color AS categoria_color
                FROM gastos g LEFT JOIN categorias c ON g.categoria_id = c.id
                ORDER BY g.fecha DESC
            """
            rows = self.conn.execute(sql).fetchall()
        return [Gasto(**dict(r)) for r in rows]

    def insertar_gasto(self, descripcion: str, monto: float, categoria_id: int) -> int:
        cur = self.conn.execute(
            "INSERT INTO gastos (descripcion, monto, categoria_id, fecha) VALUES (?, ?, ?, ?)",
            (descripcion, monto, categoria_id, datetime.now().isoformat())
        )
        self.conn.commit()
        return cur.lastrowid

    def eliminar_gasto(self, id: int):
        self.conn.execute("DELETE FROM gastos WHERE id=?", (id,))
        self.conn.commit()

    def total_mes(self, mes: str) -> float:
        row = self.conn.execute(
            "SELECT COALESCE(SUM(monto), 0) FROM gastos WHERE strftime('%Y-%m', fecha) = ?",
            (mes,)
        ).fetchone()
        return float(row[0])

    def total_por_categoria(self, mes: str) -> List[dict]:
        rows = self.conn.execute("""
            SELECT c.nombre, c.color, COALESCE(SUM(g.monto), 0) AS total
            FROM categorias c
            LEFT JOIN gastos g ON g.categoria_id = c.id
                AND strftime('%Y-%m', g.fecha) = ?
            GROUP BY c.id
            ORDER BY total DESC
        """, (mes,)).fetchall()
        return [dict(r) for r in rows]

    def cerrar(self):
        self.conn.close()
