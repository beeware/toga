# from travertino.layout import Viewport

# from toga.command import GROUP_BREAK, SECTION_BREAK
# from toga.handlers import wrapped_handler


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

        self.set_title(title)

    def __html__(self):
        return """
            <main id="toga_{id}" class="container" role="main">
            {content}
            </main>
        """.format(
            id=self.interface.id,
            content=self.interface.content._impl.__html__()
        )

    def get_title(self):
        self.interface.factory.not_implemented('Window.get_title()')
        return "?"

    def set_title(self, title):
        self.interface.factory.not_implemented('Window.set_title()')

    def set_app(self, app):
        self.interface.factory.not_implemented('Window.set_app()')

    def create_toolbar(self):
        self.interface.factory.not_implemented('Window.create_toolbar()')

    def set_content(self, widget):
        self.interface.factory.not_implemented('Window.set_content()')
        widget.viewport = WebViewport()
        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

    def show(self):
        self.interface.factory.not_implemented('Window.show()')
        # self.native.show_all()

        # # Now that the content is visible, we can do our initial hinting,
        # # and use that as the basis for setting the minimum window size.
        # self.interface.content._impl.rehint()
        # self.interface.content.style.layout(self.interface.content, Viewport(0, 0))
        # self.interface.content._impl.min_width = self.interface.content.layout.width
        # self.interface.content._impl.min_height = self.interface.content.layout.height

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
