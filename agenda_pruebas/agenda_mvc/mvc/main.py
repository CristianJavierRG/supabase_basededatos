import web

urls = (
    '/', 'controllers.index_controller.IndexController',
    '/insertar', 'controllers.insertar_controller.InsertarController',
    '/detalle/(.*)', 'controllers.detalle_controller.DetalleController',
    '/editar/(.*)', 'controllers.editar_controller.EditarController',
    '/borrar/(.*)', 'controllers.eliminar_controller.EliminarController',
)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
