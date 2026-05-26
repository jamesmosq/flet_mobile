# 06 - Navegación: Moverse entre pantallas

## ¿Cómo funciona la navegación en una app?

Cuando usas una app en tu celular, puedes ir de la pantalla principal al perfil, de ahí a la configuración, y volver. Eso es navegación.

En Flet tienes dos formas de hacer esto:

---

## Forma 1: Cambiar el contenido de la página (más simple)

La idea es tener una "zona de contenido" en la página que cambia según la pantalla activa. Es como cambiar las diapositivas de una presentación.

```python
contenido = ft.Column()  # Zona de contenido central

def mostrar_inicio(e):
    contenido.controls.clear()
    contenido.controls.append(ft.Text("Pantalla de inicio"))
    page.update()

def mostrar_perfil(e):
    contenido.controls.clear()
    contenido.controls.append(ft.Text("Pantalla de perfil"))
    page.update()
```

---

## Forma 2: Rutas con `page.go()` (más profesional)

Flet tiene un sistema de rutas parecido al de los navegadores web. Cada pantalla tiene una ruta (como una URL).

```python
# Definir qué mostrar en cada ruta
def route_change(e):
    page.views.clear()

    if page.route == "/":
        page.views.append(ft.View("/", controls=[PantallaInicio(page)]))
    elif page.route == "/perfil":
        page.views.append(ft.View("/perfil", controls=[PantallaPerfil(page)]))

    page.update()

page.on_route_change = route_change
page.go("/")  # Ir a la ruta inicial
```

Para navegar a otra pantalla:
```python
page.go("/perfil")
```

Para volver atrás:
```python
page.views.pop()
page.go(page.views[-1].route)
```

---

## NavigationBar — La barra de navegación inferior

Es la barra con íconos en la parte de abajo que ves en la mayoría de apps de celular.

```python
ft.NavigationBar(
    destinations=[
        ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),
        ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Perfil"),
        ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label="Config"),
    ],
    on_change=cambiar_pantalla
)
```

---

## Ejercicios en esta carpeta

| Archivo | Descripción |
|---|---|
| `navegacion_simple.py` | Navegación básica cambiando contenido |
| `navegacion_con_rutas.py` | Navegación profesional con `page.go()` |
| `app_con_navbar.py` | App con barra de navegación inferior (estilo móvil) |

---

## Reto

En `app_con_navbar.py`, agrega una cuarta pantalla de "Notificaciones" con un ícono de campanita y una lista de 3 notificaciones de ejemplo.
