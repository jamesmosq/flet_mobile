import flet as ft
import json
import os
from datetime import datetime
import uuid
import re


class ProductApp:
    def __init__(self):
        self.products = []
        self.load_products()
        self.page = None
        self.editing_product = None  # Para rastrear si estamos editando
        self.current_view = "form"  # "form" o "list"

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

        # Referencias a elementos de UI
        self.counter_text = None
        self.main_container = None
        self.save_button = None

    def load_products(self):
        """Cargar productos desde archivo JSON"""
        if os.path.exists('productos.json'):
            try:
                with open('productos.json', 'r', encoding='utf-8') as f:
                    self.products = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError, Exception) as e:
                print(f"Error al cargar productos: {e}")
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

    def update_counter(self):
        """Actualizar contador de productos"""
        if self.counter_text:
            self.counter_text.value = f"Total de productos: {len(self.products)}"
            self.page.update()

    def update_save_button(self):
        """Actualizar texto del botón de guardar según el modo"""
        if self.save_button:
            if self.editing_product:
                self.save_button.text = "Actualizar Producto"
                self.save_button.icon = ft.Icons.UPDATE
                self.save_button.style.bgcolor = "orange"
            else:
                self.save_button.text = "Guardar Producto"
                self.save_button.icon = ft.Icons.SAVE
                self.save_button.style.bgcolor = "green"
            self.page.update()

    def show_snackbar(self, message, color="green"):
        """Mostrar mensaje emergente"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()

    def switch_view(self, view_type):
        """Cambiar entre vista de formulario y lista"""
        self.current_view = view_type
        self.build_view()

    def validate_fields(self):
        """Validar campos del formulario"""
        errors = []

        # Campos obligatorios
        if not self.codigo_field.value or not self.codigo_field.value.strip():
            errors.append("El código es obligatorio")

        if not self.nombre_field.value or not self.nombre_field.value.strip():
            errors.append("El nombre es obligatorio")

        # Validar precios
        if self.precio_compra_field.value:
            try:
                precio_compra = float(self.precio_compra_field.value)
                if precio_compra < 0:
                    errors.append("El precio de compra no puede ser negativo")
            except ValueError:
                errors.append("El precio de compra debe ser un número válido")

        if self.precio_venta_field.value:
            try:
                precio_venta = float(self.precio_venta_field.value)
                if precio_venta < 0:
                    errors.append("El precio de venta no puede ser negativo")
            except ValueError:
                errors.append("El precio de venta debe ser un número válido")

        # Validar stock
        if self.stock_field.value:
            try:
                stock = int(self.stock_field.value)
                if stock < 0:
                    errors.append("El stock no puede ser negativo")
            except ValueError:
                errors.append("El stock debe ser un número entero válido")

        # Validar fecha de vencimiento
        if self.vencimiento_field.value:
            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            if not re.match(date_pattern, self.vencimiento_field.value):
                errors.append("La fecha de vencimiento debe tener formato YYYY-MM-DD")
            else:
                try:
                    datetime.strptime(self.vencimiento_field.value, '%Y-%m-%d')
                except ValueError:
                    errors.append("La fecha de vencimiento no es válida")

        return errors

    def save_product(self, e):
        """Guardar nuevo producto o actualizar existente"""
        # Validar campos
        errors = self.validate_fields()
        if errors:
            self.show_snackbar(f"Errores: {', '.join(errors)}", color="red")
            return

        codigo = self.codigo_field.value.strip()

        # Verificar código duplicado
        if self.editing_product is None:
            if any(p['codigo'] == codigo for p in self.products):
                self.show_snackbar("Ya existe un producto con este código", color="red")
                return
        else:
            if any(p['codigo'] == codigo and p['id'] != self.editing_product['id'] for p in self.products):
                self.show_snackbar("Ya existe otro producto con este código", color="red")
                return

        # Preparar datos del producto
        product_data = {
            'codigo': codigo,
            'nombre': self.nombre_field.value.strip(),
            'descripcion': self.descripcion_field.value.strip() if self.descripcion_field.value else "",
            'categoria': self.categoria_field.value.strip() if self.categoria_field.value else "",
            'marca': self.marca_field.value.strip() if self.marca_field.value else "",
            'precio_compra': float(self.precio_compra_field.value) if self.precio_compra_field.value else 0.0,
            'precio_venta': float(self.precio_venta_field.value) if self.precio_venta_field.value else 0.0,
            'stock': int(self.stock_field.value) if self.stock_field.value else 0,
            'unidad': self.unidad_field.value.strip() if self.unidad_field.value else "",
            'proveedor': self.proveedor_field.value.strip() if self.proveedor_field.value else "",
            'vencimiento': self.vencimiento_field.value.strip() if self.vencimiento_field.value else "",
            'ubicacion': self.ubicacion_field.value.strip() if self.ubicacion_field.value else "",
        }

        if self.editing_product is None:
            # Crear nuevo producto
            product_data.update({
                'id': str(uuid.uuid4()),
                'fecha_creacion': datetime.now().isoformat()
            })
            self.products.append(product_data)
            message = "Producto guardado correctamente"
        else:
            # Actualizar producto existente
            for i, p in enumerate(self.products):
                if p['id'] == self.editing_product['id']:
                    product_data.update({
                        'id': self.editing_product['id'],
                        'fecha_creacion': self.editing_product.get('fecha_creacion', datetime.now().isoformat()),
                        'fecha_modificacion': datetime.now().isoformat()
                    })
                    self.products[i] = product_data
                    break
            message = "Producto actualizado correctamente"

        # Guardar y limpiar
        if self.save_products():
            self.show_snackbar(message)
            self.clear_form(None)
            self.update_counter()
            # Si estamos en vista de lista, refrescar
            if self.current_view == "list":
                self.switch_view("list")
        else:
            self.show_snackbar("Error al guardar el producto", color="red")

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

        self.editing_product = None
        self.update_save_button()
        self.page.update()

    def edit_product(self, product):
        """Editar producto"""
        self.editing_product = product

        # Cambiar a vista de formulario
        self.switch_view("form")

        # Llenar formulario con datos del producto
        self.codigo_field.value = product.get('codigo', '')
        self.nombre_field.value = product.get('nombre', '')
        self.descripcion_field.value = product.get('descripcion', '')
        self.categoria_field.value = product.get('categoria', '')
        self.marca_field.value = product.get('marca', '')
        self.precio_compra_field.value = str(product.get('precio_compra', ''))
        self.precio_venta_field.value = str(product.get('precio_venta', ''))
        self.stock_field.value = str(product.get('stock', ''))
        self.unidad_field.value = product.get('unidad', '')
        self.proveedor_field.value = product.get('proveedor', '')
        self.vencimiento_field.value = product.get('vencimiento', '')
        self.ubicacion_field.value = product.get('ubicacion', '')

        self.update_save_button()
        self.page.update()
        self.show_snackbar("Producto cargado para edición. Modifica y guarda los cambios.", color="blue")

    def delete_product(self, product):
        """Eliminar producto"""

        def confirm_delete(e):
            self.page.dialog.open = False
            self.page.update()
            self.products = [p for p in self.products if p['id'] != product['id']]
            if self.save_products():
                self.show_snackbar(f"Producto '{product.get('nombre', 'N/A')}' eliminado correctamente")
                self.update_counter()
                if self.current_view == "list":
                    self.filter_products("")
            else:
                self.show_snackbar("Error al eliminar producto", color="red")

        def cancel_delete(e):
            self.page.dialog.open = False
            self.page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(
                f"¿Estás seguro de eliminar '{product.get('nombre', 'N/A')}'?\n\nCódigo: {product.get('codigo', 'N/A')}\n\nEsta acción no se puede deshacer."
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_delete),
                ft.TextButton(
                    "Eliminar",
                    on_click=confirm_delete,
                    style=ft.ButtonStyle(color=ft.Colors.RED)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
        self.page.update()

    def export_products(self, e):
        """Exportar productos a JSON"""
        if not self.products:
            self.show_snackbar("No hay productos para exportar", color="orange")
            return

        filename = f"productos_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, indent=2, ensure_ascii=False)
            self.show_snackbar(f"Productos exportados a {filename}")
        except Exception as e:
            self.show_snackbar(f"Error al exportar: {str(e)}", color="red")

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

    def build_form_view(self):
        """Construir vista de formulario"""
        return ft.Column([
            # Header con navegación
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.INVENTORY, size=40, color="blue"),
                    ft.Text("Sistema de Inventario", size=24, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Button(
                            "Formulario",
                            icon=ft.Icons.ADD,
                            on_click=lambda e: self.switch_view("form"),
                            style=ft.ButtonStyle(bgcolor="blue" if self.current_view == "form" else "grey")
                        ),
                        ft.Button(
                            "Lista de Productos",
                            icon=ft.Icons.LIST,
                            on_click=lambda e: self.switch_view("list"),
                            style=ft.ButtonStyle(bgcolor="blue" if self.current_view == "list" else "grey")
                        ),
                    ], spacing=10)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
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
                    self.save_button,
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
                content=self.counter_text,
                margin=ft.Margin(top=20),
                alignment=ft.alignment.Alignment(0, 0)
            )
        ])

    def build_list_view(self):
        """Construir vista de lista de productos"""
        # Campo de búsqueda
        search_field = ft.TextField(
            label="Buscar productos",
            hint_text="Buscar por código, nombre o categoría",
            prefix_icon=ft.Icons.SEARCH,
            on_change=lambda e: self.filter_products(e.control.value),
            border_radius=10
        )

        # Crear lista de productos
        self.products_list = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            height=500
        )

        # Mostrar todos los productos inicialmente
        self.filter_products("")

        return ft.Column([
            # Header con navegación
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.INVENTORY, size=40, color="blue"),
                    ft.Text("Sistema de Inventario", size=24, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Button(
                            "Formulario",
                            icon=ft.Icons.ADD,
                            on_click=lambda e: self.switch_view("form"),
                            style=ft.ButtonStyle(bgcolor="blue" if self.current_view == "form" else "grey")
                        ),
                        ft.Button(
                            "Lista de Productos",
                            icon=ft.Icons.LIST,
                            on_click=lambda e: self.switch_view("list"),
                            style=ft.ButtonStyle(bgcolor="blue" if self.current_view == "list" else "grey")
                        ),
                    ], spacing=10)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                margin=ft.Margin(bottom=20)
            ),

            # Barra de búsqueda
            search_field,
            ft.Divider(),

            # Lista de productos
            self.products_list,

            # Footer con estadísticas y botón nuevo
            ft.Container(
                content=ft.Row([
                    self.counter_text,
                    ft.Button(
                        "Nuevo Producto",
                        icon=ft.Icons.ADD,
                        on_click=lambda e: self.switch_view("form"),
                        style=ft.ButtonStyle(bgcolor="green", color="white")
                    ),
                    ft.Button(
                        "Exportar",
                        icon=ft.Icons.DOWNLOAD,
                        on_click=self.export_products,
                        style=ft.ButtonStyle(bgcolor="purple", color="white")
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                margin=ft.Margin(top=20)
            )
        ])

    def filter_products(self, search_term):
        """Filtrar productos según término de búsqueda"""
        if not hasattr(self, 'products_list'):
            return

        self.products_list.controls.clear()

        filtered_products = []
        if search_term:
            search_term = search_term.lower()
            filtered_products = [
                p for p in self.products
                if search_term in p.get('codigo', '').lower()
                   or search_term in p.get('nombre', '').lower()
                   or search_term in p.get('categoria', '').lower()
                   or search_term in p.get('marca', '').lower()
                   or search_term in p.get('proveedor', '').lower()
            ]
        else:
            filtered_products = self.products

        if not filtered_products:
            self.products_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.INVENTORY_2, size=80, color="grey"),
                        ft.Text("No se encontraron productos", size=18, text_align=ft.TextAlign.CENTER),
                        ft.Text("Intenta con otros términos de búsqueda", size=14, color="grey",
                                text_align=ft.TextAlign.CENTER)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.Alignment(0, 0),
                    padding=50
                )
            )
        else:
            for i, product in enumerate(filtered_products, 1):
                # Card para cada producto
                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            # Header del producto
                            ft.Row([
                                ft.Text(f"#{i} - {product.get('nombre', 'N/A')}",
                                        size=16, weight=ft.FontWeight.BOLD, expand=True),
                                ft.Chip(
                                    label=ft.Text(product.get('categoria', 'Sin categoría')),
                                    bgcolor=ft.Colors.BLUE_100
                                )
                            ]),

                            # Información principal
                            ft.Row([
                                ft.Column([
                                    ft.Text(f"Código: {product.get('codigo', 'N/A')}", size=12),
                                    ft.Text(f"Marca: {product.get('marca', 'N/A')}", size=12),
                                    ft.Text(f"Proveedor: {product.get('proveedor', 'N/A')}", size=12),
                                ], expand=True),
                                ft.Column([
                                    ft.Text(f"Precio Compra: ${float(product.get('precio_compra', 0)):.2f}", size=12),
                                    ft.Text(f"Precio Venta: ${float(product.get('precio_venta', 0)):.2f}", size=12,
                                            weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Stock: {product.get('stock', 0)} {product.get('unidad', '')}", size=12),
                                ], expand=True),
                            ]),

                            # Información adicional
                            ft.Text(
                                f"Descripción: {product.get('descripcion', 'Sin descripción')[:100]}{'...' if len(product.get('descripcion', '')) > 100 else ''}",
                                size=11, color="grey"),

                            # Botones de acción
                            ft.Row([
                                ft.Button(
                                    "Editar",
                                    icon=ft.Icons.EDIT,
                                    on_click=lambda e, p=product: self.edit_product(p),
                                    style=ft.ButtonStyle(bgcolor="orange", color="white")
                                ),
                                ft.Button(
                                    "Eliminar",
                                    icon=ft.Icons.DELETE,
                                    on_click=lambda e, p=product: self.delete_product(p),
                                    style=ft.ButtonStyle(bgcolor="red", color="white")
                                ),
                                ft.Button(
                                    "Ver Detalles",
                                    icon=ft.Icons.VISIBILITY,
                                    on_click=lambda e, p=product: self.view_product_details(p),
                                    style=ft.ButtonStyle(bgcolor="blue", color="white")
                                ),
                            ], spacing=10)
                        ], spacing=10),
                        padding=15
                    ),
                    elevation=2
                )
                self.products_list.controls.append(card)

        self.page.update()

    def view_product_details(self, product):
        """Ver detalles completos del producto"""
        details = ft.Column([
            ft.Text(f"Detalles de: {product.get('nombre', 'N/A')}", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row([
                ft.Column([
                    ft.Text(f"Código: {product.get('codigo', 'N/A')}", size=14),
                    ft.Text(f"Nombre: {product.get('nombre', 'N/A')}", size=14),
                    ft.Text(f"Categoría: {product.get('categoria', 'N/A')}", size=14),
                    ft.Text(f"Marca: {product.get('marca', 'N/A')}", size=14),
                    ft.Text(f"Proveedor: {product.get('proveedor', 'N/A')}", size=14),
                    ft.Text(f"Ubicación: {product.get('ubicacion', 'N/A')}", size=14),
                ], expand=True),
                ft.Column([
                    ft.Text(f"Precio Compra: ${float(product.get('precio_compra', 0)):.2f}", size=14),
                    ft.Text(f"Precio Venta: ${float(product.get('precio_venta', 0)):.2f}", size=14),
                    ft.Text(f"Stock: {product.get('stock', 0)} {product.get('unidad', '')}", size=14),
                    ft.Text(f"Vencimiento: {product.get('vencimiento', 'N/A')}", size=14),
                    ft.Text(f"Creado: {product.get('fecha_creacion', 'N/A')[:10]}", size=14),
                    ft.Text(
                        f"Modificado: {product.get('fecha_modificacion', 'N/A')[:10] if product.get('fecha_modificacion') else 'N/A'}",
                        size=14),
                ], expand=True),
            ]),
            ft.Text(f"Descripción: {product.get('descripcion', 'Sin descripción')}", size=14),
        ], width=600, height=400, scroll=ft.ScrollMode.AUTO)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Detalles del Producto"),
            content=details,
            actions=[
                ft.TextButton("Editar", on_click=lambda e: self.close_dialog_and_edit(product)),
                ft.TextButton("Cerrar", on_click=lambda e: self.close_current_dialog())
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def close_dialog_and_edit(self, product):
        """Cerrar diálogo y editar producto"""
        try:
            if self.page.dialog:
                self.page.dialog.open = False
                self.page.dialog = None
            self.page.update()
            self.edit_product(product)
        except Exception as ex:
            print(f"Error en close_dialog_and_edit: {ex}")

    def close_current_dialog(self):
        """Cerrar diálogo actual"""
        try:
            if self.page.dialog:
                self.page.dialog.open = False
                self.page.dialog = None
            self.page.update()
        except Exception as ex:
            print(f"Error en close_current_dialog: {ex}")

    def build_view(self):
        """Construir vista actual"""
        self.main_container.content = (
            self.build_form_view() if self.current_view == "form"
            else self.build_list_view()
        )
        self.page.update()

    def build_app(self, page: ft.Page):
        """Construir la aplicación"""
        self.page = page
        page.title = "Sistema de Inventario - CRUD Completo"
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
        self.vencimiento_field = self.create_form_field("Fecha de Vencimiento", "YYYY-MM-DD (opcional)")
        self.ubicacion_field = self.create_form_field("Ubicación en Almacén", "Ej: Pasillo A, Estante 3")

        # Botón de guardar
        self.save_button = ft.Button(
            "Guardar Producto",
            icon=ft.Icons.SAVE,
            on_click=self.save_product,
            style=ft.ButtonStyle(
                bgcolor="green",
                color="white"
            )
        )

        # Texto del contador
        self.counter_text = ft.Text(
            f"Total de productos: {len(self.products)}",
            size=14,
            color="grey"
        )

        # Container principal
        self.main_container = ft.Container()
        # Construir vista inicial
        self.build_view()

        page.add(self.main_container)


def main(page: ft.Page):
    app = ProductApp()
    app.build_app(page)


if __name__ == "__main__":
    ft.run(main)
