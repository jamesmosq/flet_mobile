import json
import time
from dataclasses import dataclass
from typing import Callable

import httpx

# ─────────────────────────────────────────────────────────────────
# CLIENTE DE LA API con autenticación (token de Laravel Sanctum)
# ─────────────────────────────────────────────────────────────────
# Novedad respecto al módulo 12: el TOKEN.
#
#   1. La app hace login  → POST /api/login
#   2. Laravel responde   → {"user": {...}, "token": "1|aBcD..."}
#   3. La app GUARDA el token (self.token)
#   4. En cada petición siguiente lo envía en un header:
#        Authorization: Bearer 1|aBcD...
#   5. Laravel lee ese header y sabe QUIÉN está haciendo la petición
#
# Es como la manilla de un concierto: te la ponen una vez en la entrada (login)
# y después solo la muestras para entrar a cada zona (cada petición).

API_URL = "http://127.0.0.1:8000/api"


@dataclass
class Registro:
    """Una petición con su respuesta (lo que muestra el Monitor de API)."""
    metodo: str
    url: str
    enviado: dict | None
    estado: int | None
    razon: str
    respuesta: object
    milisegundos: int
    con_token: bool


def imprimir_en_terminal(r: Registro):
    candado = " [con token]" if r.con_token else ""
    print(f"\n----- {r.metodo} {r.url}{candado} " + "-" * 25)
    if r.enviado is not None:
        print("Enviado:  ", json.dumps(ocultar_claves(r.enviado), ensure_ascii=False))
    print(f"Respuesta: {r.estado or '---'} {r.razon}  ({r.milisegundos} ms)")
    if r.respuesta is not None:
        print(json.dumps(r.respuesta, ensure_ascii=False, indent=2))


def ocultar_claves(datos: dict) -> dict:
    """Las contraseñas NUNCA se muestran, ni siquiera en el monitor."""
    return {k: ("********" if "password" in k else v) for k, v in datos.items()}


