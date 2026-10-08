<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Producto;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

// Controlador de API: NO devuelve vistas Blade, devuelve JSON.
// Crear con: php artisan make:controller Api/ProductoController --api --model=Producto
class ProductoController extends Controller
{
    // GET /api/productos  → lista todos
    public function index(): JsonResponse
    {
        return response()->json(Producto::orderBy('nombre')->get());
    }

    // POST /api/productos  → crea uno nuevo (201 Created)
    public function store(Request $request): JsonResponse
    {
        // Si la validación falla, Laravel responde solo con 422 y los errores en JSON
        // (porque la app envía el header "Accept: application/json").
        $datos = $request->validate($this->reglas());

        $producto = Producto::create($datos);

        return response()->json($producto, 201);
    }

    // GET /api/productos/{producto}  → muestra uno (404 si no existe)
    public function show(Producto $producto): JsonResponse
    {
        return response()->json($producto);
    }

    // PUT /api/productos/{producto}  → actualiza
    public function update(Request $request, Producto $producto): JsonResponse
    {
        $datos = $request->validate($this->reglas());

        $producto->update($datos);

        return response()->json($producto);
    }

    // DELETE /api/productos/{producto}  → elimina (204 No Content)
    public function destroy(Producto $producto): JsonResponse
    {
        $producto->delete();

        return response()->json(null, 204);
    }

    private function reglas(): array
    {
        return [
            'nombre' => 'required|string|max:100',
            'precio' => 'required|numeric|min:0',
            'stock'  => 'required|integer|min:0',
        ];
    }
}
