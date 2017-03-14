# import types
import base64
import marshal
import os
import py_compile
import tempfile

from django.conf.urls import url
from django.shortcuts import render
from django.utils.safestring import mark_safe

from toga.interface.app import App as AppInterface
from toga.interface.widgets.base import Widget

from .window import Window
from .bootstrap import bootstrap
from . import impl


class MainWindow(Window):
    pass


class App(AppInterface):
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, name, app_id, icon=None, id=None, startup=None):
        # Set the icon for the app
        # Icon.app_icon = Icon.load(icon, default=TIBERIUS_ICON)
        self.windows = []

        super().__init__(
            name=name,
            app_id=app_id,
            # icon=Icon.app_icon,
            id=id,
            startup=startup,
        )
        self._startup()

    def _startup(self):
        self.startup()

    def main_loop(self):
        pass

    # ====

    # def materialize(self):
    #     app = render.App(self.name, self.app_id, self.ports)
    #     app.main_window = self.main_window.materialize()
    #     for win_id, win in self.windows:
    #         app.windows.append(win.materialize())
    #     return app

    def __str__(self):
        return mark_safe(self.main_window._impl.__html__())

    def get_urls(self):
        urlpatterns = [
            url(r'^$', self.home, name='home'),
        ] + self.main_window.get_urls()
        for win_id, window in self.windows:
            urlpatterns += window.get_urls()
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'toga', self.name

    @property
    def ports(self):
        return ",".join(
            "%s=%s" % (name, widget.id)
            for name, widget in self.__dict__.items()
            if isinstance(widget, Widget)
        )

    def home(self, request):
        # app = self.app.materialize()
        # if app.main_window.id == self.id:
        #     window = app.main_window
        # else:
        #     try:
        #         window = app.windows[self.id]
        #     except KeyError:
        #         raise Exception("Unknown window")
        sourcefile = os.path.join(os.path.dirname(__file__), 'impl', '__init__.py')

        fd, tempname = tempfile.mkstemp()
        py_compile.compile(sourcefile, cfile=tempname, doraise=True)
        with open(os.path.join(os.path.dirname(sourcefile), tempname), 'rb') as compiled:
            toga = base64.encodebytes(compiled.read())

        widgets = {}
        for widget in ["app", "window", "box", "button", "label", "textinput", "webview"]:
            sourcefile = os.path.join(os.path.dirname(__file__), 'impl', "%s.py" % widget)

            fd, tempname = tempfile.mkstemp()
            py_compile.compile(sourcefile, cfile=tempname, doraise=True)
            with open(os.path.join(os.path.dirname(sourcefile), tempname), 'rb') as compiled:
                bytecode = base64.encodebytes(compiled.read())
                widgets['toga.%s' % widget] = {
                    'filename': sourcefile,
                    'bytecode': bytecode,
                }

        context = {
            'toga': toga,
            'widgets': widgets,
            'bootstrap': base64.encodebytes(b'\xee\x0c\r\n00000000' + marshal.dumps(bootstrap.__code__)).strip(),
            'app': self,
            'callbacks': {
                # 'sample': base64.encodebytes(b'\x08\x1c\xe8VU\x00\x00\x00' + marshal.dumps(sample.__code__)).strip()
                '%s-%s' % (widget, message): {
                    'filename': '<string>',
                    'bytecode': base64.encodebytes(b'\xee\x0c\r\n00000000' + marshal.dumps(callback.__code__)).strip()
                }
                for (widget, message), callback in self.main_window.callbacks.items()
            }
        }
        return render(request, 'toga/app.html', context)
