# 01 - Introducción a Flet

## ¿Recuerdas cuando hiciste tu primer print("Hola Mundo")?

Esto es exactamente igual, pero en lugar de imprimir en la consola, vas a mostrar cosas en una ventana visual — y esa misma ventana puede convertirse en una app para celular.

---

## ¿Cómo funciona una app en Flet?

Una app de Flet tiene tres partes fundamentales:

### 1. La función principal `main`
Todo parte de una función llamada `main` que recibe un parámetro llamado `page`. Piensa en `page` como la "hoja en blanco" donde vas a dibujar tu app.

```python
def main(page: ft.Page):
    # Aquí va todo lo que quieres mostrar
    pass
```

### 2. Los widgets
Los widgets son los elementos visuales: textos, botones, imágenes, campos de texto, etc. En Flet, todo lo que ves en pantalla es un widget.

```python
saludo = ft.Text("Hola Mundo")
```

### 3. Agregar a la página
Para que algo aparezca en pantalla, debes agregarlo a la `page`:

```python
page.add(saludo)
```

### 4. Arrancar la app
Al final, le dices a Flet que ejecute tu función `main`:

```python
ft.run(main)
```

---

## Instalación (si no lo has hecho)

```bash
pip install flet
```

---

## Ejercicios en esta carpeta

| Archivo | Descripción |
|---|---|
| `hola_mundo.py` | Tu primera app — texto en pantalla |
| `mi_presentacion.py` | Una tarjeta con tu nombre y carrera |

---

## Cómo correr los ejercicios

```bash
python hola_mundo.py
```

Se abrirá una ventana. Para cerrarla, cierra la ventana o presiona `Ctrl + C` en la terminal.

---

## Reto

Después de correr `hola_mundo.py`, intenta:
1. Cambiar el texto que aparece
2. Cambiar el tamaño del texto (busca el parámetro `size`)
3. Agregar un segundo texto abajo del primero con `page.add(...)`
