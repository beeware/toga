from gi.repository import Gtk

from toga.interface.window import Window as WindowInterface

from .command import SEPARATOR, SPACER, EXPANDING_SPACER
from .container import Container
from .utils import wrapped_handler
from . import dialogs


class Window(WindowInterface):
    _IMPL_CLASS = Gtk.Window
    _CONTAINER_CLASS = Container
    _DIALOG_MODULE = dialogs

    def __init__(self, title=None, position=(100, 100), size=(640, 480), toolbar=None, resizeable=True, closeable=True, minimizable=True):
        super().__init__(title=title, position=position, size=size, toolbar=toolbar, resizeable=resizeable, closeable=closeable, minimizable=minimizable)
        self._create()

    def create(self):
        self._impl = self._IMPL_CLASS()
        self._impl.connect("delete-event", self._on_close)
        self._impl.set_default_size(self._size[0], self._size[1])

    def _set_title(self, title):
        self._impl.set_title(title)

    def _set_app(self, app):
        app._impl.add_window(self._impl)

    def _set_toolbar(self, items):
        self._toolbar_impl = Gtk.Toolbar()
        self._toolbar_impl.set_style(Gtk.ToolbarStyle.BOTH)
        for toolbar_item in items:
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
                toolbar_item._widgets.append(item_impl)

            self._toolbar_impl.insert(item_impl, -1)

    def _set_content(self, widget):
        self._window_layout = Gtk.VBox()

        if self._toolbar:
            self._window_layout.pack_start(self._toolbar_impl, False, False, 0)
        self._window_layout.pack_start(self._container._impl, True, True, 0)

        self._impl.add(self._window_layout)

        self._container._impl.connect('size-allocate', self._on_size_allocate)

    def show(self):
        self._impl.show_all()

    def _on_close(self, widget, data):
        self.on_close()

    def _on_size_allocate(self, widget, allocation):
        # print("ON WINDOW SIZE ALLOCATION", allocation.width, allocation.height)
        self.content._update_layout(
            width=allocation.width,
            height=allocation.height
        )

    def close(self):
        self._impl.close()
