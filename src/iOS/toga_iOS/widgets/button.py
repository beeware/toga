from rubicon.objc import objc_method
from .base import Widget
from ..libs import *


# from ..utils import process_callback


class TogaButton(UIButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface.on_press:
            self.interface.on_press(self.interface)


class Button(Widget):
    def create(self):
        self.native = TogaButton.alloc().init()
        self.native.interface = self.interface

        self.native.setTitleColor_forState_(self.native.tintColor, UIControlStateNormal)
        self.native.setTitleColor_forState_(UIColor.grayColor, UIControlStateDisabled)
        self.native.addTarget_action_forControlEvents_(self.native, SEL('onPress:'), UIControlEventTouchDown)

        # Add the layout constraints
        self.add_constraints()

    def set_label(self, label):
        self.native.setTitle_forState_(label, UIControlStateNormal)

    def set_on_press(self, handler):
        pass

    def set_background_color(self, background_color):
        if background_color:
            if isinstance(background_color, tuple):
                background_color = NSColor.colorWithRed_green_blue_alpha_(background_color[0]/255,
                                                    background_color[1]/255,
                                                    background_color[2]/255, 1.0)
            elif isinstance(background_color, str):
                try:
                    background_color = NSColorUsingColorName(background_color.upper())
                except:
                    raise ValueError('Background color %s does not exist, try a RGB number (red, green, blue).' % background_color)
            else:
                raise ValueError('_set_background_color on button widget must receive a tuple or a string')

            self.native.setBordered_(False)
            self.native.setWantsLayer_(True)
            self.native.setBackgroundColor_(background_color)

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.interface.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
