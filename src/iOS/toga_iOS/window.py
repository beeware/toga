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
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self

        self.native = UIWindow.alloc().initWithFrame(UIScreen.mainScreen.bounds)

        self.set_title(title)

    def clear_content(self):
        if self.interface.content:
            for child in self.interface.content.children:
                child._impl.container = None

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

    def get_title(self):
        self.interface.factory.not_implemented("Window.get_title()")
        return "?"

    def set_title(self, title):
        self.interface.factory.not_implemented("Window.set_title()")

    def get_position(self):
        return (0, 0)

    def set_position(self, position):
        # Does nothing on mobile
        pass

    def get_size(self):
        return (UIScreen.mainScreen.bounds.size.width, UIScreen.mainScreen.bounds.size.height)

    def set_size(self, size):
        # Does nothing on mobile
        pass

    def set_app(self, app):
        pass

    def create_toolbar(self):
        pass

    def show(self):
        self.native.makeKeyAndVisible()

        # Refresh with the actual viewport to do the proper rendering.
        self.interface.content.refresh()

    def hide(self):
        # A no-op, as the window cannot be hidden.
        pass

    def get_visible(self):
        # The window is alays visible
        return True

    def close(self):
        pass
