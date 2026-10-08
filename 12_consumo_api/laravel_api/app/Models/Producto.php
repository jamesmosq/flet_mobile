<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Attributes\Hidden;
use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

// Laravel 13 configura los modelos con ATRIBUTOS de PHP (#[...]) encima de la clase,
// igual que el modelo User que trae el framework.
// (En versiones anteriores se usaban propiedades: protected $fillable = [...])

#[Table('productos')]
// Campos que se pueden llenar con Producto::create($datos) / $producto->update($datos)
#[Fillable(['nombre', 'precio', 'stock'])]
// La app no necesita estas fechas: las ocultamos del JSON
#[Hidden(['created_at', 'updated_at'])]
class Producto extends Model
{
    // Sin este cast, un decimal llega a la app como texto ("3500000.00")
    // y Python no podría formatearlo como número.
    protected function casts(): array
    {
        return [
            'precio' => 'float',
            'stock'  => 'integer',
        ];
    }
}
