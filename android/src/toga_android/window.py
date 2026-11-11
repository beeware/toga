from android import R
from android.content import Context
from android.graphics import (
    Bitmap,
    Canvas as A_Canvas,
)
from android.view import ViewTreeObserver
from java import dynamic_proxy
from java.io import ByteArrayOutputStream

from toga.constants import WindowState
from toga.types import Position, Size

from .screens import Screen as ScreenImpl


class LayoutListener(dynamic_proxy(ViewTreeObserver.OnGlobalLayoutListener)):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def onGlobalLayout(self):
        """This listener is run after each native layout pass.

        If any view's size or position has changed, the new values will be visible here.
        """
        self.window.interface.on_resize()
        native_parent = self.window.native_parent
        self.window.scaffold.container.resize_content(
            native_parent.getWidth(), native_parent.getHeight()
        )


class Window:
    def __init__(self, interface, position, size):
        self.interface = interface
        self.interface._impl = self
        self.app = None
        self.native_parent = None
        # An actual set_scaffold call will come later, but we already have a
        # placeholder scaffold we can use; this simplifies edge cases.
        self.scaffold = self.interface._scaffold._impl
        # A plain Window doesn't display a navigation bar; MainWindow does.
        self._navigation_bar_hidden = True
        # Use a shadow variable since the presence of ActionBar is not
        # a reliable indicator for confirmation of presentation mode.
        self._in_presentation_mode = False

    ######################################################################
    # Window properties
    ######################################################################

    def get_title(self):
        return str(self.scaffold.title)

    def set_title(self, title):
        self.scaffold.title = title

    ######################################################################
    # Window lifecycle
    ######################################################################

    def close(self):  # pragma: no cover
        # An Android app only ever contains a main window, and that window *can't* be
        # closed, so the platform-specific close handling is never triggered.
        pass

    def set_app(self, app):
        if len(app.interface.windows) > 1:
            raise RuntimeError("Secondary windows cannot be created on Android")

        self.app = app
        self.native_parent = self.app.native.findViewById(R.id.content)
        self.scaffold.attach(self.app.native, self.native_parent)
        self.native_parent.getViewTreeObserver().addOnGlobalLayoutListener(
            LayoutListener(self)
        )

    def show(self):  # pragma: no cover
        # The Window on Android is shown by default when the app starts.
        # Requesting show() on an already shown window is a no-op and is
        # ignored at the core level. So this method will never be reached.
        pass

    ######################################################################
    # Window content and resources
    ######################################################################

    def set_scaffold(self, scaffold):
        # Sync the current title and navigation bar state onto the new scaffold.
        scaffold.title = self.get_title()
        scaffold.navigation_bar_hidden = self._navigation_bar_hidden

        # The first scaffold is set before the window has an app; it will be
        # attached when set_app() is invoked. Core only invokes set_scaffold
        # with a *different* scaffold once the window has an app.
        if self.app is not None:
            self.scaffold.detach()
            scaffold.attach(self.app.native, self.native_parent)

        self.scaffold = scaffold

    ######################################################################
    # Window size
    ######################################################################

    def get_size(self) -> Size:
        return Size(self.scaffold.container.width, self.scaffold.container.height)

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

    def get_window_state(self, in_progress_state=False):
        if getattr(self, "app", None) is not None:
            decor_view = self.app.native.getWindow().getDecorView()
            system_ui_flags = decor_view.getSystemUiVisibility()
            if system_ui_flags & (
                decor_view.SYSTEM_UI_FLAG_FULLSCREEN
                | decor_view.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                | decor_view.SYSTEM_UI_FLAG_IMMERSIVE
            ):
                if self._in_presentation_mode:
                    return WindowState.PRESENTATION
                else:
                    return WindowState.FULLSCREEN
        return WindowState.NORMAL

    def set_window_state(self, state):
        current_state = self.get_window_state()
        decor_view = self.app.native.getWindow().getDecorView()

        if current_state == state:
            return

        match current_state, state:
            case WindowState.NORMAL, (WindowState.MAXIMIZED | WindowState.MINIMIZED):
                # no-op on Android.
                pass
            case WindowState.NORMAL, WindowState.FULLSCREEN:
                decor_view.setSystemUiVisibility(
                    # These constants are all marked as deprecated as of API 30.
                    decor_view.SYSTEM_UI_FLAG_FULLSCREEN
                    | decor_view.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                    | decor_view.SYSTEM_UI_FLAG_IMMERSIVE
                )
            case WindowState.NORMAL, _:  # state == WindowState.PRESENTATION
                decor_view.setSystemUiVisibility(
                    decor_view.SYSTEM_UI_FLAG_FULLSCREEN
                    | decor_view.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                    | decor_view.SYSTEM_UI_FLAG_IMMERSIVE
                )
                self.scaffold.apply_navigation_bar(force_hidden=True)
                self._in_presentation_mode = True

            case WindowState.FULLSCREEN, _:
                decor_view.setSystemUiVisibility(0)
                self.set_window_state(state)

            case _:  # current_state == WindowState.PRESENTATION:
                decor_view.setSystemUiVisibility(0)
                self.scaffold.apply_navigation_bar()
                self._in_presentation_mode = False
                self.set_window_state(state)

    ######################################################################
    # Window capabilities
    ######################################################################

    def get_image_data(self):
        native_content = self.scaffold.current_container.native_content
        bitmap = Bitmap.createBitmap(
            native_content.getWidth(),
            native_content.getHeight(),
            Bitmap.Config.ARGB_8888,
        )
        canvas = A_Canvas(bitmap)
        # TODO: Need to draw window background as well as the content.
        native_content.draw(canvas)

        stream = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.PNG, 0, stream)
        return bytes(stream.toByteArray())


class MainWindow(Window):
    def __init__(self, interface, position, size):
        super().__init__(interface, position, size)
        self._navigation_bar_hidden = False

    def create_toolbar(self):
        # Toolbar items are configured as part of onPrepareOptionsMenu; trigger that
        # handler.
        self.app.native.invalidateOptionsMenu()
