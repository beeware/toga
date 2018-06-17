from rubicon.objc import objc_method, CGSize
from travertino.size import at_least

from toga_iOS.libs import UIColor, UIPickerView, UITextBorderStyle, UITextField

from .base import Widget


class TogaPickerView(UIPickerView):
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

    def insert(self, index, item):
        '''Listener method for ListSource'''
        self.interface.factory.not_implemented('Selection.insert()')

    def remove(self, item):
        '''Listener method for ListSource'''
        self.interface.factory.not_implemented('Selection.remove()')

    def clear(self):
        '''Listener method for ListSource'''
        self.interface.factory.not_implemented('Selection.clear()')

    def change_source(self, source):
        # Still need to clear items first...
        for row in source:
            if not self.native.text:
                self.native.text = row.label

    def select_item(self, item):
        self.interface.factory.not_implemented('Selection.select_item()')

    def get_selected_item(self):
        return self.interface.items[self.picker.selectedRowInComponent(0)]

    def set_on_select(self, handler):
        # No special handling required
        pass
