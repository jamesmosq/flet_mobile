<?php

namespace App\Models;

// use Illuminate\Contracts\Auth\MustVerifyEmail;
use Database\Factories\UserFactory;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Attributes\Hidden;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;

// Es el User.php que trae Laravel 13. Solo cambian 2 líneas:
//   1. use Laravel\Sanctum\HasApiTokens;
//   2. agregar HasApiTokens en la línea "use HasFactory, ..."
// Con eso el usuario puede crear tokens: $user->createToken('nombre')

#[Fillable(['name', 'email', 'password'])]
#[Hidden(['password', 'remember_token'])]   // la contraseña NUNCA sale en el JSON
class User extends Authenticatable
{
    /** @use HasFactory<UserFactory> */
    use HasApiTokens, HasFactory, Notifiable;

    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'email_verified_at' => 'datetime',
            'password' => 'hashed',   // al guardar, Laravel aplica el hash automáticamente
        ];
    }
}
