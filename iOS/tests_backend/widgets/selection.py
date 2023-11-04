import asyncio

from pytest import xfail

from toga_iOS.libs import UIPickerView, UITextField

from .base import SimpleProbe
from .properties import toga_alignment, toga_color


class SelectionProbe(SimpleProbe):
    native_class = UITextField

    def __init__(self, widget):
        super().__init__(widget)
        self.native_picker = widget._impl.native_picker
        assert isinstance(self.native_picker, UIPickerView)

    def assert_resizes_on_content_change(self):
        xfail("Selection doesn't resize on content changes")

    @property
    def alignment(self):
        return toga_alignment(self.native.textAlignment)

    def assert_vertical_alignment(self, expected):
        # Vertical alignment isn't configurable on UITextField
        pass

    @property
    def color(self):
        return toga_color(self.native.textColor)

    @property
    def titles(self):
        count = self.native_picker.pickerView(
            self.native_picker, numberOfRowsInComponent=0
        )

        titles = [
            str(
                self.native_picker.pickerView(
                    self.native_picker,
                    titleForRow=index,
                    forComponent=0,
                )
            )
            for index in range(0, count)
        ]
        # iOS can't show a completely empty selection
        # For test normalization, convert the "empty" selection to []
        if titles == [""]:
            return []
        return titles

    @property
    def selected_title(self):
        title = str(self.native.text)
        picker_title = self.native_picker.pickerView(
            self.native_picker,
            titleForRow=self.native_picker.selectedRowInComponent(0),
            forComponent=0,
        )

        # Check the picker and the text display agree about the selected item
        assert title == str(picker_title)

        if title == "":
            # iOS can't show a completely empty selection
            # For test normalization, convert the "empty" selection to None
            return None
        return title

    async def select_item(self):
        self.widget.focus()
        self.native_picker.selectRow(1, inComponent=0, animated=True)
        self.native_picker.pickerView(self.native_picker, didSelectRow=1, inComponent=0)
        await asyncio.sleep(0.1)
