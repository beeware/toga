from toga_iOS.container import RootContainer
from toga_iOS.libs import (
    UIColor,
    UIScreen,
    UIWindow,
)


class Window:
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self

        self.native = UIWindow.alloc().initWithFrame(UIScreen.mainScreen.bounds)

        # Set up a container for the window's content
        # RootContainer provides a titlebar for the window.
        self.container = RootContainer()

        # Set the size of the content to the size of the window
        self.container.native.frame = self.native.bounds

        # Set the window's root controller to be the container's controller
        self.native.rootViewController = self.container.controller

        # Set the background color of the root content.
        try:
            # systemBackgroundColor() was introduced in iOS 13
            # We don't test on iOS 12, so mark the other branch as nocover
            self.native.backgroundColor = UIColor.systemBackgroundColor()
        except AttributeError:  # pragma: no cover
            self.native.backgroundColor = UIColor.whiteColor

        self.set_title(title)

    def clear_content(self):
        pass

    def set_content(self, widget):
        self.container.content = widget

    def get_title(self):
        return str(self.container.title)

    def set_title(self, title):
        self.container.title = title

    def get_position(self):
        return 0, 0

    def set_position(self, position):
        # Does nothing on mobile
        pass

    def get_size(self):
        return (
            UIScreen.mainScreen.bounds.size.width,
            UIScreen.mainScreen.bounds.size.height,
        )

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
        # The window is always visible
        return True

    def close(self):
        pass
