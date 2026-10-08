import json
import time
from dataclasses import dataclass
from typing import Callable

import httpx

# ─────────────────────────────────────────────────────────────────
# CLIENTE DE LA API: el "repositorio remoto"
# ─────────────────────────────────────────────────────────────────
# En el módulo 09 el RepositorioProductos hablaba con SQLite.
# Aquí hace EXACTAMENTE lo mismo (obtener, insertar, actualizar, eliminar),
# pero en vez de SQL envía peticiones HTTP a la API de Laravel.
#
# La UI no cambia: sigue llamando a repo.obtener_todos(), repo.insertar(), etc.
# ¡Esa es la ventaja de separar los datos de la interfaz!
#
# ¿Qué URL uso?
#   - App en escritorio (python archivo.py)  → http://127.0.0.1:8000/api
#   - Emulador de Android                    → http://10.0.2.2:8000/api
#   - Celular real (misma red WiFi)          → http://192.168.X.X:8000/api  (IP de tu PC)
#
# Para el celular, Laravel debe arrancar así:
#   php artisan serve --host=0.0.0.0 --port=8000

API_URL = "http://127.0.0.1:8000/api"


@dataclass
class Registro:
    """Una petición con su respuesta: lo mismo que ves en Insomnia."""
    metodo: str                   # GET, POST, PUT, DELETE
    url: str                      # /api/productos/5
    enviado: dict | None          # JSON que mandó la app (solo POST y PUT)
    estado: int | None            # 200, 201, 404, 422... (None = no hubo respuesta)
    razon: str                    # "OK", "Created", "Not Found"... o el error de conexión
    respuesta: object             # JSON que devolvió el servidor
    milisegundos: int


def imprimir_en_terminal(r: Registro):
    """Muestra la petición en la terminal donde corre la app."""
    print(f"\n----- {r.metodo} {r.url} " + "-" * 30)
    if r.enviado is not None:
        print("Enviado:  ", json.dumps(r.enviado, ensure_ascii=False))
    print(f"Respuesta: {r.estado or '---'} {r.razon}  ({r.milisegundos} ms)")
    if r.respuesta is not None:
        print(json.dumps(r.respuesta, ensure_ascii=False, indent=2))


class ErrorApi(Exception):
    """Error con un mensaje listo para mostrarle al usuario."""

    def __init__(self, mensaje: str, errores: dict | None = None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        # Errores de validación de Laravel (422), ej: {"precio": ["El precio es obligatorio."]}
        self.errores = errores or {}


class ApiProductos:
    """
    Encapsula todas las peticiones HTTP a /api/productos.

    Verbo HTTP   Ruta                  Acción CRUD
    ─────────    ────────────────────  ───────────
    GET          /productos            Leer todos
    GET          /productos/{id}       Leer uno
    POST         /productos            Crear
    PUT          /productos/{id}       Actualizar
    DELETE       /productos/{id}       Eliminar
    """

    def __init__(self, url_base: str = API_URL):
        # Funciones que se llaman con cada Registro (terminal, Monitor de API...)
        self.observadores: list[Callable[[Registro], None]] = [imprimir_en_terminal]

        self.cliente = httpx.Client(
            base_url=url_base,
            timeout=10,  # segundos: si el servidor no responde, no esperamos para siempre
            headers={
                # Le dice a Laravel "respóndeme en JSON", incluso cuando hay errores.
                # En rutas protegidas (módulo 13), sin esto Laravel responde 500 en vez de 401.
                "Accept": "application/json",
            },
        )

    # ─── Método central: todas las peticiones pasan por aquí ──────
    def _peticion(self, metodo: str, ruta: str, datos: dict | None = None):
        url = self.cliente.base_url.path.rstrip("/") + ruta
        inicio = time.perf_counter()
        try:
            respuesta = self.cliente.request(metodo, ruta, json=datos)
        except httpx.ConnectError:
            self._registrar(metodo, url, datos, inicio, None, "Sin conexión", None)
            raise ErrorApi("No se pudo conectar con el servidor. ¿Está encendido Laravel?")
        except httpx.TimeoutException:
            self._registrar(metodo, url, datos, inicio, None, "Tiempo agotado", None)
            raise ErrorApi("El servidor tardó demasiado en responder.")

        try:
            cuerpo = respuesta.json() if respuesta.content else None
        except ValueError:
            cuerpo = respuesta.text[:300]  # no era JSON (ej: página de error HTML)
        self._registrar(metodo, url, datos, inicio,
                        respuesta.status_code, respuesta.reason_phrase, cuerpo)

        # Códigos de estado HTTP más comunes:
        #   200 OK | 201 Creado | 204 Sin contenido (borrado)
        #   404 No encontrado | 422 Datos inválidos | 500 Error del servidor
        if respuesta.status_code == 204:
            return None
        if respuesta.status_code == 404:
            raise ErrorApi("El producto no existe (quizá alguien lo borró).")
        if respuesta.status_code == 422:
            raise ErrorApi(cuerpo.get("message", "Datos inválidos."), cuerpo.get("errors"))
        if respuesta.is_error:
            raise ErrorApi(f"Error del servidor ({respuesta.status_code}).")

        return cuerpo

    def _registrar(self, metodo, url, datos, inicio, estado, razon, cuerpo):
        """Avisa a cada observador (terminal, Monitor de API) de la petición que se hizo."""
        registro = Registro(
            metodo=metodo, url=url, enviado=datos, estado=estado, razon=razon,
            respuesta=cuerpo, milisegundos=round((time.perf_counter() - inicio) * 1000)
        )
        for observador in self.observadores:
            observador(registro)

    # ─── Operaciones CRUD ─────────────────────────────────────────
    def obtener_todos(self) -> list[dict]:
        return self._peticion("GET", "/productos")

    def obtener(self, id: int) -> dict:
        return self._peticion("GET", f"/productos/{id}")

    def insertar(self, nombre: str, precio: float, stock: int) -> dict:
        datos = {"nombre": nombre, "precio": precio, "stock": stock}
        return self._peticion("POST", "/productos", datos)

    def actualizar(self, id: int, nombre: str, precio: float, stock: int) -> dict:
        datos = {"nombre": nombre, "precio": precio, "stock": stock}
        return self._peticion("PUT", f"/productos/{id}", datos)

    def eliminar(self, id: int):
        self._peticion("DELETE", f"/productos/{id}")

    def cerrar(self):
        self.cliente.close()
