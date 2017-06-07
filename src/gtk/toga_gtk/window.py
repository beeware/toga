from gi.repository import Gtk

from toga.interface.window import Window as WindowInterface
from toga.interface.command import GROUP_BREAK, SECTION_BREAK

from .container import Container
from .utils import wrapped_handler
from . import dialogs


class Window(WindowInterface):
    _IMPL_CLASS = Gtk.Window
    _CONTAINER_CLASS = Container
    _DIALOG_MODULE = dialogs

    def __init__(self, title=None, position=(100, 100), size=(640, 480), resizeable=True, closeable=True, minimizable=True):
        super().__init__(title=title, position=position, size=size, resizeable=resizeable, closeable=closeable, minimizable=minimizable)
        self._create()

    def create(self):
        self._impl = self._IMPL_CLASS()
        self._impl.connect("delete-event", self._on_close)
        self._impl.set_default_size(self._size[0], self._size[1])

        self._toolbar_impl = None
        self._toolbar_items = None

    def _set_title(self, title):
        self._impl.set_title(title)

    def _set_app(self, app):
        app._impl.add_window(self._impl)

    def _create_toolbar(self):
        if self._toolbar_items is None:
            self._toolbar_impl = Gtk.Toolbar()
            self._toolbar_items = {}
        else:
            for cmd, item_impl in self._toolbar_items.items():
                self._toolbar_impl.remove(item_impl)
                cmd._widgets.remove(item_impl)

        self._toolbar_impl.set_style(Gtk.ToolbarStyle.BOTH)
        for cmd in self.toolbar:
            if cmd == GROUP_BREAK:
                item_impl = Gtk.SeparatorToolItem()
                item_impl.set_draw(True)
            elif cmd == SECTION_BREAK:
                item_impl = Gtk.SeparatorToolItem()
                item_impl.set_draw(False)
            else:
                item_impl = Gtk.ToolButton()
                item_impl.set_icon_widget(cmd.icon._impl_32)
                item_impl.set_label(cmd.label)
                item_impl.set_tooltip_text(cmd.tooltip)
                item_impl.connect("clicked", wrapped_handler(cmd, cmd.action))
                cmd._widgets.append(item_impl)
            self._toolbar_items[cmd] = item_impl
            self._toolbar_impl.insert(item_impl, -1)

    def _set_content(self, widget):
        self._window_layout = Gtk.VBox()

        if self._toolbar_impl:
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
