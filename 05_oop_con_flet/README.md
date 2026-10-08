# 05 - POO con Flet: Tus clases de Python en la UI

## ¿Recuerdas las clases de Python?

En el curso viste que una clase es un "molde" para crear objetos. Por ejemplo:

```python
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        return f"Hola, soy {self.nombre}"
```

En Flet, puedes aplicar exactamente lo mismo para crear **componentes de UI reutilizables**. En lugar de repetir el mismo bloque de código para cada tarjeta o botón, creas una clase y la reutilizas cuantas veces quieras.

---

## El nuevo patrón de componentes en Flet 0.80+

`ft.UserControl` fue **eliminado** en Flet 0.80. Ahora los componentes son **clases Python normales** — sin herencia especial de Flet.

> **La idea de POO es la misma:** atributos, métodos, encapsulación. Solo cambia que ya no heredas de Flet sino que guardas una referencia al widget construido.

```python
class TarjetaProducto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
        self._contenedor = None   # referencia al widget construido

    def _crear_contenido(self):
        return ft.Column([
            ft.Text(self.nombre, size=18, weight=ft.FontWeight.BOLD),
            ft.Text(f"${self.precio}", color=ft.Colors.GREEN)
        ])

    def build(self):
        # build() construye y retorna el widget
        self._contenedor = ft.Container(
            content=self._crear_contenido(),
            border=ft.Border.all(1, ft.Colors.GREY),
            padding=15,
            border_radius=10
        )
        return self._contenedor
```

Para usarlo se llama a `.build()`:

```python
def main(page: ft.Page):
    tarjeta1 = TarjetaProducto("Laptop", 2500000)
    tarjeta2 = TarjetaProducto("Mouse", 80000)
    page.add(tarjeta1.build(), tarjeta2.build())
```

---

## ¿Por qué usar clases para UI?

| Sin clases | Con clases |
|---|---|
| Copias y pegas el mismo código para cada tarjeta | Creas una clase una vez y la instancias N veces |
| Si cambias el diseño, debes cambiarlo en 10 lugares | Si cambias la clase, se actualiza en todos lados |
| Difícil de leer y mantener | Código limpio y organizado |

---

## Actualizarse a uno mismo: `self.update()`

Cuando un componente necesita actualizarse a sí mismo (por ejemplo, al hacer clic en un botón dentro del componente), usa `self.update()` en lugar de `page.update()`.

```python
def al_hacer_clic(self, e):
    self.contador += 1
    self.texto.value = str(self.contador)
    self.update()  # Solo actualiza este componente, no toda la página
```

---

## Ejercicios en esta carpeta

| Archivo | Descripción |
|---|---|
| `tarjeta_producto.py` | Componente TarjetaProducto reutilizable |
| `lista_tareas.py` | App de tareas usando clases para cada ítem |
| `componente_calificacion.py` | Widget de estrellas de calificación |

---

## Reto

En `tarjeta_producto.py`, agrega un botón "Agregar al carrito" dentro del componente. Al hacer clic, el botón debe cambiar a "En el carrito" y cambiar de color.
