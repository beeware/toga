import base64
import marshal
import os
import py_compile
from django.conf.urls import url
from django.shortcuts import render

from .libs import Window as TogaWindow


def bootstrap(element):
    import toga

    parts = element.dataset.togaClass.split('.')
    bootstrap_method = getattr(toga, 'bootstrap_' + parts[1])
    result = bootstrap_method(element)
    return result


class Window:
    def __init__(self, widget_id=None, title=None):
        self.widget_id = widget_id if widget_id else id(self)
        self._app = None
        self._content = None

        self.title = title

        self.callbacks = {}

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")

        self._app = app
        # app.support_module.__dict__['TogaWindow'] = TogaWindow

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self

        # Assign the widget to the same app as the window.
        self.content.app = self.app

    def materialize(self):
        content = self.content.materialize()

        return TogaWindow(
            widget_id=self.widget_id,
            title=self.title,
            content=content
        )

    def get_urls(self):
        # def wrap(view, cacheable=False):
        #     def wrapper(*args, **kwargs):
        #         return self.admin_view(view, cacheable)(*args, **kwargs)
        #     wrapper.admin_site = self
        #     return update_wrapper(wrapper, view)

        # Admin-site-wide views.
        urlpatterns = [
            url(r'^$', self.home, name='home'),
        ]
        return urlpatterns

    def home(self, request):
        app = self.app.materialize()
        if app.main_window.widget_id == self.widget_id:
            window = app.main_window
        else:
            try:
                window = app.windows[self.widget_id]
            except KeyError:
                raise Exception("Unknown window")

        sourcefile = os.path.join(os.path.dirname(__file__), 'libs.py')
        py_compile.compile(sourcefile)
        with open(os.path.join(
                    os.path.dirname(sourcefile),
                    '__pycache__/%s.cpython-34.pyc' % os.path.splitext(os.path.basename(sourcefile))[0]
                ), 'rb') as compiled:
            toga = base64.encodebytes(compiled.read())

        return render(request, 'toga/window.html', {
            'toga': toga,
            'bootstrap': base64.encodebytes(b'\xee\x0c\r\n00000000' + marshal.dumps(bootstrap.__code__)).strip(),
            'app': app,
            'window': window,
            'callbacks': {
                # 'sample': base64.encodebytes(b'\x08\x1c\xe8VU\x00\x00\x00' + marshal.dumps(sample.__code__)).strip()
                '%s-%s' % (widget, message): base64.encodebytes(b'\xee\x0c\r\n00000000' + marshal.dumps(callback.__code__)).strip()
                for (widget, message), callback in self.callbacks.items()
            }
        })
