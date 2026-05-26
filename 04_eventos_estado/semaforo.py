import flet as ft

# EJERCICIO: Semáforo interactivo
# Practica cambiar propiedades de widgets con eventos
# El usuario hace clic y el semáforo cambia de estado

def main(page: ft.Page):
    page.title = "Semáforo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.GREY_900

    # Los tres círculos del semáforo
    # Empezamos con el rojo encendido (color vivo) y los otros apagados (color oscuro)
    ROJO_ON = ft.Colors.RED
    ROJO_OFF = ft.Colors.RED_900

    AMARILLO_ON = ft.Colors.AMBER
    AMARILLO_OFF = ft.Colors.AMBER_900

    VERDE_ON = ft.Colors.GREEN
    VERDE_OFF = ft.Colors.GREEN_900

    # Estado inicial: rojo encendido
    estado_actual = "rojo"

    luz_roja = ft.Container(width=100, height=100, border_radius=50, bgcolor=ROJO_ON)
    luz_amarilla = ft.Container(width=100, height=100, border_radius=50, bgcolor=AMARILLO_OFF)
    luz_verde = ft.Container(width=100, height=100, border_radius=50, bgcolor=VERDE_OFF)

    texto_estado = ft.Text("PARE", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.RED)

    def cambiar_luz(e):
        nonlocal estado_actual

        # Máquina de estados: rojo → verde → amarillo → rojo → ...
        if estado_actual == "rojo":
            estado_actual = "verde"
            luz_roja.bgcolor = ROJO_OFF
            luz_amarilla.bgcolor = AMARILLO_OFF
            luz_verde.bgcolor = VERDE_ON
            texto_estado.value = "SIGA"
            texto_estado.color = ft.Colors.GREEN

        elif estado_actual == "verde":
            estado_actual = "amarillo"
            luz_roja.bgcolor = ROJO_OFF
            luz_amarilla.bgcolor = AMARILLO_ON
            luz_verde.bgcolor = VERDE_OFF
            texto_estado.value = "PRECAUCIÓN"
            texto_estado.color = ft.Colors.AMBER

        elif estado_actual == "amarillo":
            estado_actual = "rojo"
            luz_roja.bgcolor = ROJO_ON
            luz_amarilla.bgcolor = AMARILLO_OFF
            luz_verde.bgcolor = VERDE_OFF
            texto_estado.value = "PARE"
            texto_estado.color = ft.Colors.RED

        page.update()

    cuerpo_semaforo = ft.Container(
        content=ft.Column(
            controls=[luz_roja, luz_amarilla, luz_verde],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        bgcolor=ft.Colors.GREY_800,
        padding=20,
        border_radius=15,
        width=140
    )

    boton_cambiar = ft.FilledButton(
        "Cambiar luz",
        icon=ft.Icons.TRAFFIC,
        on_click=cambiar_luz,
        bgcolor=ft.Colors.GREY_700,
        color=ft.Colors.WHITE
    )

    page.add(
        cuerpo_semaforo,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        texto_estado,
        boton_cambiar,
        ft.Text("Haz clic en el botón para cambiar el semáforo",
                size=12, color=ft.Colors.GREY_500, italic=True)
    )


ft.run(main)
