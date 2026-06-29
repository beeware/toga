from PySide6.QtWidgets import QFrame, QLabel
from toga_qt.libs import qt_text_align
from toga_qt.widgets.base import Widget
from travertino.constants import TOP
from travertino.size import at_least


class HelloWorld(Widget):
    def create(self):
        self.native = QLabel()
        self.native.setText("Hello World!")
        self.native.setFrameShape(QFrame.Shape.StyledPanel)

    def set_text_align(self, alignment):
        self.native.setAlignment(qt_text_align(alignment, TOP))

    def rehint(self):
        content_size = self.native.sizeHint()
        self.interface.intrinsic.width = at_least(content_size.width())
        self.interface.intrinsic.height = at_least(content_size.height())
