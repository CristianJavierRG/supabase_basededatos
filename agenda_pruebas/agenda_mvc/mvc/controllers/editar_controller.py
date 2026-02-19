import web
from models.persona_model import PersonaModel

render = web.template.render("views/")

class EditarController:
    def GET(self, id):
        resp = PersonaModel.obtener(id)
        return render.editar({"result": resp.data})

    def POST(self, id):
        form = web.input()
        PersonaModel.actualizar(id, {
            "nombre": form.nombre,
            "email": form.email
        })
        return web.seeother("/")
