from .container import Container, Viewport
from .libs.android import R__id
from .libs.android.view import ViewTreeObserver__OnGlobalLayoutListener


class LayoutListener(ViewTreeObserver__OnGlobalLayoutListener):
    def __init__(self, viewport):
        super().__init__()
        self.viewport = viewport

    def onGlobalLayout(self):
        """This listener is run after each native layout pass.

        If any view's size or position has changed, the new values will be visible here.
        """
        self.viewport.size = (
            self.viewport.parent.getWidth(),
            self.viewport.parent.getHeight(),
        )


class Window(Container):
    def __init__(self, interface, title, position, size):
        super().__init__()
        self.interface = interface
        self.interface._impl = self
        # self.set_title(title)

    def set_app(self, app):
        self.app = app
        viewport_parent = app.native.findViewById(R__id.content)
        self.content_viewport = Viewport(viewport_parent, self.interface)
        viewport_parent.getViewTreeObserver().addOnGlobalLayoutListener(
            LayoutListener(self.content_viewport)
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
        return self.content_viewport.size

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

    def get_visible(self):
        # The window is always visible
        return True

    def close(self):
        pass

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented("Window.set_full_screen()")
