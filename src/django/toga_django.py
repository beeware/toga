import sys

from django.urls import re_path
from django.http import HttpResponse

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


class TogaApp:
    def __init__(self, app_module):
        self.app_module = app_module

    def app(self, request, state):
        # Make the Python __main__ context identify as the app being executed.
        sys.modules['__main__'] = self.app_module

        platform.current_platform = 'web'
        app = self.app_module.main(factory=factory)
        return HttpResponse(
            app._impl.render(
                state=state,
                headers=request.META,
            )
        )

    def get_urls(self):
        urlpatterns = [
            re_path(r'(?P<state>.*)$', self.app, name='app'),
        ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'toga', 'myapp'
