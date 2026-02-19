import web
import os
from supabase import create_client, Client

url: str = os.environ.get("https://bytmchkehqehpggbxjhq.supabase.co")
key: str = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ5dG1jaGtlaHFlaHBnZ2J4amhxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMxMzM4NDcsImV4cCI6MjA3ODcwOTg0N30.JbONN9pNSbMlqCxcSbiBknEoFzrbyS87y6Y2kEnHDU0")

supabase: Client = create_client(url, key)

urls = (
    "/", "Index",
    "/insertar","Insertar",
    )

render = web.template.render("templates/")
web.template.Template.globals['str'] = str
app = web.application(urls, globals())

class Index:
    def GET(self):
        respuesta_db = supabase.table("personas").select("*").execute()
        personas = respuesta_db.data
        return render.Index(personas)
         
if __name__ == "__main__":
    app.run()