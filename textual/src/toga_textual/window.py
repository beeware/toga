from rich.text import Text
from textual.app import RenderResult
from textual.reactive import Reactive
from textual.screen import Screen as TextualScreen
from textual.widget import Widget as TextualWidget
from textual.widgets import Button as TextualButton

from toga import Position, Size
from toga.constants import WindowState

from .screens import Screen as ScreenImpl


class WindowCloseButton(TextualButton):
    DEFAULT_CSS = """
    WindowCloseButton {
        dock: left;
        border: none;
        min-width: 3;
        height: 1;
        background: white 10%;
        color: white;
    }
    WindowCloseButton:hover {
        background: black;
        border: none;
    }
    WindowCloseButton:focus {
        text-style: bold;
    }
    WindowCloseButton.-active {
        border: none;
    }
    """

    def __init__(self):
        super().__init__("✕")

    def on_button_pressed(self, event):
        self.screen.impl.textual_close()
        event.stop()


class TitleSpacer(TextualWidget):
    DEFAULT_CSS = """
    TitleSpacer {
        dock: right;
        padding: 0 1;
        width: 3;
        content-align: right middle;
    }
    """

    def render(self) -> RenderResult:
        return ""


class TitleText(TextualWidget):
    DEFAULT_CSS = """
    TitleText {
        content-align: center middle;
        width: 100%;
    }
    """
    text: Reactive[str] = Reactive("")

    def __init__(self, text):
        super().__init__()
        self.text = text

    def render(self) -> RenderResult:
        return Text(self.text, no_wrap=True, overflow="ellipsis")


class TitleBar(TextualWidget):
    DEFAULT_CSS = """
    TitleBar {
        dock: top;
        width: 100%;
        background: $foreground 5%;
        color: $text;
        height: 1;
    }
    """

    def __init__(self, title="Toga"):
        super().__init__()
        self.title = TitleText(title)

    @property
    def text(self):
        return self.title.text

    @text.setter
    def text(self, value):
        self.title.text = value

    def compose(self):
        yield WindowCloseButton()
        yield self.title
        yield TitleSpacer()


class TogaWindow(TextualScreen):
    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface
        self.impl = impl

    def on_resize(self, event) -> None:
        self.interface.on_resize()
        self.impl.scaffold.refresh()


class Window:
    def __init__(self, interface, position, size):
        self.interface = interface
        # An actual set_scaffold call will come later, but we already have a
        # placeholder scaffold we can use; this simplifies edge cases.
        self.scaffold = self.interface._scaffold._impl
        self.create()

    def create(self):
        self.native = TogaWindow(self)

    ######################################################################
    # Native event handlers
    ######################################################################

    def textual_close(self):
        self.interface.on_close()

    ######################################################################
    # Window properties
    ######################################################################

    def get_title(self):
        return self.scaffold.title

    def set_title(self, title):
        self.scaffold.title = title

    ######################################################################
    # Window lifecycle
    ######################################################################

    def close(self):
        self.native.dismiss(None)

    def set_app(self, app):
        app.native.mount(self.native)
        app.native.install_screen(self.native, name=self.interface.id)

    def show(self):
        pass

    ######################################################################
    # Window content and resources
    ######################################################################

    def set_scaffold(self, scaffold):
        # Sync the current title onto the new scaffold.
        scaffold.title = self.get_title()
        # Detaching an unattached (placeholder) scaffold is a no-op.
        self.scaffold.detach()
        self.scaffold = scaffold
        scaffold.attach(self)

    ######################################################################
    # Window size
    ######################################################################

    def get_size(self) -> Size:
        return Size(self.native.size.width, self.native.size.height)

    def set_size(self, size):
        pass

    ######################################################################
    # Window position
    ######################################################################

    def get_current_screen(self):
        return ScreenImpl(self.native)

    def get_position(self) -> Position:
        return Position(0, 0)

    def set_position(self, position):
        pass

    ######################################################################
    # Window visibility
    ######################################################################

    def get_visible(self):
        return True

    def hide(self):
        pass

    ######################################################################
    # Window state
    ######################################################################

    def get_window_state(self, in_progress_state=False):
        # Windows are always normal
        return WindowState.NORMAL

    def set_window_state(self, state):
        self.interface.factory.not_implemented("Window.set_window_state()")

    ######################################################################
    # Window capabilities
    ######################################################################

    def get_image_data(self):
        self.interface.factory.not_implemented("Window.get_image_data()")


class TogaMainWindow(TogaWindow):
    def __init__(self, impl):
        super().__init__(impl)
        self.titlebar = TitleBar()

    def on_mount(self) -> None:
        self.mount(self.titlebar)


class MainWindow(Window):
    def create(self):
        self.native = TogaMainWindow(self)

    def create_menus(self):
        self.interface.factory.not_implemented("Window.create_menus()")

    def create_toolbar(self):
        self.interface.factory.not_implemented("Window.create_toolbar()")

    ######################################################################
    # Window properties
    ######################################################################

    def set_title(self, title):
        super().set_title(title)
        self.native.titlebar.text = title