class ErrorApi(Exception):
    def __init__(self, mensaje: str, errores: dict | None = None, estado: int | None = None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.errores = errores or {}   # errores de validación (422) por campo
        self.estado = estado           # código HTTP (401, 404, 422...)


class ApiCliente:

    def __init__(self, url_base: str = API_URL):
        self.token: str | None = None      # se llena al hacer login o registro
        self.usuario: dict | None = None   # datos del usuario que inició sesión
        self.observadores: list[Callable[[Registro], None]] = [imprimir_en_terminal]
        self.cliente = httpx.Client(
            base_url=url_base, timeout=10,
            headers={"Accept": "application/json"},
        )

    # ─── Método central ───────────────────────────────────────────
    def _peticion(self, metodo: str, ruta: str, datos: dict | None = None):
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        url = self.cliente.base_url.path.rstrip("/") + ruta
        inicio = time.perf_counter()
        try:
            respuesta = self.cliente.request(metodo, ruta, json=datos, headers=headers)
        except httpx.ConnectError:
            self._registrar(metodo, url, datos, inicio, None, "Sin conexión", None)
            raise ErrorApi("No se pudo conectar con el servidor. ¿Está encendido Laravel?")
        except httpx.TimeoutException:
            self._registrar(metodo, url, datos, inicio, None, "Tiempo agotado", None)
            raise ErrorApi("El servidor tardó demasiado en responder.")

        try:
            cuerpo = respuesta.json() if respuesta.content else None
        except ValueError:
            cuerpo = respuesta.text[:300]
        self._registrar(metodo, url, datos, inicio,
                        respuesta.status_code, respuesta.reason_phrase, cuerpo)

        estado = respuesta.status_code
        mensaje_laravel = cuerpo.get("message", "") if isinstance(cuerpo, dict) else ""

        if estado in (200, 201):
            return cuerpo
        if estado == 204:
            return None

        # Estos mensajes están pensados para quien está CONSTRUYENDO la API:
        # te dicen qué revisar en Laravel.
        if estado == 401:
            if mensaje_laravel == "Unauthenticated.":  # lo responde auth:sanctum
                mensaje_laravel = "Tu sesión no es válida (falta el token o ya expiró). Inicia sesión."
            raise ErrorApi(mensaje_laravel or "No autorizado.", estado=401)
        if estado == 404 and "could not be found" in mensaje_laravel:
            raise ErrorApi(f"La ruta {metodo} {url} no existe. ¿La agregaste en routes/api.php?",
                           estado=404)
        if estado == 404:
            raise ErrorApi("El registro no existe (404).", estado=404)
        if estado == 405:
            raise ErrorApi(f"La ruta {url} existe, pero no acepta {metodo}. "
                           f"Revisa el verbo en routes/api.php.", estado=405)
        if estado == 422:
            raise ErrorApi(mensaje_laravel or "Datos inválidos.", cuerpo.get("errors"), estado=422)
        if estado >= 500:
            detalle = f": {mensaje_laravel}" if mensaje_laravel else ""
            raise ErrorApi(f"Error 500 en Laravel{detalle}. Revisa storage/logs/laravel.log",
                           estado=estado)
        raise ErrorApi(f"Respuesta inesperada ({estado}).", estado=estado)

    def _registrar(self, metodo, url, datos, inicio, estado, razon, cuerpo):
        registro = Registro(
            metodo=metodo, url=url,
            enviado=ocultar_claves(datos) if datos else None,
            estado=estado, razon=razon, respuesta=cuerpo,
            milisegundos=round((time.perf_counter() - inicio) * 1000),
            con_token=self.token is not None,
        )
        for observador in self.observadores:
            observador(registro)

    def _guardar_sesion(self, cuerpo: dict):
        """Registro y login responden igual: {"user": {...}, "token": "..."}"""
        if not isinstance(cuerpo, dict) or "token" not in cuerpo or "user" not in cuerpo:
            raise ErrorApi('La respuesta debe tener la forma {"user": {...}, "token": "..."}. '
                           "Revisa qué devuelve tu controlador.")
        self.token = cuerpo["token"]
        self.usuario = cuerpo["user"]
        return self.usuario

    # ─── NIVEL 1: Autenticación ───────────────────────────────────
    def registrar(self, nombre: str, email: str, password: str, confirmacion: str) -> dict:
        cuerpo = self._peticion("POST", "/registro", {
            "name": nombre, "email": email,
            "password": password, "password_confirmation": confirmacion,
        })
        return self._guardar_sesion(cuerpo)

    def login(self, email: str, password: str) -> dict:
        cuerpo = self._peticion("POST", "/login", {"email": email, "password": password})
        return self._guardar_sesion(cuerpo)

    def perfil(self) -> dict:
        self.usuario = self._peticion("GET", "/perfil")
        return self.usuario

    def logout(self):
        try:
            self._peticion("POST", "/logout")
        finally:
            # Aunque falle, la app "olvida" el token
            self.token = None
            self.usuario = None

    # ─── NIVEL 2: Mi perfil ───────────────────────────────────────
    def actualizar_perfil(self, nombre: str, email: str) -> dict:
        self.usuario = self._peticion("PUT", "/perfil", {"name": nombre, "email": email})
        return self.usuario

    def cambiar_password(self, actual: str, nueva: str, confirmacion: str):
        self._peticion("PUT", "/perfil/password", {
            "password_actual": actual,
            "password": nueva, "password_confirmation": confirmacion,
        })

    # ─── NIVEL 3: Productos protegidos y ventas ────────────────────
    def productos(self) -> list[dict]:
        return self._peticion("GET", "/productos")

    def vender(self, id_producto: int, cantidad: int) -> dict:
        return self._peticion("POST", f"/productos/{id_producto}/vender", {"cantidad": cantidad})

    def cerrar(self):
        self.cliente.close()
