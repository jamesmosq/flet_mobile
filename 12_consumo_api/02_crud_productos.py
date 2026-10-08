import flet as ft
from api_client import ApiProductos, ErrorApi
from monitor_api import MonitorApi

# EJERCICIO 2: CRUD completo contra la API de Laravel
#
# Compara este archivo con 09_datos_externos/app_sqlite.py:
# la interfaz es casi idéntica. Lo único que cambió es el repositorio:
#
#   antes:  repo = RepositorioProductos()   → guarda en un archivo .db del celular
#   ahora:  repo = ApiProductos()           → guarda en el servidor (MySQL de Laravel)
#
# Diferencia importante: la red PUEDE FALLAR (servidor apagado, sin WiFi,
# datos inválidos...). Por eso cada llamada a la API va dentro de try/except ErrorApi.
#
# Abajo verás el MONITOR DE API: cada petición que hace la app aparece ahí
# (como en Insomnia). También se imprime en la terminal. Ocúltalo con el ícono >_
#
# Flet 0.85:
#   Abrir diálogo / SnackBar → page.show_dialog(...)
#   Cerrar diálogo           → page.pop_dialog()


def main(page: ft.Page):
    page.title = "Inventario con API"
    page.padding = 0

    repo = ApiProductos()

    # Cada petición de repo se mostrará también en el monitor
    monitor = MonitorApi()
    repo.observadores.append(monitor.agregar)

    def mostrar_ocultar_monitor(e):
        monitor.visible = not monitor.visible
        page.update()

    lista = ft.ListView(expand=True, spacing=5, padding=15)
    cargando = ft.ProgressBar(visible=False, color=ft.Colors.DEEP_PURPLE)

    def mostrar_mensaje(texto: str, error: bool = False):
        page.show_dialog(ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=ft.Colors.RED_700 if error else ft.Colors.GREEN_700
        ))

    # ─── R: Leer (GET /productos) ─────────────────────────────────
    def construir_lista():
        cargando.visible = True
        page.update()

        try:
            productos = repo.obtener_todos()
        except ErrorApi as ex:
            productos = None
            mostrar_mensaje(ex.mensaje, error=True)
        finally:
            cargando.visible = False

        lista.controls.clear()

        if productos is None:
            # No hubo conexión: ofrecemos reintentar
            lista.controls.append(estado_vacio(
                ft.Icons.CLOUD_OFF, "Sin conexión con el servidor",
                ft.FilledButton("Reintentar", icon=ft.Icons.REFRESH,
                                on_click=lambda e: construir_lista())
            ))
        elif not productos:
            lista.controls.append(estado_vacio(
                ft.Icons.INVENTORY_2, "No hay productos. Agrega el primero."
            ))
        else:
            for p in productos:
                color_stock = ft.Colors.RED if p["stock"] == 0 else ft.Colors.GREEN
                lista.controls.append(
                    ft.ListTile(
                        leading=ft.CircleAvatar(
                            content=ft.Text(p["nombre"][0].upper()),
                            bgcolor=ft.Colors.DEEP_PURPLE
                        ),
                        title=ft.Text(p["nombre"], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Row([
                            ft.Text(f"${p['precio']:,.0f}", color=ft.Colors.GREEN_700),
                            ft.Text(" | Stock: "),
                            ft.Text(str(p["stock"]), color=color_stock, weight=ft.FontWeight.BOLD)
                        ]),
                        trailing=ft.Row(
                            controls=[
                                ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE,
                                              on_click=lambda e, prod=p: abrir_formulario(prod)),
                                ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED,
                                              on_click=lambda e, prod=p: confirmar_eliminar(prod))
                            ],
                            tight=True
                        )
                    )
                )
        page.update()

    def estado_vacio(icono, texto, boton=None) -> ft.Container:
        controles = [ft.Icon(icono, size=60, color=ft.Colors.GREY_300),
                     ft.Text(texto, color=ft.Colors.GREY)]
        if boton:
            controles.append(boton)
        return ft.Container(
            content=ft.Column(controles, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.Alignment(0, 0),
            padding=40
        )

    # ─── C y U: Crear (POST) y Editar (PUT) ───────────────────────
    def abrir_formulario(producto=None):
        campo_nombre = ft.TextField(
            label="Nombre del producto",
            value=producto["nombre"] if producto else ""
        )
        campo_precio = ft.TextField(
            label="Precio", keyboard_type=ft.KeyboardType.NUMBER, width=150,
            value=str(producto["precio"]) if producto else ""
        )
        campo_stock = ft.TextField(
            label="Stock", keyboard_type=ft.KeyboardType.NUMBER, width=100,
            value=str(producto["stock"]) if producto else "0"
        )
        titulo = "Editar Producto" if producto else "Nuevo Producto"

        # Relaciona el nombre del campo en Laravel con el TextField de Flet
        campos = {"nombre": campo_nombre, "precio": campo_precio, "stock": campo_stock}

        def guardar(e):
            for campo in campos.values():
                campo.error = None

            # Validación rápida en la app (para no molestar al servidor con datos obvios)
            try:
                precio = float(campo_precio.value)
            except (ValueError, TypeError):
                campo_precio.error = "Debe ser un número"
                page.update()
                return
            try:
                stock = int(campo_stock.value or 0)
            except ValueError:
                campo_stock.error = "Debe ser un número entero"
                page.update()
                return

            nombre = campo_nombre.value.strip()
            try:
                if producto:
                    repo.actualizar(producto["id"], nombre, precio, stock)   # PUT
                else:
                    repo.insertar(nombre, precio, stock)                     # POST
            except ErrorApi as ex:
                if ex.errores:
                    # Error 422: Laravel nos dice qué campo está mal → lo mostramos debajo
                    for nombre_campo, mensajes in ex.errores.items():
                        if nombre_campo in campos:
                            campos[nombre_campo].error = mensajes[0]
                    page.update()
                else:
                    page.pop_dialog()
                    mostrar_mensaje(ex.mensaje, error=True)
                return

            page.pop_dialog()
            mostrar_mensaje("Producto actualizado" if producto else "Producto creado")
            construir_lista()

        dlg = ft.AlertDialog(
            title=ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    [campo_nombre, ft.Row([campo_precio, campo_stock])],
                    spacing=10, tight=True
                ),
                width=400
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
                ft.FilledButton("Guardar", on_click=guardar,
                                bgcolor=ft.Colors.DEEP_PURPLE, color=ft.Colors.WHITE)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.show_dialog(dlg)

    # ─── D: Eliminar (DELETE) ─────────────────────────────────────
    def confirmar_eliminar(producto):
        def eliminar(e):
            page.pop_dialog()
            try:
                repo.eliminar(producto["id"])
                mostrar_mensaje(f"'{producto['nombre']}' eliminado")
            except ErrorApi as ex:
                mostrar_mensaje(ex.mensaje, error=True)
            construir_lista()

        page.show_dialog(ft.AlertDialog(
            title=ft.Text("¿Eliminar producto?"),
            content=ft.Text(f"Se borrará '{producto['nombre']}' del servidor."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
                ft.FilledButton("Eliminar", on_click=eliminar,
                                bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        ))

    page.appbar = ft.AppBar(
        title=ft.Text("Inventario (API)", color=ft.Colors.WHITE),
        bgcolor=ft.Colors.DEEP_PURPLE,
        actions=[
            ft.IconButton(ft.Icons.REFRESH, icon_color=ft.Colors.WHITE,
                          tooltip="Recargar", on_click=lambda e: construir_lista()),
            ft.IconButton(ft.Icons.TERMINAL, icon_color=ft.Colors.WHITE,
                          tooltip="Monitor de API", on_click=mostrar_ocultar_monitor),
            ft.IconButton(ft.Icons.ADD, icon_color=ft.Colors.WHITE,
                          tooltip="Agregar producto", on_click=lambda e: abrir_formulario())
        ]
    )

    page.on_close = lambda e: repo.cerrar()

    page.add(cargando, lista, monitor)
    construir_lista()  # llamar después de add() para que page.update() funcione


ft.run(main)
