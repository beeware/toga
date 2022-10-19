from rubicon.objc import CGSize, objc_method, objc_property
from travertino.size import at_least

from toga_iOS.libs import UIColor, UIPickerView, UITextBorderStyle, UITextField
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
    def pickerView_titleForRow_forComponent_(self, pickerView, row: int, component: int):
        return str(self.interface.items[row])

    @objc_method
    def pickerView_didSelectRow_inComponent_(self, pickerView, row: int, component: int):
        self.native.text = self.interface.items[row]
        if self.interface.on_select:
            self.interface.on_select(self.interface)


class Selection(Widget):
    def create(self):
        self.native = UITextField.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.tintColor = UIColor.clearColor
        self.native.borderStyle = UITextBorderStyle.RoundedRect

        self.picker = TogaPickerView.alloc().init()
        self.picker.interface = self.interface
        self.picker.native = self.native
        self.picker.delegate = self.picker
        self.picker.dataSource = self.picker

        self.native.inputView = self.picker
        self.native.delegate = self.picker

        self.add_constraints()

    def rehint(self):
        # Height of a text input is known.
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(fitting_size.width)
        self.interface.intrinsic.height = fitting_size.height

    def remove_all_items(self):
        # No special handling required
        pass

    def add_item(self, item):
        if not self.native.text:
            self.native.text = item

    def select_item(self, item):
        self.interface.factory.not_implemented('Selection.select_item()')

    def get_selected_item(self):
        return self.interface.items[self.picker.selectedRowInComponent(0)]

    def set_on_select(self, handler):
        # No special handling required
        pass
