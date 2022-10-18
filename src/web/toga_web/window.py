from toga_web.libs import js, create_element


class WebViewport:
    def __init__(self):
        self.dpi = 96
        self.baseline_dpi = 96

    @property
    def width(self):
        return 1024

    @property
    def height(self):
        return 768


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
        self.interface.factory.not_implemented('Window.create_toolbar()')

    def clear_content(self):
        if self.interface.content:
            for child in self.interface.content.children:
                child._impl.container = None

    def set_content(self, widget):
        widget.viewport = WebViewport()

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
        self.interface.factory.not_implemented('Window.close()')

    def get_position(self):
        return (0, 0)

    def set_position(self, position):
        # Does nothing on web
        pass

    def get_size(self):
        return (self.content.viewport.width, self.content.viewport.height)

    def set_size(self, size):
        # Does nothing on web
        pass

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented('Window.set_full_screen()')
