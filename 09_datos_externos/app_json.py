import flet as ft
import json
import threading
from pathlib import Path

# EJERCICIO: Guardar y cargar configuración en JSON
# JSON es ideal para configuraciones, preferencias del usuario, datos simples

ARCHIVO_CONFIG = Path(__file__).parent / "config.json"

def cargar_config() -> dict:
    """Lee el archivo JSON. Si no existe, retorna la configuración por defecto."""
    if ARCHIVO_CONFIG.exists():
        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "nombre_usuario": "",
        "tema_oscuro": False,
        "color_tema": "BLUE",
        "notificaciones": True,
        "volumen": 70
    }

def guardar_config(config: dict):
    """Escribe el diccionario en el archivo JSON."""
    with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def main(page: ft.Page):
    page.title = "Configuración con JSON"
    page.padding = 25
    page.scroll = ft.ScrollMode.AUTO

    # Cargar la configuración guardada (o la por defecto)
    config = cargar_config()

    # Aplicar tema guardado
    page.theme_mode = ft.ThemeMode.DARK if config["tema_oscuro"] else ft.ThemeMode.LIGHT

    mensaje = ft.Text("", color=ft.Colors.GREEN, size=14)

    def guardar_y_notificar():
        guardar_config(config)
        mensaje.value = "Configuracion guardada correctamente"
        page.update()

    # ─── Widgets vinculados a la configuración ─────────────────────
    campo_nombre = ft.TextField(
        label="Tu nombre",
        value=config["nombre_usuario"],
        width=300
    )

    def al_cambiar_nombre(e):
        config["nombre_usuario"] = campo_nombre.value

    campo_nombre.on_change = al_cambiar_nombre

    switch_oscuro = ft.Switch(
        label="Modo oscuro",
        value=config["tema_oscuro"]
    )

    def al_cambiar_tema(e):
        config["tema_oscuro"] = switch_oscuro.value
        page.theme_mode = ft.ThemeMode.DARK if switch_oscuro.value else ft.ThemeMode.LIGHT
        page.update()

    switch_oscuro.on_change = al_cambiar_tema

    switch_notif = ft.Switch(
        label="Notificaciones",
        value=config["notificaciones"]
    )

    def al_cambiar_notif(e):
        config["notificaciones"] = switch_notif.value

    switch_notif.on_change = al_cambiar_notif

    slider_volumen = ft.Slider(
        min=0, max=100,
        value=config["volumen"],
        label="Volumen: {value}%",
        width=300
    )

    def al_cambiar_volumen(e):
        config["volumen"] = int(slider_volumen.value)

    slider_volumen.on_change = al_cambiar_volumen

    def guardar_todo(e):
        config["nombre_usuario"] = campo_nombre.value
        guardar_y_notificar()
        # Limpiar el campo nombre después de guardar
        campo_nombre.value = ""
        page.update()
        # Borrar el mensaje de éxito luego de 3 segundos
        def limpiar_mensaje():
            import time
            time.sleep(3)
            mensaje.value = ""
            page.update()
        threading.Thread(target=limpiar_mensaje, daemon=True).start()

    page.add(
        ft.Text("Configuracion de la App", size=28, weight=ft.FontWeight.BOLD),
        ft.Text(f"Archivo: {ARCHIVO_CONFIG}", size=11, color=ft.Colors.GREY, italic=True),
        ft.Divider(),
        ft.Text("Perfil", size=16, weight=ft.FontWeight.BOLD),
        campo_nombre,
        ft.Divider(),
        ft.Text("Apariencia", size=16, weight=ft.FontWeight.BOLD),
        switch_oscuro,
        ft.Divider(),
        ft.Text("Preferencias", size=16, weight=ft.FontWeight.BOLD),
        switch_notif,
        ft.Text("Volumen del sistema:"),
        slider_volumen,
        ft.Divider(),
        ft.FilledButton(
            "Guardar configuracion",
            icon=ft.Icons.SAVE,
            on_click=guardar_todo,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE
        ),
        mensaje,
        ft.Text(
            "Cierra y vuelve a abrir la app — tus ajustes estarán guardados.",
            size=12, color=ft.Colors.GREY, italic=True
        )
    )


ft.run(main)
