import sys

from flask.globals import request
from flask.views import View

from toga import platform


class TogaView(View):
    def __init__(self, app_module):
        super().__init__()
        self.app_module = app_module

    def dispatch_request(self, state):
        # Make the Python __main__ context identify as the app being executed.
        sys.modules['__main__'] = self.app_module

        # Set the current platform to be `web`
        platform.current_platform = 'web'

        # Instantiate the app
        app = self.app_module.main()

        # Render the app
        return app._impl.render(
            state=state,
            headers=dict(request.headers)
        )


class App:
    def __init__(self, app_module, name='toga'):
        self.app_module = app_module
        self.name = name

    def route(self, app, path):
        view = TogaView.as_view(self.name, app_module=self.app_module)

        app.add_url_rule(
            '{path}'.format(path=path),
            defaults={'state': ''},
            view_func=view
        )
        app.add_url_rule(
            '{path}<path:state>'.format(path=path),
            view_func=view
        )
