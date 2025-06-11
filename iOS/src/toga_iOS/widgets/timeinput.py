import datetime

from rubicon.objc import SEL, CGSize
from travertino.size import at_least

from toga_iOS.libs import (
    NSCalendar,
    NSCalendarUnit,
    NSDateComponents,
    UIControlContentHorizontalAlignmentLeft,
    UIControlEventValueChanged,
    UIDatePickerMode,
)

from .base import Widget
from .dateinput import TogaDatePicker


def py_time(native_time):
    components = NSCalendar.currentCalendar.components(
        NSCalendarUnit.Hour | NSCalendarUnit.Minute,
        fromDate=native_time,
    )
    return datetime.time(components.hour, components.minute, 0)


def native_time(py_time):
    components = NSDateComponents.alloc().init()
    components.setHour(py_time.hour)
    components.setMinute(py_time.minute)
    components.setSecond(0)
    return NSCalendar.currentCalendar.dateFromComponents(components)


class TimeInput(Widget):
    def create(self):
        self.native = TogaDatePicker.new()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.delegate = self.native

        self.native.datePickerMode = UIDatePickerMode.Time
        self.native.contentHorizontalAlignment = UIControlContentHorizontalAlignmentLeft

        self.native.addTarget(
            self.native,
            action=SEL("dateInputDidChange:"),
            forControlEvents=UIControlEventValueChanged,
        )

        # Ensure there are maximum and minimum times,
        # since otherwise the get_min_time and get_max_time
        # functions return None, which is problematic sometimes.
        #
        # This is already handled on startup by toga_core, but
        # the implementation also gets the min time and the max
        # time to clip to when setting, which will return null on
        # the first call.
        self.set_min_time(datetime.time(0, 0, 0))
        self.set_max_time(datetime.time(23, 59, 0))

        # Add the layout constraints
        self.add_constraints()

    def get_value(self):
        return py_time(self.native.date)

    def set_value(self, value):
        self.native.date = native_time(value.replace(second=0, microsecond=0))
        self.interface.on_change()

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = fitting_size.height

    def get_min_time(self):
        return py_time(self.native.minimumDate)

    def set_min_time(self, value):
        self.native.minimumDate = native_time(value)

    def get_max_time(self):
        return py_time(self.native.maximumDate)

    def set_max_time(self, value):
        self.native.maximumDate = native_time(value)

    def set_color(self, color):
        # pass, since there is no reliable way to change color
        pass

    def set_background_color(self, color):
        # pass, since background color setting makes corners straight
        pass
