from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider
from travertino.size import at_least

from toga.widgets.slider import IntSliderImpl

from .base import Widget


class Slider(Widget, IntSliderImpl):
    def create(self):
        IntSliderImpl.__init__(self)
        self.native = QSlider(Qt.Orientation.Horizontal)
        self.native.setMinimum(0)
        self.native.setTickInterval(1)
        self.native.valueChanged.connect(self.qt_on_change)
        self.native.sliderPressed.connect(self.qt_on_press)
        self.native.sliderReleased.connect(self.qt_on_release)

    def qt_on_change(self, value):
        self.on_change()

    def qt_on_press(self):
        self.interface.on_press()

    def qt_on_release(self):
        self.interface.on_release()

    def get_int_value(self) -> int:
        return self.native.value()

    def set_int_value(self, value: int) -> None:
        self.native.setValue(value)

    def get_int_max(self) -> int:
        return self.native.maximum()

    def set_int_max(self, max: int) -> None:
        self.native.setMaximum(max)

    def set_ticks_visible(self, visible: bool) -> None:
        if visible:
            self.native.setTickPosition(QSlider.TickPosition.TicksBelow)
        else:
            self.native.setTickPosition(QSlider.TickPosition.NoTicks)

    def rehint(self):
        size = self.native.sizeHint()
        self.interface.intrinsic.width = at_least(
            max(self.interface._MIN_WIDTH, size.width())
        )
        self.interface.intrinsic.height = size.height()
