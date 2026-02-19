import web
import sqlite3

urls = (
    "/", "Index",
    "/insertar","Insertar",
    "/editar/(.*)","Editar",
    "/detalle/(.*)","Detalle",
    "/borrar/(.*)","Borrar",
    )

render = web.template.render("templates/")
web.template.Template.globals['str'] = str
app = web.application(urls, globals())


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class Index:
    def GET(self):
        connection = None
        try:
            # Intento de conexión a la base de datos (manejo específico para error 3.1)
            try:
                connection = sqlite3.connect("agenda.db")
                cursor = connection.cursor()
            except sqlite3.OperationalError as error:
                print(f"Error de conexión (3.1): {str(error)}")
                return render.index({
                    "personas": [],
                    "error": "Error 3.1: No se pudo conectar con la base de datos"
                })
            except sqlite3.Error as error:
                print(f"Error general de SQLite (3.1): {str(error)}")
                return render.index({
                    "personas": [],
                    "error": "Error 3.1: Problema con la base de datos"
                })

            # Verificar si la tabla existe (error 3.2)
            try:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='personas';")
                if not cursor.fetchone():
                    return render.index({
                        "personas": [],
                        "error": "Error 3.2: La tabla 'personas' no existe"
                    })
            except sqlite3.Error as error:
                print(f"Error al verificar tablas (3.2): {str(error)}")
                return render.index({
                    "personas": [],
                    "error": "Error 3.2: No se puede acceder a la estructura de la base de datos"
                })

            # Consulta de personas (errores 3.3 y 3.4)
            try:
                cursor.execute("SELECT * FROM personas;")
                personas = cursor.fetchall()
                
                if not personas:
                    return render.index({
                        "personas": [],
                        "info": "Info 3.4: La base de datos está vacía"
                    })
                
                return render.index({
                    "personas": personas,
                    "error": None
                })
                
            except sqlite3.Error as error:
                print(f"Error en consulta SQL (3.3): {str(error)}")
                return render.index({
                    "personas": [],
                    "error": f"Error 3.3: Problema en la consulta - {str(error)}"
                })
                
        except Exception as error:
            print(f"Error inesperado: {str(error)}")
            return render.index({
                "personas": [],
                "error": f"Error inesperado: {str(error)}"
            })
        finally:
            if connection:
                connection.close()

class Insertar:
    def GET(self):
        try:
            return render.insertar()
        except Exception as error:
            print(f"Error 001: {error.args[0]}")
            return render.insertar()

    def POST(self):
        try:
            form = web.input()
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            cursor.execute(
                "insert into personas(nombre,email) values (?, ?)",
                (form.nombre, form.email),
            )
            conection.commit()
            conection.close()
            print(f"Inserted: {form.nombre}, {form.email}")
            return web.seeother("/")
        except Exception as error:
            print(f"Error 002: {error.args[0]}")
            raise web.seeother("/")

class Detalle:

    def GET(self,id_persona):
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            sql = "select * from personas where id_persona = ?;"
            datos = (id_persona,)
            personas = cursor.execute(sql,datos)
            
            respuesta={
                "persona" : personas.fetchone(),
                "error": None
            }
            print(f"RESPUESTA: {respuesta}")
            return render.detalle(respuesta)
        except sqlite3.OperationalError as error:
            print(f"Error 004: {error.args[0]}")
            respuesta={
                "persona" : {},
                "error": "Error en la base de datos"
            }
            return render.detalle(respuesta)

