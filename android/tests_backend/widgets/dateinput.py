import re
from abc import ABC, abstractmethod
from datetime import date

from android.content import DialogInterface

from .textinput import TextInputProbe


def py_date(native_date):
    return date.fromtimestamp(native_date / 1000)


class DateTimeInputProbe(TextInputProbe, ABC):
    @abstractmethod
    async def _check_dialog_value(self):
        pass

    @abstractmethod
    async def _change_dialog_value(self):
        pass

    async def change(self, delta):
        try:
            self.native.performClick()
            await self.redraw("Show dialog")
            assert self._dialog.isShowing()

            await self._check_dialog_value()
            await self._change_dialog_value(delta)

            self._dialog.getButton(DialogInterface.BUTTON_POSITIVE).performClick()
            await self.redraw("Click OK")
            assert not self._dialog.isShowing()
        except Exception:
            self._dialog.dismiss()  # Clean up for the next test
            raise

    @property
    def _dialog(self):
        return self.widget._impl._dialog


class DateInputProbe(DateTimeInputProbe):
    supports_limits = True

    @property
    def value(self):
        text = str(self.native.getText())
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", text)
        return date.fromisoformat(text)

    @property
    def min_value(self):
        return py_date(self._picker.getMinDate())

    @property
    def max_value(self):
        return py_date(self._picker.getMaxDate())

    async def _check_dialog_value(self):
        dialog_value = date(
            self._picker.getYear(),
            self._picker.getMonth() + 1,
            self._picker.getDayOfMonth(),
        )
        assert dialog_value == self.value

    async def _change_dialog_value(self, delta):
        new_day = self._picker.getDayOfMonth() + delta
        if not (1 <= new_day <= 28):
            raise ValueError("Cannot cross month boundaries")

        self._dialog.updateDate(
            self._picker.getYear(), self._picker.getMonth(), new_day
        )
        await self.redraw(f"Change value by {delta} days")

    @property
    def _picker(self):
        return self._dialog.getDatePicker()
