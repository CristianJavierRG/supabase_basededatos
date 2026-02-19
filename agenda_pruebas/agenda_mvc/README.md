# Agenda MVC (supabase auth)

Esta versión del controlador `insertar` usa Supabase Auth para registrar usuarios con email + password antes de insertar la fila en la tabla `personas`.

Requisitos:
- Archivo `.env` con las variables:
  - SUPABASE_URL
  - SUPABASE_KEY

Cómo funciona la inserción:
- El formulario `/insertar` ahora pide `nombre`, `email` y `password`.
- Al enviar, el servidor intentará primero registrar al usuario en `supabase.auth.sign_up({email, password})`.
- Si la creación en Auth falla (email duplicado, contraseña inválida, etc.), se muestra el error en la misma página de `insertar`.
- Si la creación en Auth es exitosa, se inserta la fila en la tabla `personas` con `nombre` y `email`.

Notas para desarrollo:
- Asegúrate de que tu proyecto tenga las dependencias (`supabase`, `python-dotenv`, `web.py`) instaladas.
- Para probar localmente, define el `.env` con tus credenciales de Supabase y ejecuta `python mvc/main.py`.
