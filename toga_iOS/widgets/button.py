from __future__ import print_function, absolute_import, division, unicode_literals

from rubicon.objc import objc_method

from ..libs import *
from .base import Widget


class ButtonImpl(UIButton):
    @objc_method('v@')
    def onPress_(self, obj):
        print ("in on_press handler")
        if self.__dict__['interface'].on_press:
            self.__dict__['interface'].on_press(self.__dict__['interface'])


class Button(Widget):
    def __init__(self, label, on_press=None):
        super(Button, self).__init__()

        self.on_press = on_press
        self.label = label

        self.startup()

    def startup(self):
        self._impl = ButtonImpl.alloc().init()
        self._impl.__dict__['interface'] = self

        self._impl.setTitle_forState_(self.label, UIControlStateNormal)
        self._impl.setTitleColor_forState_(UIColor.blackColor(), UIControlStateNormal)
        self._impl.addTarget_action_forControlEvents_(self._impl, get_selector('onPress:'), UIControlEventTouchDown)

        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
