import flet as ft

# EJERCICIO: App de lista de tareas usando clases
# Cada tarea es un objeto de la clase ItemTarea
# La app principal gestiona la lista de tareas
#
# CAMBIO en Flet 0.80+: ft.UserControl fue eliminado.
# Ahora usamos clases Python normales con un metodo build()
# que retorna el widget, y actualizamos con widget.update().


class ItemTarea:
    """Representa una sola tarea en la lista"""

    def __init__(self, texto: str, al_eliminar):
        self.texto = texto
        self.completada = False
        self.al_eliminar = al_eliminar
        self._contenedor = None

    def toggle_completada(self, e):
        self.completada = not self.completada
        self._contenedor.content = self._crear_fila()
        self._contenedor.update()

    def eliminar(self, e):
        self.al_eliminar(self)

    def _crear_fila(self) -> ft.Row:
        color_texto = ft.Colors.GREY_400 if self.completada else ft.Colors.BLACK
        decoracion = ft.TextDecoration.LINE_THROUGH if self.completada else ft.TextDecoration.NONE

        return ft.Row(
            controls=[
                ft.Checkbox(
                    value=self.completada,
                    on_change=self.toggle_completada
                ),
                ft.Text(
                    self.texto,
                    size=16,
                    color=color_texto,
                    style=ft.TextStyle(decoration=decoracion),
                    expand=True
                ),
                ft.IconButton(
                    ft.Icons.DELETE_OUTLINE,
                    icon_color=ft.Colors.RED_300,
                    on_click=self.eliminar,
                    tooltip="Eliminar tarea"
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

    def build(self) -> ft.Container:
        """Retorna el widget listo para agregar a la pagina."""
        self._contenedor = ft.Container(
            content=self._crear_fila(),
            bgcolor=ft.Colors.WHITE,
            padding=ft.Padding.symmetric(horizontal=15, vertical=8),
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_200)
        )
        return self._contenedor


def main(page: ft.Page):
    page.title = "Lista de Tareas"
    page.bgcolor = ft.Colors.GREY_100
    page.padding = 20

    lista_ui = ft.Column(spacing=8)
    tareas: list[ItemTarea] = []

    contador = ft.Text("0 tareas pendientes", size=13, color=ft.Colors.GREY)

    def actualizar_contador():
        total = len(tareas)
        completadas = sum(1 for t in tareas if t.completada)
        pendientes = total - completadas
        contador.value = f"{pendientes} pendiente(s) — {completadas} completada(s)"
        page.update()

    def eliminar_tarea(item: ItemTarea):
        tareas.remove(item)
        lista_ui.controls.remove(item._contenedor)
        actualizar_contador()

    def agregar_tarea(e):
        texto = campo_nueva_tarea.value.strip()
        if not texto:
            return

        nueva = ItemTarea(texto=texto, al_eliminar=eliminar_tarea)
        tareas.append(nueva)
        lista_ui.controls.append(nueva.build())
        campo_nueva_tarea.value = ""
        campo_nueva_tarea.focus()
        actualizar_contador()

    campo_nueva_tarea = ft.TextField(
        label="Nueva tarea...",
        expand=True,
        on_submit=agregar_tarea
    )

    boton_agregar = ft.FilledButton(
        "Agregar",
        icon=ft.Icons.ADD,
        on_click=agregar_tarea,
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE
    )

    # Tareas de ejemplo al inicio
    for texto_inicial in ["Leer el README de cada carpeta", "Correr todos los ejercicios", "Modificar los retos"]:
        nueva = ItemTarea(texto=texto_inicial, al_eliminar=eliminar_tarea)
        tareas.append(nueva)
        lista_ui.controls.append(nueva.build())
    actualizar_contador()

    page.add(
        ft.Text("Mi Lista de Tareas", size=28, weight=ft.FontWeight.BOLD),
        contador,
        ft.Divider(),
        ft.Row(controls=[campo_nueva_tarea, boton_agregar]),
        ft.Divider(height=10),
        lista_ui
    )


ft.run(main)
