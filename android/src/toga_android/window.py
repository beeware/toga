from decimal import ROUND_UP

from .container import Container
from .libs.android import R__id
from .libs.android.view import ViewTreeObserver__OnGlobalLayoutListener


class LayoutListener(ViewTreeObserver__OnGlobalLayoutListener):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def onGlobalLayout(self):
        """This listener is run after each native layout pass.

        If any view's size or position has changed, the new values will be visible here.
        """
        native_parent = self.window.native_content.getParent()
        self.window.resize_content(native_parent.getWidth(), native_parent.getHeight())


class Window(Container):
    def __init__(self, interface, title, position, size):
        super().__init__()
        self.interface = interface
        self.interface._impl = self
        # self.set_title(title)

    def set_app(self, app):
        self.app = app
        native_parent = app.native.findViewById(R__id.content)
        self.init_container(native_parent)
        native_parent.getViewTreeObserver().addOnGlobalLayoutListener(
            LayoutListener(self)
        )

    def get_title(self):
        return str(self.app.native.getTitle())

    def set_title(self, title):
        self.app.native.setTitle(title)

    def get_position(self):
        return 0, 0

    def set_position(self, position):
        # Does nothing on mobile
        pass

    def get_size(self):
        return (self.width, self.height)

    def set_size(self, size):
        # Does nothing on mobile
        pass

    def create_toolbar(self):
        pass

    def show(self):
        pass

    def hide(self):
        # A no-op, as the window cannot be hidden.
        pass

    def refreshed(self):
        if self.native_width and self.native_height:
            layout = self.interface.content.layout
            available_width = self.scale_out(self.native_width, ROUND_UP)
            available_height = self.scale_out(self.native_height, ROUND_UP)
            if (layout.width > available_width) or (layout.height > available_height):
                # Show the sizes in terms of CSS pixels.
                print(
                    f"Warning: Window content {(layout.width, layout.height)} "
                    f"exceeds available space {(available_width, available_height)}"
                )

        super().refreshed()

    def get_visible(self):
        # The window is always visible
        return True

    def close(self):
        pass

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented("Window.set_full_screen()")
