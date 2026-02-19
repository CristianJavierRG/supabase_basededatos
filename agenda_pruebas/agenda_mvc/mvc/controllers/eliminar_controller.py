import web
from models.persona_model import PersonaModel

render = web.template.render("views/")

class EliminarController:
    def GET(self, id):
        resp = PersonaModel.obtener(id)
        return render.eliminar({"result": resp.data})

    def POST(self, id):
        PersonaModel.eliminar(id)
        return web.seeother("/")
