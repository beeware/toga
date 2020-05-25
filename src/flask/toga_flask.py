import sys

from flask.globals import request
from flask.views import View

from toga import platform
from toga_web import factory

# Examples of valid version strings
# __version__ = '1.2.3.dev1'  # Development release 1
# __version__ = '1.2.3a1'     # Alpha Release 1
# __version__ = '1.2.3b1'     # Beta Release 1
# __version__ = '1.2.3rc1'    # RC Release 1
# __version__ = '1.2.3'       # Final Release
# __version__ = '1.2.3.post1' # Post Release 1

__version__ = '0.3.0.dev20'


class TogaView(View):
    def __init__(self, app_module):
        super().__init__()
        self.app_module = app_module

    def dispatch_request(self, state):
        # Make the Python __main__ context identify as the app being executed.
        sys.modules['__main__'] = self.app_module

        platform.current_platform = 'web'
        app = self.app_module.main(factory=factory)
        return app._impl.render(
            state=state,
            headers=dict(request.headers)
        )


class TogaApp:
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
