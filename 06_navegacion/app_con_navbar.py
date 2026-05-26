import flet as ft

# EJERCICIO: App con NavigationBar (barra inferior estilo móvil)
# Este es el patrón de navegación más común en apps de Android/iOS

def main(page: ft.Page):
    page.title = "App con NavBar"
    page.padding = 0

    # ─── Contenido de cada pantalla ────────────────────────────────

    def contenido_inicio():
        return ft.Column(
            controls=[
                ft.Container(height=20),
                ft.Text("Bienvenido", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Esta es la pantalla principal", color=ft.Colors.GREY),
                ft.Divider(),
                # Simula una lista de noticias/cards
                *[
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"Novedad #{i}", weight=ft.FontWeight.BOLD),
                            ft.Text("Descripción corta de la novedad...", color=ft.Colors.GREY, size=13)
                        ]),
                        bgcolor=ft.Colors.BLUE_50,
                        padding=15,
                        border_radius=10
                    )
                    for i in range(1, 5)
                ]
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def contenido_buscar():
        campo = ft.TextField(
            label="Buscar...",
            prefix_icon=ft.Icons.SEARCH,
            expand=True
        )
        resultados = ft.Column()

        def buscar(e):
            resultados.controls.clear()
            if campo.value:
                for i in range(3):
                    resultados.controls.append(
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.ARTICLE),
                            title=ft.Text(f'Resultado para "{campo.value}" #{i+1}'),
                            subtitle=ft.Text("Descripción del resultado...")
                        )
                    )
            page.update()

        campo.on_submit = buscar

        return ft.Column(
            controls=[
                ft.Container(height=20),
                ft.Text("Buscar", size=28, weight=ft.FontWeight.BOLD),
                ft.Row([campo, ft.FilledButton("Buscar", on_click=buscar)]),
                resultados
            ],
            spacing=10
        )

    def contenido_perfil():
        return ft.Column(
            controls=[
                ft.Container(height=20),
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, size=60, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.BLUE,
                    width=100, height=100, border_radius=50,
                    alignment=ft.Alignment(0, 0)
                ),
                ft.Text("Usuario Demo", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("usuario@email.com", color=ft.Colors.GREY),
                ft.Divider(),
                ft.ListTile(leading=ft.Icon(ft.Icons.EDIT), title=ft.Text("Editar perfil")),
                ft.ListTile(leading=ft.Icon(ft.Icons.LOCK), title=ft.Text("Cambiar contraseña")),
                ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT), title=ft.Text("Cerrar sesión"),
                            text_color=ft.Colors.RED),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            scroll=ft.ScrollMode.AUTO
        )

    # ─── Zona de contenido principal ──────────────────────────────
    zona = ft.Container(
        content=contenido_inicio(),
        expand=True,
        padding=ft.Padding.symmetric(horizontal=20)
    )

    titulos = ["Inicio", "Buscar", "Perfil"]
    pantallas = [contenido_inicio, contenido_buscar, contenido_perfil]

    titulo_appbar = ft.Text("Inicio", color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.BOLD)
    page.appbar = ft.AppBar(
        title=titulo_appbar,
        bgcolor=ft.Colors.BLUE,
        center_title=True
    )

    def cambiar_pantalla(e):
        indice = e.control.selected_index
        zona.content = pantallas[indice]()
        titulo_appbar.value = titulos[indice]
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Inicio"),
            ft.NavigationBarDestination(icon=ft.Icons.SEARCH_OUTLINED, selected_icon=ft.Icons.SEARCH, label="Buscar"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINED, selected_icon=ft.Icons.PERSON, label="Perfil"),
        ],
        on_change=cambiar_pantalla,
        selected_index=0
    )

    page.add(zona)


ft.run(main)
