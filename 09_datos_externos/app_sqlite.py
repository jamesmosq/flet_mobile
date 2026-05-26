import flet as ft
import sqlite3
from pathlib import Path

# EJERCICIO: App con SQLite — los datos se guardan aunque cierres la app
# Patrón: separamos la lógica de datos (Repositorio) de la UI (main)

# ─────────────────────────────────────────────────────────────────
# CAPA DE DATOS: El repositorio maneja todo lo relacionado con SQLite
# ─────────────────────────────────────────────────────────────────

class RepositorioProductos:
    """
    Esta clase encapsula todas las operaciones de base de datos.
    La UI no sabe ni le importa cómo se guardan los datos.
    """

    def __init__(self):
        # El archivo .db se crea en la misma carpeta que este script
        ruta_db = Path(__file__).parent / "productos.db"
        self.conexion = sqlite3.connect(str(ruta_db), check_same_thread=False)
        self.conexion.row_factory = sqlite3.Row  # Devuelve filas como diccionarios
        self._crear_tablas()

    def _crear_tablas(self):
        self.conexion.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre  TEXT    NOT NULL,
                precio  REAL    NOT NULL,
                stock   INTEGER DEFAULT 0
            )
        """)
        self.conexion.commit()

    def obtener_todos(self) -> list:
        cursor = self.conexion.execute("SELECT * FROM productos ORDER BY nombre")
        return [dict(fila) for fila in cursor.fetchall()]

    def insertar(self, nombre: str, precio: float, stock: int) -> int:
        cursor = self.conexion.execute(
            "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
            (nombre, precio, stock)
        )
        self.conexion.commit()
        return cursor.lastrowid

    def actualizar(self, id: int, nombre: str, precio: float, stock: int):
        self.conexion.execute(
            "UPDATE productos SET nombre=?, precio=?, stock=? WHERE id=?",
            (nombre, precio, stock, id)
        )
        self.conexion.commit()

    def eliminar(self, id: int):
        self.conexion.execute("DELETE FROM productos WHERE id=?", (id,))
        self.conexion.commit()

    def cerrar(self):
        self.conexion.close()


# ─────────────────────────────────────────────────────────────────
# CAPA DE UI: La app solo habla con el repositorio
# ─────────────────────────────────────────────────────────────────

def main(page: ft.Page):
    page.title = "Inventario con SQLite"
    page.padding = 0

    repo = RepositorioProductos()

    lista = ft.ListView(expand=True, spacing=5, padding=15)

    def construir_lista():
        lista.controls.clear()
        productos = repo.obtener_todos()

        if not productos:
            lista.controls.append(
                ft.Container(
                    content=ft.Column(
                        [ft.Icon(ft.Icons.INVENTORY_2, size=60, color=ft.Colors.GREY_300),
                         ft.Text("No hay productos. Agrega el primero.", color=ft.Colors.GREY)],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.Alignment(0, 0),
                    expand=True
                )
            )
        else:
            for p in productos:
                color_stock = ft.Colors.RED if p["stock"] == 0 else ft.Colors.GREEN
                lista.controls.append(
                    ft.ListTile(
                        leading=ft.CircleAvatar(
                            content=ft.Text(p["nombre"][0].upper()),
                            bgcolor=ft.Colors.INDIGO
                        ),
                        title=ft.Text(p["nombre"], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Row([
                            ft.Text(f"${p['precio']:,.0f}", color=ft.Colors.GREEN_700),
                            ft.Text(" | Stock: "),
                            ft.Text(str(p["stock"]), color=color_stock, weight=ft.FontWeight.BOLD)
                        ]),
                        trailing=ft.Row(
                            controls=[
                                ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE,
                                              on_click=lambda e, prod=p: abrir_formulario(prod)),
                                ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED,
                                              on_click=lambda e, prod=p: eliminar(prod["id"]))
                            ],
                            tight=True
                        )
                    )
                )
        page.update()

    # ─── Formulario (page.open / page.close — Flet 0.85) ─────────
    def abrir_formulario(producto=None):
        campo_nombre = ft.TextField(
            label="Nombre del producto", expand=True,
            value=producto["nombre"] if producto else ""
        )
        campo_precio = ft.TextField(
            label="Precio", keyboard_type=ft.KeyboardType.NUMBER, width=150,
            value=str(producto["precio"]) if producto else ""
        )
        campo_stock = ft.TextField(
            label="Stock", keyboard_type=ft.KeyboardType.NUMBER, width=100,
            value=str(producto["stock"]) if producto else "0"
        )
        titulo = "Editar Producto" if producto else "Nuevo Producto"

        def guardar(e):
            valido = True
            if not campo_nombre.value.strip():
                campo_nombre.error_text = "Obligatorio"
                valido = False
            else:
                campo_nombre.error_text = None
            try:
                precio = float(campo_precio.value)
                campo_precio.error_text = None
            except (ValueError, TypeError):
                campo_precio.error_text = "Debe ser un numero"
                valido = False

            if not valido:
                page.update()
                return

            stock = int(campo_stock.value or 0)
            if producto:
                repo.actualizar(producto["id"], campo_nombre.value.strip(), precio, stock)
            else:
                repo.insertar(campo_nombre.value.strip(), precio, stock)

            page.pop_dialog()
            construir_lista()

        def cancelar(e):
            page.pop_dialog()

        dlg = ft.AlertDialog(
            title=ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    [campo_nombre, ft.Row([campo_precio, campo_stock])],
                    spacing=10, tight=True
                ),
                width=400
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.FilledButton("Guardar", on_click=guardar,
                                bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.show_dialog(dlg)

    def eliminar(id: int):
        repo.eliminar(id)
        construir_lista()

    page.appbar = ft.AppBar(
        title=ft.Text("Inventario (SQLite)", color=ft.Colors.WHITE),
        bgcolor=ft.Colors.INDIGO,
        actions=[
            ft.IconButton(ft.Icons.ADD, icon_color=ft.Colors.WHITE,
                          tooltip="Agregar producto",
                          on_click=lambda e: abrir_formulario())
        ]
    )

    # Limpiar la conexión cuando la app se cierra
    def al_cerrar(e):
        repo.cerrar()

    page.on_close = al_cerrar

    page.add(lista)
    construir_lista()  # llamar después de add() para que page.update() funcione


ft.run(main)
