<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\Rule;
use Illuminate\Validation\ValidationException;

// NIVEL 1 (mostrar) y NIVEL 2 (actualizar, cambiar contraseña)
// Todas estas rutas están dentro de middleware('auth:sanctum'):
// $request->user() es el dueño del token que envió la app.
class PerfilController extends Controller
{
    // GET /api/perfil
    public function mostrar(Request $request): JsonResponse
    {
        return response()->json($request->user());
    }

    // PUT /api/perfil
    public function actualizar(Request $request): JsonResponse
    {
        $user = $request->user();

        $datos = $request->validate([
            'name'  => 'required|string|max:100',
            // unique, PERO ignorando al propio usuario: si deja su mismo email, no es error
            'email' => ['required', 'email', 'max:255', Rule::unique('users')->ignore($user->id)],
        ]);

        $user->update($datos);

        return response()->json($user);
    }

    // PUT /api/perfil/password
    public function cambiarPassword(Request $request): Response
    {
        $datos = $request->validate([
            'password_actual' => 'required|string',
            'password'        => 'required|string|min:8|confirmed',
        ]);

        $user = $request->user();

        if (! Hash::check($datos['password_actual'], $user->password)) {
            // Lanza un 422 con el error en el campo indicado, igual que validate()
            throw ValidationException::withMessages([
                'password_actual' => 'La contraseña actual no es correcta.',
            ]);
        }

        $user->update(['password' => $datos['password']]);

        // Seguridad: cerramos la sesión en los OTROS dispositivos (menos en este)
        $user->tokens()->where('id', '!=', $user->currentAccessToken()->id)->delete();

        return response()->noContent();
    }
}
