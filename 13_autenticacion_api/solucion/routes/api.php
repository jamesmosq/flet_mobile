<?php

use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\PerfilController;
use App\Http\Controllers\Api\ProductoController;
use Illuminate\Support\Facades\Route;

// ─── Rutas PÚBLICAS: cualquiera puede llamarlas (todavía no hay token) ───
Route::post('/registro', [AuthController::class, 'registro']);
Route::post('/login', [AuthController::class, 'login']);

// ─── Rutas PROTEGIDAS: exigen el header "Authorization: Bearer <token>" ───
// Sin token (o con uno inválido) Laravel responde 401 automáticamente.
Route::middleware('auth:sanctum')->group(function () {

    // NIVEL 1
    Route::get('/perfil', [PerfilController::class, 'mostrar']);
    Route::post('/logout', [AuthController::class, 'logout']);

    // NIVEL 2
    Route::put('/perfil', [PerfilController::class, 'actualizar']);
    Route::put('/perfil/password', [PerfilController::class, 'cambiarPassword']);

    // NIVEL 3: los productos del módulo 12, ahora protegidos
    Route::apiResource('productos', ProductoController::class)
        ->parameters(['productos' => 'producto']);
    Route::post('/productos/{producto}/vender', [ProductoController::class, 'vender']);
});
