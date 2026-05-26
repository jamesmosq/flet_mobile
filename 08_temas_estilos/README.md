# 08 - Temas y Estilos: Darle diseño a tu app

## ¿Por qué importa el diseño?

Una app que funciona bien pero se ve horrible no va a ser usada. El diseño es parte de la experiencia del usuario. En esta sección aprenderás a darle identidad visual a tu app.

---

## ft.Theme — El sistema de temas de Flet

El tema controla los colores, fuentes y estilos de **toda** la app de forma consistente. Si defines un color primario azul en el tema, todos los botones, barras y elementos de la app van a usar ese azul automáticamente.

```python
page.theme = ft.Theme(
    color_scheme_seed=ft.Colors.BLUE,  # Color semilla — genera toda la paleta
    font_family="Roboto"               # Fuente de toda la app
)
```

---

## Modo oscuro y modo claro

```python
# Activar modo oscuro
page.theme_mode = ft.ThemeMode.DARK

# Activar modo claro
page.theme_mode = ft.ThemeMode.LIGHT

# Seguir la configuración del sistema
page.theme_mode = ft.ThemeMode.SYSTEM
```

---

## Colores en Flet

Flet usa la paleta de Material Design. Los colores tienen variantes numéricas: 100 es muy claro, 900 es muy oscuro.

```python
ft.Colors.BLUE         # Azul estándar
ft.Colors.BLUE_100     # Azul muy claro
ft.Colors.BLUE_900     # Azul muy oscuro
ft.Colors.BLUE_ACCENT  # Azul vibrante/acento
```

También puedes usar colores personalizados en formato hex:
```python
color_personalizado = "#FF5733"
ft.Container(bgcolor=color_personalizado)
```

---

## Diseño responsivo

Una app responsiva se adapta al tamaño de la pantalla. En Flet puedes detectar el tamaño con `page.width` y `page.height`.

```python
def main(page: ft.Page):
    def redimensionar(e):
        if page.width < 600:
            # Vista móvil
            columnas.value = 1
        else:
            # Vista escritorio
            columnas.value = 3
        page.update()

    page.on_resize = redimensionar
```

---

## Gradientes y sombras

```python
# Fondo degradado
ft.Container(
    gradient=ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.bottom_right,
        colors=[ft.Colors.BLUE, ft.Colors.PURPLE]
    )
)

# Sombra
ft.Container(
    shadow=ft.BoxShadow(
        blur_radius=15,
        spread_radius=1,
        color=ft.Colors.BLUE_200,
        offset=ft.Offset(0, 5)
    )
)
```

---

## Ejercicios en esta carpeta

| Archivo | Descripción |
|---|---|
| `tema_oscuro_claro.py` | App con toggle entre modo oscuro y claro |
| `paleta_colores.py` | Explorador de colores de Flet |
| `diseno_responsivo.py` | App que cambia layout según el tamaño de pantalla |

---

## Reto

En `tema_oscuro_claro.py`, agrega la opción de elegir entre 3 colores de tema diferentes (azul, verde, naranja) además del toggle oscuro/claro.
