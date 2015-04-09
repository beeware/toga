from __future__ import print_function, absolute_import, division, unicode_literals

from rubicon.objc import objc_method, get_selector

from .base import Widget
from ..libs import *
from ..utils import process_callback


class ButtonImpl(NSButton):
    @objc_method('v@')
    def onPress_(self, obj):
        if self.__dict__['interface'].on_press:
            process_callback(self.__dict__['interface'].on_press(self.__dict__['interface']))

    @objc_method('v')
    def viewWillDraw(self):
        layout = self.__dict__['interface'].layout
        self.setFrame_(NSRect(NSPoint(layout.left, layout.top), NSSize(layout.width, layout.height)))


class Button(Widget):
    def __init__(self, label, on_press=None, **style):
        super(Button, self).__init__(**style)
        self.label = label
        self.on_press = on_press

        self.startup()

    def startup(self):
        self._impl = ButtonImpl.alloc().init()
        self._impl.__dict__['interface'] = self

        self._impl.setBezelStyle_(NSRoundedBezelStyle)
        self._impl.setButtonType_(NSMomentaryPushInButton)
        self._impl.setTitle_(at(self.label))
        self._impl.setTarget_(self._impl)
        self._impl.setAction_(get_selector('onPress:'))

        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        # Height of a button is known.
        if self.height is None:
            self.height = self._impl.fittingSize().height
        # Set the minimum width of a button to be a square
        if self.min_width is None:
            self.min_width = self._impl.fittingSize().width
