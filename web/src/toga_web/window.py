from toga_web.libs import create_element, js

from .screens import Screen as ScreenImpl


class Window:
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self

        self.native = create_element(
            "main",
            id=f"toga_{self.interface.id}",
            classes=["toga", "window", "container"],
            role="main",
        )

        app_placeholder = js.document.getElementById("app-placeholder")
        app_placeholder.appendChild(self.native)

        self.set_title(title)

    ######################################################################
    # Native event handlers
    ######################################################################

    def on_close(self, *args):
        pass

    def on_size_allocate(self, widget, allocation):
        pass

    ######################################################################
    # Window properties
    ######################################################################

    def get_title(self):
        return js.document.title

    def set_title(self, title):
        js.document.title = title

    ######################################################################
    # Window lifecycle
    ######################################################################

    def close(self):
        self.interface.factory.not_implemented("Window.close()")

    def create_toolbar(self):
        self.interface.factory.not_implemented("Window.create_toolbar()")

    def set_app(self, app):
        pass

    def show(self):
        self.native.style = "visibility: visible;"

    ######################################################################
    # Window content and resources
    ######################################################################

    def clear_content(self):
        if self.interface.content:
            for child in self.interface.content.children:
                child._impl.container = None

    def set_content(self, widget):
        # Remove existing content of the window.
        for child in self.native.childNodes:
            self.native.removeChild(child)

        # Add all children to the content widget.
        self.native.appendChild(widget.native)

    ######################################################################
    # Window size
    ######################################################################

    def get_size(self):
        return self.native.offsetWidth, self.native.offsetHeight

    def set_size(self, size):
        # Does nothing on web
        pass

    ######################################################################
    # Window position
    ######################################################################

    def get_current_screen(self):
        return ScreenImpl(js.document.documentElement)

    def get_position(self):
        return 0, 0

    def set_position(self, position):
        # Does nothing on web
        pass

    ######################################################################
    # Window visibility
    ######################################################################

    def get_visible(self):
        self.interface.not_implemented("Window.get_visible()")

    def hide(self):
        self.native.style = "visibility: hidden;"

    ######################################################################
    # Window state
    ######################################################################

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented("Window.set_full_screen()")

    ######################################################################
    # Window capabilities
    ######################################################################

    def get_image_data(self):
        self.interface.factory.not_implemented("Window.get_image_data()")
