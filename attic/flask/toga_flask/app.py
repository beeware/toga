import sys

from flask.globals import request
from flask.views import View

from toga import platform


class TogaApp(View):
    def __init__(self, app_module):
        super().__init__()
        self.app_module = app_module

    def dispatch_request(self):
        # Make the Python __main__ context identify as the app being executed.
        sys.modules['__main__'] = self.app_module

        # Set the current platform to be `web`
        platform.current_platform = 'web'

        # Instantiate the app
        app = self.app_module.main()

        # Render the app
        return app._impl.render(
            state={},
            headers=dict(request.headers)
        )
