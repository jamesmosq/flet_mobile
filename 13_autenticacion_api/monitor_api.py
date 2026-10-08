import json
import flet as ft
from api_cliente import Registro

# COMPONENTE: Monitor de API
#
# Es como tener Insomnia DENTRO de la app: cada vez que la app habla con la API,
# aquí aparece una tarjeta con la petición y la respuesta.
#
#   POST  /api/productos                   201 Created   35 ms
#   Enviado:   {"nombre": "Teclado", "precio": 120000.0, "stock": 7}
#   Respuesta: {"id": 4, "nombre": "Teclado", ...}
#
# Uso:
#   monitor = MonitorApi()
#   api.observadores.append(monitor.agregar)    # cada petición llama a monitor.agregar()
#
# El candado 🔒 indica que la petición llevaba el token (header Authorization).
#
# Es solo una herramienta para aprender y depurar: en una app real se quita.

# Los mismos colores que usa Insomnia para cada verbo
COLOR_METODO = {
    "GET": ft.Colors.PURPLE_300,
    "POST": ft.Colors.GREEN_400,
    "PUT": ft.Colors.ORANGE_400,
    "DELETE": ft.Colors.RED_400,
}
MAX_LINEAS = 12  # para que un GET con muchos productos no llene la pantalla


def color_estado(estado: int | None) -> str:
    if estado is None or estado >= 500:
        return ft.Colors.RED_400       # sin conexión o error del servidor
    if estado >= 400:
        return ft.Colors.ORANGE_400    # error del cliente (404, 422...)
    return ft.Colors.GREEN_400         # 2xx: todo bien


def a_texto_json(datos) -> str:
    texto = json.dumps(datos, ensure_ascii=False, indent=2)
    lineas = texto.splitlines()
    if len(lineas) > MAX_LINEAS:
        lineas = lineas[:MAX_LINEAS] + [f"... ({len(lineas) - MAX_LINEAS} líneas más)"]
    return "\n".join(lineas)


class MonitorApi(ft.Container):

    def __init__(self, alto: int = 280):
        super().__init__()
        self.lista = ft.ListView(spacing=6, expand=True)

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.TERMINAL, color=ft.Colors.GREEN_400, size=18),
                        ft.Text("Monitor de API", color=ft.Colors.WHITE,
                                weight=ft.FontWeight.BOLD),
                        ft.Text("toca una petición para ver el detalle", size=11,
                                color=ft.Colors.GREY_500, expand=True),
                        ft.TextButton("Limpiar", on_click=self.limpiar),
                    ]
                ),
                self.lista,
            ],
            spacing=4,
        )
        self.bgcolor = ft.Colors.GREY_900
        self.padding = 10
        self.height = alto

    def agregar(self, r: Registro):
        """Se llama automáticamente con cada petición que hace ApiCliente."""
        detalle = []
        if r.enviado is not None:
            detalle.append(self._bloque("Enviado (body)", r.enviado))
        if r.respuesta is not None:
            detalle.append(self._bloque("Respuesta", r.respuesta))
        elif r.estado == 204:
            detalle.append(ft.Text("(204: la respuesta no trae contenido)",
                                   size=12, color=ft.Colors.GREY_500, italic=True))

        # Los GET exitosos (recargar la lista) empiezan cerrados para no tapar
        # lo interesante: lo que se ENVIÓ (POST/PUT/DELETE) y los errores.
        hubo_error = r.estado is None or r.estado >= 400
        cuerpo = ft.Column(detalle, spacing=4, visible=r.metodo != "GET" or hubo_error)

        def mostrar_ocultar(e):
            cuerpo.visible = not cuerpo.visible
            cuerpo.update()

        tarjeta = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                ft.Text(r.metodo, size=12, weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLACK),
                                bgcolor=COLOR_METODO.get(r.metodo, ft.Colors.GREY),
                                padding=ft.Padding(6, 2, 6, 2), border_radius=4,
                            ),
                            ft.Text(r.url, color=ft.Colors.WHITE, size=13,
                                    font_family="Consolas", expand=True),
                            ft.Icon(ft.Icons.LOCK, size=14, color=ft.Colors.AMBER_300,
                                    tooltip="Enviada con token",
                                    visible=r.con_token),
                            ft.Text(f"{r.estado or '---'} {r.razon}", size=12,
                                    weight=ft.FontWeight.BOLD, color=color_estado(r.estado)),
                            ft.Text(f"{r.milisegundos} ms", size=11, color=ft.Colors.GREY_500),
                        ],
                        spacing=8,
                    ),
                    cuerpo,
                ],
                spacing=6,
            ),
            bgcolor=ft.Colors.GREY_800,
            border_radius=6,
            padding=8,
            on_click=mostrar_ocultar,  # tocar la tarjeta muestra/oculta el detalle
        )

        self.lista.controls.insert(0, tarjeta)   # la más reciente arriba
        del self.lista.controls[30:]             # guardamos solo las últimas 30
        try:
            self.update()
        except RuntimeError:
            pass  # el monitor aún no está en la página: se verá al agregarlo

    def _bloque(self, titulo: str, datos) -> ft.Column:
        return ft.Column(
            controls=[
                ft.Text(titulo, size=11, color=ft.Colors.GREY_400),
                ft.Text(a_texto_json(datos), size=12, font_family="Consolas",
                        color=ft.Colors.LIGHT_GREEN_200, selectable=True),
            ],
            spacing=2,
        )

    def limpiar(self, e):
        self.lista.controls.clear()
        self.update()
