# Ruta de Aprendizaje: Flet con Python

Bienvenido a la ruta de aprendizaje de **Flet**, el framework que te permite crear apps para celular, escritorio y web usando **solo Python**.

---

## ¿Qué es Flet?

Flet es una librería de Python que usa **Flutter** por debajo (la tecnología con la que están hechas muchas apps modernas para Android e iOS). La gran ventaja es que **tú no necesitas aprender Flutter ni Dart** — solo Python, que ya conoces.

---

## Ruta del curso

El curso completo tiene **tres etapas**. Este repositorio cubre la tercera, la app móvil, y en los módulos 12 y 13 la conecta con lo que construiste en las dos primeras.

```
  ETAPA 1                    ETAPA 2                    ETAPA 3
  Laravel (web)        ──►   API REST con Laravel ──►   App móvil con Flet
  ─────────────              ────────────────────       ──────────────────
  Rutas, controladores,      Endpoints que responden    Interfaz, navegación,
  modelos, migraciones,      JSON, validación,          formularios... y al
  Eloquent, validación       códigos HTTP, Insomnia     final: ¡consumir TU API!
```

**¿Por qué en este orden?** Cada etapa se apoya en la anterior. Cuando llegues a conectar la app con la API, vas a entender **los dos lados**: si la app muestra un error `422`, sabrás que viene del `$request->validate()` que tú escribiste.

### ¿Qué necesito saber antes de cada parte?

| Módulos | Necesitas saber | Si no lo sabes aún... |
|---|---|---|
| `01` a `10` (Flet) | Python básico y POO | Estos módulos **no dependen de Laravel**: puedes avanzarlos en paralelo con las etapas 1 y 2 |
| `12_consumo_api` | Etapa 2: qué es una API, verbos HTTP, JSON, probar en Insomnia | Trae `servidor_prueba.py` para practicar sin Laravel, pero lo ideal es usar **tu** API |
| `13_autenticacion_api` | Etapa 1 y 2 completas: crear rutas, controladores y validaciones en Laravel | Aquí **tú construyes la API**: sin Laravel no podrás avanzar |

### Un mismo proyecto que crece

La idea es no empezar de cero en cada etapa: es **el mismo sistema**, que va creciendo.

1. En Laravel construyes una **tienda** con productos (web).
2. Le agregas una **API** para que otras aplicaciones puedan usar esos datos.
3. Construyes la **app móvil** que la consume (módulo 12) y le agregas usuarios con inicio de sesión (módulo 13).

> **Proyecto final:** elige tu propio tema (biblioteca, gimnasio, citas médicas, inventario...) y construye las tres capas: **web en Laravel + API + app móvil en Flet**.

---

## ¿Qué voy a aprender?

Sigue las carpetas en orden. Cada una tiene su propio README con explicaciones y ejercicios listos para correr.

| Carpeta | Tema | Lo que vas a hacer |
|---|---|---|
| `01_introduccion` | Primeros pasos | Tu primera app con Flet |
| `02_widgets_basicos` | Widgets | Botones, textos, campos de texto |
| `03_layouts` | Layouts | Organizar elementos en pantalla |
| `04_eventos_estado` | Eventos y estado | Hacer que la app reaccione a acciones |
| `05_oop_con_flet` | POO + Flet | Usar tus clases de Python en la UI |
| `06_navegacion` | Navegación | Moverse entre pantallas |
| `07_formularios_listas` | Formularios y listas | Crear y mostrar datos |
| `08_temas_estilos` | Temas y estilos | Darle diseño a tu app |
| `09_datos_externos` | Datos reales | Conectar con bases de datos |
| `10_app_movil_final` | App final | Empaquetar para Android/iOS |
| `12_consumo_api` | APIs REST | Conectar la app con una API Laravel (CRUD) |
| `13_autenticacion_api` | Autenticación | Construir tu propia API: registro, login y tokens con Laravel Sanctum |

---

## Antes de empezar: Instala Flet

Abre tu terminal y ejecuta:

```bash
pip install flet
```

Para verificar que quedó bien instalado:

```bash
python -m flet --version
```

---

## Como correr cada ejercicio

Desde la terminal, dentro de la carpeta del ejercicio:

```bash
python nombre_del_archivo.py
```

Se abrirá una ventana de escritorio. Cuando llegues a la carpeta `10`, aprenderás a convertirla en APK para Android.

---

## Recuerda

- Lee el README de cada carpeta antes de abrir el código.
- Intenta modificar los ejercicios — cambiar colores, textos, agregar botones.
- Si algo no funciona, revisa que el entorno virtual esté activo.
- Lee [`CONSEJOS.md`](CONSEJOS.md): errores comunes, tutoriales desactualizados, cómo leer un error y cómo pedir ayuda.

¡Comencemos!
