import flet as ft

# Este archivo muestra cómo funcionan los layouts principales de Flet
# Corre el archivo y observa cómo se organiza cada sección en pantalla

def main(page: ft.Page):
    page.title = "Layouts en Flet"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    # ─── COLUMN: de arriba hacia abajo ────────────────────────────
    ejemplo_column = ft.Column(
        controls=[
            ft.Text("Soy el primero (arriba)", color=ft.Colors.RED),
            ft.Text("Soy el segundo (medio)", color=ft.Colors.GREEN),
            ft.Text("Soy el tercero (abajo)", color=ft.Colors.BLUE),
        ]
    )

    caja_column = ft.Container(
        content=ft.Column([
            ft.Text("ft.Column — vertical", weight=ft.FontWeight.BOLD),
            ejemplo_column
        ]),
        border=ft.Border.all(2, ft.Colors.GREY_400),
        padding=15,
        border_radius=10
    )

    # ─── ROW: de izquierda a derecha ──────────────────────────────
    ejemplo_row = ft.Row(
        controls=[
            ft.Container(ft.Text("A"), bgcolor=ft.Colors.RED_100, padding=10, border_radius=5),
            ft.Container(ft.Text("B"), bgcolor=ft.Colors.GREEN_100, padding=10, border_radius=5),
            ft.Container(ft.Text("C"), bgcolor=ft.Colors.BLUE_100, padding=10, border_radius=5),
        ]
    )

    caja_row = ft.Container(
        content=ft.Column([
            ft.Text("ft.Row — horizontal", weight=ft.FontWeight.BOLD),
            ejemplo_row
        ]),
        border=ft.Border.all(2, ft.Colors.GREY_400),
        padding=15,
        border_radius=10
    )

    # ─── CONTAINER: caja decorativa ───────────────────────────────
    ejemplo_container = ft.Container(
        content=ft.Text("Soy un Container con estilo", color=ft.Colors.WHITE, size=18),
        bgcolor=ft.Colors.INDIGO,
        padding=20,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.INDIGO_200),
        width=300,
        height=80,
    )

    caja_container = ft.Container(
        content=ft.Column([
            ft.Text("ft.Container — caja decorativa", weight=ft.FontWeight.BOLD),
            ejemplo_container
        ]),
        border=ft.Border.all(2, ft.Colors.GREY_400),
        padding=15,
        border_radius=10
    )

    # ─── STACK: uno encima del otro ───────────────────────────────
    ejemplo_stack = ft.Stack(
        controls=[
            # Este es el fondo (se dibuja primero)
            ft.Container(
                bgcolor=ft.Colors.TEAL,
                width=250,
                height=100,
                border_radius=10
            ),
            # Este texto queda "encima" del fondo
            ft.Container(
                content=ft.Text("Texto sobre el fondo", color=ft.Colors.WHITE, size=18),
                padding=ft.Padding.only(left=20, top=35)
            )
        ],
        width=250,
        height=100
    )

    caja_stack = ft.Container(
        content=ft.Column([
            ft.Text("ft.Stack — uno encima del otro", weight=ft.FontWeight.BOLD),
            ejemplo_stack
        ]),
        border=ft.Border.all(2, ft.Colors.GREY_400),
        padding=15,
        border_radius=10
    )

    # ─── ROW con alineación centrada ──────────────────────────────
    ejemplo_row_centrado = ft.Row(
        controls=[
            ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER),
            ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER),
            ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER),
        ],
        alignment=ft.MainAxisAlignment.CENTER  # Centra los íconos horizontalmente
    )

    caja_centrado = ft.Container(
        content=ft.Column([
            ft.Text("ft.Row centrado", weight=ft.FontWeight.BOLD),
            ejemplo_row_centrado
        ]),
        border=ft.Border.all(2, ft.Colors.GREY_400),
        padding=15,
        border_radius=10
    )

    page.add(
        ft.Text("Ejemplos de Layouts", size=28, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        caja_column,
        ft.Divider(),
        caja_row,
        ft.Divider(),
        caja_container,
        ft.Divider(),
        caja_stack,
        ft.Divider(),
        caja_centrado
    )


ft.run(main)
