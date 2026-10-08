# Guía de pruebas: ver lo que pasa entre la app y la API

Cuando probaste la API con **Insomnia**, veías todo: la petición que enviabas y la respuesta del servidor.

Con la app es distinto: tocas "Guardar" y... ¿qué se envió? ¿Qué respondió Laravel? ¿Llegó el dato a la base de datos? Esta guía te enseña a **verlo todo**.

---

## La idea: la app es "un Insomnia con botones"

Tu app hace **exactamente lo mismo** que hacías en Insomnia. La diferencia es que la petición se arma con lo que el usuario escribe en el formulario:

| En Insomnia tú... | En la app... |
|---|---|
| Eliges el verbo: `POST` | El botón **Guardar** de "Nuevo producto" llama a `repo.insertar()`, que usa `POST` |
| Escribes la URL: `/api/productos` | Está en `api_client.py` (`API_URL`) |
| Escribes el body JSON a mano | Se arma con lo que hay en los `TextField` |
| Lees la respuesta en el panel derecho | Se convierte en la lista de productos (o en un mensaje de error) |

---

## Prepara tu pantalla: 3 ventanas

```
┌───────────────────────────┬──────────────────────────────┐
│ 1. Terminal Laravel       │ 2. App Flet                  │
│ php artisan serve         │ python 02_crud_productos.py  │
│                           │ ┌──────────────────────────┐ │
│ (aquí ves llegar cada     │ │  lista de productos      │ │
│  petición al servidor)    │ ├──────────────────────────┤ │
│                           │ │  Monitor de API          │ │
├───────────────────────────┤ │  POST /api/productos 201 │ │
│ 3. Insomnia               │ └──────────────────────────┘ │
│ (para comprobar desde     │                              │
│  "afuera" que es verdad)  │                              │
└───────────────────────────┴──────────────────────────────┘
```

1. **Terminal de Laravel:** `php artisan serve`. Cada petición que llega aparece como una línea nueva, con la ruta y el tiempo. Así compruebas que la petición **sí salió del celular y llegó al servidor**.
2. **La app:** `python 02_crud_productos.py`. Abajo está el **Monitor de API**: cada petición de la app aparece ahí, con lo que se envió y lo que respondió el servidor. Lo mismo se imprime en la terminal donde corriste la app.
3. **Insomnia:** con la petición `GET http://127.0.0.1:8000/api/productos` lista para enviar.

> ¿No tienes Laravel listo todavía? Usa `python servidor_prueba.py` en la ventana 1. Muestra cada petición de forma parecida.

---

## Cómo leer el Monitor de API

```
 POST  /api/productos                          201 Created   35 ms
 Enviado (body)
 { "nombre": "Teclado", "precio": 120000.0, "stock": 7 }
 Respuesta
 { "id": 4, "nombre": "Teclado", "precio": 120000.0, "stock": 7 }
```

| Parte | Qué significa |
|---|---|
| `POST` | Verbo HTTP (mismos colores que Insomnia) |
| `/api/productos` | Ruta de Laravel que se llamó (revísala con `php artisan route:list`) |
| `201 Created` | Código de estado. **Verde** = bien, **naranja** = error del cliente (404, 422), **rojo** = sin conexión o error 500 |
| `35 ms` | Cuánto tardó el servidor en responder |
| Enviado (body) | El JSON que armó la app con el formulario (como el body en Insomnia) |
| Respuesta | El JSON que devolvió el controlador de Laravel |

Los `GET` aparecen cerrados para no llenar la pantalla. **Tócalos** para ver la respuesta.

---

## Práctica guiada

Haz cada paso y **anota lo que ves en las 3 ventanas**.

### Parte A: el CRUD funciona

| # | Haz esto en la app | Monitor de API | Terminal Laravel | Compruébalo en Insomnia |
|---|---|---|---|---|
| 1 | Abre la app | `GET /api/productos` → `200 OK` | +1 línea `/api/productos` | `GET /api/productos` devuelve lo mismo que muestra la app |
| 2 | **+** → crea "Teclado", 120000, 7 | `POST` → `201 Created`, y luego un `GET` para recargar | +2 líneas | El Teclado aparece en el `GET`. **¿Qué `id` le asignó MySQL?** |
| 3 | Edita el Teclado → stock 3 | `PUT /api/productos/{id}` → `200 OK` | +1 línea `/api/productos/{id}` | `GET /api/productos/{id}` → stock 3 |
| 4 | Elimina el Teclado | `DELETE /api/productos/{id}` → `204 No Content` | +1 línea `/api/productos/{id}` | `GET /api/productos/{id}` → `404` |

> **Pregunta:** en el paso 2, ¿por qué hay **dos** peticiones si solo tocaste un botón? (Pista: busca `construir_lista()` en `guardar()`).

### Parte B: el camino contrario (de Insomnia a la app)

| # | Haz esto | ¿Qué pasa en la app? |
|---|---|---|
| 5 | En Insomnia: `POST /api/productos` con `{"nombre": "Desde Insomnia", "precio": 1000, "stock": 1}` | **Nada todavía.** La app no se entera sola |
| 6 | En la app: toca **Recargar** (↻) | Ahora sí aparece "Desde Insomnia" |

> **Conclusión:** la app solo sabe lo que le dice la API **cuando le pregunta**. Así funcionan casi todas las apps: piden los datos al abrir una pantalla o al recargar.

### Parte C: provoca errores a propósito

| # | Haz esto | Monitor de API | ¿Qué ve el usuario? |
|---|---|---|---|
| 7 | Crea un producto **sin nombre** | `POST` → `422`. En la respuesta está `errors.nombre` | El mensaje de Laravel debajo del campo Nombre |
| 8 | Abre "Editar" en un producto. **Antes de guardar**, bórralo desde Insomnia. Ahora toca Guardar | `PUT` → `404 Not Found` | "El producto no existe (quizá alguien lo borró)" |
| 9 | **Apaga Laravel** (Ctrl+C) y toca Recargar | `GET` → `--- Sin conexión` (en rojo) | "No se pudo conectar con el servidor" + botón Reintentar |
| 10 | Vuelve a encender Laravel y toca **Reintentar** | `GET` → `200 OK` | La lista vuelve |

> **Compara el 7 con Insomnia:** envía el mismo body vacío desde Insomnia, **sin** el header `Accept: application/json`. ¿Qué responde Laravel? ¿Por qué la app siempre envía ese header?

---

## ¿Algo no funciona? Busca el error por capas

Sigue este orden. Así sabes si el problema está en **Laravel** o en **la app**:

```
1. ¿Funciona en Insomnia?          NO → el problema está en Laravel (rutas, controlador, BD)
          │ SÍ
2. ¿La petición sale en el Monitor? NO → el problema está en la app (¿se llama al repo?)
          │ SÍ
3. ¿Qué código de estado tiene?
     --- Sin conexión → Laravel apagado o URL equivocada (API_URL en api_client.py)
     404              → la ruta o el id no existen (php artisan route:list)
     422              → mira "errors" en la respuesta: el JSON no cumple las reglas de validate()
     500              → error en el PHP: revisa storage/logs/laravel.log
     200/201 pero la lista no cambia → el problema está en la UI (¿se llamó a construir_lista()?)
```

---

## Para el celular

Cuando pruebes en el celular o en el emulador no tendrás la terminal, pero **el Monitor de API sigue ahí**, dentro de la app. Si ves `--- Sin conexión`, casi siempre es la URL. Revisa la tabla de `localhost` en el [README](README.md#el-problema-del-localhost-lee-esto).
