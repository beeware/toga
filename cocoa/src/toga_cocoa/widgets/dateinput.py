import datetime

from rubicon.objc import SEL, objc_method, objc_property
from travertino.constants import TRANSPARENT
from travertino.size import at_least

from toga.widgets.dateinput import MAX_DATE, MIN_DATE
from toga_cocoa.colors import native_color

from ..libs import (
    NSCalendar,
    NSCalendarUnit,
    NSColor,
    NSDateComponents,
    NSDatePicker,
    NSDatePickerElementFlags,
    NSDatePickerMode,
    NSDatePickerStyle,
)
from .base import Widget


class TogaDatePicker(NSDatePicker):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def dateInputDidChange_(self, dateInput) -> None:
        self.interface.on_change()


def py_date(native_date):
    components = NSCalendar.currentCalendar.components(
        NSCalendarUnit.Year | NSCalendarUnit.Month | NSCalendarUnit.Day,
        fromDate=native_date,
    )
    return datetime.date(components.year, components.month, components.day)


def native_date(py_date):
    components = NSDateComponents.alloc().init()
    components.setYear(py_date.year)
    components.setMonth(py_date.month)
    components.setDay(py_date.day)
    return NSCalendar.currentCalendar.dateFromComponents(components)


class DateInput(Widget):
    def create(self):
        self.native = TogaDatePicker.new()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.setTarget_(self.native)
        self.native.setAction_(SEL("dateInputDidChange:"))

        self.native.datePickerMode = NSDatePickerMode.Single
        self.native.datePickerStyle = NSDatePickerStyle.TextFieldAndStepper
        self.native.datePickerElements = NSDatePickerElementFlags.YearMonthDay

        # Ensure there are maximum and minimum dates,
        # since otherwise the get_min_date and get_max_date
        # functions return None, which is problematic sometimes.
        #
        # This is already handled on startup by toga_core, but
        # the implementation also gets the min date and the max
        # date to clip when setting, which will return null on
        # the first call.
        self.set_min_date(MIN_DATE)
        self.set_max_date(MAX_DATE)

        # Add the layout constraints
        self.add_constraints()

    def get_value(self):
        return py_date(self.native.dateValue)

    def set_value(self, value):
        self.native.dateValue = native_date(value)
        self.interface.on_change()

    def rehint(self):
        self.interface.intrinsic.width = at_least(
            self.native.intrinsicContentSize().width
        )
        self.interface.intrinsic.height = self.native.intrinsicContentSize().height

    def get_min_date(self):
        return py_date(self.native.minDate)

    def set_min_date(self, value):
        self.native.minDate = native_date(value)

    def get_max_date(self):
        return py_date(self.native.maxDate)

    def set_max_date(self, value):
        self.native.maxDate = native_date(value)

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
