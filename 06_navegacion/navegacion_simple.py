import flet as ft

# EJERCICIO: Navegación simple cambiando el contenido central
# Es el enfoque más fácil de entender para empezar con navegación

def main(page: ft.Page):
    page.title = "Navegación Simple"
    page.padding = 0

    # ─── Pantallas ─────────────────────────────────────────────────
    # Cada "pantalla" es simplemente un Container con contenido diferente

    def pantalla_inicio():
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(ft.Icons.HOME, size=80, color=ft.Colors.BLUE),
                    ft.Text("Pantalla de Inicio", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text("Esta es la pantalla principal de la app.", size=16, color=ft.Colors.GREY),
                    ft.FilledButton(
                        "Ir a Mi Perfil",
                        icon=ft.Icons.PERSON,
                        on_click=lambda e: navegar("perfil")
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15
            ),
            expand=True,
            alignment=ft.Alignment(0, 0)
        )

    def pantalla_perfil():
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(ft.Icons.PERSON, size=80, color=ft.Colors.GREEN),
                    ft.Text("Mi Perfil", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text("Aquí va la información del usuario.", size=16, color=ft.Colors.GREY),
                    ft.FilledButton(
                        "Ir a Configuración",
                        icon=ft.Icons.SETTINGS,
                        on_click=lambda e: navegar("config")
                    ),
                    ft.TextButton(
                        "Volver al Inicio",
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda e: navegar("inicio")
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15
            ),
            expand=True,
            alignment=ft.Alignment(0, 0)
        )

    def pantalla_config():
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(ft.Icons.SETTINGS, size=80, color=ft.Colors.ORANGE),
                    ft.Text("Configuración", size=28, weight=ft.FontWeight.BOLD),
                    ft.Switch(label="Modo oscuro"),
                    ft.Switch(label="Notificaciones", value=True),
                    ft.Slider(min=0, max=100, value=70, label="Volumen: {value}%"),
                    ft.TextButton(
                        "Volver al Inicio",
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda e: navegar("inicio")
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15
            ),
            expand=True,
            alignment=ft.Alignment(0, 0)
        )

    # ─── Zona de contenido ─────────────────────────────────────────
    zona_contenido = ft.Container(expand=True)

    def navegar(pantalla: str):
        """Cambia el contenido central según la pantalla elegida"""
        if pantalla == "inicio":
            zona_contenido.content = pantalla_inicio()
            titulo_appbar.value = "Inicio"
        elif pantalla == "perfil":
            zona_contenido.content = pantalla_perfil()
            titulo_appbar.value = "Mi Perfil"
        elif pantalla == "config":
            zona_contenido.content = pantalla_config()
            titulo_appbar.value = "Configuración"
        page.update()

    # ─── AppBar (barra superior) ───────────────────────────────────
    titulo_appbar = ft.Text("Inicio", color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.BOLD)
    page.appbar = ft.AppBar(
        title=titulo_appbar,
        bgcolor=ft.Colors.BLUE,
        center_title=True
    )

    # Mostrar la pantalla de inicio al arrancar
    navegar("inicio")

    page.add(zona_contenido)


ft.run(main)
