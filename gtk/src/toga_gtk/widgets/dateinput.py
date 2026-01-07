import datetime

from travertino.size import at_least

from toga.widgets.dateinput import MAX_DATE, MIN_DATE

from ..libs import GTK_VERSION, GLib, Gtk
from .base import Widget


def py_date(native_date):
    if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
        year, month, day = native_date
        return datetime.date(year, month + 1, day)
    else:  # pragma: no-cover-if-gtk3
        return datetime.date(
            native_date.get_year(),
            native_date.get_month(),
            native_date.get_day_of_month(),
        )


def native_date(py_date):
    if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
        return py_date.year, py_date.month - 1, py_date.day
    else:  # pragma: no-cover-if-gtk3
        return GLib.DateTime.new_local(
            py_date.year, py_date.month, py_date.day, 0, 0, 0
        )


class DateInput(Widget):
    def create(self):
        self.native = Gtk.Calendar()

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

        self.native.connect("day-selected", self.gtk_on_change)
        self.native.connect("next-month", self.gtk_on_change)
        self.native.connect("next-year", self.gtk_on_change)
        self.native.connect("prev-month", self.gtk_on_change)
        self.native.connect("prev-year", self.gtk_on_change)
        self._suppress_signals = False

    def get_value(self):
        return py_date(self.native.get_date())

    def set_value(self, value):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            year, month, day = native_date(value)

            self.native.select_month(month=month, year=year)
            self.native.select_day(day=day)
        else:  # pragma: no-cover-if-gtk3
            # The signal must be emitted manually on GTK4,
            # as no signal is emitted when switching between
            # years without changing date.  Emission of signals
            # on programmatic change in GTK4 is also undocumented
            # behavior, as the docs implies that the signals
            # we connect to emits on user action only.
            self._suppress_signals = True
            try:
                self.native.select_day(native_date(value))
            finally:
                self._suppress_signals = False
            self.gtk_on_change()

    def rehint(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            width = self.native.get_preferred_width()
            height = self.native.get_preferred_height()

            self.interface.intrinsic.width = at_least(width[0])
            self.interface.intrinsic.height = height[0]
        else:  # pragma: no-cover-if-gtk3
            min_size, _ = self.native.get_preferred_size()
            self.interface.intrinsic.width = at_least(min_size.width)
            self.interface.intrinsic.height = min_size.height

    def get_min_date(self):
        return py_date(self.native.minDate)

    def set_min_date(self, value):
        self.native.minDate = native_date(value)

    def get_max_date(self):
        return py_date(self.native.maxDate)

    def set_max_date(self, value):
        self.native.maxDate = native_date(value)

    def gtk_on_change(self, *_args):
        if self._suppress_signals:  # pragma: no-cover-if-gtk3
            return
        current_date = self.get_value()
        min_date = self.get_min_date()
        max_date = self.get_max_date()

        if current_date < min_date:
            self.set_value(min_date)
        elif current_date > max_date:
            self.set_value(max_date)

        self.interface.on_change()
