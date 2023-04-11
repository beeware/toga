from toga_cocoa.libs import NSTextField, NSTextView

from .base import SimpleProbe


class TextInputProbe(SimpleProbe):
    native_class = NSTextField

    @property
    def has_focus(self):
        # When the NSTextField gets focus, a field editor is created, and that editor
        # has the original widget as the delegate. The first responder is the Field Editor.
        return isinstance(self.native.window.firstResponder, NSTextView) and (
            self.native.window.firstResponder.delegate == self.native
        )
