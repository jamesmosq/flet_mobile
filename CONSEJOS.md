# Consejos para el curso

Este documento junta los errores más comunes y los trucos que te ahorran horas. Vuelve a leerlo cada vez que algo "no funciona y no sé por qué".

---

## 1. Antes de empezar: un solo Python

El problema número uno del curso **no es de código**: es tener **varios Python instalados** y que cada herramienta use uno distinto.

**Síntoma:** instalaste Flet, pero al correr la app sale `ModuleNotFoundError: No module named 'flet'`. O el comando `flet` dice una versión y tu código se comporta como otra.

**Solución:** usa un entorno virtual por proyecto.

```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac / Linux
pip install flet httpx
```

Y en **PyCharm**: *Settings → Project → Python Interpreter* → elige el `venv` de tu proyecto.

Para saber qué Python y qué Flet estás usando de verdad:

```bash
python -c "import sys, flet; print(sys.executable); print(flet.__version__)"
```

> **Truco:** usa `python -m pip install ...` en vez de `pip install ...`. Así instalas en **el mismo** Python con el que corres la app.

---

## 2. Flet 0.85: cuidado con los tutoriales viejos

Flet cambió mucho entre versiones. Lo que ves en YouTube, en foros o lo que te sugiere una IA **puede ser de una versión vieja**. Este curso usa **Flet 0.85**:

| Tutoriales viejos | Flet 0.85 (este curso) |
|---|---|
| `ft.app(target=main)` (todavía funciona, pero es obsoleto) | `ft.run(main)` |
| `page.open(dialogo)` / `page.close(dialogo)` | `page.show_dialog(dialogo)` / `page.pop_dialog()` |
| `campo.error_text = "..."` | `campo.error = "..."` |
| `page.snack_bar = ft.SnackBar(...)` | `page.show_dialog(ft.SnackBar(...))` |
| `ft.colors.RED`, `ft.icons.ADD` | `ft.Colors.RED`, `ft.Icons.ADD` (con mayúscula) |

> **El más traicionero:** `campo.error_text = "Obligatorio"` **no da ningún error**. Python lo acepta, pero el mensaje nunca aparece. Si algo "no hace nada", sospecha de un nombre de propiedad viejo.

**¿Cómo verifico si una propiedad existe?**

```python
import flet as ft
print([p for p in dir(ft.TextField()) if "error" in p])
# ['cursor_error_color', 'error', 'error_max_lines', 'error_style']
```

---

## 3. Errores comunes en Flet

### "Cambié el valor pero la pantalla no cambia"
Te faltó `page.update()`. Flet no redibuja solo: cambias las propiedades y luego **avisas** que hay cambios.

```python
contador.value = str(numero)
page.update()   # ← sin esto, no se ve el cambio
```

### "Control must be added to the page first"
Llamaste a `control.update()` antes de agregar el control con `page.add(...)`. Primero se agrega y después se actualiza. Por eso en los ejercicios verás `construir_lista()` **después** de `page.add(lista)`.

### "Todos los botones de la lista borran el último elemento"
Es el error clásico de las `lambda` dentro de un `for`:

```python
# MAL: cuando hagas clic, p ya vale el último producto
for p in productos:
    ft.IconButton(ft.Icons.DELETE, on_click=lambda e: eliminar(p))

# BIEN: prod=p "congela" el valor de cada vuelta
for p in productos:
    ft.IconButton(ft.Icons.DELETE, on_click=lambda e, prod=p: eliminar(prod))
```

### "Un campo del formulario se estira hasta abajo"
`expand=True` significa "ocupa todo el espacio disponible" **en la dirección del contenedor**. En una `Row` se estira a lo ancho (normalmente es lo que quieres). En una `Column` se estira **a lo alto**.

### "El diálogo no se cierra"
En Flet 0.85 se cierra con `page.pop_dialog()`. Revisa que el botón "Cancelar" tenga `on_click`.

---

## 4. Cómo leer un error (traceback)

Cuando Python falla, imprime un bloque largo. **No te asustes: léelo de abajo hacia arriba.**

```
Traceback (most recent call last):
  File ".../flet/...", line 300, in ...            ← código de Flet (ignóralo)
  File "C:/.../mi_app.py", line 42, in guardar     ← ¡TU archivo y TU línea!
    precio = float(campo_precio.value)
ValueError: could not convert string to float: 'abc'   ← QUÉ pasó
```

1. **La última línea** dice qué pasó (`ValueError`, `KeyError`, `AttributeError`...).
2. **Sube** hasta la primera línea que mencione **tu archivo**. Ahí está el problema.
3. Ignora las líneas de `flet/`, `asyncio/`, `httpx/`: son código de las librerías.

| Error | Casi siempre significa |
|---|---|
| `ModuleNotFoundError` | No instalaste la librería en **este** Python (ver sección 1) |
| `AttributeError: ... has no attribute 'x'` | Escribiste mal el nombre, o es de una versión vieja de Flet |
| `KeyError: 'nombre'` | El diccionario no tiene esa clave (¿la API la devuelve con otro nombre?) |
| `TypeError: ... NoneType` | Una variable que creías llena está en `None` |
| `ValueError` al convertir | El usuario escribió texto donde esperabas número: valida antes |

