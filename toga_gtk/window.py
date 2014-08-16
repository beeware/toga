from __future__ import print_function, absolute_import, division

from gi.repository import Gtk

from .utils import wrapped_handler
from .command import SEPARATOR, SPACER, EXPANDING_SPACER


class Window(object):
    _IMPL_CLASS = Gtk.Window

    def __init__(self, title=None, position=(100, 100), size=(640, 480), toolbar=None):
        self._app = None
        self._container = None
        self._size = size
        self._toolbar_impl = None

        self.title = title
        self.position = position

        self.startup()

        self.toolbar = toolbar

    def startup(self):
        self._impl = self._IMPL_CLASS()
        self._impl.connect("delete-event", self._on_close)
        self._impl.set_default_size(self._size[0], self._size[1])

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")

        self._app = app

    @property
    def toolbar(self):
        return self._toolbar

    @toolbar.setter
    def toolbar(self, value):
        # If there are toolbar items defined, add a toolbar to the window
        self._toolbar = value
        if self._toolbar:
            self._toolbar_impl = Gtk.Toolbar()
            self._toolbar_impl.set_style(Gtk.ToolbarStyle.BOTH)
            for toolbar_item in self._toolbar:
                if toolbar_item in (SEPARATOR, SPACER, EXPANDING_SPACER):
                    item_impl = Gtk.SeparatorToolItem()
                    if toolbar_item == EXPANDING_SPACER:
                        item_impl.set_expand(True)
                    item_impl.set_draw(toolbar_item == SEPARATOR)
                else:
                    item_impl = Gtk.ToolButton()
                    item_impl.set_icon_widget(toolbar_item.icon._impl_32)
                    item_impl.set_label(toolbar_item.label)
                    item_impl.set_tooltip_text(toolbar_item.tooltip)
                    item_impl.connect("clicked", wrapped_handler(toolbar_item, toolbar_item.action))

                self._toolbar_impl.insert(item_impl, -1)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self
        self._content.app = self.app

        self._container = Gtk.VBox()

        if self._toolbar:
            self._container.pack_start(self._toolbar_impl, True, True, 0)
        self._container.pack_start(self.content._impl, True, True, 0)
        self._impl.add(self._container)

    def show(self):
        self._impl.show_all()

    def _on_close(self, widget, data):
        self.on_close()

    def on_close(self):
        pass
