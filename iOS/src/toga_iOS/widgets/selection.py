from rubicon.objc import CGSize, objc_method, objc_property
from travertino.size import at_least

from toga_iOS.colors import native_color
from toga_iOS.libs import (
    NSTextAlignment,
    UIColor,
    UIPickerView,
    UITextBorderStyle,
    UITextField,
)
from toga_iOS.widgets.base import Widget


class TogaPickerView(UIPickerView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def numberOfComponentsInPickerView_(self, pickerView) -> int:
        return 1

    @objc_method
    def pickerView_numberOfRowsInComponent_(self, pickerView, component: int) -> int:
        return len(self.interface.items)

    @objc_method
    def pickerView_titleForRow_forComponent_(
        self,
        pickerView,
        row: int,
        component: int,
    ):
        try:
            item = self.interface.items[int(row)]
            label = self.interface._title_for_item(item)
            return label
        except IndexError:
            # iOS can't have a fully empty picker; there's always a row 0.
            # If we get an index error, it will be because the data source
            # is empty, so return an empty string.
            return ""

    @objc_method
    def pickerView_didSelectRow_inComponent_(
        self, pickerView, row: int, component: int
    ):
        item = self.interface.items[row]
        label = self.interface._title_for_item(item)
        self.native.text = label
        self.interface.on_change()


class Selection(Widget):
    def create(self):
        self.native = UITextField.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.tintColor = UIColor.clearColor
        self.native.borderStyle = UITextBorderStyle.RoundedRect

        self.native_picker = TogaPickerView.alloc().init()
        self.native_picker.interface = self.interface
        self.native_picker.impl = self
        self.native_picker.native = self.native
        self.native_picker.delegate = self.native_picker
        self.native_picker.dataSource = self.native_picker

        self.native.inputView = self.native_picker
        self.native.delegate = self.native_picker

        # The iOS widget doesn't maintain a local concept of the number of items, so its
        # not possible to identify if the current visual display is empty during a
        # change of source. Maintain a local boolean to track when we believe our
        # local representation has no items.
        self._empty = True

        self.add_constraints()

    def set_alignment(self, value):
        self.native.textAlignment = NSTextAlignment(value)

    def set_color(self, color):
        self.native.textColor = native_color(color)

    def set_background_color(self, color):
        self.set_background_color_simple(color)

    def set_font(self, font):
        self.native.font = font._impl.native

    def rehint(self):
        # Height of a text input is known.
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(
            max(self.interface._MIN_WIDTH, fitting_size.width)
        )
        self.interface.intrinsic.height = fitting_size.height

    def _reset_selection(self):
        try:
            default_item = self.interface.items[0]
        except IndexError:
            # Deleted the last item; source is empty
            default_item = None
            self._empty = True

        self.select_item(0, default_item)

    def insert(self, index, item):
        if self._empty:
            # If you're inserting the first item, make sure it's selected
            self.select_item(index, item)
            self._empty = False
        else:
            # If you're inserting before the current selection,
            # the index of the current selection needs to be increased by 1.
            selected_index = self.native_picker.selectedRowInComponent(0)
            if index <= selected_index:
                self.native_picker.selectRow(
                    selected_index + 1, inComponent=0, animated=False
                )

        # Get rid of focus to force the user to re-open the selection
        self.native_picker.resignFirstResponder()

    def change(self, item):
        index = self.interface.items.index(item)
        if self.native_picker.selectedRowInComponent(0) == index:
            self.native.text = self.interface._title_for_item(item)

        # Get rid of focus to force the user to re-open the selection
        self.native_picker.resignFirstResponder()

        # Changing the item text can change the layout size
        self.interface.refresh()

    def remove(self, index, item):
        selection_change = self.native_picker.selectedRowInComponent(0) == index

        # Get rid of focus to force the user to re-open the selection
        self.native_picker.resignFirstResponder()

        if selection_change:
            self._reset_selection()

    def clear(self):
        self._empty = True
        # Get rid of focus to force the user to re-open the selection
        self.native_picker.resignFirstResponder()
        self._reset_selection()

    def select_item(self, index, item):
        if item is not None:
            self.native.text = self.interface._title_for_item(item)
            self.native_picker.selectRow(index, inComponent=0, animated=False)
        else:
            self.native.text = ""
        self.interface.on_change()

    def get_selected_index(self):
        if self._empty:
            return None
        return self.native_picker.selectedRowInComponent(0)
