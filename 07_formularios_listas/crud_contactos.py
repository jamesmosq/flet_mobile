import flet as ft
from dataclasses import dataclass
from typing import List

# EJERCICIO: CRUD completo de contactos
# C = Crear  → botón "Nuevo Contacto"
# R = Leer   → lista de tarjetas
# U = Editar → botón "Editar" en cada tarjeta
# D = Borrar → botón "Eliminar" en cada tarjeta
#
# IMPORTANTE Flet 0.85:
#   Abrir diálogo  → page.show_dialog(dialogo)
#   Cerrar diálogo → page.pop_dialog()
#   page.open() / page.close() NO existen en Flet 0.85


@dataclass
class Contacto:
    id: int
    nombre: str
    telefono: str
    email: str


def main(page: ft.Page):
    page.title = "Agenda de Contactos"
    page.bgcolor = ft.Colors.GREY_100
    page.padding = 0

    # ─── Estado ───────────────────────────────────────────────────
    contactos: List[Contacto] = [
        Contacto(1, "Ana Garcia",   "300-123-4567", "ana@email.com"),
        Contacto(2, "Carlos Lopez", "310-987-6543", "carlos@email.com"),
        Contacto(3, "Maria Torres", "320-555-1234", "maria@email.com"),
    ]
    siguiente_id = [4]

    lista_contactos = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)
    contador_texto  = ft.Text("", size=13, color=ft.Colors.GREY_600)

    # ─── R: Construir tarjeta visual por contacto ─────────────────
    def tarjeta_contacto(c: Contacto) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    c.nombre[0].upper(),
                                    size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE
                                ),
                                bgcolor=ft.Colors.BLUE,
                                width=50, height=50, border_radius=25,
                                alignment=ft.Alignment(0, 0)
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(c.nombre,   size=16, weight=ft.FontWeight.BOLD),
                                    ft.Text(c.telefono, size=13, color=ft.Colors.GREY_600),
                                ],
                                spacing=2, expand=True
                            )
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.EMAIL_OUTLINED, size=15, color=ft.Colors.GREY_500),
                            ft.Text(c.email, size=13, color=ft.Colors.GREY_600)
                        ],
                        spacing=6
                    ),
                    ft.Divider(height=6),
                    ft.Row(
                        controls=[
                            ft.FilledButton(         # U: Update
                                "Editar",
                                icon=ft.Icons.EDIT,
                                on_click=lambda e, x=c: abrir_formulario(x),
                                expand=True
                            ),
                            ft.FilledButton(         # D: Delete
                                "Eliminar",
                                icon=ft.Icons.DELETE,
                                on_click=lambda e, x=c: confirmar_eliminar(x),
                                bgcolor=ft.Colors.RED_400,
                                color=ft.Colors.WHITE,
                                expand=True
                            ),
                        ],
                        spacing=8
                    )
                ],
                spacing=8
            ),
            bgcolor=ft.Colors.WHITE,
            padding=16,
            border_radius=12,
            shadow=ft.BoxShadow(
                blur_radius=4, color=ft.Colors.GREY_300, offset=ft.Offset(0, 2)
            )
        )

    # ─── R: Reconstruir toda la lista en pantalla ─────────────────
    def construir_lista():
        lista_contactos.controls.clear()
        if not contactos:
            lista_contactos.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.CONTACTS, size=60, color=ft.Colors.GREY_300),
                            ft.Text("Sin contactos. Agrega el primero.",
                                    color=ft.Colors.GREY, text_align=ft.TextAlign.CENTER)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.Alignment(0, 0),
                    padding=40
                )
            )
        else:
            for c in contactos:
                lista_contactos.controls.append(tarjeta_contacto(c))

        total = len(contactos)
        contador_texto.value = f"{total} contacto{'s' if total != 1 else ''}"
        page.update()

    # ─── C y U: Formulario de crear / editar ──────────────────────
    def abrir_formulario(contacto: Contacto = None):
        # Campos del formulario — se crean frescos en cada apertura
        campo_nombre   = ft.TextField(label="Nombre completo",
                                      value=contacto.nombre   if contacto else "")
        campo_telefono = ft.TextField(label="Telefono",
                                      value=contacto.telefono if contacto else "")
        campo_email    = ft.TextField(label="Email",
                                      value=contacto.email    if contacto else "")

        titulo = "Editar Contacto" if contacto else "Nuevo Contacto"

        def guardar(e):
            # Validar campos obligatorios
            valido = True
            if not campo_nombre.value.strip():
                campo_nombre.error_text = "Obligatorio"
                valido = False
            else:
                campo_nombre.error_text = None

            if not campo_email.value.strip():
                campo_email.error_text = "Obligatorio"
                valido = False
            else:
                campo_email.error_text = None

            if not valido:
                page.update()
                return

            if contacto:
                # U: actualizar el objeto existente
                contacto.nombre   = campo_nombre.value.strip()
                contacto.telefono = campo_telefono.value.strip()
                contacto.email    = campo_email.value.strip()
            else:
                # C: crear un nuevo contacto y agregar a la lista
                contactos.append(Contacto(
                    id=siguiente_id[0],
                    nombre=campo_nombre.value.strip(),
                    telefono=campo_telefono.value.strip(),
                    email=campo_email.value.strip()
                ))
                siguiente_id[0] += 1

            page.pop_dialog()   # cerrar el diálogo correctamente
            construir_lista()

        def cancelar(e):
            page.pop_dialog()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    controls=[campo_nombre, campo_telefono, campo_email],
                    spacing=10, tight=True
                ),
                width=340
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.FilledButton(
                    "Guardar",
                    icon=ft.Icons.SAVE,
                    on_click=guardar,
                    bgcolor=ft.Colors.BLUE,
                    color=ft.Colors.WHITE
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.show_dialog(dlg)

    # ─── D: Confirmación de eliminación ───────────────────────────
    def confirmar_eliminar(contacto: Contacto):
        def eliminar(e):
            contactos.remove(contacto)
            page.pop_dialog()
            construir_lista()

        def cancelar(e):
            page.pop_dialog()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar contacto"),
            content=ft.Text(
                f"¿Seguro que quieres eliminar a {contacto.nombre}?\n"
                "Esta accion no se puede deshacer."
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.FilledButton(
                    "Si, eliminar",
                    icon=ft.Icons.DELETE_FOREVER,
                    on_click=eliminar,
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.show_dialog(dlg)

    # ─── AppBar y botón principal ──────────────────────────────────
    page.appbar = ft.AppBar(
        title=ft.Text("Mis Contactos", color=ft.Colors.WHITE),
        bgcolor=ft.Colors.BLUE,
        center_title=True
    )

    construir_lista()

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    # C: botón siempre visible en la parte superior
                    ft.FilledButton(
                        "Nuevo Contacto",
                        icon=ft.Icons.PERSON_ADD,
                        on_click=lambda e: abrir_formulario(),
                        bgcolor=ft.Colors.BLUE,
                        color=ft.Colors.WHITE
                    ),
                    ft.Row(
                        controls=[
                            ft.Text("Contactos", size=18, weight=ft.FontWeight.BOLD),
                            contador_texto
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    lista_contactos,
                ],
                spacing=12,
                expand=True
            ),
            padding=16,
            expand=True
        )
    )


ft.run(main)
