class Scaffold:
    def __init__(self, interface):
        self.interface = interface
        self._title = ""
        self._content = None
        # The window impl this scaffold is displayed in; None while not attached.
        self._window = None

    @property
    def current_container(self):
        return self

    def _mount_content(self):
        # widget.native is a NativeProxy; window.native is a plain JsProxy, so the
        # node must be unwrapped manually before passing it to a DOM method.
        self._window.native.appendChild(self._content.native.unwrap())

    def _unmount_content(self):
        self._window.native.removeChild(self._content.native.unwrap())

    def set_content(self, widget):
        if self._content is not None and self._window is not None:
            self._unmount_content()
        self._content = widget
        if self._content is not None and self._window is not None:
            self._mount_content()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    def refresh(self):
        if self._content is not None:
            self._content.interface.refresh()

    def attach(self, window):
        self._window = window
        if self._content is not None:
            self._mount_content()

    def detach(self):
        if self._content is not None and self._window is not None:
            self._unmount_content()
        self._window = None
