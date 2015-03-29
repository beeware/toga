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
        layout = self.__dict__['interface']._css.layout
        self.setFrame_(NSRect(NSPoint(layout.left, layout.top), NSSize(layout.width, layout.height)))


class Button(Widget):
    def __init__(self, label, on_press=None):
        super(Button, self).__init__()
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
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        # Height of a button is known and fixed.
        self.style(height=self._impl.fittingSize().height)
