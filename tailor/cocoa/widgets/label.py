from tailor.cocoa.libs import *
from tailor.cocoa.widgets.base import Widget


class Label(Widget):
    def __init__(self, value=None, placeholder=None, command=None):
        super(Label, self).__init__()

        self.command = command

        self._impl = NSTextField.new()

        self._impl.setEditable_(False)
        self._impl.setBezeled_(False)
