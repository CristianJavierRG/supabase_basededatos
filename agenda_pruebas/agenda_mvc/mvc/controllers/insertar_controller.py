import web
from models.persona_model import PersonaModel

render = web.template.render("views/")

class InsertarController:
    def GET(self):
        return render.insertar({})

    def POST(self):
        form = web.input()
        nombre = form.get("nombre")
        email = form.get("email")
        password = form.get("password")

        # validaciones básicas en backend para evitar llamadas innecesarias
        if not password or len(password) < 6:
            return render.insertar({"error": "La contraseña debe tener al menos 6 caracteres."})

        # primero intentamos crear el usuario en Auth de Supabase
        auth_resp = PersonaModel.crear_usuario_auth(email, password)

        # normalizar la respuesta en dict y asegurar error como string
        auth_error = None
        if isinstance(auth_resp, dict):
            auth_error = auth_resp.get('error')
        elif hasattr(auth_resp, 'error'):
            auth_error = getattr(auth_resp, 'error')

        if auth_error:
            # asegurar que sea string para evitar problemas al renderizar la plantilla
            return render.insertar({"error": str(auth_error)})

        # si el usuario en Auth se creó correctamente, insertamos en tabla 'personas'
        response = PersonaModel.insertar({
            "nombre": nombre,
            "email": email
        })

        if hasattr(response, 'error') and response.error:
            return render.insertar({"error": response.error})

        return web.seeother("/")
