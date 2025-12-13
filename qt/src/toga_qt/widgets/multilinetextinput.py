from PySide6.QtWidgets import QTextEdit
from travertino.constants import TOP
from travertino.size import at_least

from ..libs import qt_text_align
from .base import Widget


class MultilineTextInput(Widget):
    def create(self):
        self.native = QTextEdit()
        self.native.setAcceptRichText(False)
        self.native.textChanged.connect(self.qt_on_change)

    def qt_on_change(self):
        self.interface.on_change()

    def get_readonly(self):
        return self.native.isReadOnly()

    def set_readonly(self, value):
        self.native.setReadOnly(value)

    def get_placeholder(self):
        return self.native.placeholderText()

    def set_placeholder(self, value):
        self.native.setPlaceholderText(value)

    def get_value(self):
        return self.native.toPlainText()

    def set_value(self, value):
        self.native.setPlainText(value)

    def set_text_align(self, alignment):
        text_option = self.native.document().defaultTextOption()
        text_option.setAlignment(qt_text_align(alignment, TOP))
        self.native.document().setDefaultTextOption(text_option)

    def scroll_to_bottom(self):
        scrollbar = self.native.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def scroll_to_top(self):
        scrollbar = self.native.verticalScrollBar()
        scrollbar.setValue(scrollbar.minimum())

    def rehint(self):
        size = self.native.sizeHint()
        self.interface.intrinsic.width = at_least(
            max(self.interface._MIN_WIDTH, size.width())
        )
        self.interface.intrinsic.height = at_least(
            max(self.interface._MIN_HEIGHT, size.height())
        )
