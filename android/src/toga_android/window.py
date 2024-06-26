from decimal import ROUND_UP

from android import R
from android.content import Context
from android.graphics import (
    Bitmap,
    Canvas as A_Canvas,
)
from android.view import ViewTreeObserver
from java import dynamic_proxy
from java.io import ByteArrayOutputStream

from toga.types import Position, Size

from .container import Container
from .screens import Screen as ScreenImpl


class LayoutListener(dynamic_proxy(ViewTreeObserver.OnGlobalLayoutListener)):
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
        self._initial_title = title

    ######################################################################
    # Window properties
    ######################################################################

    def get_title(self):
        return str(self.app.native.getTitle())

    def set_title(self, title):
        self.app.native.setTitle(title)

    ######################################################################
    # Window lifecycle
    ######################################################################

    def close(self):  # pragma: no cover
        # An Android app only ever contains a main window, and that window *can't* be
        # closed, so the platform-specific close handling is never triggered.
        pass

    def configure_titlebar(self):  # pragma: no cover
        # Hide the titlebar on a simple window. The testbed can't create a simple
        # window, so we can't test this.
        self.app.native.getSupportActionBar().hide()

    def set_app(self, app):
        if len(app.interface.windows) > 1:
            raise RuntimeError("Secondary windows cannot be created on Android")

        self.app = app
        native_parent = self.app.native.findViewById(R.id.content)
        self.init_container(native_parent)
        native_parent.getViewTreeObserver().addOnGlobalLayoutListener(
            LayoutListener(self)
        )
        self.set_title(self._initial_title)

    def show(self):
        pass

    ######################################################################
    # Window content and resources
    ######################################################################

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

    ######################################################################
    # Window size
    ######################################################################

    def get_size(self) -> Size:
        return Size(self.width, self.height)

    def set_size(self, size):
        # Does nothing on mobile
        pass

    ######################################################################
    # Window position
    ######################################################################

    def get_current_screen(self):
        context = self.app.native.getApplicationContext()
        window_manager = context.getSystemService(Context.WINDOW_SERVICE)
        return ScreenImpl(self.app, window_manager.getDefaultDisplay())

    def get_position(self) -> Position:
        return Position(0, 0)

    def set_position(self, position):
        # Does nothing on mobile
        pass

    ######################################################################
    # Window visibility
    ######################################################################

    def hide(self):
        # A no-op, as the window cannot be hidden.
        pass

    def get_visible(self):
        # The window is always visible
        return True

    ######################################################################
    # Window state
    ######################################################################

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented("Window.set_full_screen()")

    ######################################################################
    # Window capabilities
    ######################################################################

    def get_image_data(self):
        bitmap = Bitmap.createBitmap(
            self.native_content.getWidth(),
            self.native_content.getHeight(),
            Bitmap.Config.ARGB_8888,
        )
        canvas = A_Canvas(bitmap)
        # TODO: Need to draw window background as well as the content.
        self.native_content.draw(canvas)

        stream = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.PNG, 0, stream)
        return bytes(stream.toByteArray())


class MainWindow(Window):
    def configure_titlebar(self):
        # Display the titlebar on a MainWindow.
        pass

    def create_toolbar(self):
        # Toolbar items are configured as part of onPrepareOptionsMenu; trigger that
        # handler.
        self.app.native.invalidateOptionsMenu()
