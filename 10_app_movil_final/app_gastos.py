import flet as ft
from datetime import datetime
import sys
import os

# Aseguramos que los módulos locales (db.py, modelos.py) se encuentren
sys.path.insert(0, os.path.dirname(__file__))

from db import BaseDatos
from modelos import Gasto, Categoria

# ─────────────────────────────────────────────────────────────────
# APP FINAL: Gestor de Gastos Personales
# Combina todo lo aprendido en la ruta:
#   - Widgets y layouts (carpetas 02, 03)
#   - Eventos y estado (carpeta 04)
#   - POO con UserControl (carpeta 05)
#   - Navegación con NavigationBar (carpeta 06)
#   - Formularios y listas CRUD (carpeta 07)
#   - Temas (carpeta 08)
#   - SQLite persistente (carpeta 09)
# ─────────────────────────────────────────────────────────────────


class TarjetaGasto:
    """Componente reutilizable para mostrar un gasto en la lista."""

    def __init__(self, gasto: Gasto, al_eliminar):
        self.gasto = gasto
        self.al_eliminar = al_eliminar

    def build(self):
        color = self.gasto.categoria_color or "#607D8B"
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=5,
                        height=60,
                        bgcolor=color,
                        border_radius=ft.BorderRadius.only(top_left=5, bottom_left=5)
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(self.gasto.descripcion, weight=ft.FontWeight.BOLD, size=15),
                            ft.Text(
                                f"{self.gasto.categoria_nombre or 'Sin categoria'} · {self.gasto.fecha_formateada}",
                                size=12, color=ft.Colors.GREY
                            )
                        ],
                        spacing=2,
                        expand=True
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(f"${self.gasto.monto:,.0f}", size=16,
                                    weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                            ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.GREY_400,
                                          icon_size=20, on_click=lambda e: self.al_eliminar(self.gasto.id))
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        spacing=0
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=ft.Padding.only(right=10, top=5, bottom=5),
            shadow=ft.BoxShadow(blur_radius=3, color=ft.Colors.GREY_200)
        )


