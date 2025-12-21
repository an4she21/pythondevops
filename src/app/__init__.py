from flask import Flask
import sys
import importlib


def create_app():
    app = Flask(__name__)
    with app.app_context():
        # Force reload modules to ensure routes are registered to this app instance
        # This is necessary because Python caches imports, and we need routes
        # to be registered to each new app instance
        module_names = ['app.views', 'app.apis']
        for module_name in module_names:
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
            else:
                # Import for the first time
                if module_name == 'app.views':
                    from . import views  # noqa: E402,F401
                elif module_name == 'app.apis':
                    from . import apis  # noqa: E402,F401
    return app
