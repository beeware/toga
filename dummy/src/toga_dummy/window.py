from pathlib import Path

import toga_dummy

from .utils import LoggedObject


class Container:
    def __init__(self, content=None):
        self.baseline_dpi = 96
        self.dpi = 96

        # Prime the underlying storage before using setter
        self._content = None
        self.content = content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if self._content:
            self._content.container = None

        self._content = value
        if value:
            value.container = self

    @property
    def width(self):
        return self.content.get_size()[0]

    @property
    def height(self):
        return self.content.get_size()[1]

    def refreshed(self):
        if self.content:
            self.content.refresh()


class Window(LoggedObject):
    def __init__(self, interface, title, position, size):
        super().__init__()
        self._action("create Window")
        self.interface = interface
        self.container = Container()

        self.set_title(title)
        self.set_position(position)
        self.set_size(size)

    def create_toolbar(self):
        self._action("create toolbar")

    def set_content(self, widget):
        self.container.content = widget
        self._action("set content", widget=widget)
        self._set_value("content", widget)

    def get_title(self):
        return self._get_value("title")

    def set_title(self, title):
        self._set_value("title", title)

    def get_position(self):
        return self._get_value("position")

    def set_position(self, position):
        self._set_value("position", position)

    def get_size(self):
        return self._get_value("size", (640, 480))

    def set_size(self, size):
        self._set_value("size", size)

    def set_app(self, app):
        self._set_value("app", app)

    def show(self):
        self._action("show")
        self._set_value("visible", True)

    def hide(self):
        self._action("hide")
        self._set_value("visible", False)

    def get_visible(self):
        return self._get_value("visible")

    def close(self):
        self._action("close")
        self._set_value("visible", False)

    def get_image_data(self):
        self._action("get image data")
        path = Path(toga_dummy.__file__).parent / "resources/screenshot.png"
        return path.read_bytes()

    def set_full_screen(self, is_full_screen):
        self._action("set full screen", full_screen=is_full_screen)

    def simulate_close(self):
        self.interface.on_close()
