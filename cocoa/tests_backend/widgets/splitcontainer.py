from toga_cocoa.libs import NSSplitView

from .base import SimpleProbe


class SplitContainerProbe(SimpleProbe):
    native_class = NSSplitView

    @property
    def has_content(self):
        return len(self.native.documentView.subviews) > 0

    @property
    def document_height(self):
        return self.native.documentView.bounds.size.height

    @property
    def document_width(self):
        return self.native.documentView.bounds.size.width

    def move_split(self, position):
        self.native.setPosition(position, ofDividerAtIndex=0)
