from __future__ import print_function, absolute_import, division

from gi.repository import Gtk

from .utils import wrapped_handler
from .command import SEPARATOR, SPACER, EXPANDING_SPACER


class Window(object):
    _IMPL_CLASS = Gtk.Window

    def __init__(self, title=None, position=(100, 100), size=(640, 480), toolbar=None):
        self._app = None
        self._impl = None
        self._container = None
        self._size = size
        self._toolbar = None
        self.title = title
        self.position = position
        self.toolbar = toolbar

    def _startup(self):
        self._impl = self._IMPL_CLASS()
        self._impl.connect("delete-event", self._on_close)
        self._impl.set_default_size(self._size[0], self._size[1])

        # If there are toolbar items defined, add a toolbar to the window
        if self.toolbar:
            self._container = Gtk.VBox()
            self._toolbar = Gtk.Toolbar()
            self._toolbar.set_style(Gtk.ToolbarStyle.BOTH)
            for toolbar_item in self.toolbar:
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

                self._toolbar.insert(item_impl, -1)

        self.on_startup()

        if self.content:
            # Assign the widget to the same app as the window.
            # This initiates startup logic.
            self.content.app = self.app
            self._set_content()

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")

        self._app = app
        self._startup()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self
        if self._impl:
            # Assign the widget to the same app as the window.
            # This initiates startup logic.
            widget.app = self.app
            self._set_content()

    def _set_content(self):
        if self._container:
            self._container.pack_start(self._toolbar, True, True, 0)
            self._container.pack_start(self.content._impl, True, True, 0)
            self._impl.add(self._container)
        else:
            self._impl.add(self.content._impl)

    def show(self):
        self._impl.show_all()

    def on_startup(self):
        pass

    def _on_close(self, widget, data):
        self.on_close()

    def on_close(self):
        pass
