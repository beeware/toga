from toga.interface.window import Window as WindowInterface

from .libs import *

from .container import Container
from . import dialogs


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

    # def _set_toolbar(self, items):

    def _set_content(self, widget):
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
