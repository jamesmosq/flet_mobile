<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Producto extends Model
{
    protected $table = 'productos';

    // Campos que se pueden llenar con Producto::create($datos) / $producto->update($datos)
    protected $fillable = ['nombre', 'precio', 'stock'];

    // Sin este cast, un decimal llega a la app como texto ("3500000.00")
    // y Python no podría formatearlo como número.
    protected $casts = [
        'precio' => 'float',
        'stock'  => 'integer',
    ];

    // La app no necesita estas fechas: las ocultamos del JSON
    protected $hidden = ['created_at', 'updated_at'];
}
