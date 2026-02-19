import web
from models.persona_model import PersonaModel

render = web.template.render("views/")

class DetalleController:
    def GET(self, id):
        resp = PersonaModel.obtener(id)
        return render.detalle({"result": resp.data})
    