from toga.types import Size

from ..utils import LoggedObject


class Widget(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.interface._impl = self
        self.container = None
        self.create()

    def get_size(self) -> Size:
        return Size(37, 42)

    def create(self):
        self._action("create Widget")

    def set_app(self, app):
        self._set_value("app", app)

    def set_window(self, window):
        self._set_value("window", window)

    def get_enabled(self):
        return self._get_value("enabled", True)

    def set_enabled(self, value):
        self._set_value("enabled", value)

    def focus(self):
        self._action("focus")

    def get_tab_index(self):
        return self._get_value("tab_index", None)

    def set_tab_index(self, tab_index):
        self._set_value("tab_index", tab_index)

    ######################################################################
    # APPLICATOR
    ######################################################################

    def set_bounds(self, x, y, width, height):
        self._action("set bounds", x=x, y=y, width=width, height=height)

    def set_alignment(self, alignment):
        self._action("set alignment", alignment=alignment)

    def set_hidden(self, hidden):
        self._action("set hidden", hidden=hidden)

    def set_font(self, font):
        self._action("set font", font=font)

    def set_color(self, color):
        self._action("set color", color=color)

    def set_background_color(self, color):
        self._action("set background color", color=color)

    ######################################################################
    # INTERFACE
    ######################################################################

    def add_child(self, child):
        child.container = self.container
        self._action("add child", child=child)

    def insert_child(self, index, child):
        child.container = self.container
        self._action("insert child", index=index, child=child)

    def remove_child(self, child):
        child.container = None
        self._action("remove child", child=child)

    def refresh(self):
        self._action("refresh")