---

## 5. Trucos para trabajar más rápido

- **Recarga automática:** `flet run mi_app.py` reinicia la app cada vez que guardas el archivo. No tienes que cerrarla y abrirla.
- **Pruébala como celular en el navegador:** `flet run --web mi_app.py`, y en Chrome abre las herramientas (F12) → ícono de celular. Así ves cómo se ve en pantalla pequeña.
- **`print()` es tu amigo:** imprime valores para ver qué está pasando. Aparecen en la terminal donde corriste la app.
- **El depurador de PyCharm:** haz clic al lado del número de línea (punto rojo) y corre con el botón **Debug** (el ícono del insecto). La app se detiene ahí y puedes ver el valor de cada variable.
- **Primero en escritorio:** desarrolla y prueba en la PC. Compila el APK solo cuando todo funcione: compilar tarda minutos.

---

## 6. Trabajando con APIs (módulo 12)

1. **Prueba la API en Insomnia ANTES de usarla desde la app.** Si falla en Insomnia, el problema está en Laravel, no en Flet.
2. **`localhost` en el celular es el celular, no tu PC.** Usa `10.0.2.2` en el emulador y la IP de tu PC en un celular real. Arranca Laravel con `php artisan serve --host=0.0.0.0`.
3. **Envía siempre el header `Accept: application/json`.** Sin él, una ruta protegida sin token responde `500 Route [login] not defined` en vez de `401` (y en versiones viejas de Laravel, los errores llegaban como HTML).
4. **Mira el código de estado antes que nada.** 2xx = bien, 404 = no existe, 422 = datos inválidos (lee `errors`), 500 = error en tu PHP (revisa `storage/logs/laravel.log`).
5. **Usa el Monitor de API** de `02_crud_productos.py` para ver qué envía tu app. Más detalle en [`12_consumo_api/GUIA_PRUEBAS.md`](12_consumo_api/GUIA_PRUEBAS.md).

---

## 7. Buenas prácticas de código

- **Separa la UI de los datos.** La pantalla no debería saber si los datos vienen de SQLite o de una API (patrón repositorio, módulos 09 y 12).
- **Valida lo que escribe el usuario.** Nunca confíes en que escribió un número donde pediste un número.
- **Nombres que expliquen:** `campo_precio` es mejor que `tf2`, y `construir_lista()` es mejor que `hacer()`.
- **Funciones cortas.** Si una función ocupa más que la pantalla, probablemente hace demasiadas cosas.
- **No pegues contraseñas, tokens ni URLs privadas en el código.** Usa variables de entorno o un archivo `.env` (que está en `.gitignore`).

---

## 8. Git: guarda tu progreso

```bash
git status                       # ¿qué cambié?
git add archivo.py               # preparar un archivo
git commit -m "Agrego validación al formulario"
git push                         # subir a GitHub
```

- **Haz commits pequeños y seguido.** Si rompes algo, puedes volver atrás.
- **Escribe mensajes que expliquen el porqué:** "Corrijo precio que no se guardaba" es mejor que "cambios".
- **No subas basura:** `__pycache__/`, `venv/`, `.idea/`, `build/` y `.env` ya están en el `.gitignore`.

---

## 9. Usar IA (ChatGPT, Claude, Copilot...) sin hacerte daño

La IA es una excelente ayuda **si la usas para aprender**, no para copiar.

- **Dile la versión:** "Estoy usando **Flet 0.85** y Python 3.12". Si no, te dará código viejo (sección 2).
- **Pídele que te explique**, no solo que te lo resuelva: "¿Por qué este código no muestra el error debajo del campo?".
- **Verifica lo que te da.** Si usa `page.open`, `error_text` o `ft.app`, está desactualizado.
- **Si no entiendes una línea, no la entregues.** En la sustentación te van a preguntar por ella.

---

## 10. Cómo pedir ayuda (al profe, a un compañero o a una IA)

Una buena pregunta se responde en 2 minutos. Una mala, en 20. Incluye:

1. **Qué querías que pasara:** "Al tocar Guardar, el producto debería aparecer en la lista".
2. **Qué pasó en realidad:** "No aparece, y en la terminal sale este error: ...".
3. **El error completo**, copiado como texto (no una foto borrosa de la pantalla).
4. **El pedazo de código** donde crees que está el problema.
5. **Qué ya intentaste.**

---

## Checklist antes de entregar

- [ ] La app abre sin errores en la terminal
- [ ] Probé crear, editar y eliminar, y también los casos con datos inválidos
- [ ] Los formularios muestran mensajes de error claros
- [ ] Si usa API: funciona con el servidor apagado (muestra un mensaje, no se cierra)
- [ ] El código tiene nombres claros y no hay código comentado "de prueba"
- [ ] Hice commit y push de la última versión
- [ ] Puedo explicar cada parte del código
