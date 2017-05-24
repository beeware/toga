from toga.interface.window import Window as WindowInterface

from .libs import *

from .container import Container
from . import dialogs
from .command import SEPARATOR, SPACER, EXPANDING_SPACER

"""
According to:
https://msdn.microsoft.com/en-us/library/windows/desktop/ms647553(v=vs.85).aspx
"The system assigns a position value to all items in a menu, including separators."
For this reason I have not assigned Index values to any menu items. -- Bruce Eckel
"""

def menu_item(menu_text, on_click_function):
    "Create a single item on a menu"
    _menu_item = WinForms.MenuItem()
    _menu_item.Text = menu_text
    _menu_item.Click += on_click_function
    # How you assign the Index, in case it's actually necessary:
    # _menu_item.Index = 4
    return _menu_item

def menu(menu_text, menu_items):
    "Create one drop-down menu for the menu bar"
    _menu = WinForms.MenuItem()
    _menu.Text = menu_text
    for item in menu_items:
        _menu.MenuItems.Add(item)
    # How you assign the Index, in case it's actually necessary:
    # _menu.Index = 3
    return _menu

def menu_bar(menus):
    "Assemble the menus into a menu bar"
    _menu_bar = WinForms.MainMenu()
    _menu_bar.MenuItems.AddRange(menus)
    return _menu_bar

class Window(WindowInterface):
    # _IMPL_CLASS = WinForms.Form
    _CONTAINER_CLASS = Container
    _DIALOG_MODULE = dialogs

    def __init__(self, title=None, position=(100, 100), size=(640, 480), toolbar=None, resizeable=True, closeable=True, minimizable=True):
        super().__init__(title=title, position=position, size=size, toolbar=toolbar, resizeable=resizeable, closeable=closeable, minimizable=minimizable)
        self._create()

    def create(self):
        self._impl = WinForms.Form(self)
        self._impl.ClientSize = Size(self._size[0], self._size[1])
        self._impl.Resize += self._on_resize

        self._impl.Menu = menu_bar((
            # Add more menus as needed:
            menu("&File", (
                # Add more menu items as needed:
                menu_item("&Exit", self.file_exit_on_click),
            )),
            menu("&Help", (
                menu_item("&About", self.help_about_on_click),
            )),
        ))

    def file_exit_on_click(self, sender, args):
        print("Stub file exit")

    def help_about_on_click(self, sender, args):
        print("Stub help about...")

    def _set_toolbar(self, items):
        self._toolbar_impl = WinForms.ToolStrip()
        for toolbar_item in items:
            if toolbar_item == SEPARATOR:
                item_impl = WinForms.ToolStripSeparator()
            elif toolbar_item == SPACER:
                item_impl = WinForms.ToolStripSeparator()
            elif toolbar_item == EXPANDING_SPACER:
                item_impl = WinForms.ToolStripSeparator() # todo: check how this behaves on other platforms
            else:
                item_impl = WinForms.ToolStripButton()
            self._toolbar_impl.Items.Add(item_impl)


    def _set_content(self, widget):
        if (self.toolbar):
            self._impl.Controls.Add(self._toolbar_impl)

        self._impl.Controls.Add(widget._container._impl)

    def _set_title(self, title):
        self._impl.Text = title

    def show(self):
        # The first render of the content will establish the
        # minimum possible content size; use that to enforce
        # a minimum window size.
        TITLEBAR_HEIGHT = 36
        self._impl.MinimumSize = Size(
            int(self.content.layout.width),
            int(self.content.layout.height) + TITLEBAR_HEIGHT
        )

        # Set the size of the container to be the same as the window
        self._container._impl.Size = self._impl.ClientSize

        # Do the first layout render.
        self._container._update_layout(
            width=self._impl.ClientSize.Width,
            height=self._impl.ClientSize.Height,
        )

    def close(self):
        self._impl.Close()


    def _on_resize(self, sender, args):
        if self.content:
            # Set the size of the container to be the same as the window
            self._container._impl.Size = self._impl.ClientSize
            # Re-layout the content
            self.content._update_layout(
                width=sender.ClientSize.Width,
                height=sender.ClientSize.Height,
            )
