# 04 - Eventos y Estado

## El concepto más importante de Flet (y de cualquier app)

Hasta ahora las apps que hiciste solo **muestran** información. Pero una app real **reacciona** a lo que hace el usuario: un clic, escribir algo, mover un slider...

Eso se logra con dos conceptos: **eventos** y **estado**.

---

## ¿Qué es un evento?

Un evento es algo que **pasa**: el usuario hizo clic en un botón, escribió en un campo, movió un slider, cerró la app...

En Flet, los eventos se manejan con funciones. Cuando ocurre un evento, Flet llama a tu función automáticamente.

```python
def cuando_hacen_clic(e):
    print("¡Me hicieron clic!")

ft.ElevatedButton(text="Haz clic", on_click=cuando_hacen_clic)
```

> **Recuerda de Python:** esto es exactamente lo mismo que pasarle una función como argumento a otra función (los callbacks que ya viste). `on_click=cuando_hacen_clic` no llama a la función — solo le dice a Flet "cuando pase el clic, llama a esta función".

---

## ¿Qué es el estado?

El estado es la **información actual** de tu app en un momento dado.

Por ejemplo, en un contador:
- El estado es el número actual (0, 1, 2, 3...)
- Cuando el usuario hace clic en "+", el estado cambia (0 → 1)
- La pantalla debe reflejar ese cambio

En Python puro, el estado es simplemente una variable:

```python
contador = 0  # Este es el estado

def incrementar(e):
    global contador   # Recuerda: global para modificar variables fuera de la función
    contador += 1
    texto.value = str(contador)
    page.update()     # Le dices a Flet: "actualiza la pantalla con los nuevos valores"
```

---

## El truco más importante: `page.update()`

**Siempre que cambies el valor de un widget después de que la app ya cargó, debes llamar `page.update()`.**

Sin `page.update()`, el cambio ocurre en memoria pero **no se ve en pantalla**.

```python
texto.value = "Nuevo texto"   # Cambié el valor en memoria
page.update()                 # Ahora SÍ aparece en pantalla
```

---

## Eventos más comunes

| Evento | Cuándo se activa |
|---|---|
| `on_click` | Al hacer clic (botones) |
| `on_change` | Al cambiar el valor (TextField, Checkbox, Slider) |
| `on_submit` | Al presionar Enter en un TextField |
| `on_hover` | Al pasar el mouse encima |

---

## Ejercicios en esta carpeta

| Archivo | Descripción |
|---|---|
| `contador.py` | Contador con botones + y - |
| `semaforo.py` | Semáforo interactivo |
| `formulario_reactivo.py` | Formulario que reacciona mientras escribes |

---

## Reto

En `contador.py`, el contador llega hasta cualquier número. Intenta:
1. Que no pueda bajar de 0
2. Que no pueda subir de 10
3. Que los botones se desactiven cuando lleguen al límite
