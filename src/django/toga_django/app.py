# import types

from .window import Window
from .widgets.base import Widget
from .libs import App as TogaApp


class App:
    def __init__(self, name, app_id, icon=None, startup=None):
        self.name = name
        self.app_id = app_id
        self.widget_id = app_id

        # Set the icon for the app
        # Icon.app_icon = Icon.load(icon, default=TIBERIUS_ICON)
        # self.icon = Icon.app_icon

        self._startup_method = startup
        self._startup()

    def _startup(self):
        # self.support_module = types.ModuleType('app')
        # self.support_module.__dict__['TogaApp'] = TogaApp

        self.main_window = Window()
        self.main_window.app = self

        self.windows = {}

        # Call the user code to populate the main window
        self.startup()

    def startup(self):
        if self._startup_method:
            self.main_window.content = self._startup_method(self)

    def materialize(self):
        app = TogaApp(self.name, self.app_id, self.ports)
        app.main_window = self.main_window.materialize()
        for win_id, win in self.windows:
            app.windows.append(win.materialize())
        return app

    def get_urls(self):
        urlpatterns = self.main_window.get_urls()
        for win_id, window in self.windows:
            urlpatterns += window.get_urls()
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'toga', self.name

    @property
    def ports(self):
        return {
            name: widget.widget_id
            for name, widget in self.__dict__.items()
            if isinstance(widget, Widget)
        }
