import flet as ft

# EJERCICIO: Toggle entre modo oscuro y modo claro
# También muestra cómo cambiar el color semilla del tema

def main(page: ft.Page):
    page.title = "Temas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)

    # ─── Colores de tema disponibles ──────────────────────────────
    colores_tema = {
        "Azul": ft.Colors.BLUE,
        "Verde": ft.Colors.GREEN,
        "Naranja": ft.Colors.ORANGE,
        "Morado": ft.Colors.PURPLE,
        "Rojo": ft.Colors.RED,
    }

    texto_modo = ft.Text("Modo Claro", size=18)
    icono_modo = ft.Icon(ft.Icons.LIGHT_MODE, size=30)

    def toggle_modo(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            texto_modo.value = "Modo Oscuro"
            icono_modo.name = ft.Icons.DARK_MODE
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            texto_modo.value = "Modo Claro"
            icono_modo.name = ft.Icons.LIGHT_MODE
        page.update()

    def cambiar_color(color_valor):
        page.theme = ft.Theme(color_scheme_seed=color_valor)
        page.update()

    # Botones de color de tema
    botones_color = ft.Row(
        controls=[
            ft.FilledButton(
                nombre,
                bgcolor=color,
                color=ft.Colors.WHITE,
                on_click=lambda e, c=color: cambiar_color(c)
            )
            for nombre, color in colores_tema.items()
        ],
        wrap=True
    )

    # Elementos de demostración que cambian con el tema
    demo = ft.Column(
        controls=[
            ft.FilledButton("Botón Elevado", icon=ft.Icons.STAR),
            ft.OutlinedButton("Botón con Contorno"),
            ft.FilledButton("Botón Relleno"),
            ft.TextField(label="Campo de texto"),
            ft.Checkbox(label="Checkbox de ejemplo", value=True),
            ft.Switch(label="Switch de ejemplo", value=True),
            ft.ProgressBar(value=0.7, width=300),
            ft.Slider(value=50, min=0, max=100, width=300),
        ],
        spacing=10
    )

    page.add(
        ft.Text("Control de Temas", size=28, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text("Modo de la app:", size=16),
        ft.Row(
            controls=[icono_modo, texto_modo, ft.Switch(value=False, on_change=toggle_modo)],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        ft.Divider(),
        ft.Text("Color del tema:", size=16),
        botones_color,
        ft.Divider(),
        ft.Text("Vista previa de elementos:", size=16),
        demo
    )


ft.run(main)
