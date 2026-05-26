# 02 - Widgets Básicos

## ¿Qué es un widget?

Piensa en los widgets como los **ladrillos** con los que construyes una app. Cada cosa que ves en la pantalla — un botón, un texto, una imagen, una caja de texto — es un widget.

En Flet, todos los widgets empiezan con `ft.` (que es el módulo de Flet). Por ejemplo:
- `ft.Text` → muestra texto
- `ft.ElevatedButton` → un botón con sombra
- `ft.TextField` → una caja donde el usuario escribe
- `ft.Icon` → un ícono de Material Design
- `ft.Image` → una imagen
- `ft.Checkbox` → una casilla de verificación

---

## Los widgets más importantes

### ft.Text — Para mostrar texto

```python
ft.Text(
    value="Hola",       # El texto que muestra
    size=20,            # Tamaño de la fuente
    color=ft.Colors.RED,  # Color del texto
    weight=ft.FontWeight.BOLD  # Negrita
)
```

### ft.ElevatedButton — El botón más común

```python
ft.ElevatedButton(
    text="Haz clic aquí",
    on_click=mi_funcion,  # Función que se llama al hacer clic
    bgcolor=ft.Colors.BLUE,
    color=ft.Colors.WHITE
)
```

> **Recuerda de Python:** `on_click=mi_funcion` le pasa la función como argumento (sin los paréntesis `()`). Es lo mismo que los callbacks que viste en Python.

### ft.TextField — Para que el usuario escriba

```python
ft.TextField(
    label="Escribe tu nombre",  # Texto que aparece como guía
    hint_text="Ej: Juan Pérez",  # Texto de ayuda dentro del campo
    width=300
)
```

### ft.Checkbox — Casilla de verificación

```python
ft.Checkbox(
    label="Acepto los términos",
    value=False  # True = marcado, False = sin marcar
)
```

### ft.Icon — Íconos

```python
ft.Icon(
    name=ft.Icons.STAR,  # Nombre del ícono
    color=ft.Colors.AMBER,
    size=40
)
```

---

## Ejercicios en esta carpeta

| Archivo | Descripción |
|---|---|
| `ejercicio_widgets.py` | Galería de widgets principales |
| `calculadora_simple.py` | Mini calculadora de suma |

---

## Reto

En `calculadora_simple.py`, la app solo suma. Intenta agregar botones para restar, multiplicar y dividir.
