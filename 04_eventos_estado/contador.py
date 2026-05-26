import flet as ft

# EJERCICIO: Contador con botones + y -
# Concepto clave: el estado (la variable "cuenta") cambia y la pantalla se actualiza

def main(page: ft.Page):
    page.title = "Contador"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # El ESTADO de nuestra app es este número
    # Todo lo que pase en la app va a modificar esta variable
    cuenta = 0

    # Este texto mostrará el número actual
    texto_numero = ft.Text(
        value=str(cuenta),
        size=80,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE
    )

    texto_label = ft.Text("Contador", size=18, color=ft.Colors.GREY)

    # ─── Funciones de evento ──────────────────────────────────────

    def incrementar(e):
        nonlocal cuenta  # nonlocal en vez de global porque estamos dentro de main()
        cuenta += 1
        texto_numero.value = str(cuenta)
        # Actualizar el color según el valor
        if cuenta > 0:
            texto_numero.color = ft.Colors.GREEN
        page.update()

    def decrementar(e):
        nonlocal cuenta
        cuenta -= 1
        texto_numero.value = str(cuenta)
        # Rojo si es negativo, azul si es cero, verde si es positivo
        if cuenta < 0:
            texto_numero.color = ft.Colors.RED
        elif cuenta == 0:
            texto_numero.color = ft.Colors.BLUE
        else:
            texto_numero.color = ft.Colors.GREEN
        page.update()

    def reiniciar(e):
        nonlocal cuenta
        cuenta = 0
        texto_numero.value = "0"
        texto_numero.color = ft.Colors.BLUE
        page.update()

    # ─── Botones ──────────────────────────────────────────────────
    boton_menos = ft.FilledButton(
        "-",
        on_click=decrementar,
        width=80,
        height=80,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=30))
    )

    boton_mas = ft.FilledButton(
        "+",
        on_click=incrementar,
        width=80,
        height=80,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=30)),
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE
    )

    boton_reset = ft.TextButton(
        "Reiniciar",
        on_click=reiniciar,
        icon=ft.Icons.REFRESH
    )

    fila_botones = ft.Row(
        controls=[boton_menos, texto_numero, boton_mas],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    page.add(
        texto_label,
        fila_botones,
        boton_reset
    )


ft.run(main)
