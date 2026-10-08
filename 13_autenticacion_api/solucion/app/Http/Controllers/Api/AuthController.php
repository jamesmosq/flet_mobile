<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Hash;

// NIVEL 1: Autenticación
// Crear con: php artisan make:controller Api/AuthController
class AuthController extends Controller
{
    // POST /api/registro  → crea el usuario y le entrega su primer token (201)
    public function registro(Request $request): JsonResponse
    {
        $datos = $request->validate([
            'name'     => 'required|string|max:100',
            'email'    => 'required|email|max:255|unique:users',   // no puede repetirse
            'password' => 'required|string|min:8|confirmed',       // exige password_confirmation
        ]);

        // No hace falta Hash::make(): el cast 'password' => 'hashed' del modelo lo hace solo
        $user = User::create($datos);

        return response()->json([
            'user'  => $user,
            'token' => $user->createToken('app-movil')->plainTextToken,
        ], 201);
    }

    // POST /api/login  → verifica las credenciales y entrega un token nuevo (200)
    public function login(Request $request): JsonResponse
    {
        $datos = $request->validate([
            'email'    => 'required|email',
            'password' => 'required|string',
        ]);

        $user = User::where('email', $datos['email'])->first();

        // Hash::check compara la clave escrita con el hash guardado en la BD.
        // Mismo mensaje si el email no existe o la clave está mal: así un atacante
        // no puede averiguar qué emails están registrados.
        if (! $user || ! Hash::check($datos['password'], $user->password)) {
            return response()->json(['message' => 'Email o contraseña incorrectos.'], 401);
        }

        return response()->json([
            'user'  => $user,
            'token' => $user->createToken('app-movil')->plainTextToken,
        ]);
    }

    // POST /api/logout  → borra el token con el que se hizo esta petición (204)
    public function logout(Request $request): Response
    {
        $request->user()->currentAccessToken()->delete();

        return response()->noContent();
    }
}
