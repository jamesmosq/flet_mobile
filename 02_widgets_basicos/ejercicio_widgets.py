import flet as ft

# Este archivo es una "galería" de los widgets más usados en Flet
# Úsalo como referencia cuando no recuerdes cómo se escribe algo

def main(page: ft.Page):
    page.title = "Galería de Widgets"
    page.scroll = ft.ScrollMode.AUTO  # Permite hacer scroll si el contenido es largo

    # ─── TEXTOS ────────────────────────────────────────────────────
    titulo_seccion_texto = ft.Text("TEXTOS", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY)

    texto_normal = ft.Text("Texto normal", size=16)
    texto_grande = ft.Text("Texto grande", size=30)
    texto_negrita = ft.Text("Texto en negrita", size=18, weight=ft.FontWeight.BOLD)
    texto_color = ft.Text("Texto con color", size=18, color=ft.Colors.PURPLE)
    texto_italica = ft.Text("Texto en cursiva", size=18, italic=True)

    # ─── BOTONES ───────────────────────────────────────────────────
    titulo_seccion_botones = ft.Text("BOTONES", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY)

    # Función que se activa cuando se hace clic en un botón
    def al_hacer_clic(e):
        # e.control es el botón que fue clickeado
        print(f"Hiciste clic en: {e.control.text}")

    boton_elevado = ft.FilledButton("Botón Elevado", on_click=al_hacer_clic)
    boton_contorno = ft.OutlinedButton("Botón con Contorno", on_click=al_hacer_clic)
    boton_texto = ft.TextButton("Botón de Texto", on_click=al_hacer_clic)
    boton_icono = ft.FilledButton(
        "Con Ícono",
        icon=ft.Icons.THUMB_UP,
        on_click=al_hacer_clic,
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE
    )

    # ─── CAMPOS DE TEXTO ───────────────────────────────────────────
    titulo_seccion_campos = ft.Text("CAMPOS DE TEXTO", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY)

    campo_normal = ft.TextField(label="Campo normal", width=300)
    campo_password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    campo_multilinea = ft.TextField(label="Comentario", multiline=True, min_lines=3, max_lines=5, width=300)

    # ─── CHECKBOX Y SWITCH ─────────────────────────────────────────
    titulo_seccion_checks = ft.Text("CHECKBOX Y SWITCH", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY)

    check1 = ft.Checkbox(label="Opción 1", value=True)
    check2 = ft.Checkbox(label="Opción 2", value=False)
    switch = ft.Switch(label="Modo oscuro", value=False)

    # ─── ÍCONOS ────────────────────────────────────────────────────
    titulo_seccion_iconos = ft.Text("ÍCONOS", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY)

    iconos = ft.Row([
        ft.Icon(ft.Icons.HOME, color=ft.Colors.BLUE, size=40),
        ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER, size=40),
        ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED, size=40),
        ft.Icon(ft.Icons.PERSON, color=ft.Colors.GREEN, size=40),
        ft.Icon(ft.Icons.SETTINGS, color=ft.Colors.GREY, size=40),
    ])

    # ─── AGREGAR TODO A LA PÁGINA ─────────────────────────────────
    page.add(
        titulo_seccion_texto,
        texto_normal, texto_grande, texto_negrita, texto_color, texto_italica,
        ft.Divider(),
        titulo_seccion_botones,
        boton_elevado, boton_contorno, boton_texto, boton_icono,
        ft.Divider(),
        titulo_seccion_campos,
        campo_normal, campo_password, campo_multilinea,
        ft.Divider(),
        titulo_seccion_checks,
        check1, check2, switch,
        ft.Divider(),
        titulo_seccion_iconos,
        iconos
    )


ft.run(main)
