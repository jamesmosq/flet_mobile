# 03 - Layouts: Organizar elementos en pantalla

## ¿Recuerdas las listas en Python?

Cuando guardabas varios elementos en una lista `[a, b, c]`, los tenías organizados en orden. Los layouts en Flet funcionan igual: son **contenedores que organizan widgets**.

---

## ¿Qué es un layout?

Un layout es simplemente un widget que **contiene otros widgets** y los organiza de cierta manera en la pantalla.

---

## Los layouts principales

### ft.Column — Organiza elementos de arriba hacia abajo (vertical)

```python
ft.Column([
    ft.Text("Primero"),   # ← arriba
    ft.Text("Segundo"),   # ← en el medio
    ft.Text("Tercero"),   # ← abajo
])
```

Piénsalo como una **pila vertical** de elementos.

---

### ft.Row — Organiza elementos de izquierda a derecha (horizontal)

```python
ft.Row([
    ft.Text("Izquierda"),
    ft.Text("Centro"),
    ft.Text("Derecha"),
])
```

Piénsalo como una **fila horizontal** de elementos.

---

### ft.Container — Una caja con propiedades visuales

El `Container` es como una caja invisible que puedes decorar: darle color de fondo, bordes redondeados, sombra, margen, etc.

```python
ft.Container(
    content=ft.Text("Estoy dentro de una caja"),
    bgcolor=ft.Colors.BLUE_100,
    padding=20,           # Espacio interior
    border_radius=10,     # Esquinas redondeadas
    width=200,
    height=100
)
```

---

### ft.Stack — Elementos uno encima del otro

```python
ft.Stack([
    ft.Container(bgcolor=ft.Colors.BLUE, width=200, height=200),
    ft.Text("Texto encima del fondo azul", color=ft.Colors.WHITE)
])
```

---

## Cómo combinar layouts (anidación)

La clave para diseñar pantallas complejas es **anidar layouts**, igual que anidas listas en Python:

```python
ft.Column([
    ft.Row([          # Una fila dentro de una columna
        ft.Text("Nombre:"),
        ft.Text("Juan")
    ]),
    ft.Row([
        ft.Text("Edad:"),
        ft.Text("20")
    ])
])
```

---

## Alineación

Tanto `Row` como `Column` tienen parámetros para alinear:

```python
ft.Row(
    controls=[...],
    alignment=ft.MainAxisAlignment.CENTER,         # Horizontal en Row
    vertical_alignment=ft.CrossAxisAlignment.CENTER  # Vertical en Row
)
```

---

## Ejercicios en esta carpeta

| Archivo | Descripción |
|---|---|
| `ejercicio_layouts.py` | Muestra Column, Row, Container y Stack |
| `tarjeta_perfil.py` | Tarjeta de perfil con layouts combinados |

---

## Reto

En `tarjeta_perfil.py`, el perfil tiene información básica. Intenta agregar:
1. Una fila de íconos de redes sociales abajo de la tarjeta
2. Un segundo color de fondo para la mitad superior de la tarjeta (usa Stack)
