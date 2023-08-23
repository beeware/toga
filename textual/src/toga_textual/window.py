from rich.text import Text

from textual.app import RenderResult
from textual.reactive import Reactive
from textual.screen import Screen as TextualScreen
from textual.widget import Widget as TextualWidget

from .container import Container


class CloseIcon(TextualWidget):
    DEFAULT_CSS = """
    CloseIcon {
        dock: left;
        padding: 0 1;
        width: 4;
        content-align: left middle;
    }
    """

    def render(self) -> RenderResult:
        return "⭘"


class TitleSpacer(TextualWidget):
    DEFAULT_CSS = """
    TitleSpacer {
        dock: right;
        padding: 0 1;
        width: 4;
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

    def __init__(self, title):
        super().__init__()
        self.title = TitleText(title)

    @property
    def text(self):
        return self.title.text

    @text.setter
    def text(self, value):
        self.title.text = value

    def compose(self):
        yield CloseIcon()
        yield self.title
        yield TitleSpacer()


class TogaWindow(TextualScreen):
    def __init__(self, impl, title):
        super().__init__()
        self.interface = impl.interface
        self.impl = impl
        self.titlebar = TitleBar(title)

    def on_mount(self) -> None:
        self.mount(self.titlebar)

    def on_resize(self, event) -> None:
        self.interface.content.refresh()


class Window:
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.native = TogaWindow(self, title)
        self.container = Container(self.native)

    def create_toolbar(self):
        pass

    def clear_content(self):
        pass

    def set_content(self, widget):
        self.container.content = widget

        self.native.mount(widget.native)

    def get_title(self):
        return self.native.titlebar.text

    def set_title(self, title):
        self.native.titlebar.text = title

    def get_position(self):
        return (0, 0)

    def set_position(self, position):
        pass

    def get_size(self):
        return (self.native.size.width, self.native.size.height)

    def set_size(self, size):
        pass

    def set_app(self, app):
        app.native.install_screen(self.native, name=self.interface.id)

    def show(self):
        pass

    def hide(self):
        pass

    def get_visible(self):
        return True

    def close(self):
        pass

    def set_full_screen(self, is_full_screen):
        pass
