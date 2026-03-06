from travertino.size import at_least

from toga_cocoa.colors import native_color
from toga_cocoa.libs import NSTextAlignment, NSTextField
from toga_cocoa.widgets.base import Widget


class HelloWorld(Widget):
    def create(self):
        self.native = NSTextField.alloc().init()
        self.native.stringValue = "Hello World!"
        self.native.drawsBackground = False
        self.native.editable = False
        self.native.bezeled = True

        # Add the layout constraints
        self.add_constraints()

    def set_text_align(self, alignment):
        self.native.alignment = NSTextAlignment(alignment)

    def set_color(self, color):
        self.native.textColor = native_color(color)

    def set_font(self, font):
        self.native.font = font._impl.native

    def rehint(self):
        content_size = self.native.intrinsicContentSize()
        self.interface.intrinsic.width = at_least(content_size.width)
        self.interface.intrinsic.height = at_least(content_size.height)
