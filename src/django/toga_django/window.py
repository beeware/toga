from toga.interface.window import Window as WindowInterface

import base64
import marshal
import os
import py_compile
from django.conf.urls import url
from django.shortcuts import render
from django.utils.safestring import mark_safe

from . import impl
from . import dialogs
from .bootstrap import bootstrap
from .container import Container


class Window(WindowInterface):
    _IMPL_CLASS = impl.Window
    _CONTAINER_CLASS = Container
    _DIALOG_MODULE = dialogs

    def __init__(self, title=None, position=(100, 100), size=(640, 480), toolbar=None, resizeable=True, closeable=True, minimizable=True):
        super().__init__(title=title, position=position, size=size, toolbar=toolbar, resizeable=resizeable, closeable=closeable, minimizable=minimizable)
        self.id = id(self)
        self.callbacks = {}

        self._create()

    def create(self):
        self._impl = impl.Window(
            id=self.id,
            title=self._config['title']
        )

    def _set_toolbar(self, items):
        pass

    def _set_content(self, widget):
        self._impl.set_content(widget._impl)

    def _set_title(self, title):
        # self._impl.set_title(title)
        pass

    def __str__(self):
        return mark_safe(self._impl.__html__())

    def get_urls(self):
        # def wrap(view, cacheable=False):
        #     def wrapper(*args, **kwargs):
        #         return self.admin_view(view, cacheable)(*args, **kwargs)
        #     wrapper.admin_site = self
        #     return update_wrapper(wrapper, view)

        # Admin-site-wide views.
        urlpatterns = [
        ]
        return urlpatterns

    def show(self):
        pass

    def home(self, request):
        # app = self.app.materialize()
        # if app.main_window.id == self.id:
        #     window = app.main_window
        # else:
        #     try:
        #         window = app.windows[self.id]
        #     except KeyError:
        #         raise Exception("Unknown window")

        sourcefile = os.path.join(os.path.dirname(__file__), 'render', '__init__.py')

        fd, tempname = tempfile.mkstemp()
        py_compile.compile(sourcefile, cfile=tempname, doraise=True)
        with open(os.path.join(os.path.dirname(sourcefile), tempname), 'rb') as compiled:
            toga = base64.encodebytes(compiled.read())

        return render(request, 'toga/app.html', {
            'toga': toga,
            'bootstrap': base64.encodebytes(b'\xee\x0c\r\n00000000' + marshal.dumps(bootstrap.__code__)).strip(),
            'window': self._impl,
            'callbacks': {
                # 'sample': base64.encodebytes(b'\x08\x1c\xe8VU\x00\x00\x00' + marshal.dumps(sample.__code__)).strip()
                '%s-%s' % (widget, message): base64.encodebytes(b'\xee\x0c\r\n00000000' + marshal.dumps(callback.__code__)).strip()
                for (widget, message), callback in self.callbacks.items()
            }
        })
