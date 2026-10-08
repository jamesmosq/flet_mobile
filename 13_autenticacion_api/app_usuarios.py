import flet as ft
from api_cliente import ApiCliente, ErrorApi
from monitor_api import MonitorApi

# APP: Mi Tienda — registro, login, perfil y ventas
#
# ESTA APP YA ESTÁ TERMINADA. Tu trabajo es construir en Laravel la API que ella espera.
# Lee RETO.md: ahí está el contrato (qué endpoints, qué reciben y qué responden).
#
# Debajo de cada botón verás qué endpoint llama, ej: "POST /api/login".
# Mientras no exista en Laravel, el Monitor de API mostrará 404; cuando lo construyas, 200.
#
# Pantallas (navegación del módulo 06: cambiamos el contenido central):
#   login → registro → inicio (productos) → perfil


def main(page: ft.Page):
    page.title = "Mi Tienda"
    page.padding = 0

    api = ApiCliente()
    monitor = MonitorApi(alto=200)  # más bajo: los formularios necesitan espacio
    api.observadores.append(monitor.agregar)

    contenido = ft.Container(expand=True)

    # ─── Utilidades ───────────────────────────────────────────────
    def mostrar_mensaje(texto: str, error: bool = False):
        page.show_dialog(ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=ft.Colors.RED_700 if error else ft.Colors.GREEN_700
        ))

    def manejar_error(ex: ErrorApi, campos: dict | None = None):
        """
        Muestra el error donde corresponde:
          - 422 → debajo de cada campo (los errores de validación de Laravel)
          - 401 con sesión iniciada → el token ya no sirve: volver al login
          - otro → mensaje en la parte de abajo
        """
        campos = campos or {}
        if ex.errores:
            for nombre_campo, mensajes in ex.errores.items():
                if nombre_campo in campos:
                    campos[nombre_campo].error = mensajes[0]
                else:
                    mostrar_mensaje(mensajes[0], error=True)
            page.update()
        elif ex.estado == 401 and api.token:
            api.token = None
            navegar("login")
            mostrar_mensaje(ex.mensaje, error=True)
        else:
            mostrar_mensaje(ex.mensaje, error=True)

    def limpiar_errores(campos: dict):
        for campo in campos.values():
            campo.error = None

    def pista(endpoint: str) -> ft.Text:
        """Texto pequeño que le dice al estudiante qué endpoint usa cada botón."""
        return ft.Text(f"Llama a: {endpoint}", size=11, color=ft.Colors.GREY_500,
                       font_family="Consolas")

    def campo(label: str, icono, password: bool = False, valor: str = "", **kw) -> ft.TextField:
        return ft.TextField(label=label, prefix_icon=icono, value=valor, width=320,
                            password=password, can_reveal_password=password, **kw)

    def formulario(controles: list) -> ft.Container:
        """Centra un formulario en la pantalla (con scroll si no cabe)."""
        return ft.Container(
            content=ft.Column(controles, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                              spacing=12, scroll=ft.ScrollMode.AUTO),
            alignment=ft.Alignment(0, -0.5),
            padding=20,
            expand=True,
        )

    # ─── PANTALLA: Login (NIVEL 1) ────────────────────────────────
    def pantalla_login():
        email = campo("Email", ft.Icons.EMAIL, keyboard_type=ft.KeyboardType.EMAIL, autofocus=True)
        clave = campo("Contraseña", ft.Icons.LOCK, password=True)
        campos = {"email": email, "password": clave}

        def entrar(e):
            limpiar_errores(campos)
            try:
                usuario = api.login(email.value.strip(), clave.value)
            except ErrorApi as ex:
                manejar_error(ex, campos)
                return
            navegar("inicio")
            mostrar_mensaje(f"¡Hola, {usuario['name']}!")

        clave.on_submit = entrar  # Enter en la contraseña = clic en Entrar

        return formulario([
            ft.Icon(ft.Icons.STOREFRONT, size=70, color=ft.Colors.INDIGO),
            ft.Text("Iniciar sesión", size=26, weight=ft.FontWeight.BOLD),
            email, clave,
            ft.FilledButton("Entrar", icon=ft.Icons.LOGIN, width=320, on_click=entrar),
            pista("POST /api/login"),
            ft.TextButton("¿No tienes cuenta? Regístrate", on_click=lambda e: navegar("registro")),
        ])

    # ─── PANTALLA: Registro (NIVEL 1) ─────────────────────────────
    def pantalla_registro():
        nombre = campo("Nombre", ft.Icons.PERSON, autofocus=True)
        email = campo("Email", ft.Icons.EMAIL, keyboard_type=ft.KeyboardType.EMAIL)
        clave = campo("Contraseña (mínimo 8)", ft.Icons.LOCK, password=True)
        confirmar = campo("Confirmar contraseña", ft.Icons.LOCK_OUTLINE, password=True)
        # Las claves son los nombres de los campos que espera Laravel
        campos = {"name": nombre, "email": email,
                  "password": clave, "password_confirmation": confirmar}

        def registrarse(e):
            limpiar_errores(campos)
            try:
                usuario = api.registrar(nombre.value.strip(), email.value.strip(),
                                        clave.value, confirmar.value)
            except ErrorApi as ex:
                manejar_error(ex, campos)
                return
            navegar("inicio")
            mostrar_mensaje(f"Cuenta creada. ¡Bienvenido/a, {usuario['name']}!")

        return formulario([
            ft.Icon(ft.Icons.PERSON_ADD, size=70, color=ft.Colors.INDIGO),
            ft.Text("Crear cuenta", size=26, weight=ft.FontWeight.BOLD),
            nombre, email, clave, confirmar,
            ft.FilledButton("Registrarme", icon=ft.Icons.CHECK, width=320, on_click=registrarse),
            pista("POST /api/registro"),
            ft.TextButton("Ya tengo cuenta", on_click=lambda e: navegar("login")),
        ])

    # ─── PANTALLA: Inicio con productos (NIVEL 3) ─────────────────
    def pantalla_inicio():
        lista = ft.ListView(expand=True, spacing=5, padding=ft.Padding(15, 0, 15, 15))

        def cargar_productos():
            lista.controls.clear()
            try:
                productos = api.productos()
            except ErrorApi as ex:
                if ex.estado == 401:
                    manejar_error(ex)
                    return
                lista.controls.append(ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.INVENTORY_2, size=50, color=ft.Colors.GREY_400),
                        ft.Text("No se pudieron cargar los productos", weight=ft.FontWeight.BOLD),
                        ft.Text(ex.mensaje, color=ft.Colors.GREY, text_align=ft.TextAlign.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=30, alignment=ft.Alignment(0, 0),
                ))
                page.update()
                return

            for p in productos:
                lista.controls.append(ft.ListTile(
                    leading=ft.CircleAvatar(content=ft.Text(p["nombre"][0].upper()),
                                            bgcolor=ft.Colors.INDIGO),
                    title=ft.Text(p["nombre"], weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"${p['precio']:,.0f}  |  Stock: {p['stock']}",
                                     color=ft.Colors.RED if p["stock"] == 0 else None),
                    trailing=ft.FilledButton(
                        "Vender", icon=ft.Icons.SHOPPING_CART,
                        disabled=p["stock"] == 0,
                        on_click=lambda e, prod=p: abrir_venta(prod)
                    ),
                ))
            if not productos:
                lista.controls.append(ft.Text("No hay productos.", color=ft.Colors.GREY))
            page.update()

        def abrir_venta(producto):
            cantidad = ft.TextField(label="Cantidad", value="1", width=280, autofocus=True,
                                    keyboard_type=ft.KeyboardType.NUMBER)

            def vender(e):
                cantidad.error = None
                try:
                    n = int(cantidad.value)
                except ValueError:
                    cantidad.error = "Debe ser un número entero"
                    page.update()
                    return
                try:
                    actualizado = api.vender(producto["id"], n)
                except ErrorApi as ex:
                    if ex.errores:
                        manejar_error(ex, {"cantidad": cantidad})
                    else:
                        page.pop_dialog()
                        manejar_error(ex)
                    return
                page.pop_dialog()
                mostrar_mensaje(f"Vendiste {n} × {producto['nombre']}. "
                                f"Quedan {actualizado['stock']}.")
                cargar_productos()

            page.show_dialog(ft.AlertDialog(
                title=ft.Text(f"Vender {producto['nombre']}"),
                content=ft.Column([
                    ft.Text(f"Disponibles: {producto['stock']}"),
                    cantidad,
                    pista(f"POST /api/productos/{producto['id']}/vender"),
                ], tight=True, spacing=10),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
                    ft.FilledButton("Vender", on_click=vender),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            ))

        vista = ft.Column([
            ft.Container(
                ft.Row([ft.Text("Productos", size=20, weight=ft.FontWeight.BOLD),
                        pista("GET /api/productos")],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.Padding(15, 15, 15, 5),
            ),
            lista,
        ], expand=True, spacing=0)

        # Cargamos la lista justo después de mostrar la pantalla
        return vista, cargar_productos

    # ─── PANTALLA: Mi perfil (NIVEL 1: ver | NIVEL 2: editar) ─────
    def pantalla_perfil():
        nombre = campo("Nombre", ft.Icons.PERSON)
        email = campo("Email", ft.Icons.EMAIL, keyboard_type=ft.KeyboardType.EMAIL)
        datos = {"name": nombre, "email": email}

        actual = campo("Contraseña actual", ft.Icons.LOCK_CLOCK, password=True)
        nueva = campo("Nueva contraseña", ft.Icons.LOCK, password=True)
        confirmar = campo("Confirmar nueva contraseña", ft.Icons.LOCK_OUTLINE, password=True)
        claves = {"password_actual": actual, "password": nueva,
                  "password_confirmation": confirmar}

        def cargar_perfil():
            # GET /api/perfil: pedimos los datos frescos al servidor
            try:
                usuario = api.perfil()
            except ErrorApi as ex:
                manejar_error(ex)
                return
            nombre.value = usuario["name"]
            email.value = usuario["email"]
            page.update()

        def guardar_datos(e):
            limpiar_errores(datos)
            try:
                api.actualizar_perfil(nombre.value.strip(), email.value.strip())
            except ErrorApi as ex:
                manejar_error(ex, datos)
                return
            page.appbar.title.value = f"Hola, {api.usuario['name']}"
            page.update()
            mostrar_mensaje("Datos actualizados")

        def cambiar_clave(e):
            limpiar_errores(claves)
            try:
                api.cambiar_password(actual.value, nueva.value, confirmar.value)
            except ErrorApi as ex:
                manejar_error(ex, claves)
                return
            for c in claves.values():
                c.value = ""
            page.update()
            mostrar_mensaje("Contraseña cambiada")

        vista = formulario([
            ft.Text("Mis datos", size=20, weight=ft.FontWeight.BOLD),
            pista("GET /api/perfil"),
            nombre, email,
            ft.FilledButton("Guardar cambios", icon=ft.Icons.SAVE, width=320,
                            on_click=guardar_datos),
            pista("PUT /api/perfil"),
            ft.Divider(height=30),
            ft.Text("Cambiar contraseña", size=20, weight=ft.FontWeight.BOLD),
            actual, nueva, confirmar,
            ft.FilledButton("Cambiar contraseña", icon=ft.Icons.KEY, width=320,
                            on_click=cambiar_clave),
            pista("PUT /api/perfil/password"),
        ])
        return vista, cargar_perfil

    # ─── Cerrar sesión (NIVEL 1) ──────────────────────────────────
    def cerrar_sesion(e):
        try:
            api.logout()   # POST /api/logout (el token se olvida pase lo que pase)
        except ErrorApi:
            pass
        navegar("login")
        mostrar_mensaje("Sesión cerrada")

    # ─── Navegación ───────────────────────────────────────────────
    def mostrar_ocultar_monitor(e):
        monitor.visible = not monitor.visible
        page.update()

    boton_monitor = ft.IconButton(ft.Icons.TERMINAL, icon_color=ft.Colors.WHITE,
                                  tooltip="Monitor de API", on_click=mostrar_ocultar_monitor)

    def barra(titulo: str, acciones: list | None = None, volver: str | None = None):
        return ft.AppBar(
            title=ft.Text(titulo, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.INDIGO,
            leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color=ft.Colors.WHITE,
                                  on_click=lambda e: navegar(volver)) if volver else None,
            actions=(acciones or []) + [boton_monitor],
        )

    def navegar(nombre: str):
        al_mostrar = None

        if nombre == "login":
            page.appbar = barra("Mi Tienda")
            contenido.content = pantalla_login()
        elif nombre == "registro":
            page.appbar = barra("Mi Tienda", volver="login")
            contenido.content = pantalla_registro()
        elif nombre == "inicio":
            vista, al_mostrar = pantalla_inicio()
            page.appbar = barra(f"Hola, {api.usuario['name']}", acciones=[
                ft.IconButton(ft.Icons.REFRESH, icon_color=ft.Colors.WHITE, tooltip="Recargar",
                              on_click=lambda e: al_mostrar()),
                ft.PopupMenuButton(icon=ft.Icons.ACCOUNT_CIRCLE, icon_color=ft.Colors.WHITE, items=[
                    ft.PopupMenuItem(content="Mi perfil", icon=ft.Icons.PERSON,
                                     on_click=lambda e: navegar("perfil")),
                    ft.PopupMenuItem(content="Cerrar sesión", icon=ft.Icons.LOGOUT,
                                     on_click=cerrar_sesion),
                ]),
            ])
            contenido.content = vista
        elif nombre == "perfil":
            vista, al_mostrar = pantalla_perfil()
            page.appbar = barra("Mi perfil", volver="inicio")
            contenido.content = vista

        page.update()
        if al_mostrar:
            al_mostrar()   # pedir los datos a la API una vez que la pantalla ya se ve

    page.on_close = lambda e: api.cerrar()

    page.add(contenido, monitor)
    navegar("login")


ft.run(main)
