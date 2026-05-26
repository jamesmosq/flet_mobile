import flet as ft

# EJERCICIO: Componente reutilizable con clases
#
# CAMBIO en Flet 0.80+: ft.UserControl fue eliminado.
# Ahora los componentes son clases Python normales que guardan
# una referencia a su widget y lo actualizan con widget.update().
# El concepto de POO es exactamente el mismo — solo cambia la herencia.


class TarjetaProducto:
    """
    Clase que representa una tarjeta de producto reutilizable.
    En lugar de heredar de ft.UserControl, guardamos el widget
    en self._contenedor y lo actualizamos directamente.
    """

    def __init__(self, nombre: str, precio: float, categoria: str, disponible: bool = True):
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.disponible = disponible
        self.en_carrito = False
        self._contenedor = None  # referencia al widget construido

    def agregar_al_carrito(self, e):
        self.en_carrito = not self.en_carrito
        # Reconstruimos el contenido y actualizamos solo este componente
        self._contenedor.content = self._crear_contenido()
        self._contenedor.update()

    def _crear_contenido(self) -> ft.Column:
        """Construye el Column con todo el contenido visual de la tarjeta."""
        color_precio = ft.Colors.GREEN if self.disponible else ft.Colors.GREY
        texto_disponible = "Disponible" if self.disponible else "Agotado"
        color_disponible = ft.Colors.GREEN_700 if self.disponible else ft.Colors.RED_700

        if self.en_carrito:
            boton = ft.FilledButton(
                "En el carrito",
                icon=ft.Icons.CHECK_CIRCLE,
                on_click=self.agregar_al_carrito,
                bgcolor=ft.Colors.GREEN,
                color=ft.Colors.WHITE
            )
        else:
            boton = ft.FilledButton(
                "Agregar",
                icon=ft.Icons.SHOPPING_CART,
                on_click=self.agregar_al_carrito,
                disabled=not self.disponible
            )

        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(self.categoria, size=11, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.BLUE_400,
                            padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                            border_radius=20
                        ),
                        ft.Text(texto_disponible, size=11, color=color_disponible)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Icon(ft.Icons.INVENTORY_2, size=50, color=ft.Colors.BLUE_GREY_300),
                ft.Text(self.nombre, size=16, weight=ft.FontWeight.BOLD),
                ft.Text(
                    f"${self.precio:,.0f}",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=color_precio
                ),
                boton
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8
        )

    def build(self) -> ft.Container:
        """
        Construye y retorna el widget listo para agregar a la pagina.
        Llama: page.add(tarjeta.build())
        """
        self._contenedor = ft.Container(
            content=self._crear_contenido(),
            width=180,
            padding=15,
            border_radius=15,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.GREY_300)
        )
        return self._contenedor


def main(page: ft.Page):
    page.title = "Tienda - Componentes Reutilizables"
    page.bgcolor = ft.Colors.GREY_100
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Creamos instancias y llamamos a .build() para obtener el widget
    productos = [
        TarjetaProducto("Laptop Pro",         3500000, "Tecnologia"),
        TarjetaProducto("Mouse Inalambrico",    85000, "Accesorios"),
        TarjetaProducto("Teclado Mecanico",    250000, "Accesorios", disponible=False),
        TarjetaProducto("Monitor 4K",         1800000, "Tecnologia"),
    ]

    page.add(
        ft.Text("Nuestra Tienda", size=28, weight=ft.FontWeight.BOLD),
        ft.Text(
            "Cada tarjeta es una instancia de la clase TarjetaProducto",
            size=13, color=ft.Colors.GREY, italic=True
        ),
        ft.Divider(),
        ft.Row(
            controls=[p.build() for p in productos],
            wrap=True,
            spacing=15,
            run_spacing=15
        )
    )


ft.run(main)
