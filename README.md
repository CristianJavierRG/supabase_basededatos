# Agenda con Supabase y web.py

Aplicación sencilla de gestión de personas construida con `web.py` y cliente de Supabase (Base de datos estilo PostgreSQL/MySQL en Supabase). Permite listar, insertar, editar, ver detalle y eliminar registros de la tabla `personas`.

**Descripción**
- **Qué hace:** Aplicación CRUD (Crear, Leer, Actualizar, Eliminar) que gestiona contactos (nombre y email) usando Supabase como backend de datos y `web.py` como framework web ligero.
- **Caso de uso:** Proyecto de ejemplo y plantilla para integrar Supabase con aplicaciones Python sencillas.

**Tecnologías**
- **Lenguaje:** Python 3
- **Framework web:** web.py
- **Base de datos:** Supabase (cliente oficial de Python)
- **Plantillas:** Módulo de templates de `web.py` (carpeta `agenda_supabase/templates`)
- **Dependencias:** Ver [requirements.txt](requirements.txt)

**Instalación y ejecución**
- **Clonar repo:**

```bash
git clone https://github.com/CristianJavierRG/supabase_basededatos.git
cd supabase_basededatos
```

- **Crear entorno virtual e instalar dependencias:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- **Variables de entorno:** Crear un archivo `.env` en la raíz o exportar las variables necesarias:

```
SUPABASE_URL=<tu_supabase_url>
SUPABASE_KEY=<tu_supabase_anon_or_service_key>
```

- **Ejecutar la aplicación:**

```bash
python agenda_supabase/app.py
```

- **Acceder en el navegador:** http://localhost:8080

**Esquema esperado (tabla `personas`)**
- Las operaciones del proyecto usan la tabla `personas` con (al menos) las siguientes columnas:
	- `id_persona` (clave primaria)
	- `nombre` (texto)
	- `email` (texto)

Si necesitas, crea la tabla en tu proyecto Supabase con un SQL similar al siguiente:

```sql
create table if not exists personas (
	id_persona serial primary key,
	nombre text,
	email text
);
```

**Endpoints**
- **GET /** : Lista todos los registros (pagina principal).
- **GET /insertar** : Formulario para crear una nueva persona.
- **POST /insertar** : Inserta la nueva persona en Supabase.
- **GET /detalle/<id>** : Muestra el detalle de la persona identificada por `id_persona`.
- **GET /editar/<id>** : Formulario para editar la persona.
- **POST /editar/<id>** : Actualiza la persona en Supabase.
- **GET /borrar/<id>** : Muestra confirmación de borrado.
- **POST /borrar/<id>** : Elimina la persona de la tabla.

Los endpoints están implementados en [agenda_supabase/app.py](agenda_supabase/app.py).

**Estructura del proyecto**
- **Carpeta principal de interés:** [agenda_supabase](agenda_supabase)
- **Archivo principal:** [agenda_supabase/app.py](agenda_supabase/app.py)
- **Templates:** [agenda_supabase/templates](agenda_supabase/templates)
- **Dependencias:** [requirements.txt](requirements.txt)

**Depuración y notas**
- El cliente Supabase devuelve respuestas que pueden incluir `error` o `status_code`; el código actual intenta detectar y mostrar errores sencillos en el formulario de inserción (ver `agenda_supabase/app.py`).
- Para ver mensajes de depuración, observa la salida del servidor donde se imprimen respuestas crudas del cliente Supabase.

**Autor**
- Cristian Javier (repositorio: CristianJavierRG/supabase_basededatos)

---
