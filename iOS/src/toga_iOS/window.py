from toga_iOS.container import RootContainer
from toga_iOS.libs import (
    UIColor,
    UIScreen,
    UIWindow,
)


class Window:
    _is_main_window = False

    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self

        if not self._is_main_window:
            raise RuntimeError(
                "Secondary windows cannot be created on mobile platforms"
            )

        self.native = UIWindow.alloc().initWithFrame(UIScreen.mainScreen.bounds)

        # Set up a container for the window's content
        # RootContainer provides a titlebar for the window.
        self.container = RootContainer(on_refresh=self.content_refreshed)

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

    def set_content(self, widget):
        self.container.content = widget

    def content_refreshed(self, container):
        min_width = self.interface.content.layout.min_width
        min_height = self.interface.content.layout.min_height

        # If the minimum layout is bigger than the current window, log a warning
        if self.container.width < min_width or self.container.height < min_height:
            print(
                f"Warning: Window content {(min_width, min_height)} "
                f"exceeds available space {(self.container.width, self.container.height)}"
            )

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

    def hide(self):
        # A no-op, as the window cannot be hidden.
        pass

    def get_visible(self):
        # The window is always visible
        return True

    def set_full_screen(self, is_full_screen):
        # Windows are always full screen
        pass

    def close(self):
        pass
