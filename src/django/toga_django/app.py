import sys

from django.urls import re_path
from django.http import HttpResponse

from toga import platform
from toga_web import factory


class App:
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
