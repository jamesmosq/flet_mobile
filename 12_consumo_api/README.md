# 12 - Consumo de API: Conectar la app móvil con una plataforma web

## ¿Dónde estamos?

En el módulo 09 guardaste los datos en **SQLite**, dentro del mismo dispositivo. Eso tiene un problema: si tienes la app en dos celulares, cada uno guarda sus propios datos y nunca se enteran de lo que hace el otro.

Las apps reales (Rappi, Instagram, el portal de tu universidad...) guardan los datos en un **servidor central**. La app móvil y la página web leen y escriben en **la misma base de datos** a través de una **API**.

En el curso ya aprendiste a construir una API con **Laravel**. Ahora vas a hacer que tu app Flet la consuma.

---

## La arquitectura

```
 ┌──────────────────┐        HTTP + JSON         ┌──────────────────┐        SQL        ┌─────────┐
 │   App Flet       │  ───── petición ────────►  │   API Laravel    │  ─────────────►   │  MySQL  │
 │   (celular)      │  ◄──── respuesta ───────   │   (servidor)     │  ◄─────────────   │         │
 └──────────────────┘                            └──────────────────┘                   └─────────┘
                                                        ▲
 ┌──────────────────┐                                   │
 │  Plataforma web  │  ─────────────────────────────────┘
 │  (navegador)     │      la web usa la MISMA base de datos
 └──────────────────┘
```

- La **app nunca toca la base de datos directamente**. Solo le pide cosas a la API.
- La API **valida** los datos, los guarda en MySQL y responde con **JSON**.
- Si creas un producto desde el celular, aparece en la web, y al revés.

---

## Conceptos clave

### 1. API REST y verbos HTTP

Una API REST organiza todo alrededor de **recursos** (productos, usuarios, pedidos...). Cada operación CRUD se hace con un verbo HTTP distinto sobre una URL:

| CRUD | Verbo HTTP | URL | Laravel (método del controlador) |
|---|---|---|---|
| **R**ead (todos) | `GET` | `/api/productos` | `index()` |
| **R**ead (uno) | `GET` | `/api/productos/5` | `show()` |
| **C**reate | `POST` | `/api/productos` | `store()` |
| **U**pdate | `PUT` | `/api/productos/5` | `update()` |
| **D**elete | `DELETE` | `/api/productos/5` | `destroy()` |

### 2. JSON: el idioma en común

PHP y Python no se entienden entre sí, pero ambos hablan **JSON**:

```json
{ "id": 5, "nombre": "Laptop", "precio": 3500000.0, "stock": 5 }
```

En Python, `respuesta.json()` convierte eso en un diccionario normal: `p["nombre"]`, `p["precio"]`...

### 3. Códigos de estado HTTP

El servidor siempre responde con un número que indica qué pasó:

| Código | Significado | ¿Cuándo lo envía Laravel? |
|---|---|---|
| `200` | OK | GET o PUT exitoso |
| `201` | Created | POST exitoso (se creó el registro) |
| `204` | No Content | DELETE exitoso (no hay nada que devolver) |
| `404` | Not Found | El id no existe |
| `422` | Unprocessable Content | Falló la validación (`$request->validate`) |
| `500` | Server Error | Hay un error en tu código PHP |

### 4. La librería `httpx`

Para hacer peticiones HTTP desde Python usamos `httpx` (ya viene instalada con Flet):

```python
import httpx

r = httpx.get("http://127.0.0.1:8000/api/productos")
print(r.status_code)   # 200
print(r.json())        # [{'id': 1, 'nombre': 'Laptop', ...}, ...]

r = httpx.post("http://127.0.0.1:8000/api/productos",
               json={"nombre": "Mouse", "precio": 85000, "stock": 20},
               headers={"Accept": "application/json"})
print(r.status_code)   # 201
```

> **Importante:** siempre envía el header `Accept: application/json`. Así Laravel responde los errores en JSON. Sin él, un error de validación devuelve una **redirección HTML** y tu app no sabrá qué pasó.

---

## El problema del `localhost` (¡lee esto!)

`localhost` o `127.0.0.1` significa **"este mismo aparato"**. Si la app corre en el celular, `localhost` es el celular, no tu PC. Por eso la URL cambia según dónde corras la app:

| ¿Dónde corre la app Flet? | URL de la API |
|---|---|
| Escritorio (`python archivo.py`) | `http://127.0.0.1:8000/api` |
| Emulador de Android | `http://10.0.2.2:8000/api` (alias especial de tu PC) |
| Celular real en la misma red WiFi | `http://192.168.X.X:8000/api` (la IP de tu PC) |

Para el celular real:

