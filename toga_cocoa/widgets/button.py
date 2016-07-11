from rubicon.objc import objc_method, get_selector

from .base import Widget
from ..libs import *
from ..utils import process_callback


class TogaButton(NSButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface.on_press:
            process_callback(self.interface.on_press(self.interface))


class Button(Widget):
    def __init__(self, label, on_press=None, style=None):
        super(Button, self).__init__(style=style)
        self.label = label
        self.on_press = on_press

        self.startup()

    def startup(self):
        self._impl = TogaButton.alloc().init()
        self._impl.interface = self

        self._impl.setBezelStyle_(NSRoundedBezelStyle)
        self._impl.setButtonType_(NSMomentaryPushInButton)
        self._impl.setTitle_(at(self.label))
        self._impl.setTarget_(self._impl)
        self._impl.setAction_(get_selector('onPress:'))

        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setAutoresizesSubviews_(False)

        # Height of a button is known. Set the minimum width
        # of a button to be a square
        self.style.hint(
            height=self._impl.fittingSize().height,
            width=(self._impl.fittingSize().width, None)
        )
