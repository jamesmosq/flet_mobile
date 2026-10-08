# 13 - Autenticación: construye tu propia API con usuarios

## ¿Qué cambia en este módulo?

En el módulo 12 **consumiste** una API que ya existía. Ahora vas a **construirla**: la app ya está hecha y tú creas en Laravel los endpoints que necesita.

Y aparece algo que toda app real tiene: **usuarios**. Registrarse, iniciar sesión, ver mi perfil y que solo los usuarios con sesión iniciada puedan vender productos.

> 📋 **El enunciado completo, con el contrato de la API y pistas, está en [`RETO.md`](RETO.md).** Este README explica los conceptos que necesitas antes de empezar.

---

## Conceptos clave

### 1. Autenticación vs. autorización

| | Pregunta | Si falla, HTTP responde |
|---|---|---|
| **Autenticación** | ¿Quién eres? | `401 Unauthorized`: "no sé quién eres, inicia sesión" |
| **Autorización** | ¿Tienes permiso para esto? | `403 Forbidden`: "sé quién eres, pero no puedes hacer esto" |

En este módulo trabajamos la **autenticación**. Un ejemplo de autorización sería "solo los administradores pueden borrar productos".

### 2. Nunca guardes contraseñas: guarda su *hash*

Si alguien roba tu base de datos, no debería poder leer las contraseñas. Por eso se guarda un **hash**: una transformación que **no se puede revertir**.

```
Contraseña:  secreta123
En la BD:    $2y$12$Kx8vQ3mZ...Wq9e   ← imposible volver a "secreta123"
```

¿Y cómo verificamos el login si no podemos leerla? Se aplica el hash a la clave que escribió el usuario y se **comparan los hashes**: `Hash::check('secreta123', $user->password)` → `true`.

> En Laravel 13 el modelo `User` ya trae `'password' => 'hashed'` en `casts()`: al guardar, aplica el hash automáticamente.

### 3. Tokens: la "manilla" del concierto

Una API **no recuerda** quién eres entre una petición y otra (cada petición llega sola). Por eso se usan **tokens**:

```
  App                                              Laravel
   │  POST /api/login {email, password}              │
   │ ──────────────────────────────────────────────► │  ¿clave correcta? → crea un token
   │ ◄────────────────────────────────────────────── │
   │  {"user": {...}, "token": "1|aBcD..."}          │
   │                                                 │
   │  GUARDA el token                                │
   │                                                 │
   │  GET /api/perfil                                │
   │  Authorization: Bearer 1|aBcD...                │
   │ ──────────────────────────────────────────────► │  ¿token válido? → ¿de quién es?
   │ ◄────────────────────────────────────────────── │
   │  {"id": 1, "name": "Ana", ...}                  │
```

Es como la manilla de un concierto: te la ponen **una vez** en la entrada (login) y después solo la muestras para entrar a cada zona (cada petición).

**Laravel Sanctum** es el paquete que crea y verifica esos tokens. Los guarda en la tabla `personal_access_tokens`.

### 4. Rutas públicas y protegidas

```php
// Públicas: cualquiera puede llamarlas
Route::post('/login', ...);

// Protegidas: sin un token válido, Laravel responde 401 automáticamente
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/perfil', ...);
});
```

Un **middleware** es un "guardia" que revisa la petición **antes** de que llegue al controlador.

### 5. No todo es CRUD

`POST /api/productos/5/vender` no crea, lee, actualiza ni borra un producto: es una **acción** con una **regla de negocio** ("no vender más de lo que hay"). Las APIs reales están llenas de endpoints así.

---

## Archivos de esta carpeta

| Archivo | Para qué sirve |
|---|---|
| [`RETO.md`](RETO.md) | **Empieza aquí.** El contrato de la API, los 3 niveles, pistas y checklist |
| `app_usuarios.py` | La app terminada: Login, Registro, Productos (vender) y Mi perfil |
| `api_cliente.py` | Cliente de la API: guarda el token y lo envía en cada petición |
| `monitor_api.py` | Monitor de API (el del módulo 12, con 🔒 cuando la petición lleva token) |
| [`solucion/`](solucion/) | La solución en Laravel 13. **Úsala para comparar, no para copiar** |

---

## Cómo trabajar

```bash
# Terminal 1: tu proyecto Laravel
php artisan serve

# Terminal 2: la app
python app_usuarios.py
```

1. Lee el contrato del endpoint en `RETO.md`.
2. Constrúyelo en Laravel (ruta → controlador → validación → respuesta).
3. Pruébalo en **Insomnia**, incluidos los casos de error.
4. Pruébalo en la **app** y mira el Monitor de API.
5. Marca el checklist y pasa al siguiente.

> **Truco para Insomnia:** después del login, copia el `token` de la respuesta. En las peticiones protegidas, ve a la pestaña **Auth → Bearer Token** y pégalo ahí. Es exactamente lo que hace la app.

---

## Seguridad: lo que la app hace bien (y por qué)

Revisa `api_cliente.py` y busca cada uno de estos puntos:

- **Las contraseñas nunca se muestran**, ni siquiera en el Monitor: `ocultar_claves()` las cambia por `********`.
- **Al cerrar sesión, la app olvida el token** aunque falle la petición (`finally` en `logout()`).
- **Si el servidor responde 401** con la sesión iniciada, la app asume que el token ya no sirve y vuelve al login.
- En producción, la API debe usar **`https://`**. Con `http://` el token viaja sin cifrar y cualquiera en la misma red WiFi podría leerlo.
