# 07 - Formularios y Listas: Crear y Mostrar Datos

## La combinación más usada en apps reales

El 80% de las apps que usas en el día a día hacen básicamente esto:
1. Muestran una **lista** de datos (contactos, productos, tareas, mensajes...)
2. Tienen un **formulario** para agregar o editar datos

En esta sección aprenderás ambas cosas y las combinarás para hacer un CRUD completo.

---

## ¿Qué es un CRUD?

CRUD son las 4 operaciones básicas sobre datos:

| Letra | Operación | En español |
|---|---|---|
| **C** | Create | Crear |
| **R** | Read | Leer / Mostrar |
| **U** | Update | Actualizar / Editar |
| **D** | Delete | Eliminar |

Si tu app puede hacer estas 4 cosas, ya tienes la base de casi cualquier sistema.

---

## Widgets para listas

### ft.ListView — Lista con scroll

```python
ft.ListView(
    controls=[
        ft.ListTile(title=ft.Text("Elemento 1")),
        ft.ListTile(title=ft.Text("Elemento 2")),
    ],
    expand=True
)
```

### ft.ListTile — Un ítem de lista estándar

```python
ft.ListTile(
    leading=ft.Icon(ft.Icons.PERSON),   # Ícono a la izquierda
    title=ft.Text("Juan García"),        # Texto principal
    subtitle=ft.Text("juan@email.com"),  # Texto secundario
    trailing=ft.IconButton(ft.Icons.DELETE)  # Botón a la derecha
)
```

### ft.DataTable — Una tabla con filas y columnas

```python
ft.DataTable(
    columns=[
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Edad")),
    ],
    rows=[
        ft.DataRow(cells=[
            ft.DataCell(ft.Text("Ana")),
            ft.DataCell(ft.Text("22")),
        ]),
    ]
)
```

---

## Formularios con validación

Un formulario sin validación es una puerta abierta a errores. Siempre verifica que los datos estén correctos antes de procesarlos.

```python
campo = ft.TextField(label="Nombre")

def guardar(e):
    if not campo.value.strip():
        campo.error_text = "El nombre es obligatorio"
        page.update()
        return
    campo.error_text = None  # Quita el error si estaba
    # ... guardar el dato
    page.update()
```

---

## AlertDialog — Ventana emergente de confirmación

```python
def confirmar_eliminacion(e):
    def confirmar(e):
        dialogo.open = False
        # ... eliminar el elemento
        page.update()

    dialogo = ft.AlertDialog(
        title=ft.Text("¿Estás seguro?"),
        content=ft.Text("Esta acción no se puede deshacer"),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(dialogo, 'open', False) or page.update()),
            ft.ElevatedButton("Eliminar", on_click=confirmar, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)
        ]
    )
    page.dialog = dialogo
    dialogo.open = True
    page.update()
```

---

## Ejercicios en esta carpeta

| Archivo | Descripción |
|---|---|
| `crud_contactos.py` | CRUD completo de contactos (Crear, Ver, Editar, Eliminar) |
| `tabla_estudiantes.py` | Tabla de estudiantes con DataTable |

---

## Reto

En `crud_contactos.py`, agrega una función de **búsqueda** que filtre los contactos mientras el usuario escribe en un campo de búsqueda.
