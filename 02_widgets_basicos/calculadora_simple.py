import flet as ft

# Calculadora con las 4 operaciones básicas
# Conceptos que practicas aquí:
#   - Widgets: TextField, ElevatedButton, Text
#   - Eventos: on_click (una función diferente por operación)
#   - Estado: texto_resultado cambia según lo que se calcule
#   - page.update() para refrescar la pantalla

def main(page: ft.Page):
    page.title = "Calculadora"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.GREY_100

    # ─── Campos de entrada ────────────────────────────────────────
    estilo_campo = {"width": 130, "keyboard_type": ft.KeyboardType.NUMBER, "text_align": ft.TextAlign.CENTER}

    campo_num1 = ft.TextField(label="Número 1", **estilo_campo)
    campo_num2 = ft.TextField(label="Número 2", **estilo_campo)

    # ─── Pantalla de resultado ────────────────────────────────────
    pantalla = ft.Container(
        content=ft.Text("0", size=36, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, text_align=ft.TextAlign.RIGHT),
        bgcolor=ft.Colors.BLUE_GREY_800,
        border_radius=12,
        padding=ft.Padding.symmetric(horizontal=20, vertical=15),
        width=300,
    )

    etiqueta_operacion = ft.Text("", size=13, color=ft.Colors.GREY_600, italic=True)

    # ─── Lógica central ───────────────────────────────────────────
    def calcular(operacion: str):
        """
        Recibe el símbolo de la operación y calcula el resultado.
        Una sola función para las 4 operaciones — evita repetir código.
        Recuerda el concepto de DRY: Don't Repeat Yourself.
        """
        pantalla.content.color = ft.Colors.WHITE

        try:
            if not campo_num1.value or not campo_num2.value:
                raise ValueError("campos vacíos")

            num1 = float(campo_num1.value)
            num2 = float(campo_num2.value)

            if operacion == "+":
                resultado = num1 + num2
            elif operacion == "-":
                resultado = num1 - num2
            elif operacion == "×":
                resultado = num1 * num2
            elif operacion == "÷":
                if num2 == 0:
                    raise ZeroDivisionError()
                resultado = num1 / num2

            # Si el resultado es entero, lo mostramos sin decimales
            if resultado == int(resultado):
                texto = str(int(resultado))
            else:
                texto = f"{resultado:.4f}".rstrip("0")

            pantalla.content.value = texto
            etiqueta_operacion.value = f"{num1} {operacion} {num2} ="

        except ZeroDivisionError:
            pantalla.content.value = "÷ 0 error"
            pantalla.content.color = ft.Colors.RED_300
            etiqueta_operacion.value = "No se puede dividir entre cero"

        except ValueError:
            pantalla.content.value = "?"
            pantalla.content.color = ft.Colors.AMBER_300
            etiqueta_operacion.value = "Escribe dos números primero"

        page.update()

    def limpiar(e):
        campo_num1.value = ""
        campo_num2.value = ""
        pantalla.content.value = "0"
        pantalla.content.color = ft.Colors.WHITE
        etiqueta_operacion.value = ""
        campo_num1.focus()
        page.update()

    # ─── Botones de operaciones ───────────────────────────────────
    def boton_op(simbolo, color, icono):
        return ft.FilledButton(
            simbolo,
            icon=icono,
            on_click=lambda e: calcular(simbolo),
            bgcolor=color,
            color=ft.Colors.WHITE,
            width=65,
            height=55,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        )

    fila_botones = ft.Row(
        controls=[
            boton_op("+", ft.Colors.BLUE,        ft.Icons.ADD),
            boton_op("-", ft.Colors.ORANGE,      ft.Icons.REMOVE),
            boton_op("×", ft.Colors.GREEN,       ft.Icons.CLOSE),
            boton_op("÷", ft.Colors.PURPLE,      ft.Icons.PERCENT),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8
    )

    boton_limpiar = ft.TextButton(
        "Limpiar",
        icon=ft.Icons.REFRESH,
        on_click=limpiar,
    )

    # ─── Layout principal ─────────────────────────────────────────
    tarjeta = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Calculadora", size=22, weight=ft.FontWeight.BOLD),
                ft.Divider(height=5),
                ft.Row([campo_num1, ft.Text("y", size=16, color=ft.Colors.GREY), campo_num2],
                       alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.Divider(height=5),
                fila_botones,
                ft.Divider(height=5),
                etiqueta_operacion,
                pantalla,
                boton_limpiar,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        padding=30,
        width=360,
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.GREY_300, offset=ft.Offset(0, 5))
    )

    page.add(tarjeta)


ft.run(main)
