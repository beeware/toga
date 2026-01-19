from abc import abstractmethod

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from ..colors import native_color, toga_color


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self._container = None
        self.native = None
        self.create()
        self.native.hide()
        self._hidden = True
        self.native.setPalette(QApplication.style().standardPalette())

        if not hasattr(self, "_background_color_role"):
            self._background_color_role = self.native.backgroundRole()
        if not hasattr(self, "_foreground_color_role"):
            self._foreground_color_role = self.native.foregroundRole()
        if not hasattr(self, "_default_background_color"):
            self._default_background_color = toga_color(
                self.native.palette().color(self._background_color_role)
            )
        # if not hasattr(self, "_default_foreground_color"):
        self._default_foreground_color = toga_color(
            self.native.palette().color(self._foreground_color_role)
        )

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        if self.container:
            assert container is None, f"{self} already has a container"

            # Existing container should be removed
            self.native.setParent(None)
            self._container = None
            self.native.hide()
        elif container:
            # setting container
            self._container = container
            self.native.setParent(container.native)
            self.set_hidden(self._hidden)

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    @abstractmethod
    def create(self): ...

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    def get_enabled(self):
        return self.native.isEnabled()

    def set_enabled(self, value):
        self.native.setEnabled(value)

    @property
    def has_focus(self):
        return self.native.hasFocus()

    def focus(self):
        if not self.has_focus:
            self.native.setFocus(Qt.OtherFocusReason)

    def get_tab_index(self):
        self.interface.factory.not_implemented("Widget.get_tab_index()")

    def set_tab_index(self, tab_index):
        self.interface.factory.not_implemented("Widget.set_tab_index()")

    ######################################################################
    # APPLICATOR
    ######################################################################

    def set_bounds(self, x, y, width, height):
        self.native.setGeometry(x, y, width, height)

    def set_hidden(self, hidden):
        if self.container is not None:
            self._apply_hidden(hidden)
        self._hidden = hidden

    def _apply_hidden(self, hidden):
        self.native.setHidden(hidden)

    def set_text_align(self, alignment):
        pass  # If appropriate, a widget subclass will implement this.

    def set_color(self, color):
        if color is None:
            color = self._default_foreground_color
        palette = self.native.palette()
        palette.setColor(self._foreground_color_role, native_color(color))
        self.native.setPalette(palette)

    def set_background_color(self, color):
        if color is None:
            color = self._default_background_color
        palette = self.native.palette()
        palette.setColor(self._background_color_role, native_color(color))
        self.native.setPalette(palette)

    def set_font(self, font):
        self.native.setFont(font._impl.native)

    ######################################################################
    # INTERFACE
    ######################################################################

    def add_child(self, child):
        child.container = self.container

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    def refresh(self):
        self.rehint()

    # A subclass will implement rehint
