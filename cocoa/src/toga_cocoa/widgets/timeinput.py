import datetime

from rubicon.objc import SEL
from travertino.constants import TRANSPARENT
from travertino.size import at_least

from ..colors import native_color
from ..libs import (
    NSCalendar,
    NSCalendarUnit,
    NSColor,
    NSDateComponents,
    NSDatePickerElementFlags,
    NSDatePickerMode,
    NSDatePickerStyle,
)
from .base import Widget
from .dateinput import TogaDatePicker


def py_time(native_time):
    components = NSCalendar.currentCalendar.components(
        NSCalendarUnit.Hour | NSCalendarUnit.Minute | NSCalendarUnit.Second,
        fromDate=native_time,
    )
    return datetime.time(components.hour, components.minute, components.second)


def native_time(py_time):
    components = NSDateComponents.alloc().init()
    components.setHour(py_time.hour)
    components.setMinute(py_time.minute)
    components.setSecond(py_time.second)
    return NSCalendar.currentCalendar.dateFromComponents(components)


class TimeInput(Widget):
    def create(self):
        self.native = TogaDatePicker.new()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.setTarget_(self.native)
        self.native.setAction_(SEL("dateInputDidChange:"))

        self.native.datePickerMode = NSDatePickerMode.Single
        self.native.datePickerStyle = NSDatePickerStyle.TextFieldAndStepper
        self.native.datePickerElements = NSDatePickerElementFlags.HourMinuteSecond

        # Ensure there are maximum and minimum times,
        # since otherwise the get_min_time and get_max_time
        # functions return None, which is problematic sometimes.
        #
        # This is already handled on startup by toga_core, but
        # the implementation also gets the min time and the max
        # time to clip when setting, which will return null on
        # the first call.
        self.set_min_time(datetime.time(0, 0, 0))
        self.set_max_time(datetime.time(23, 59, 59))

        # Add the layout constraints
        self.add_constraints()

    def get_value(self):
        return py_time(self.native.dateValue)

    def set_value(self, value):
        self.native.dateValue = native_time(value)
        self.interface.on_change()

    def rehint(self):
        self.interface.intrinsic.width = at_least(
            self.native.intrinsicContentSize().width
        )
        self.interface.intrinsic.height = self.native.intrinsicContentSize().height

    def get_min_time(self):
        return py_time(self.native.minDate)

    def set_min_time(self, value):
        self.native.minDate = native_time(value)

    def get_max_time(self):
        return py_time(self.native.maxDate)

    def set_max_time(self, value):
        self.native.maxDate = native_time(value)

    def set_color(self, color):
        if color is None:
            self.native.textColor = NSColor.controlTextColor
        else:
            self.native.textColor = native_color(color)

    def set_background_color(self, color):
        if color is TRANSPARENT:
            self.native.setBezeled(False)
            self.native.drawsBackground = False
            self.native.backgroundColor = NSColor.clearColor
        elif color is not None:
            self.native.drawsBackground = True
            # On light mode, bezeling implies that
            # the background color will not be drawn
            # properly.
            self.native.setBezeled(False)
            self.native.backgroundColor = native_color(color)
        else:
            # For some reason, only *not* drawing background
            # will draw the correct control background color
            # in dark mode.
            self.native.drawsBackground = False
            self.native.setBezeled(True)
            self.native.backgroundColor = NSColor.controlBackgroundColor
