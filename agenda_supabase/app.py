import web
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

urls = (
    '/', 'Index',
    '/insertar', 'Insertar',
    '/detalle/(.*)', 'Detalle',
    '/editar/(.*)', 'Editar',
    '/borrar/(.*)', 'Eliminar',
)

app = web.application(urls, globals())
render = web.template.render("templates/")


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class Index:
    def GET(self):
        response = supabase.table("personas").select("*").execute()
        return render.index({"result": response.data})

class Insertar:
    def GET(self):
        return render.insertar({})

    def POST(self):
        form = web.input()
        response = supabase.table("personas").insert({
            "nombre": form.get('nombre'),
            "email": form.get('email')
        }).execute()

        # Log the raw response so you can see errors in the server output
        print("[DEBUG] Supabase insert response:", response)

        # If supabase client returns an error object, show it in the form
        err = None
        if hasattr(response, 'error') and response.error:
            err = response.error
        elif hasattr(response, 'status_code') and response.status_code not in (200, 201):
            err = f"HTTP status {response.status_code}"

        if err:
            return render.insertar({"error": err})

        return web.seeother("/")

class Detalle:
    def GET(self, id):
        resp = supabase.table("personas").select("*").eq("id_persona", id).single().execute()
        return render.detalle({"result": resp.data})

class Editar:
    def GET(self, id):
        resp = supabase.table("personas").select("*").eq("id_persona", id).single().execute()
        return render.editar({"result": resp.data})

    def POST(self, id):
        form = web.input()
        supabase.table("personas").update({
            "nombre": form.nombre,
            "email": form.email
        }).eq("id_persona", id).execute()
        return web.seeother("/")


class Eliminar:
    def GET(self, id):
        resp = supabase.table("personas").select("*").eq("id_persona", id).single().execute()
        return render.eliminar({"result": resp.data})

    def POST(self, id):
        supabase.table("personas").delete().eq("id_persona", id).execute()
        return web.seeother("/")


application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
