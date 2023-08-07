from textual.screen import Screen as TextualScreen
from textual.widgets import Button as TextualButton, Header as TextualHeader

from .container import Container


class TogaWindow(TextualScreen):
    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface
        self.impl = impl

    def on_mount(self) -> None:
        self.mount(TextualHeader())

    # Textual catches events at the level of the Screen/Window;
    # redirect to the widget instance.
    def on_button_pressed(self, event: TextualButton.Pressed) -> None:
        event.button.on_press(event)


class Window:
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.native = TogaWindow(self)
        self.container = Container()
        self.set_title(title)

    def create_toolbar(self):
        pass

    def clear_content(self):
        pass

    def set_content(self, widget):
        self.container.content = widget

        self.native.mount(widget.native)

    def get_title(self):
        return self._title

    def set_title(self, title):
        self._title = title

    def get_position(self):
        return (0, 0)

    def set_position(self, position):
        pass

    def get_size(self):
        return (80, 25)

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
