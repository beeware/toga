from toga_web.libs import create_element, js


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

    def get_title(self):
        return js.document.title

    def set_title(self, title):
        js.document.title = title

    def set_app(self, app):
        pass

    def create_toolbar(self):
        self.interface.factory.not_implemented("Window.create_toolbar()")

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

    def show(self):
        self.native.style = "visibility: visible;"

    def hide(self):
        self.native.style = "visibility: hidden;"

    def get_visible(self):
        self.interface.not_implemented("Window.get_visible()")

    def on_close(self, *args):
        pass

    def on_size_allocate(self, widget, allocation):
        pass

    def close(self):
        self.interface.factory.not_implemented("Window.close()")

    def get_position(self):
        return 0, 0

    def set_position(self, position):
        # Does nothing on web
        pass

    def get_size(self):
        return self.native.offsetWidth, self.native.offsetHeight

    def set_size(self, size):
        # Does nothing on web
        pass

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented("Window.set_full_screen()")

    @property
    def cursor_position(self):
        """Return the cursor position with respect to the specified window."""
        self.interface.factory.not_implemented("Window.cursor_position")

    @cursor_position.setter
    def cursor_position(self, value: tuple[int, int]):
        """Set the cursor position with respect to the specified window."""
        self.interface.factory.not_implemented("Window.cursor_position")

    @property
    def cursor_visible(self):
        """Return the status of cursor visibility for the specified window."""
        self.interface.factory.not_implemented("Window.cursor_visible")

    @cursor_visible.setter
    def cursor_visible(self, value: bool):
        """Set the cursor visibility for the specified window."""
        self.interface.factory.not_implemented("Window.cursor_visible")

    def show_cursor(self):
        """Show cursor for the specified window."""
        self.interface.factory.not_implemented("Window.show_cursor()")

    def hide_cursor(self):
        """Hide cursor from view for the specified window."""
        self.interface.factory.not_implemented("Window.hide_cursor()")
