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

    async def change(self):
        try:
            self._dialog.show()
            await self.redraw("Show dialog")

            await self._check_dialog_value()
            await self._change_dialog_value()

            self._dialog.getButton(DialogInterface.BUTTON_POSITIVE).performClick()
            await self.redraw("Click OK")
        except Exception:
            self._dialog.dismiss()
            raise

    @property
    def _dialog(self):
        return self.widget._impl._dialog


class DateInputProbe(DateTimeInputProbe):
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

    async def _change_dialog_value(self):
        next_day = self._picker.getDayOfMonth() + 1
        if next_day > 28:
            next_day = 1

        self._dialog.updateDate(
            self._picker.getYear(), self._picker.getMonth(), next_day
        )
        await self.redraw("Increment day")

    @property
    def _picker(self):
        return self._dialog.getDatePicker()
