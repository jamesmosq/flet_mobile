import flet as ft
import json
import os
from datetime import datetime
import uuid


class ProductApp:
    def __init__(self):
        self.products = []
        self.load_products()
        self.page = None

        # Referencias a los campos del formulario
        self.codigo_field = None
        self.nombre_field = None
        self.descripcion_field = None
        self.categoria_field = None
        self.marca_field = None
        self.precio_compra_field = None
        self.precio_venta_field = None
        self.stock_field = None
        self.unidad_field = None
        self.proveedor_field = None
        self.vencimiento_field = None
        self.ubicacion_field = None

    def load_products(self):
        """Cargar productos desde archivo JSON"""
        if os.path.exists('productos.json'):
            try:
                with open('productos.json', 'r', encoding='utf-8') as f:
                    self.products = json.load(f)
            except:
                self.products = []
        else:
            self.products = []

    def save_products(self):
        """Guardar productos en archivo JSON"""
        try:
            with open('productos.json', 'w', encoding='utf-8') as f:
                json.dump(self.products, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar: {str(e)}")
            return False

    def show_snackbar(self, message, color="green"):
        """Mostrar mensaje emergente"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()

    def show_dialog(self, title, content):
        """Mostrar diálogo modal"""
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=content,
            actions=[
                ft.TextButton("Cerrar", on_click=lambda _: self.close_dialog(dialog))
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def close_dialog(self, dialog):
        """Cerrar diálogo"""
        dialog.open = False
        self.page.update()

    def save_product(self, e):
        """Guardar nuevo producto"""
        # Validar campos obligatorios
        if not self.codigo_field.value or not self.nombre_field.value:
            self.show_snackbar("El código y nombre son obligatorios",  color="red")
            return

        # Verificar código duplicado
        if any(p['codigo'] == self.codigo_field.value for p in self.products):
            self.show_snackbar("Ya existe un producto con este código", color="red")
            return

        # Crear producto
        product = {
            'id': str(uuid.uuid4()),
            'codigo': self.codigo_field.value,
            'nombre': self.nombre_field.value,
            'descripcion': self.descripcion_field.value,
            'categoria': self.categoria_field.value,
            'marca': self.marca_field.value,
            'precio_compra': self.precio_compra_field.value,
            'precio_venta': self.precio_venta_field.value,
            'stock': self.stock_field.value,
            'unidad': self.unidad_field.value,
            'proveedor': self.proveedor_field.value,
            'vencimiento': self.vencimiento_field.value,
            'ubicacion': self.ubicacion_field.value,
            'fecha_creacion': datetime.now().isoformat()
        }

        # Agregar y guardar
        self.products.append(product)
        if self.save_products():
            self.show_snackbar("Producto guardado correctamente")
            self.clear_form(None)
        else:
            self.show_snackbar("Error al guardar el producto", ft.Colors.RED)

    def clear_form(self, e):
        """Limpiar formulario"""
        fields = [
            self.codigo_field, self.nombre_field, self.descripcion_field,
            self.categoria_field, self.marca_field, self.precio_compra_field,
            self.precio_venta_field, self.stock_field, self.unidad_field,
            self.proveedor_field, self.vencimiento_field, self.ubicacion_field
        ]

        for field in fields:
            if field:
                field.value = ""

        self.page.update()

    def view_products(self, e):
        """Ver lista de productos"""
        if not self.products:
            self.show_snackbar("No hay productos guardados", ft.Colors.ORANGE)
            return

        # Crear lista de productos
        products_list = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            height=400
        )

        for i, product in enumerate(self.products, 1):
            # Card para cada producto
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"#{i} - {product.get('nombre', 'N/A')}",
                                size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Código: {product.get('codigo', 'N/A')}"),
                        ft.Text(f"Categoría: {product.get('categoria', 'N/A')}"),
                        ft.Text(f"Precio: ${product.get('precio_venta', 'N/A')}"),
                        ft.Text(f"Stock: {product.get('stock', 'N/A')} {product.get('unidad', '')}"),
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar",
                                on_click=lambda _, p=product: self.edit_product(p)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar",
                                icon_color=ft.Colors.RED,
                                on_click=lambda _, p=product: self.delete_product(p)
                            )
                        ])
                    ]),
                    padding=15
                ),
                elevation=2
            )
            products_list.controls.append(card)

        self.show_dialog("Productos Guardados", products_list)

    def edit_product(self, product):
        """Editar producto"""
        # Llenar formulario con datos del producto
        self.codigo_field.value = product.get('codigo', '')
        self.nombre_field.value = product.get('nombre', '')
        self.descripcion_field.value = product.get('descripcion', '')
        self.categoria_field.value = product.get('categoria', '')
        self.marca_field.value = product.get('marca', '')
        self.precio_compra_field.value = product.get('precio_compra', '')
        self.precio_venta_field.value = product.get('precio_venta', '')
        self.stock_field.value = product.get('stock', '')
        self.unidad_field.value = product.get('unidad', '')
        self.proveedor_field.value = product.get('proveedor', '')
        self.vencimiento_field.value = product.get('vencimiento', '')
        self.ubicacion_field.value = product.get('ubicacion', '')

        # Cerrar diálogo y actualizar página
        if self.page.dialog:
            self.page.dialog.open = False
        self.page.update()

        self.show_snackbar("Producto cargado para edición. Recuerda guardarlo.")

    def delete_product(self, product):
        """Eliminar producto"""

        # Confirmar eliminación
        def confirm_delete(e):
            self.products = [p for p in self.products if p['id'] != product['id']]
            if self.save_products():
                self.show_snackbar("Producto eliminado correctamente")
                # Cerrar diálogos
                if self.page.dialog:
                    self.page.dialog.open = False
                self.page.update()
            else:
                self.show_snackbar("Error al eliminar producto", ft.Colors.RED)

        def cancel_delete(e):
            if self.page.dialog:
                self.page.dialog.open = False
            self.page.update()

        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Estás seguro de eliminar '{product.get('nombre', 'N/A')}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_delete),
                ft.TextButton("Eliminar", on_click=confirm_delete,
                              style=ft.ButtonStyle(color=ft.Colors.RED))
            ]
        )

        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
        self.page.update()

    def export_products(self, e):
        """Exportar productos a JSON"""
        if not self.products:
            self.show_snackbar("No hay productos para exportar", ft.Colors.ORANGE)
            return

        filename = f"productos_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, indent=2, ensure_ascii=False)
            self.show_snackbar(f"Productos exportados a {filename}")
        except Exception as e:
            self.show_snackbar(f"Error al exportar: {str(e)}", ft.Colors.RED)

    def create_form_field(self, label, hint, multiline=False, keyboard_type=None):
        """Crear campo de formulario consistente"""
        return ft.TextField(
            label=label,
            hint_text=hint,
            multiline=multiline,
            max_lines=3 if multiline else 1,
            keyboard_type=keyboard_type,
            filled=True,
            border_radius=10
        )

    def build_app(self, page: ft.Page):
        """Construir la aplicación"""
        self.page = page
        page.title = "Captura de Productos"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        page.scroll = ft.ScrollMode.AUTO

        # Crear campos del formulario
        self.codigo_field = self.create_form_field("Código del Producto*", "Ej: PROD001")
        self.nombre_field = self.create_form_field("Nombre del Producto*", "Ej: Laptop Dell")
        self.descripcion_field = self.create_form_field("Descripción", "Descripción detallada", multiline=True)
        self.categoria_field = self.create_form_field("Categoría", "Ej: Electrónicos")
        self.marca_field = self.create_form_field("Marca", "Ej: Dell")
        self.precio_compra_field = self.create_form_field("Precio de Compra", "0.00",
                                                          keyboard_type=ft.KeyboardType.NUMBER)
        self.precio_venta_field = self.create_form_field("Precio de Venta", "0.00",
                                                         keyboard_type=ft.KeyboardType.NUMBER)
        self.stock_field = self.create_form_field("Cantidad en Stock", "0", keyboard_type=ft.KeyboardType.NUMBER)
        self.unidad_field = self.create_form_field("Unidad de Medida", "Ej: piezas, kg, litros")
        self.proveedor_field = self.create_form_field("Proveedor", "Nombre del proveedor")
        self.vencimiento_field = self.create_form_field("Fecha de Vencimiento", "YYYY-MM-DD")
        self.ubicacion_field = self.create_form_field("Ubicación en Almacén", "Ej: Pasillo A, Estante 3")

        # Layout principal
        main_content = ft.Column([
            # Header
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.INVENTORY, size=40, color="blue"),
                    ft.Text("Captura de Productos", size=24, weight=ft.FontWeight.BOLD),
                ]),
                margin=ft.Margin(bottom=20)
            ),

            # Formulario en dos columnas
            ft.Row([
                # Columna izquierda
                ft.Column([
                    self.codigo_field,
                    self.nombre_field,
                    self.descripcion_field,
                    self.categoria_field,
                    self.marca_field,
                    self.precio_compra_field,
                ], spacing=15, expand=True),

                # Columna derecha
                ft.Column([
                    self.precio_venta_field,
                    self.stock_field,
                    self.unidad_field,
                    self.proveedor_field,
                    self.vencimiento_field,
                    self.ubicacion_field,
                ], spacing=15, expand=True),
            ], spacing=20),

            # Botones de acción
            ft.Container(
                content=ft.Row([
                    ft.Button(
                        "Guardar Producto",
                        icon=ft.Icons.SAVE,
                        on_click=self.save_product,
                        style=ft.ButtonStyle(
                            bgcolor="green",
                            color="white"
                        )
                    ),
                    ft.Button(
                        "Limpiar Campos",
                        icon=ft.Icons.CLEAR,
                        on_click=self.clear_form,
                        style=ft.ButtonStyle(
                            bgcolor="orange",
                            color="white"
                        )
                    ),
                    ft.Button(
                        "Ver Productos",
                        icon=ft.Icons.LIST,
                        on_click=self.view_products,
                        style=ft.ButtonStyle(
                            bgcolor="blue",
                            color="white"
                        )
                    ),
                    ft.Button(
                        "Exportar",
                        icon=ft.Icons.DOWNLOAD,
                        on_click=self.export_products,
                        style=ft.ButtonStyle(
                            bgcolor="purple",
                            color="white"
                        )
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                margin=ft.Margin(top=30)
            ),

            # Footer con estadísticas
            ft.Container(
                content=ft.Text(
                    f"Total de productos: {len(self.products)}",
                    size=14,
                    color="grey"
                ),
                margin=ft.Margin(top=20),
                alignment=ft.alignment.Alignment(0, 0)
            )
        ])

        page.add(main_content)


def main(page: ft.Page):
    app = ProductApp()
    app.build_app(page)


if __name__ == "__main__":
    ft.run(main)
