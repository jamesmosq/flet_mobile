# 10 - App Móvil Final: Empaquetando para Android/iOS

## ¡Llegaste al final de la ruta!

Si llegaste hasta aquí, ya sabes:
- Crear interfaces con widgets y layouts
- Manejar eventos y estado
- Aplicar POO para componentes reutilizables
- Navegar entre pantallas
- Hacer CRUD con formularios y listas
- Aplicar temas y diseño
- Conectar con bases de datos SQLite

Ahora vamos a convertir todo eso en una **app real para celular**.

---

## La app final: Gestor de Gastos Personales

En esta carpeta construirás una app completa que combina todo lo que aprendiste:

| Funcionalidad | Concepto aplicado |
|---|---|
| Pantalla de login | Formularios + validación |
| Lista de gastos | ListView + CRUD |
| Agregar gasto | Formulario + SQLite |
| Gráfica de resumen | Contenedores + colores dinámicos |
| Navegación por pestañas | NavigationBar |
| Tema oscuro/claro | ft.Theme |

---

## Paso 1: Verificar que Flet está instalado

```bash
pip install flet
python -m flet --version
```

---

## Paso 2: Correr la app en modo escritorio primero

```bash
python app_gastos.py
```

Siempre desarrolla y prueba en escritorio primero — es mucho más rápido que compilar para celular cada vez.

---

## Paso 3: Probarla en el navegador web

```bash
flet run --web app_gastos.py
```

Abre `http://localhost:8550` en el navegador. Si se ve bien en web, generalmente se verá bien en móvil.

---

## Paso 4: Compilar para Android (APK)

Primero necesitas instalar Flutter y Android SDK. Sigue la guía oficial:
- https://flet.dev/docs/publish/android

Una vez configurado:

```bash
flet build apk
```

El archivo `.apk` quedará en la carpeta `build/apk/`. Puedes enviárselo a tu celular y instalarlo directamente.

---

## Paso 5: Compilar para iOS (solo en Mac)

```bash
flet build ipa
```

---

## Paso 6: Subir a Google Play Store

Para publicar en Play Store necesitas:
1. Una cuenta de desarrollador Google ($25 pago único)
2. Compilar con `flet build aab` (Android App Bundle)
3. Subir el `.aab` a la Play Console

---

## Estructura de la app final

```
10_app_movil_final/
├── app_gastos.py        # Punto de entrada principal
├── db.py                # Repositorio SQLite
├── modelos.py           # Clases de datos (Gasto, Categoria)
├── pantallas/
│   ├── login.py         # Pantalla de login
│   ├── inicio.py        # Resumen de gastos
│   ├── lista_gastos.py  # Lista CRUD de gastos
│   └── ajustes.py       # Configuración
└── gastos.db            # Base de datos (se crea automáticamente)
```

---

## Corre la app final

```bash
python app_gastos.py
```

---

## Checklist antes de compilar para Android

- [ ] La app corre sin errores en escritorio
- [ ] La app se ve bien en ventana pequeña (simula pantalla de celular)
- [ ] Todos los textos son legibles sin acercar
- [ ] Los botones son suficientemente grandes para tocar con el dedo
- [ ] Los campos de texto usan el tipo de teclado correcto (`keyboard_type`)
- [ ] La app no se cuelga si el usuario deja un campo vacío

---

## Recursos para seguir aprendiendo

- Documentación oficial de Flet: https://flet.dev/docs
- Galería de controles: https://flet.dev/gallery
- Ejemplos en GitHub: https://github.com/flet-dev/examples
