import datetime

from rubicon.objc import SEL, CGSize, objc_method, objc_property

from toga_iOS.libs import (
    NSCalendar,
    NSCalendarUnit,
    NSDateComponents,
    UIControlEventValueChanged,
    UIDatePicker,
    UIDatePickerMode,
)
from toga_iOS.widgets.base import Widget


class TogaDatePicker(UIDatePicker):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def dateInputDidChange_(self, dateInput) -> None:
        self.interface._value_changed()


def py_date(native_date):
    components = NSCalendar.currentCalendar.components(
        NSCalendarUnit(
            NSCalendarUnit.Year.value
            | NSCalendarUnit.Month.value
            | NSCalendarUnit.Day.value
        ),
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

        self.native.addTarget(
            self.native,
            action=SEL("dateInputDidChange:"),
            forControlEvents=UIControlEventValueChanged,
        )

        self._toga_max_date = datetime.date(8999, 1, 1)
        self._toga_min_date = datetime.date(1800, 1, 1)

        # Ensure that we always have maximum and minimum dates,
        # since otherwise the get_min_date and get_max_date
        # functions return None, which is problematic sometimes.
        self.set_min_date(self._toga_min_date)
        self.set_max_date(self._toga_max_date)

        # Add the layout constraints
        self.add_constraints()

    def get_value(self):
        return py_date(self.native.date)

    def set_value(self, value):
        self.native.date = native_date(value)
        self.interface._value_changed()

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = fitting_size.width
        self.interface.intrinsic.height = fitting_size.height

    def get_min_date(self):
        return py_date(self.native.minimumDate)

    def normalize_date(self, value):
        if value < self._toga_min_date:
            value = self._toga_min_date
        if value > self._toga_max_date:
            value = self._toga_max_date
        return value

    def set_min_date(self, value):
        value = self.normalize_date(value)
        self.native.minimumDate = native_date(value)

    def get_max_date(self):
        return py_date(self.native.maximumDate)

    def set_max_date(self, value):
        value = self.normalize_date(value)
        self.native.maximumDate = native_date(value)
