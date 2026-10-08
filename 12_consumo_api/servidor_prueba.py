import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# SERVIDOR DE PRUEBA (imita la API de Laravel)
#
# ¿Para qué sirve? Para practicar con la app Flet aunque todavía no tengas
# Laravel funcionando. Responde en las MISMAS rutas y con el MISMO formato JSON
# que el ProductoController de la carpeta laravel_api/.
#
#   python servidor_prueba.py
#
# Los datos viven en memoria: al cerrar el servidor se pierden.
# Cuando tengas Laravel listo, apaga este servidor y usa:  php artisan serve

PUERTO = 8000

productos = {
    1: {"id": 1, "nombre": "Laptop", "precio": 3500000.0, "stock": 5},
    2: {"id": 2, "nombre": "Mouse inalámbrico", "precio": 85000.0, "stock": 20},
    3: {"id": 3, "nombre": "Monitor 24\"", "precio": 780000.0, "stock": 0},
}
siguiente_id = 4


def validar(datos: dict) -> dict:
    """Mismas reglas que $request->validate() en el controlador de Laravel."""
    errores = {}
    nombre = datos.get("nombre")
    if not isinstance(nombre, str) or not nombre.strip():
        errores["nombre"] = ["El campo nombre es obligatorio."]
    elif len(nombre) > 100:
        errores["nombre"] = ["El campo nombre no debe tener más de 100 caracteres."]

    precio = datos.get("precio")
    if not isinstance(precio, (int, float)) or isinstance(precio, bool):
        errores["precio"] = ["El campo precio debe ser un número."]
    elif precio < 0:
        errores["precio"] = ["El campo precio debe ser al menos 0."]

    stock = datos.get("stock")
    if not isinstance(stock, int) or isinstance(stock, bool):
        errores["stock"] = ["El campo stock debe ser un número entero."]
    elif stock < 0:
        errores["stock"] = ["El campo stock debe ser al menos 0."]
    return errores


class ManejadorApi(BaseHTTPRequestHandler):

    # ─── Utilidades ───────────────────────────────────────────────
    def responder(self, codigo: int, cuerpo=None):
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if cuerpo is not None:
            self.wfile.write(json.dumps(cuerpo, ensure_ascii=False).encode("utf-8"))

    def leer_json(self) -> dict:
        largo = int(self.headers.get("Content-Length", 0))
        try:
            return json.loads(self.rfile.read(largo) or b"{}")
        except json.JSONDecodeError:
            return {}

    def obtener_id(self):
        """'/api/productos/7' → 7 | '/api/productos' → None | otra ruta → False"""
        partes = self.path.strip("/").split("/")
        if partes[:2] != ["api", "productos"] or len(partes) > 3:
            return False
        if len(partes) == 2:
            return None
        return int(partes[2]) if partes[2].isdigit() else False

    def no_encontrado(self):
        self.responder(404, {"message": "No query results for model [App\\Models\\Producto]."})

    def guardar(self, id_existente=None):
        global siguiente_id
        datos = self.leer_json()
        errores = validar(datos)
        if errores:
            primer_error = next(iter(errores.values()))[0]
            self.responder(422, {"message": primer_error, "errors": errores})
            return

        if id_existente is None:
            id_nuevo, siguiente_id = siguiente_id, siguiente_id + 1
            codigo = 201
        else:
            id_nuevo, codigo = id_existente, 200

        productos[id_nuevo] = {
            "id": id_nuevo,
            "nombre": datos["nombre"].strip(),
            "precio": float(datos["precio"]),
            "stock": datos["stock"],
        }
        self.responder(codigo, productos[id_nuevo])

    # ─── Rutas (equivalen a Route::apiResource) ───────────────────
    def do_GET(self):
        id = self.obtener_id()
        if id is False:
            self.no_encontrado()
        elif id is None:                                   # GET /api/productos
            self.responder(200, sorted(productos.values(), key=lambda p: p["nombre"]))
        elif id in productos:                              # GET /api/productos/{id}
            self.responder(200, productos[id])
        else:
            self.no_encontrado()

    def do_POST(self):                                     # POST /api/productos
        if self.obtener_id() is None:
            self.guardar()
        else:
            self.no_encontrado()

    def do_PUT(self):                                      # PUT /api/productos/{id}
        id = self.obtener_id()
        if id in productos:
            self.guardar(id)
        else:
            self.no_encontrado()

    def do_DELETE(self):                                   # DELETE /api/productos/{id}
        id = self.obtener_id()
        if id in productos:
            del productos[id]
            self.responder(204)
        else:
            self.no_encontrado()


if __name__ == "__main__":
    # 0.0.0.0 = acepta conexiones de otros dispositivos de la red (tu celular)
    servidor = ThreadingHTTPServer(("0.0.0.0", PUERTO), ManejadorApi)
    print(f"API de prueba en http://127.0.0.1:{PUERTO}/api/productos  (Ctrl+C para salir)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
