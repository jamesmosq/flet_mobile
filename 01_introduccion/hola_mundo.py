import flet as ft

# En Flet, todo parte de una función llamada "main"
# El parámetro "page" es la pantalla donde vas a poner las cosas
def main(page: ft.Page):
    # Título que aparece en la barra de la ventana
    page.title = "Mi primera app con Flet"

    # ft.Text crea un texto visible en pantalla
    # size= controla el tamaño, weight= si es negrita
    saludo = ft.Text(
        value="¡Hola Mundo desde Flet!",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE
    )

    subtitulo = ft.Text(
        value="Esta es mi primera aplicación con Python + Flet",
        size=16,
        color=ft.Colors.GREY_700
    )

    # page.add() agrega los widgets a la pantalla, en orden de arriba hacia abajo
    page.add(saludo, subtitulo)


# ft.run(main) le dice a Flet: "arranca la app y usa la función main"
ft.run(main)
