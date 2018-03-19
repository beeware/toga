from travertino.layout import Viewport

from .libs import *


class iOSViewport:
    def __init__(self, screen):
        self.screen = screen
        self.dpi = 96  # FIXME This is almost certainly wrong...

        self.kb_height = 0.0

    @property
    def statusbar_height(self):
        if UIApplication.sharedApplication.statusBarOrientation == UIInterfaceOrientation.Portrait.value:
            # This is the height of the status bar.
            return 16
        else:
            return 0

    @property
    def width(self):
        return self.screen.bounds.size.width

    @property
    def height(self):
        # Remove the height of the keyboard and the titlebar
        # from the available viewport height
        return self.screen.bounds.size.height - self.kb_height - self.statusbar_height


class Window:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        self.screen = UIScreen.mainScreen
        self.native = UIWindow.alloc().initWithFrame(self.screen.bounds)
        self.native.interface = self.interface

    def set_content(self, widget):
        widget.viewport = iOSViewport(self.screen)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

        if getattr(widget, 'controller', None):
            self.controller = widget.controller
        else:
            self.controller = UIViewController.alloc().init()

        self.native.rootViewController = self.controller
        self.controller.view = widget.native

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

        # Refresh with the actual viewport to do the proper rendering.
        self.interface.content.refresh()

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
