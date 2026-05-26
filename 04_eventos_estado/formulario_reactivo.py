import flet as ft

# EJERCICIO: Formulario que reacciona mientras el usuario escribe
# Evento on_change: se activa cada vez que el usuario cambia algo en el campo
# Evento on_submit: se activa cuando el usuario presiona Enter

def main(page: ft.Page):
    page.title = "Formulario Reactivo"
    page.padding = 30

    # Vista previa del nombre (se actualiza en tiempo real)
    preview_nombre = ft.Text("Tu nombre aparecerá aquí", size=20, color=ft.Colors.GREY_400, italic=True)
    preview_completo = ft.Text("", size=16, color=ft.Colors.BLUE_700)

    campo_nombre = ft.TextField(label="Nombre")
    campo_apellido = ft.TextField(label="Apellido")
    campo_edad = ft.TextField(label="Edad", keyboard_type=ft.KeyboardType.NUMBER, width=150)

    # Indicador de fortaleza de contraseña
    barra_fortaleza = ft.ProgressBar(value=0, color=ft.Colors.RED, width=300)
    texto_fortaleza = ft.Text("", size=12)

    campo_password = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=300
    )

    # ─── Funciones de evento ──────────────────────────────────────

    # on_change en el nombre: actualiza la vista previa mientras el usuario escribe
    def al_escribir_nombre(e):
        nombre = campo_nombre.value
        apellido = campo_apellido.value

        if nombre:
            preview_nombre.value = nombre
            preview_nombre.color = ft.Colors.BLACK
        else:
            preview_nombre.value = "Tu nombre aparecerá aquí"
            preview_nombre.color = ft.Colors.GREY_400
            preview_nombre.italic = True

        if nombre and apellido:
            preview_completo.value = f"Nombre completo: {nombre} {apellido}"
        else:
            preview_completo.value = ""

        page.update()

    # Misma función para el apellido
    campo_nombre.on_change = al_escribir_nombre
    campo_apellido.on_change = al_escribir_nombre

    def al_escribir_password(e):
        password = campo_password.value
        longitud = len(password)

        if longitud == 0:
            barra_fortaleza.value = 0
            texto_fortaleza.value = ""
        elif longitud < 4:
            barra_fortaleza.value = 0.25
            barra_fortaleza.color = ft.Colors.RED
            texto_fortaleza.value = "Muy debil"
            texto_fortaleza.color = ft.Colors.RED
        elif longitud < 8:
            barra_fortaleza.value = 0.5
            barra_fortaleza.color = ft.Colors.ORANGE
            texto_fortaleza.value = "Debil"
            texto_fortaleza.color = ft.Colors.ORANGE
        elif longitud < 12:
            barra_fortaleza.value = 0.75
            barra_fortaleza.color = ft.Colors.AMBER
            texto_fortaleza.value = "Moderada"
            texto_fortaleza.color = ft.Colors.AMBER
        else:
            barra_fortaleza.value = 1.0
            barra_fortaleza.color = ft.Colors.GREEN
            texto_fortaleza.value = "Fuerte"
            texto_fortaleza.color = ft.Colors.GREEN

        page.update()

    campo_password.on_change = al_escribir_password

    # on_submit: se activa cuando presionas Enter en el campo de edad
    def al_enviar(e):
        errores = []
        if not campo_nombre.value:
            errores.append("- El nombre es obligatorio")
        if not campo_apellido.value:
            errores.append("- El apellido es obligatorio")
        if not campo_edad.value or not campo_edad.value.isdigit():
            errores.append("- La edad debe ser un número")

        if errores:
            sb = ft.SnackBar(content=ft.Text("\n".join(errores)), bgcolor=ft.Colors.RED_700, open=True)
        else:
            sb = ft.SnackBar(
                content=ft.Text(f"Registro exitoso: {campo_nombre.value} {campo_apellido.value}, {campo_edad.value} años"),
                bgcolor=ft.Colors.GREEN_700, open=True
            )
        page.overlay.append(sb)
        page.update()

    page.add(
        ft.Text("Formulario Reactivo", size=28, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text("Vista previa:", size=14, color=ft.Colors.GREY),
        preview_nombre,
        preview_completo,
        ft.Divider(),
        campo_nombre,
        campo_apellido,
        campo_edad,
        ft.Divider(),
        ft.Text("Contraseña:", size=14),
        campo_password,
        barra_fortaleza,
        texto_fortaleza,
        ft.Divider(),
        ft.FilledButton(
            "Registrar",
            icon=ft.Icons.SAVE,
            on_click=al_enviar,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE
        )
    )


ft.run(main)