1. Averigua la IP de tu PC con `ipconfig` (Windows) en la línea **Dirección IPv4**.
2. Arranca Laravel aceptando conexiones de la red:
   ```bash
   php artisan serve --host=0.0.0.0 --port=8000
   ```
3. Cambia `API_URL` en `api_client.py`.
4. Si no conecta, revisa que el **Firewall de Windows** permita el puerto 8000.

---

## Patrón repositorio... ahora remoto

¿Recuerdas `RepositorioProductos` del módulo 09? En `api_client.py` está `ApiProductos`, que tiene **los mismos métodos**. La diferencia es que por dentro hace peticiones HTTP en lugar de SQL:

```python
# Módulo 09 — RepositorioProductos (SQLite)
def insertar(self, nombre, precio, stock):
    self.conexion.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                          (nombre, precio, stock))

# Módulo 12 — ApiProductos (API)
def insertar(self, nombre, precio, stock):
    datos = {"nombre": nombre, "precio": precio, "stock": stock}
    return self._peticion("POST", "/productos", datos)
```

Por eso `02_crud_productos.py` se parece **muchísimo** a `app_sqlite.py`. La UI no sabe ni le importa de dónde vienen los datos.

### Lo nuevo: la red puede fallar

Con SQLite el archivo siempre está ahí. Con una API pueden pasar muchas cosas: el servidor está apagado, no hay WiFi, los datos son inválidos... Por eso:

```python
try:
    repo.insertar(nombre, precio, stock)
except ErrorApi as ex:
    mostrar_mensaje(ex.mensaje, error=True)   # "No se pudo conectar con el servidor..."
```

`ApiProductos` convierte cada problema (conexión, 404, 422, 500) en un `ErrorApi` con un mensaje claro para el usuario. Si es un error de validación (422), `ex.errores` trae el error **de cada campo**, y la app lo muestra debajo del `TextField` correspondiente.

---

## Ejercicios en esta carpeta

| Archivo | Descripción |
|---|---|
| `api_client.py` | Clase `ApiProductos`: el CRUD completo por HTTP, con manejo de errores |
| `01_listar_productos.py` | Tu primer `GET`: petición "a mano" y lista de productos |
| `02_crud_productos.py` | App completa: crear, listar, editar y eliminar contra la API |
| `monitor_api.py` | Componente **Monitor de API**: muestra dentro de la app cada petición y su respuesta (como Insomnia) |
| `GUIA_PRUEBAS.md` | **Práctica guiada:** cómo probar la app y ver qué pasa entre la app y la API |
| `servidor_prueba.py` | Servidor en Python que **imita** la API de Laravel, para practicar sin Laravel |
| `laravel_api/` | Archivos clave de Laravel (migración, modelo, controlador, rutas) y su guía |

---

## Cómo correrlo

**Opción A: con Laravel (lo real).** Sigue la guía de [`laravel_api/README.md`](laravel_api/README.md) y luego:

```bash
php artisan serve                 # en la carpeta del proyecto Laravel
python 02_crud_productos.py       # en esta carpeta, en otra terminal
```

**Opción B: sin Laravel (para practicar rápido).**

```bash
python servidor_prueba.py         # terminal 1
python 02_crud_productos.py       # terminal 2
```

> **¿Y cómo veo lo que hace la app?** Abajo de la app está el **Monitor de API**: muestra cada petición (verbo, URL, JSON enviado, código de estado y respuesta), igual que Insomnia. Sigue la práctica de [`GUIA_PRUEBAS.md`](GUIA_PRUEBAS.md).

---

## Al compilar el APK

- Si en escritorio funciona pero en el celular no, casi siempre es la **URL** (ver la tabla del `localhost`).
- Android bloquea por defecto las conexiones `http://` sin cifrar. Para clase está bien usar `http`, pero en una app publicada la API debe usar **`https://`**.
- `flet run --web` corre la app **en el navegador**. Ahí sí aplican las reglas de **CORS**: Laravel debe permitir el origen `http://localhost:8550` (ver `config/cors.php`).

---

## Retos

1. **Buscar:** agrega un `TextField` de búsqueda que llame a `GET /api/productos?buscar=lap`. En Laravel, filtra con `where('nombre', 'like', "%$buscar%")`.
2. **Detalle:** al tocar un producto, abre una pantalla nueva que use `repo.obtener(id)` (`GET /api/productos/{id}`).
3. **Nuevo campo:** agrega `categoria` a la migración, al modelo (`$fillable`), a las reglas de validación y al formulario de Flet. Así practicas el recorrido completo: **BD → API → App**.
4. **Avanzado:** protege la API con **Laravel Sanctum**. Haz una pantalla de login que guarde el token y envíalo en cada petición con el header `Authorization: Bearer <token>`.
