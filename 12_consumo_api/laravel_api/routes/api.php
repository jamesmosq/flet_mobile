<?php

use App\Http\Controllers\Api\ProductoController;
use Illuminate\Support\Facades\Route;

// Todas las rutas de este archivo llevan el prefijo /api automáticamente.
//
// apiResource crea las 5 rutas del CRUD de una sola vez:
//   GET     /api/productos              → index
//   POST    /api/productos              → store
//   GET     /api/productos/{producto}   → show
//   PUT     /api/productos/{producto}   → update
//   DELETE  /api/productos/{producto}   → destroy
//
// Compruébalo con: php artisan route:list --path=api
Route::apiResource('productos', ProductoController::class)
    ->parameters(['productos' => 'producto']);
