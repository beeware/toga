from toga_cocoa.libs import NSWindow, NSWindowStyleMask

from .probe import BaseProbe


class WindowProbe(BaseProbe):
    def __init__(self, app, window):
        super().__init__()
        self.app = app
        self.window = window
        self.impl = window._impl
        self.native = window._impl.native
        assert isinstance(self.native, NSWindow)

    def close(self):
        self.native.performClose(None)

    @property
    def content_size(self):
        return (
            self.native.contentView.frame.size.width,
            self.native.contentView.frame.size.height,
        )

    @property
    def is_full_screen(self):
        return bool(self.native.styleMask & NSWindowStyleMask.FullScreen)

    @property
    def is_resizable(self):
        return bool(self.native.styleMask & NSWindowStyleMask.Resizable)

    @property
    def is_closeable(self):
        return bool(self.native.styleMask & NSWindowStyleMask.Closable)

    @property
    def is_minimizable(self):
        return bool(self.native.styleMask & NSWindowStyleMask.Miniaturizable)

    @property
    def is_minimized(self):
        return bool(self.native.isMiniaturized)

    def minimize(self):
        self.native.performMiniaturize(None)

    def unminimize(self):
        self.native.deminiaturize(None)
