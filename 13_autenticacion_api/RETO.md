# Reto: construye la API que la app necesita

La app `app_usuarios.py` **ya está terminada**. Tiene registro, login, perfil y venta de productos... pero ninguno de esos botones funciona, porque **la API todavía no existe**.

Tu trabajo: construir en Laravel 13 los endpoints que la app espera, **respetando exactamente el contrato** de abajo.

> **Así trabajan los equipos reales:** el equipo de la app móvil y el del backend acuerdan un *contrato de API* (rutas, datos de entrada y respuestas). Cada uno construye su parte por separado y, si los dos cumplen el contrato, todo encaja.

---

## Cómo sabrás que vas bien

Corre la app (`python app_usuarios.py`) y mira el **Monitor de API**. A medida que construyes, los códigos irán cambiando:

```
POST /api/registro   404 Not Found         ← todavía no existe la ruta
POST /api/registro   500 Server Error      ← la ruta existe, pero el controlador falla
POST /api/registro   422 Unprocessable     ← ¡ya valida! (prueba un email repetido)
POST /api/registro   201 Created           ← endpoint terminado
```

La app también te da **pistas** en los mensajes de error, por ejemplo:
- *"La ruta POST /api/registro no existe. ¿La agregaste en routes/api.php?"*
- *"La ruta /api/login existe, pero no acepta GET. Revisa el verbo en routes/api.php."*
- *"Error 500 en Laravel: Call to undefined method... Revisa storage/logs/laravel.log"*

> **Recomendación:** prueba cada endpoint **primero en Insomnia** y luego en la app. Si funciona en Insomnia y no en la app, compara lo que envía cada uno usando el Monitor.

---

## Preparación (una sola vez)

Usa el proyecto Laravel del módulo 12 (el de productos), o crea uno nuevo y copia los archivos de `12_consumo_api/laravel_api/`.

```bash
php artisan install:api      # instala Sanctum y crea routes/api.php (si no lo hiciste en el 12)
php artisan migrate
```

Al final, `install:api` te avisa:

```
Please add the [Laravel\Sanctum\HasApiTokens] trait to your User model.
```

**¡Hazle caso!** Abre `app/Models/User.php` y agrega el trait `HasApiTokens`. Sin él, `$user->createToken()` no existe.

---

## NIVEL 1: Autenticación

Crea el controlador:

```bash
php artisan make:controller Api/AuthController
php artisan make:controller Api/PerfilController
```

### 1.1 `POST /api/registro`

| | |
|---|---|
| **Es** | Pública (sin token) |
| **Recibe** | `name`, `email`, `password`, `password_confirmation` |
| **Valida** | `name` obligatorio (máx. 100) · `email` obligatorio, válido y **único** en `users` · `password` obligatorio, mínimo 8 y **confirmado** |
| **Éxito** | `201` → `{"user": {...}, "token": "1\|abc..."}` |
| **Errores** | `422` si falla la validación |

```json
// Respuesta 201
{
  "user": { "id": 1, "name": "Ana", "email": "ana@correo.com", "created_at": "...", "updated_at": "..." },
  "token": "1|GvGwVg7OrsXk2..."
}
```

> **Pistas**
> - La regla `confirmed` busca automáticamente un campo llamado `password_confirmation`.
> - Para crear el token: `$user->createToken('app-movil')->plainTextToken`.
> - ¿Hay que hacer `Hash::make()`? Mira el método `casts()` del modelo `User`: ya tiene `'password' => 'hashed'`.
> - Verifica en la base de datos que la contraseña quedó como `$2y$12$...` y **no** en texto plano.

### 1.2 `POST /api/login`

| | |
|---|---|
| **Es** | Pública |
| **Recibe** | `email`, `password` |
| **Éxito** | `200` → `{"user": {...}, "token": "..."}` (mismo formato que el registro) |
| **Errores** | `401` → `{"message": "Email o contraseña incorrectos."}` · `422` si falta algún campo |

> **Pistas**
> - Busca el usuario por email y compara la clave con `Hash::check($claveEscrita, $user->password)`.
> - Responde **el mismo mensaje** si el email no existe o si la clave está mal. ¿Por qué crees que es más seguro así?

### 1.3 `GET /api/perfil`

| | |
|---|---|
| **Es** | **Protegida** (requiere token) |
| **Éxito** | `200` → los datos del usuario dueño del token |
| **Errores** | `401` sin token o con token inválido |

> **Pistas**
> - Agrupa las rutas protegidas: `Route::middleware('auth:sanctum')->group(function () { ... });`
> - Dentro de una ruta protegida, `$request->user()` es el usuario que envió el token. No necesitas buscarlo.
> - ¿Aparece el campo `password` en la respuesta? No debería. ¿Qué lo oculta? (Mira `#[Hidden]` en el modelo).
> - ¿En Insomnia te sale **`500 Route [login] not defined`** en vez de `401`? Te falta el header `Accept: application/json`. Sin él, Laravel cree que eres un navegador y trata de mandarte a una página de login que tu API no tiene.

### 1.4 `POST /api/logout`