def main(page: ft.Page):
    page.title = "Mis Gastos"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    db = BaseDatos()
    mes_actual = datetime.now().strftime("%Y-%m")
    categorias = db.obtener_categorias()

    # ─── PANTALLA 1: RESUMEN ──────────────────────────────────────
    def construir_resumen():
        total = db.total_mes(mes_actual)
        por_categoria = db.total_por_categoria(mes_actual)
        gastos_mes = db.obtener_gastos(mes_actual)

        # Barras de progreso por categoría
        barras = []
        max_total = max((r["total"] for r in por_categoria), default=1) or 1
        for cat in por_categoria:
            if cat["total"] > 0:
                barras.append(
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(cat["nombre"], size=13, expand=True),
                                    ft.Text(f"${cat['total']:,.0f}", size=13,
                                            weight=ft.FontWeight.BOLD)
                                ]
                            ),
                            ft.ProgressBar(
                                value=cat["total"] / max_total,
                                color=cat["color"],
                                bgcolor=ft.Colors.GREY_200,
                                height=8,
                                border_radius=4
                            )
                        ],
                        spacing=4
                    )
                )

        ultimos_gastos = [
            TarjetaGasto(g, lambda id: None).build()
            for g in gastos_mes[:3]
        ]

        return ft.Column(
            controls=[
                # Card del total del mes
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                datetime.now().strftime("%B %Y").capitalize(),
                                color=ft.Colors.WHITE70, size=14
                            ),
                            ft.Text(f"${total:,.0f}", color=ft.Colors.WHITE,
                                    size=36, weight=ft.FontWeight.BOLD),
                            ft.Text("Gasto total del mes", color=ft.Colors.WHITE70, size=12)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4
                    ),
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment(-1, -1),
                        end=ft.Alignment(1, 1),
                        colors=[ft.Colors.INDIGO_700, ft.Colors.PURPLE_700]
                    ),
                    padding=30,
                    alignment=ft.Alignment(0, 0),
                    border_radius=ft.BorderRadius.only(bottom_left=25, bottom_right=25)
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Por categoria", size=16, weight=ft.FontWeight.BOLD),
                            *(barras if barras else [ft.Text("Sin gastos este mes", color=ft.Colors.GREY)]),
                            ft.Divider(),
                            ft.Text("Ultimos gastos", size=16, weight=ft.FontWeight.BOLD),
                            *(ultimos_gastos if ultimos_gastos else [ft.Text("Ningun gasto registrado", color=ft.Colors.GREY)]),
                        ],
                        spacing=12
                    ),
                    padding=20
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=0
        )

    # ─── PANTALLA 2: LISTA DE GASTOS ─────────────────────────────
    lista_gastos_col = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)

    def construir_lista_gastos():
        lista_gastos_col.controls.clear()
        gastos = db.obtener_gastos(mes_actual)
        if not gastos:
            lista_gastos_col.controls.append(
                ft.Container(
                    content=ft.Column(
                        [ft.Icon(ft.Icons.RECEIPT_LONG, size=60, color=ft.Colors.GREY_300),
                         ft.Text("Sin gastos. Agrega el primero con el boton +",
                                 color=ft.Colors.GREY, text_align=ft.TextAlign.CENTER)],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.Alignment(0, 0),
                    expand=True,
                    padding=40
                )
            )
        else:
            for gasto in gastos:
                lista_gastos_col.controls.append(
                    TarjetaGasto(gasto, eliminar_gasto).build()
                )
        page.update()

    def eliminar_gasto(id: int):
        db.eliminar_gasto(id)
        construir_lista_gastos()
        zona.content = construir_resumen()
        page.update()

    pantalla_lista = ft.Container(
        content=ft.Column(
            controls=[lista_gastos_col],
            expand=True
        ),
        padding=ft.Padding.symmetric(horizontal=15, vertical=10),
        expand=True
    )

    # ─── PANTALLA 3: AJUSTES ─────────────────────────────────────
    switch_tema = ft.Switch(
        label="Modo oscuro",
        value=page.theme_mode == ft.ThemeMode.DARK
    )

    def toggle_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if switch_tema.value else ft.ThemeMode.LIGHT
        page.update()

    switch_tema.on_change = toggle_tema

    pantalla_ajustes = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Ajustes", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                switch_tema,
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.INFO_OUTLINE),
                    title=ft.Text("Gestor de Gastos"),
                    subtitle=ft.Text("Version 1.0 — hecho con Flet + Python")
                )
            ],
            spacing=10
        ),
        padding=20
    )

    # ─── FORMULARIO: Agregar gasto ────────────────────────────────
    campo_desc = ft.TextField(label="Descripcion del gasto", expand=True)
    campo_monto = ft.TextField(label="Monto ($)", keyboard_type=ft.KeyboardType.NUMBER, width=150)
    dropdown_cat = ft.Dropdown(
        label="Categoria",
        options=[ft.dropdown.Option(key=str(c.id), text=c.nombre) for c in categorias],
        value=str(categorias[0].id) if categorias else None,
        width=300
    )

    def abrir_formulario(e):
        campo_desc.value = ""
        campo_monto.value = ""
        campo_desc.error_text = None
        campo_monto.error_text = None

        def guardar(e):
            valido = True
            if not campo_desc.value.strip():
                campo_desc.error_text = "Obligatorio"
                valido = False
            else:
                campo_desc.error_text = None
            try:
                monto = float(campo_monto.value)
                campo_monto.error_text = None
            except (ValueError, TypeError):
                campo_monto.error_text = "Numero invalido"
                valido = False

            if not valido:
                page.update()
                return

            db.insertar_gasto(
                campo_desc.value.strip(),
                monto,
                int(dropdown_cat.value)
            )
            page.pop_dialog()
            construir_lista_gastos()
            zona.content = construir_resumen()
            page.update()

        def cancelar(e):
            page.pop_dialog()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nuevo Gasto"),
            content=ft.Container(
                content=ft.Column(
                    [campo_desc, campo_monto, dropdown_cat],
                    spacing=10, tight=True
                ),
                width=350
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.FilledButton("Guardar", on_click=guardar,
                                bgcolor=ft.Colors.INDIGO, color=ft.Colors.WHITE)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.show_dialog(dlg)

    # ─── NAVEGACIÓN Y ESTRUCTURA PRINCIPAL ───────────────────────
    titulos = ["Resumen", "Mis Gastos", "Ajustes"]
    zona = ft.Container(content=construir_resumen(), expand=True)
    construir_lista_gastos()

    def cambiar_pantalla(e):
        idx = e.control.selected_index
        titulo_bar.value = titulos[idx]
        if idx == 0:
            zona.content = construir_resumen()
        elif idx == 1:
            zona.content = pantalla_lista
        else:
            zona.content = pantalla_ajustes
        # El FAB solo aparece en la pantalla de gastos
        page.floating_action_button.visible = idx == 1
        page.update()

    titulo_bar = ft.Text("Resumen", color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.BOLD)

    page.appbar = ft.AppBar(
        title=titulo_bar,
        bgcolor=ft.Colors.INDIGO_700,
        center_title=True
    )

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Resumen"),
            ft.NavigationBarDestination(icon=ft.Icons.RECEIPT_LONG_OUTLINED, selected_icon=ft.Icons.RECEIPT_LONG, label="Gastos"),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label="Ajustes"),
        ],
        on_change=cambiar_pantalla,
        selected_index=0
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=abrir_formulario,
        bgcolor=ft.Colors.INDIGO,
        visible=False
    )

    page.on_close = lambda e: db.cerrar()
    page.add(zona)


ft.run(main)
