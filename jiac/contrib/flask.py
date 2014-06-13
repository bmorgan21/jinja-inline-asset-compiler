class JIAC(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.jinja_env.add_extension('jiac.CompilerExtension')
        app.jinja_env.compiler_enabled = app.config.get('COMPILER_ENABLED', True)
        app.jinja_env.compiler_debug = app.config.get('COMPILER_DEBUG', False)
        app.jinja_env.compiler_include_path = app.config.get('COMPILER_INCLUDE_PATH', [])
