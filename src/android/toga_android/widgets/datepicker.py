from datetime import date, datetime

from ..libs.android import R__drawable
from ..libs.android.view import OnClickListener, View__MeasureSpec
from ..libs.android.widget import DatePickerDialog
from ..libs.android.widget import \
    DatePickerDialog__OnDateSetListener as OnDateSetListener
from ..libs.android.widget import EditText
from .base import Widget


def _date_to_milli(value):
    if isinstance(value, str):
        value = date.fromisoformat(value)
    datetime_value = datetime.combine(value, datetime.min.time())
    timestamp = datetime_value.timestamp()
    return int(timestamp * 1000)

class TogaDatePickerClickListener(OnClickListener):
    def __init__(self, picker_impl):
        super().__init__()
        self.picker_impl = picker_impl
    
    
    def onClick(self, _):
        self.picker_impl._create_dialog()


class TogaDatePickerDateSetListener(OnDateSetListener):
    def __init__(self, picker_impl):
        super().__init__()
        self.picker_impl = picker_impl

    def onDateSet(self, _, year, month, day):
        new_value = date(year, month + 1, day)
        
        self.picker_impl._showing = False
        self.picker_impl._dialog = None
        self.picker_impl.set_value(new_value)
        if self.picker_impl.interface.on_change:
            self.picker_impl.interface.on_change(self.picker_impl, new_value)
        

class DatePicker(Widget):
    def create(self):
        self._value = None
        self._dialog = None
        self._showing = False
        self.native = EditText(self._native_activity)
        self.native.setHint("YYYY-MM-DD")
        self.native.setFocusable(False)
        self.native.setClickable(False)
        self.native.setCursorVisible(False)
        self.native.setFocusableInTouchMode(False)
        self.native.setLongClickable(False)
        self.native.setCompoundDrawablesWithIntrinsicBounds(R__drawable.ic_menu_my_calendar, 0, 0, 0)
        self.native.setOnClickListener(TogaDatePickerClickListener(self))
        
    
    def set_value(self, value):
        if isinstance(value, str):
            value = date.fromisoformat(value)
        self._value = value
        if value is not None: 
            self.native.setText(value.isoformat())
            if self._dialog is not None and self._showing:
                self._dialog.updateDate(value.year, value.month - 1, value.day)
    
    def get_value(self):
        return self._value

    def set_min_date(self, value):
        if value is not None and self._dialog is not None and self._showing:
            self._dialog.getDatePicker().setMinDate(_date_to_milli(value))
        
    def set_max_date(self, value):
        if value is not None and self._dialog is not None and self._showing:
            self._dialog.getDatePicker().setMaxDate(_date_to_milli(value))

    def set_on_change(self, handler):
        # nothing to do here, but it just has to exist
        pass

    def rehint(self):
        self.interface.intrinsic.width = self.native.getMeasuredWidth()
        # Refuse to call measure() if widget has no container, i.e., has no LayoutParams.
        # On Android, EditText's measure() throws NullPointerException if the widget has no
        # LayoutParams.
        if not self.native.getLayoutParams():
            return
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
    
    def _create_dialog(self):
        self._dialog = DatePickerDialog(self._native_activity)
        self._showing = True
        self.set_value(self.get_value())
        self.set_min_date(self.interface._min_date)
        self.set_max_date(self.interface._max_date)
        self._dialog.setOnDateSetListener(TogaDatePickerDateSetListener(self))
        self._dialog.show()
