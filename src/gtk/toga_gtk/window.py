from toga.command import GROUP_BREAK, SECTION_BREAK
from toga.handlers import wrapped_handler

from . import dialogs
from .libs import Gtk


class GtkViewport:
    def __init__(self, native):
        self.native = native
        # GDK/GTK always renders at 96dpi. When HiDPI mode is enabled, it is
        # managed at the compositor level. See
        # https://wiki.archlinux.org/index.php/HiDPI#GDK_3_(GTK_3) for details
        self.dpi = 96
        self.baseline_dpi = self.dpi

    @property
    def width(self):
        # Treat `native=None` as a 0x0 viewport.
        if self.native is None:
            return 0
        return self.native.get_allocated_width()

    @property
    def height(self):
        if self.native is None:
            return 0
        return self.native.get_allocated_height()


class Window:
    _IMPL_CLASS = Gtk.Window

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        self.native = self._IMPL_CLASS()
        self.native._impl = self

        self.native.connect("delete-event", self.gtk_on_close)
        self.native.set_default_size(self.interface.size[0], self.interface.size[1])

        # Set the window deletable/closeable.
        self.native.set_deletable(self.interface.closeable)

        self.toolbar_native = None
        self.toolbar_items = None

    def set_title(self, title):
        self.native.set_title(title)

    def set_app(self, app):
        app.native.add_window(self.native)

    def create_toolbar(self):
        if self.toolbar_items is None:
            self.toolbar_native = Gtk.Toolbar()
            self.toolbar_items = {}
        else:
            for cmd, item_impl in self.toolbar_items.items():
                self.toolbar_native.remove(item_impl)
                cmd._impl.native.remove(item_impl)

        self.toolbar_native.set_style(Gtk.ToolbarStyle.BOTH)
        for cmd in self.interface.toolbar:
            if cmd == GROUP_BREAK:
                item_impl = Gtk.SeparatorToolItem()
                item_impl.set_draw(True)
            elif cmd == SECTION_BREAK:
                item_impl = Gtk.SeparatorToolItem()
                item_impl.set_draw(False)
            else:
                item_impl = Gtk.ToolButton()
                icon_impl = cmd.icon.bind(self.interface.factory)
                item_impl.set_icon_widget(icon_impl.native_32)
                item_impl.set_label(cmd.label)
                item_impl.set_tooltip_text(cmd.tooltip)
                item_impl.connect("clicked", wrapped_handler(cmd, cmd.action))
                cmd._impl.native.append(item_impl)
            self.toolbar_items[cmd] = item_impl
            self.toolbar_native.insert(item_impl, -1)

    def set_content(self, widget):
        # Construct the top-level layout, and set the window's view to
        # the be the widget's native object.
        self.layout = Gtk.VBox()

        if self.toolbar_native:
            self.layout.pack_start(self.toolbar_native, False, False, 0)
        self.layout.pack_start(widget.native, True, True, 0)

        self.native.add(self.layout)

        # Make the window sensitive to size changes
        widget.native.connect('size-allocate', self.on_size_allocate)

        # Set the widget's viewport to be based on the window's content.
        widget.viewport = GtkViewport(widget.native)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

    def show(self):
        self.native.show_all()

        # Now that the content is visible, we can do our initial hinting,
        # and use that as the basis for setting the minimum window size.
        self.interface.content._impl.rehint()
        self.interface.content.style.layout(
            self.interface.content,
            GtkViewport(native=None)
        )
        self.interface.content._impl.min_width = self.interface.content.layout.width
        self.interface.content._impl.min_height = self.interface.content.layout.height

    def gtk_on_close(self, widget, data):
        if self.interface.on_close:
            self.interface.on_close()

    def on_close(self, *args):
        pass

    def on_size_allocate(self, widget, allocation):
        #  ("ON WINDOW SIZE ALLOCATION", allocation.width, allocation.height)
        pass

    def close(self):
        self.native.close()

    def set_position(self, position):
        pass

    def set_size(self, size):
        pass

    def set_full_screen(self, is_full_screen):
        if is_full_screen:
            self.native.fullscreen()
        else:
            self.native.unfullscreen()

    def info_dialog(self, title, message):
        return dialogs.info(self.interface, title, message)

    def question_dialog(self, title, message):
        return dialogs.question(self.interface, title, message)

    def confirm_dialog(self, title, message):
        return dialogs.confirm(self.interface, title, message)

    def error_dialog(self, title, message):
        return dialogs.error(self.interface, title, message)

    def stack_trace_dialog(self, title, message, content, retry=False):
        return dialogs.stack_trace(self.interface, title, message, content, retry)

    def save_file_dialog(self, title, suggested_filename, file_types):
        return dialogs.save_file(self.interface, title, suggested_filename, file_types)

    def open_file_dialog(self, title, initial_directory, file_types, multiselect):
        '''Note that at this time, GTK does not recommend setting the initial
        directory. This function explicitly chooses not to pass it along:
        https://developer.gnome.org/gtk3/stable/GtkFileChooser.html#gtk-file-chooser-set-current-folder
        '''
        return dialogs.open_file(self.interface, title, file_types, multiselect)

    def select_folder_dialog(self, title, initial_directory, multiselect):
        '''Note that at this time, GTK does not recommend setting the initial
        directory. This function explicitly chooses not to pass it along:
        https://developer.gnome.org/gtk3/stable/GtkFileChooser.html#gtk-file-chooser-set-current-folder
        '''
        return dialogs.select_folder(self.interface, title, multiselect)
