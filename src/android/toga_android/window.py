
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
        self._create()

    def set_content(self, widget):
        if self.native is None:
            widget.native = TogaLayout(self.app.native, widget)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

        self.app._impl.setContentView(self._container._impl)

    def set_title(self, title):
        pass

    def set_position(self, position):
        pass

    def set_size(self, size):
        pass

    def set_app(self, app):
        pass

    def create_toolbar(self):
        pass

    def show(self):
        pass

    def info_dialog(self, title, message):
        raise NotImplementedError()

    def question_dialog(self, title, message):
        raise NotImplementedError()

    def confirm_dialog(self, title, message):
        raise NotImplementedError()

    def error_dialog(self, title, message):
        raise NotImplementedError()

    def stack_trace_dialog(self, title, message, content, retry=False):
        raise NotImplementedError()

    def save_file_dialog(self, title, suggested_filename, file_types):
        raise NotImplementedError()
