from toga_iOS import dialogs
from toga_iOS.libs import UIApplication, UIScreen, UIViewController, UIWindow


class iOSViewport:
    def __init__(self, view):
        self.view = view
        # iOS renders everything at 96dpi.
        self.dpi = 96
        self.baseline_dpi = self.dpi

        self.kb_height = 0.0

    @property
    def statusbar_height(self):
        # This is the height of the status bar frame.
        # If the status bar isn't visible (e.g., on iPhones in landscape orientation)
        # the size will be 0.
        return UIApplication.sharedApplication.statusBarFrame.size.height

    @property
    def width(self):
        return self.view.bounds.size.width

    @property
    def height(self):
        # Remove the height of the keyboard and the titlebar
        # from the available viewport height
        return self.view.bounds.size.height - self.kb_height - self.statusbar_height


class Window:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        self.native = UIWindow.alloc().initWithFrame(UIScreen.mainScreen.bounds)
        self.native.interface = self.interface

    def set_content(self, widget):
        widget.viewport = iOSViewport(self.native)

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
        return dialogs.info_dialog(self.interface, title, message)

    def question_dialog(self, title, message):
        return dialogs.question_dialog(self.interface, title, message)

    def confirm_dialog(self, title, message):
        return dialogs.confirm_dialog(self.interface, title, message)

    def error_dialog(self, title, message):
        return dialogs.error_dialog(self.interface, title, message)

    def stack_trace_dialog(self, title, message, content, retry=False):
        self.interface.factory.not_implemented('Window.stack_trace_dialog()')
