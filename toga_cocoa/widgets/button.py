from __future__ import print_function, absolute_import, division


from .base import Widget
from ..libs import *
from ..utils import process_callback


class ButtonImpl_impl(object):
    ButtonImpl = ObjCSubclass('NSButton', 'ButtonImpl')

    @ButtonImpl.method('v@')
    def onPress_(self, obj):
        if self.interface.on_press:
            process_callback(self.interface.on_press(self.interface))


ButtonImpl = ObjCClass('ButtonImpl')


class Button(Widget):
    def __init__(self, label, on_press=None):
        super(Button, self).__init__()
        self.label = label
        self.on_press = on_press

        self.startup()

    def startup(self):
        self._impl = ButtonImpl.alloc().init()
        self._impl.interface = self

        self._impl.setBezelStyle_(NSRoundedBezelStyle)
        self._impl.setButtonType_(NSMomentaryPushInButton)
        self._impl.setTitle_(get_NSString(self.label))
        self._impl.setTarget_(self._impl)
        self._impl.setAction_(get_selector('onPress:'))
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
