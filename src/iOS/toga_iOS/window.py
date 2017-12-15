from .container import Container
from .libs import *


class Window:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.container = None
        self.create()

    def create(self):
        self.screen = UIScreen.mainScreen
        self.native = UIWindow.alloc().initWithFrame_(self.screen.bounds)
        self.native.interface = self.interface

    def set_content(self, widget):
        if widget.native is None:
            self.container = Container()
            self.container.content = widget
        else:
            self.container = widget

        if getattr(widget, 'controller', None):
            self.controller = widget.controller
        else:
            self.controller = UIViewController.alloc().init()

        self.native.rootViewController = self.controller
        self.controller.view = self.container.native

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
        self.native.makeKeyAndVisible()
        # self._impl.visualizeConstraints_(self._impl.contentView().constraints())
        # Do the first layout render.
        self.interface.content._update_layout(
            width=self.screen.bounds.size.width,
            height=self.screen.bounds.size.height
        )

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
