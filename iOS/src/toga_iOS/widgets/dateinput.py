import datetime

from rubicon.objc import SEL, CGSize, objc_method, objc_property
from travertino.size import at_least

from toga.widgets.dateinput import MAX_DATE, MIN_DATE
from toga_iOS.libs import (
    NSCalendar,
    NSCalendarUnit,
    NSDateComponents,
    UIControlContentHorizontalAlignmentLeft,
    UIControlEventValueChanged,
    UIDatePicker,
    UIDatePickerMode,
)

from .base import Widget


class TogaDatePicker(UIDatePicker):
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
        self.native.delegate = self.native

        self.native.datePickerMode = UIDatePickerMode.Date
        self.native.contentHorizontalAlignment = UIControlContentHorizontalAlignmentLeft

        self.native.addTarget(
            self.native,
            action=SEL("dateInputDidChange:"),
            forControlEvents=UIControlEventValueChanged,
        )

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
        return py_date(self.native.date)

    def set_value(self, value):
        self.native.date = native_date(value)
        self.interface.on_change()

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = fitting_size.height

    def get_min_date(self):
        return py_date(self.native.minimumDate)

    def set_min_date(self, value):
        self.native.minimumDate = native_date(value)

    def get_max_date(self):
        return py_date(self.native.maximumDate)

    def set_max_date(self, value):
        self.native.maximumDate = native_date(value)

    def set_color(self, color):
        # pass, since there is no reliable way to change color
        pass

    def set_background_color(self, color):
        # pass, since background color setting makes corners straight
        pass
