from toga_cocoa.libs import (
    NSClosableWindowMask,
    NSMiniaturizableWindowMask,
    NSResizableWindowMask,
    NSWindow,
)

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
    def is_resizable(self):
        return bool(self.native.styleMask & NSResizableWindowMask)

    @property
    def is_closeable(self):
        return bool(self.native.styleMask & NSClosableWindowMask)

    @property
    def is_minimizable(self):
        return bool(self.native.styleMask & NSMiniaturizableWindowMask)

    @property
    def is_minimized(self):
        return bool(self.native.isMiniaturized)

    def minimize(self):
        self.native.performMiniaturize(None)

    def unminimize(self):
        self.native.deminiaturize(None)
