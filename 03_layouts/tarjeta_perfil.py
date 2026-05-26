import flet as ft

# EJERCICIO: Tarjeta de perfil usando layouts combinados
# Practica anidar Column, Row y Container para crear un diseño real

def main(page: ft.Page):
    page.title = "Tarjeta de Perfil"
    page.bgcolor = ft.Colors.GREY_200
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ─── Sección del avatar (ícono de persona) ────────────────────
    avatar = ft.Container(
        content=ft.Icon(ft.Icons.PERSON, size=60, color=ft.Colors.WHITE),
        bgcolor=ft.Colors.BLUE,
        width=100,
        height=100,
        border_radius=50,  # Círculo perfecto: border_radius = mitad del ancho
        alignment=ft.Alignment(0, 0)
    )

    # ─── Información del perfil ────────────────────────────────────
    nombre = ft.Text("Ana García", size=22, weight=ft.FontWeight.BOLD)
    cargo = ft.Text("Desarrolladora Python", size=14, color=ft.Colors.GREY_600)

    # Row con íconos de información (igual que en un CV)
    fila_email = ft.Row(
        controls=[
            ft.Icon(ft.Icons.EMAIL, color=ft.Colors.BLUE, size=18),
            ft.Text("ana@ejemplo.com", size=13)
        ],
        spacing=8  # Espacio entre el ícono y el texto
    )

    fila_ubicacion = ft.Row(
        controls=[
            ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.RED, size=18),
            ft.Text("Bogotá, Colombia", size=13)
        ],
        spacing=8
    )

    # ─── Estadísticas (Row con 3 columnas) ────────────────────────
    # Función helper para crear cada bloque de estadística
    def stat_bloque(numero, etiqueta):
        return ft.Column(
            controls=[
                ft.Text(numero, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                ft.Text(etiqueta, size=12, color=ft.Colors.GREY_600)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2
        )

    fila_stats = ft.Row(
        controls=[
            stat_bloque("42", "Proyectos"),
            ft.VerticalDivider(width=1, color=ft.Colors.GREY_300),
            stat_bloque("128", "Seguidores"),
            ft.VerticalDivider(width=1, color=ft.Colors.GREY_300),
            stat_bloque("89", "Siguiendo"),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )

    # ─── La tarjeta completa ──────────────────────────────────────
    # Column principal que contiene todo, de arriba hacia abajo
    contenido_tarjeta = ft.Column(
        controls=[
            avatar,
            nombre,
            cargo,
            ft.Divider(height=10),
            fila_email,
            fila_ubicacion,
            ft.Divider(height=10),
            fila_stats,
            ft.FilledButton(
                "Seguir",
                icon=ft.Icons.PERSON_ADD,
                bgcolor=ft.Colors.BLUE,
                color=ft.Colors.WHITE,
                width=200
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8
    )

    tarjeta = ft.Container(
        content=contenido_tarjeta,
        bgcolor=ft.Colors.WHITE,
        padding=30,
        border_radius=20,
        width=350,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.GREY_400,
            offset=ft.Offset(0, 5)
        )
    )

    page.add(tarjeta)


ft.run(main)