| | |
|---|---|
| **Es** | Protegida |
| **Éxito** | `204` sin contenido. **El token usado deja de funcionar.** |

> **Pistas**
> - `$request->user()->currentAccessToken()->delete();`
> - Para responder 204: `return response()->noContent();`
> - **Compruébalo:** después del logout, usa el mismo token en Insomnia para `GET /api/perfil`. Debe dar `401`.

---

## NIVEL 2: Mi perfil

### 2.1 `PUT /api/perfil`

| | |
|---|---|
| **Es** | Protegida |
| **Recibe** | `name`, `email` |
| **Valida** | Igual que el registro, pero el email debe ser único **sin contar al propio usuario** |
| **Éxito** | `200` → el usuario actualizado |
| **Errores** | `422` si el email ya lo usa **otra** persona |

> **Pista:** si usas `unique:users` tal cual, el usuario no podrá guardar sin cambiar su email (¡el suyo ya existe!). Busca `Rule::unique('users')->ignore(...)` en la documentación de Laravel.

### 2.2 `PUT /api/perfil/password`

| | |
|---|---|
| **Es** | Protegida |
| **Recibe** | `password_actual`, `password`, `password_confirmation` |
| **Éxito** | `204` sin contenido |
| **Errores** | `422` con el error en **`password_actual`** si la clave actual no es correcta |

> **Pistas**
> - Para lanzar un 422 "a mano" en un campo específico:
>   ```php
>   throw ValidationException::withMessages(['password_actual' => 'La contraseña actual no es correcta.']);
>   ```
> - **Extra de seguridad:** al cambiar la clave, cierra la sesión en los *otros* dispositivos borrando sus tokens (`$user->tokens()`).

---

## NIVEL 3: Proteger y vender

### 3.1 Proteger los productos

Mueve el `Route::apiResource('productos', ...)` del módulo 12 **dentro** del grupo `auth:sanctum`.

**Compruébalo:** en Insomnia, `GET /api/productos` sin token → `401`. En la app, con sesión iniciada → `200` (verás el ícono de candado en el Monitor).

### 3.2 `POST /api/productos/{producto}/vender`

| | |
|---|---|
| **Es** | Protegida |
| **Recibe** | `cantidad` (entero, mínimo 1) |
| **Regla de negocio** | No se puede vender más de lo que hay en stock |
| **Éxito** | `200` → el producto con el stock **ya descontado** |
| **Errores** | `422` en `cantidad` → `"Solo hay N unidades disponibles."` · `404` si el producto no existe |

> **Pistas**
> - Este endpoint **no es un CRUD**: es una *acción*. Por eso no sale de `apiResource` y lo registras tú: `Route::post('/productos/{producto}/vender', ...)`.
> - Con `Producto $producto` en el método, Laravel busca el producto solo (y responde 404 si no existe).
> - `$producto->decrement('stock', $cantidad)` resta y guarda en un solo paso.
> - `$producto->fresh()` vuelve a leer el producto de la BD (con el stock nuevo).

---

## Retos extra (opcionales)

1. **Frenar ataques de fuerza bruta:** limita el login a 5 intentos por minuto con el middleware `throttle:5,1`. ¿Qué código HTTP responde Laravel al pasarse del límite? Haz que la app muestre un mensaje claro.
2. **Historial de ventas:** crea la tabla `ventas` (`producto_id`, `user_id`, `cantidad`, `total`) y guarda cada venta. Agrega `GET /api/ventas` con las ventas **del usuario que inició sesión**.
3. **Recordar la sesión:** hoy, si cierras la app, tienes que volver a iniciar sesión. Investiga cómo guardar el token en el dispositivo con Flet y úsalo al abrir la app (llamando a `GET /api/perfil` para comprobar que sigue siendo válido).
4. **Mensajes en español:** instala `laravel-lang/common` para que Laravel responda "El campo email ya ha sido registrado" en vez de "The email has already been taken".

---

## Checklist de entrega

**Nivel 1**
- [ ] Puedo registrarme desde la app y quedo dentro (pantalla de productos)
- [ ] Registrarme con un email repetido muestra el error **debajo del campo Email**
- [ ] La contraseña se guarda con hash en la base de datos (no en texto plano)
- [ ] Login con clave incorrecta → `401` y mensaje claro
- [ ] `GET /api/perfil` sin token → `401` (probado en Insomnia)
- [ ] Después del logout, el token viejo ya no sirve (probado en Insomnia)
- [ ] `password` **nunca** aparece en ninguna respuesta

**Nivel 2**
- [ ] Puedo cambiar mi nombre sin cambiar el email (no da error de "email repetido")
- [ ] No puedo usar el email de otro usuario
- [ ] Cambiar la contraseña con la clave actual incorrecta muestra el error debajo del campo

**Nivel 3**
- [ ] Los productos sin token responden `401`
- [ ] Vender descuenta el stock y la lista se actualiza
- [ ] Vender más de lo disponible muestra "Solo hay N unidades disponibles."

> **¿Atascado?** La solución completa está en [`solucion/`](solucion/). Úsala para **comparar** después de intentarlo, no para copiar: el objetivo es que puedas explicar cada línea.
