import flet as ft

# EJERCICIO: Crea tu propia tarjeta de presentación
# Modifica los valores con tu información real

def main(page: ft.Page):
    page.title = "Mi Presentación"
    page.bgcolor = ft.Colors.BLUE_GREY_900  # Color de fondo de la pantalla

    # --- Cambia estos datos con los tuyos ---
    nombre = "Tu Nombre Aquí"
    carrera = "Ingeniería / Sistemas / etc."
    semestre = "X Semestre"
    frase = "Una frase que te describa..."
    # ----------------------------------------

    # ft.Icon muestra íconos de Material Design
    icono_persona = ft.Icon(
        ft.Icons.PERSON_ROUNDED,
        size=80,
        color=ft.Colors.WHITE
    )

    texto_nombre = ft.Text(
        value=nombre,
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE
    )

    texto_carrera = ft.Text(
        value=carrera,
        size=16,
        color=ft.Colors.BLUE_200
    )

    texto_semestre = ft.Text(
        value=semestre,
        size=14,
        color=ft.Colors.GREY_400
    )

    texto_frase = ft.Text(
        value=f'"{frase}"',
        size=13,
        italic=True,
        color=ft.Colors.GREY_300
    )

    # ft.Divider es una línea horizontal separadora
    linea = ft.Divider(color=ft.Colors.BLUE_400, thickness=1)

    # Agrega todos los widgets a la página de arriba hacia abajo
    page.add(
        icono_persona,
        texto_nombre,
        texto_carrera,
        texto_semestre,
        linea,
        texto_frase
    )


ft.run(main)
