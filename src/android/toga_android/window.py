class Window:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.container = None
        self.create()

    def create(self):
        pass

    def set_app(self, app):
        self._create()

    def set_content(self, widget):
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
