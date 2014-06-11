class JIAC(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.jinja_env.add_extension('jac.CompilerExtension')
        app.jinja_env.compressor_enabled = app.config.get('COMPRESSOR_ENABLED', True)
        app.jinja_env.compressor_debug = app.config.get('COMPRESSOR_DEBUG', False)
