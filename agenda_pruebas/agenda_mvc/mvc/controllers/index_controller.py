import web
from models.persona_model import PersonaModel

render = web.template.render("views/")

class IndexController:
    def GET(self):
        result = PersonaModel.obtener_todos()
        return render.index({"result": result.data})
