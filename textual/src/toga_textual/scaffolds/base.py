from ..widgets.base import Scalable


class Scaffold(Scalable):
    def __init__(self, interface):
        self.interface = interface
        self._title = ""
        self._content = None
        # The window impl this scaffold is displayed in; None while not attached.
        self._window = None

    ######################################################################
    # Container interface (used by content widgets)
    ######################################################################

    @property
    def native(self):
        # Content is mounted directly onto the attached window's screen.
        return self._window.native

    @property
    def width(self):
        if self._window is None:
            return 0
        return self.scale_out_horizontal(self._window.native.size[0])

    @property
    def height(self):
        if self._window is None:
            return 0
        # Subtract 1 to remove the height of the header
        return self.scale_out_vertical(self._window.native.size[1] - 1)

    def refreshed(self):
        pass

    ######################################################################
    # Scaffold interface
    ######################################################################

    @property
    def current_container(self):
        return self

    @property
    def content(self):
        return self._content

    def set_content(self, widget):
        if self._content is not None:
            self._unmount_content()
            self._content.container = None

        self._content = widget
        if widget is not None:
            widget.container = self
            if self._window is not None:
                widget.install(parent=self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    def refresh(self):
        if self._content is not None:
            self._content.interface.refresh()

    ######################################################################
    # Attachment to a window
    ######################################################################

    def _unmount_content(self):
        if self._window is not None and self._content.native.is_attached:
            self._window.native.remove_children([self._content.native])

    def attach(self, window):
        self._window = window
        if self._content is not None:
            self._content.install(parent=self)

    def detach(self):
        if self._content is not None:
            self._unmount_content()
        self._window = None
