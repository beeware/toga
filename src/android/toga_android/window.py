from .libs.activity import MainActivity


class AndroidViewport:
    def __init__(self, native):
        self.native = native
        self.dpi = 96  # FIXME This is almost certainly wrong...
        # self.dpi = ... self.interface.app._impl.device_scale

    @property
    def width(self):
        return self.native.ClientSize.Width

    @property
    def height(self):
        return self.native.ClientSize.Height


class Window:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        pass

    def set_app(self, app):
        pass

    def set_content(self, widget):
        MainActivity.singletonThis.setContentView(widget.native)

    def set_title(self, title):
        pass

    def set_position(self, position):
        pass

    def set_size(self, size):
        pass

    def create_toolbar(self):
        pass

    def show(self):
        pass

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented('Window.set_full_screen()')

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


class MainWindow(Window):
    pass
