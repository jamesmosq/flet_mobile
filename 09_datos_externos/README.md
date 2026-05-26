# 09 - Datos Externos: Conectar la app con datos reales

## ¿Recuerdas la base de datos del curso?

En el curso trabajaste con bases de datos relacionales. Aquí vamos a conectar Flet con SQLite (una base de datos liviana que no necesita servidor) para que los datos persistan entre sesiones.

---

## ¿Qué es SQLite?

SQLite es una base de datos que guarda todo en **un solo archivo** `.db`. Es perfecta para apps de escritorio y móvil porque:
- No necesitas instalar ningún servidor
- El archivo viaja con la app
- Python ya trae el módulo `sqlite3` incluido — no necesitas instalar nada extra

---

## Conexión básica a SQLite en Python

```python
import sqlite3

# Conectar (crea el archivo si no existe)
conexion = sqlite3.connect("mi_app.db")
cursor = conexion.cursor()

# Crear tabla
cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL
    )
""")
conexion.commit()

# Insertar
cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", ("Laptop", 3500000))
conexion.commit()

# Consultar
cursor.execute("SELECT * FROM productos")
filas = cursor.fetchall()

# Cerrar
conexion.close()
```

> **Recuerda:** los `?` en el SQL se reemplazan por los valores de la tupla. Nunca hagas concatenación de strings en SQL — es inseguro (inyección SQL).

---

## Patrón repositorio: separar los datos de la UI

La buena práctica es **separar** el código de base de datos del código de UI. Esto se llama patrón repositorio:

```python
# db.py — Solo maneja la base de datos
class RepositorioProductos:
    def __init__(self, archivo_db: str):
        self.conexion = sqlite3.connect(archivo_db)
        self._crear_tablas()

    def _crear_tablas(self):
        ...

    def obtener_todos(self):
        ...

    def insertar(self, nombre, precio):
        ...

    def eliminar(self, id):
        ...
```

```python
# app.py — Solo maneja la UI, llama al repositorio para los datos
repo = RepositorioProductos("productos.db")

def main(page):
    productos = repo.obtener_todos()
    # Mostrar en la UI...
```

---

## Ejercicios en esta carpeta

| Archivo | Descripción |
|---|---|
| `app_sqlite.py` | App completa con SQLite: CRUD persistente |
| `app_json.py` | Guardar y cargar configuración en JSON |

---

## Reto

En `app_sqlite.py`, agrega una columna "fecha_creacion" que guarde automáticamente cuándo se creó cada registro usando `datetime.now()`.
