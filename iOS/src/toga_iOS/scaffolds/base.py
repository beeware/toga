from toga_iOS.container import ControlledContainer
from toga_iOS.libs import UINavigationController


class Scaffold:
    def __init__(self, interface):
        self.interface = interface
        self.last_refreshed_size = (0, 0)
        self._navigation_bar_hidden = False
        self.container = ControlledContainer(
            on_refresh=self.content_refreshed, on_native_layout=self.on_native_layout
        )
        self.nav_controller = UINavigationController.alloc().initWithRootViewController(
            self.container.controller
        )

    @property
    def navigation_bar_hidden(self):
        return self._navigation_bar_hidden

    @property
    def current_container(self):
        return self.container

    @navigation_bar_hidden.setter
    def navigation_bar_hidden(self, hidden):
        self._navigation_bar_hidden = hidden
        self.nav_controller.setNavigationBarHidden(hidden, animated=True)

    def set_content(self, widget):
        self.container.content = widget

    @property
    def title(self):
        return self.container.controller.title

    @title.setter
    def title(self, value):
        self.container.controller.title = value

    def refresh(self):
        if self.container.content:
            self.container.content.interface.refresh()

    def content_refreshed(self, container):
        min_width = self.interface.content.layout.min_width
        min_height = self.interface.content.layout.min_height

        # An initial layout uses (0, 0); in this case nothing is even being
        # shown on screen so we can ignore that safely.
        # Else, If the minimum layout is bigger than the current window, log a
        # warning
        if (container.width, container.height) != (0, 0) and (
            container.width < min_width or container.height < min_height
        ):
            print(
                f"Warning: Window content {(min_width, min_height)} "
                f"exceeds available space "
                f"{(container.width, container.height)}"
            )

    @property
    def window(self):
        return self.interface.window._impl if self.interface.window else None

    def notify_resize(self, container):
        if (container.width, container.height) != self.last_refreshed_size:
            self.last_refreshed_size = (container.width, container.height)
            self.window.interface.on_resize()
            self.refresh()

    def on_native_layout(self, container):
        # If the navigation bar is hidden, then we must query for the size
        # of the status bar to use as our inset.
        # The testbed will not instantiate a simple app so no-cover the first
        # branch
        if self.navigation_bar_hidden:  # pragma: no cover
            # When status bar heights change, a relayout of the window will
            # be triggered by the native layer, which is how we can catch this
            # and use this value correctly here.
            if self.window:
                # Do this because of line length...
                status_bar_manager = self.window.native.windowScene.statusBarManager
                status_bar_height = status_bar_manager.statusBarFrame.size.height
                # On iPadOS, the status bar height may not always be in the
                # window of the application.  This can be detected by seeing if
                # the status bar height is influencing the safe area insets of
                # the container, as iPadOS window corners are smaller than the
                # top status bar.
                if container.native.safeAreaInsets.top >= status_bar_height:
                    container.top_inset = status_bar_height
                else:
                    container.top_inset = 0
            else:
                container.top_inset = 0
        else:
            # Instead of manually computing the geometry at the top,
            # this check is used because iOS's algorithms to place the
            # navigation bar at an appropriate height appears to be
            # a mystery... also, when the navigation bar metrics change,
            # a layout appears to be triggered in the innner subview,
            # and that's how we can catch it.
            container.top_inset = (
                self.nav_controller.navigationBar.frame.origin.y
                + self.nav_controller.navigationBar.frame.size.height
            )

        self.notify_resize(container)
