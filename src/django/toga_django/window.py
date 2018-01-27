import base64
import marshal
import os
import py_compile

from django.shortcuts import render
from django.utils.safestring import mark_safe
from toga.interface.window import Window as WindowInterface

from . import dialogs
from . import impl
from .bootstrap import bootstrap
from .container import Container


class Window(WindowInterface):
    _IMPL_CLASS = impl.Window
    _CONTAINER_CLASS = Container
    _DIALOG_MODULE = dialogs

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.container = None
        self.create()

    def create(self):
        self._impl = impl.Window(
            id=self.id,
            title=self._config['title']
        )

    def set_toolbar(self, items):
        pass

    def set_content(self, widget):
        self._impl.set_content(widget._impl)

    def set_title(self, title):
        # self._impl.set_title(title)
        pass

    def set_app(self, app):
        pass

    def set_position(self, position):
        pass

    def set_size(self, size):
        pass

    def on_close(self, widget, data):
        pass

    def create_toolbar(self, toolbar):
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

    def info_dialog(self, title, message):
        self.interface.factory.not_implemented('Window.info_dialog()')

    def question_dialog(self, title, message):
        self.interface.factory.not_implemented('Window.question_dialog()')

    def confirm_dialog(self, title, message):
        self.interface.factory.not_implemented('Window.confirm_dialog()')

    def error_dialog(self, title, message):
        self.interface.factory.not_implemented('Window.error_dialog()')

    def stack_trace_dialog(self, title, message, content, retry=False):
        self.interface.factory.not_implemented('Window.stack_trace_dialog()')

    def save_file_dialog(self, title, suggested_filename, file_types):
        self.interface.factory.not_implemented('Window.save_file_dialog()')