class Editar:
    
    def GET(self, id_persona):
        try:
            # Validar ID
            try:
                id_persona_int = int(id_persona)
            except ValueError:
                raise web.notfound("ID inválido")
            
            # Estructura base de respuesta
            respuesta = {
                "persona": None,
                "error": None
            }
            
            connection = sqlite3.connect("agenda.db")
            cursor = connection.cursor()
            
            # Consulta parametrizada
            cursor.execute("SELECT * FROM personas WHERE id_persona = ?", (id_persona_int,))
            persona = cursor.fetchone()
            connection.close()
            
            if persona:
                respuesta["persona"] = persona
            else:
                raise web.notfound("Persona no encontrada")
            
            return render.editar(respuesta)
            
        except web.notfound as e:
            raise e  # Re-lanzar los errores 404
        except Exception as error:
            print(f"Error al obtener datos: {error}")
            respuesta["error"] = "Error al cargar los datos"
            return render.editar(respuesta)


    def POST(self, id_persona):
        connection = None
        try:
            # Validar ID
            if not id_persona.isdigit():
                raise ValueError("ID inválido")
                
            # Obtener datos del formulario
            form = web.input()
            nombre = form.nombre.strip() if 'nombre' in form else ''
            email = form.email.strip() if 'email' in form else ''
            
            # Validaciones básicas
            if not nombre or not email:
                raise ValueError("Nombre y email son requeridos")
                
            if len(nombre) > 50 or len(email) > 50:
                raise ValueError("Los campos no deben exceder 50 caracteres")
            
            connection = sqlite3.connect("agenda.db")
            cursor = connection.cursor()
            
            # Verificar existencia del registro
            cursor.execute("SELECT 1 FROM personas WHERE id_persona = ?", (int(id_persona),))
            if not cursor.fetchone():
                raise ValueError("Registro no existe")
            
            # Actualización segura
            cursor.execute(
                "UPDATE personas SET nombre = ?, email = ? WHERE id_persona = ?",
                (nombre, email, int(id_persona)))
            
            if cursor.rowcount == 0:
                raise ValueError("No se actualizó ningún registro")
            
            connection.commit()
            return web.seeother("/")
            
        except ValueError as error:
            # Recargar los datos para mostrar el formulario con errores
            if connection:
                cursor.execute("SELECT * FROM personas WHERE id_persona = ?", (int(id_persona),))
                persona = cursor.fetchone()
                connection.close()
            else:
                persona = None
                
            respuesta = {
                "persona": persona if persona else [id_persona, nombre or '', email or ''],
                "error": str(error)
            }
            return render.editar(respuesta)
            
        except Exception as error:
            print(f"Error grave: {error}")
            if connection:
                connection.rollback()
                connection.close()
            respuesta = {
                "persona": None,
                "error": "Error interno al procesar la solicitud"
            }
            return render.editar(respuesta)      

class Borrar:

    def GET(self, id_persona):
        try:
            # Validar ID
            try:
                id_persona_int = int(id_persona)
            except ValueError:
                raise web.notfound("ID inválido")
            
            # Estructura base de respuesta
            respuesta = {
                "persona": None,
                "error": None
            }
            
            # Obtener datos de la persona a borrar
            connection = sqlite3.connect("agenda.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM personas WHERE id_persona = ?", (id_persona_int,))
            persona = cursor.fetchone()
            connection.close()
            
            if not persona:
                raise web.notfound("Persona no encontrada")
            
            respuesta["persona"] = persona
            return render.borrar(respuesta)  # Usará tu template borrar.html
            
        except Exception as error:
            print(f"Error al cargar datos para borrar: {error}")
            respuesta["error"] = "Error al cargar datos"
            return render.borrar(respuesta)

    def POST(self, id_persona):
        try:
            # Validar ID
            try:
                id_persona_int = int(id_persona)
            except ValueError:
                raise ValueError("ID inválido")
            
            connection = sqlite3.connect("agenda.db")
            cursor = connection.cursor()
            
            # Verificar que existe antes de borrar
            cursor.execute("SELECT 1 FROM personas WHERE id_persona = ?", (id_persona_int,))
            if not cursor.fetchone():
                raise ValueError("Registro no existe")
            
            # Borrar el registro
            cursor.execute("DELETE FROM personas WHERE id_persona = ?", (id_persona_int,))
            
            if cursor.rowcount == 0:
                raise ValueError("No se eliminó ningún registro")
            
            connection.commit()
            return web.seeother("/")  # Redirigir al listado principal
            
        except Exception as error:
            print(f"Error al borrar: {error}")
            if 'connection' in locals():
                connection.rollback()
            
            # Recargar los datos para mostrar el formulario con error
            respuesta = {
                "persona": None,
                "error": f"No se pudo borrar: {str(error)}"
            }
            
            try:
                if 'connection' not in locals():
                    connection = sqlite3.connect("agenda.db")
                    cursor = connection.cursor()
                
                cursor.execute("SELECT * FROM personas WHERE id_persona = ?", (id_persona_int,))
                respuesta["persona"] = cursor.fetchone()
            except:
                pass
            finally:
                if 'connection' in locals():
                    connection.close()
            
            return render.borrar(respuesta)
        
if __name__ == "__main__":
    app.run()