from config.supabase_cliente import supabase

class PersonaModel:

    @staticmethod
    def obtener_todos():
        return supabase.table("personas").select("*").execute()

    @staticmethod
    def insertar(data):
        return supabase.table("personas").insert(data).execute()

    @staticmethod
    def crear_usuario_auth(email, password):
        """Crea un usuario en el Auth de Supabase mediante email + password.

        Devuelve la respuesta cruda de supabase.auth.sign_up para que el
        controlador pueda manejar errores y sesiones según sea necesario.
        """
        try:
            resp = supabase.auth.sign_up({"email": email, "password": password})
            # unificar formato de retorno: dict con keys user, session, error
            # Algunas versiones de la librería devuelven objetos con atributos.
            if hasattr(resp, 'json'):
                # httpx/requests-like response object
                try:
                    j = resp.json()
                except Exception:
                    j = None
            else:
                j = resp

            # Construir respuesta consistente
            result = {"user": None, "session": None, "error": None}
            if isinstance(j, dict):
                result['user'] = j.get('user')
                result['session'] = j.get('session')
                result['error'] = j.get('error')
            else:
                # si es un objeto con atributos
                result['user'] = getattr(resp, 'user', None)
                result['session'] = getattr(resp, 'session', None)
                result['error'] = getattr(resp, 'error', None)

            return result
        except Exception as e:
            # devolver siempre un dict con la clave 'error' como string para el controlador
            return {"user": None, "session": None, "error": str(e)}

    @staticmethod
    def obtener(id):
        return supabase.table("personas").select("*").eq("id_persona", id).single().execute()

    @staticmethod
    def actualizar(id, data):
        return supabase.table("personas").update(data).eq("id_persona", id).execute()

    @staticmethod
    def eliminar(id):
        return supabase.table("personas").delete().eq("id_persona", id).execute()
