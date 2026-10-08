# API de Productos con Laravel

Esta carpeta **no es un proyecto Laravel completo**. Contiene solo los **4 archivos clave** que debes crear o copiar dentro de tu proyecto, en la misma ruta:

| Archivo | Para qué sirve |
|---|---|
| `database/migrations/..._create_productos_table.php` | Crea la tabla `productos` en MySQL |
| `app/Models/Producto.php` | Modelo Eloquent: campos permitidos y conversión de tipos |
| `app/Http/Controllers/Api/ProductoController.php` | Las 5 acciones del CRUD, que responden en JSON |
| `routes/api.php` | Registra las rutas `/api/productos` |

---

## Paso 1: Crear el proyecto (si aún no lo tienes)

```bash
composer create-project laravel/laravel api-productos
cd api-productos
```

## Paso 2: Configurar la base de datos

En el archivo `.env`:

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=api_productos
DB_USERNAME=root
DB_PASSWORD=
```

Crea la base de datos `api_productos` en phpMyAdmin (o en tu cliente MySQL).

## Paso 3: Activar las rutas de API

Desde Laravel 11, el archivo `routes/api.php` **ya no viene incluido**. Se activa con:

```bash
php artisan install:api
```

> Este comando también instala **Sanctum**, que usarás en el reto de autenticación.

## Paso 4: Modelo y migración

```bash
php artisan make:model Producto -m
```

Reemplaza el contenido de los archivos generados con los de esta carpeta:
- `app/Models/Producto.php`
- `database/migrations/xxxx_create_productos_table.php` (deja el nombre que generó Artisan y copia solo el contenido)

Luego ejecuta la migración:

```bash
php artisan migrate
```

## Paso 5: Controlador de API

```bash
php artisan make:controller Api/ProductoController --api --model=Producto
```

La opción `--api` genera solo los 5 métodos del CRUD (sin `create` ni `edit`, que son formularios HTML y una API no los necesita). Copia el contenido de `app/Http/Controllers/Api/ProductoController.php`.

## Paso 6: Rutas

Copia `routes/api.php` y comprueba que quedaron las 5 rutas:

```bash
php artisan route:list --path=api
```

```
GET|HEAD   api/productos ............. productos.index
POST       api/productos ............. productos.store
GET|HEAD   api/productos/{producto} .. productos.show
PUT|PATCH  api/productos/{producto} .. productos.update
DELETE     api/productos/{producto} .. productos.destroy
```

## Paso 7: Encender el servidor

```bash
# Solo para tu PC (app en escritorio o emulador):
php artisan serve

# Para que el celular real también pueda conectarse:
php artisan serve --host=0.0.0.0 --port=8000
```

---

## Paso 8: Probar la API ANTES de usar la app

Primero comprueba que la API funciona sola. Si falla aquí, el problema está en Laravel y no en Flet.

Abre en el navegador: `http://127.0.0.1:8000/api/productos` → debe mostrar `[]`.

Con **Postman** o **Thunder Client** (o `curl`):

```bash
# Crear
curl -X POST http://127.0.0.1:8000/api/productos \
     -H "Accept: application/json" -H "Content-Type: application/json" \
     -d '{"nombre": "Laptop", "precio": 3500000, "stock": 5}'

# Validación (debe responder 422 con los errores)
curl -X POST http://127.0.0.1:8000/api/productos \
     -H "Accept: application/json" -H "Content-Type: application/json" \
     -d '{"nombre": ""}'
```

Respuesta de un error de validación (esto es lo que la app Flet muestra debajo de cada campo):

```json
{
  "message": "The nombre field is required. (and 2 more errors)",
  "errors": {
    "nombre": ["The nombre field is required."],
    "precio": ["The precio field is required."],
    "stock":  ["The stock field is required."]
  }
}
```

> **¿Mensajes en español?** Instala las traducciones con `composer require laravel-lang/common --dev` y `php artisan lang:add es`, y pon `APP_LOCALE=es` en el `.env`.

---

## Detalles que hacen la diferencia

- **`Accept: application/json`:** sin este header, cuando la validación falla Laravel responde con una *redirección* (pensada para formularios web). La app Flet siempre lo envía.
- **`$casts` en el modelo:** una columna `decimal` llega como texto (`"3500000.00"`). Con `'precio' => 'float'` llega como número (`3500000.0`).
- **Route Model Binding:** en `show(Producto $producto)` Laravel busca el producto por id automáticamente. Si no existe, responde `404` sin que escribas ningún `if`.
- **Códigos de estado:** `store` devuelve `201` y `destroy` devuelve `204`. La app los usa para saber qué pasó.
- **CORS:** solo importa si corres la app con `flet run --web` (navegador). Una app de escritorio o un APK no tienen restricciones de CORS.
