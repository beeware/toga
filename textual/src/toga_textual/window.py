from rich.text import Text

from textual.app import RenderResult
from textual.reactive import Reactive
from textual.screen import Screen as TextualScreen
from textual.widget import Widget as TextualWidget
from textual.widgets import Button as TextualButton
from toga import Position, Size

from .container import Container
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

    def __init__(self):
        super().__init__()
        self.title = TitleText("Toga")

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
        self.interface.content.refresh()


class Window:
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.create()
        self.container = Container(self.native)
        self.set_title(title)

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
        return self.title

    def set_title(self, title):
        self.title = title

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

    def clear_content(self):
        pass

    def set_content(self, widget):
        self.container.content = widget
        widget.install(parent=self)

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

    def set_full_screen(self, is_full_screen):
        pass

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

    def get_title(self):
        return self.native.titlebar.text

    def set_title(self, title):
        self.native.titlebar.text = title
