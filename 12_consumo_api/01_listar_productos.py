import flet as ft
import httpx

# EJERCICIO 1: Tu primera petición a una API (solo lectura — GET)
#
# Aquí NO usamos todavía la clase ApiProductos: hacemos la petición "a mano"
# para ver claramente los 3 pasos de consumir una API:
#   1. Enviar la petición HTTP      → httpx.get(url)
#   2. Revisar el código de estado  → respuesta.status_code
#   3. Convertir el JSON a Python   → respuesta.json()  (lista de diccionarios)
#
# Antes de correrlo, enciende la API (Laravel o el servidor de prueba):
#   php artisan serve            ó        python servidor_prueba.py

URL = "http://127.0.0.1:8000/api/productos"


def main(page: ft.Page):
    page.title = "Productos desde la API"
    page.padding = 0

    lista = ft.ListView(expand=True, spacing=5, padding=15)
    estado = ft.Text("", size=13, color=ft.Colors.GREY_600)
    cargando = ft.ProgressBar(visible=False, color=ft.Colors.TEAL)

    def cargar_productos(e=None):
        cargando.visible = True
        estado.value = f"GET {URL} ..."
        page.update()

        try:
            # 1. Enviar la petición (Accept: JSON → Laravel siempre responde JSON)
            respuesta = httpx.get(URL, headers={"Accept": "application/json"}, timeout=10)

            # 2. Revisar el código de estado (200 = todo bien)
            if respuesta.status_code != 200:
                estado.value = f"El servidor respondió con error {respuesta.status_code}"
                return

            # 3. JSON → lista de diccionarios de Python
            productos = respuesta.json()

            lista.controls.clear()
            for p in productos:
                lista.controls.append(
                    ft.ListTile(
                        leading=ft.CircleAvatar(
                            content=ft.Text(p["nombre"][0].upper()),
                            bgcolor=ft.Colors.TEAL
                        ),
                        title=ft.Text(p["nombre"], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"${p['precio']:,.0f}  |  Stock: {p['stock']}"),
                    )
                )
            estado.value = f"200 OK — {len(productos)} productos recibidos"

        except httpx.ConnectError:
            estado.value = "No se pudo conectar. ¿Encendiste el servidor?"
        finally:
            # finally se ejecuta SIEMPRE, haya error o no
            cargando.visible = False
            page.update()

    page.appbar = ft.AppBar(
        title=ft.Text("Productos (API)", color=ft.Colors.WHITE),
        bgcolor=ft.Colors.TEAL,
        actions=[
            ft.IconButton(ft.Icons.REFRESH, icon_color=ft.Colors.WHITE,
                          tooltip="Recargar", on_click=cargar_productos)
        ]
    )

    page.add(
        cargando,
        ft.Container(estado, padding=ft.Padding(15, 10, 15, 0)),
        lista
    )
    cargar_productos()


ft.run(main)
