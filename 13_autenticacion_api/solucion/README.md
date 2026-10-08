# Solución del reto (Laravel 13)

> ⚠️ **¿Ya lo intentaste?** Aprendes mucho más peleando 20 minutos con un error que copiando la solución en 2. Úsala para **comparar** tu código cuando ya funcione, o para destrabarte en un punto concreto.

Esta solución fue probada en **Laravel 13.35** con Sanctum, contra la app `app_usuarios.py`.

## Archivos

| Archivo | Nivel | Qué hace |
|---|---|---|
| `app/Models/User.php` | 1 | El `User` de Laravel 13 + el trait `HasApiTokens` |
| `app/Http/Controllers/Api/AuthController.php` | 1 | `registro`, `login`, `logout` |
| `app/Http/Controllers/Api/PerfilController.php` | 1 y 2 | `mostrar`, `actualizar`, `cambiarPassword` |
| `app/Http/Controllers/Api/ProductoController.php` | 3 | El CRUD del módulo 12 + `vender` |
| `routes/api.php` | 1, 2 y 3 | Rutas públicas y protegidas con `auth:sanctum` |

El modelo `Producto` y su migración son los mismos del módulo 12 (`12_consumo_api/laravel_api/`).

## Montarla en un proyecto nuevo

```bash
composer create-project laravel/laravel api-tienda
cd api-tienda
php artisan install:api
```

Copia los archivos de esta carpeta **y** los del módulo 12 (`app/Models/Producto.php` y la migración de productos) en las mismas rutas, y luego:

```bash
php artisan migrate
php artisan route:list --path=api     # deben salir 12 rutas
php artisan serve
```

Para tener productos de prueba:

```bash
php artisan tinker
>>> App\Models\Producto::create(['nombre' => 'Laptop', 'precio' => 3500000, 'stock' => 5]);
```

## Decisiones que vale la pena discutir en clase

- **¿Por qué el login responde 401 y no 422?** La petición está bien formada (por eso no es 422), pero las credenciales no identifican a nadie. Ojo: Laravel Breeze, por ejemplo, responde 422 en este caso. Ambas convenciones existen; lo importante es que el **contrato** lo diga y que la app y la API lo respeten.
- **¿Por qué el mismo mensaje si el email no existe o si la clave está mal?** Si dijéramos "ese email no está registrado", un atacante podría averiguar qué emails tienen cuenta.
- **¿Por qué `Hash::check` y no la regla `current_password` en el cambio de clave?** Laravel tiene la regla `current_password`, que hace lo mismo en una línea. Aquí usamos `Hash::check` porque deja a la vista **cómo** se verifica una contraseña con hash. Reto: reemplázalo por la regla y comprueba que la app sigue mostrando el error en el campo correcto.
- **¿Por qué `vender` usa `decrement()`?** Resta directamente en la base de datos (`UPDATE ... SET stock = stock - 3`), sin leer, restar en PHP y volver a guardar.
