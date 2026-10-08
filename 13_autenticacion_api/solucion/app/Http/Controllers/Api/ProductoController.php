<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Producto;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;

// Es el ProductoController del módulo 12 + el método vender() del NIVEL 3.
class ProductoController extends Controller
{
    public function index(): JsonResponse
    {
        return response()->json(Producto::orderBy('nombre')->get());
    }

    public function store(Request $request): JsonResponse
    {
        $producto = Producto::create($request->validate($this->reglas()));

        return response()->json($producto, 201);
    }

    public function show(Producto $producto): JsonResponse
    {
        return response()->json($producto);
    }

    public function update(Request $request, Producto $producto): JsonResponse
    {
        $producto->update($request->validate($this->reglas()));

        return response()->json($producto);
    }

    public function destroy(Producto $producto): JsonResponse
    {
        $producto->delete();

        return response()->json(null, 204);
    }

    // POST /api/productos/{producto}/vender   ← NIVEL 3
    // No es un CRUD: es una ACCIÓN con reglas de negocio.
    public function vender(Request $request, Producto $producto): JsonResponse
    {
        $datos = $request->validate([
            'cantidad' => 'required|integer|min:1',
        ]);

        // Regla de negocio: no se puede vender más de lo que hay
        if ($datos['cantidad'] > $producto->stock) {
            throw ValidationException::withMessages([
                'cantidad' => "Solo hay {$producto->stock} unidades disponibles.",
            ]);
        }

        $producto->decrement('stock', $datos['cantidad']);

        return response()->json($producto->fresh());
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
