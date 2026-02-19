import web
from supabase import create_client

SUPABASE_URL = "https://relbkuzzsosyzukksdov.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJlbGJrdXp6c29zeXp1a2tzZG92Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMwODA4NDksImV4cCI6MjA3ODY1Njg0OX0.1rxbc9AiaGnc4p7J3AwhJrzfjTctSgs4GwWUZiiP_e0"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

urls = ("/", "Index")
app = web.application(urls, globals())
render = web.template.render("templates/")

class Index:
    def GET(self):
        response = supabase.table("personas").select("*").execute()
        personas = response.data  # Lista de diccionarios
        return render.index({"personas": personas})

if __name__ == "__main__":
    web.config.debug = False
    app.run()
