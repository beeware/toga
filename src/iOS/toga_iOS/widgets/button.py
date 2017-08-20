from rubicon.objc import objc_method

from toga.interface import Button as ButtonInterface

from .base import WidgetMixin
from ..libs import *
# from ..utils import process_callback


class TogaButton(UIButton):
    @objc_method
    def onPress_(self, obj) -> None:
        if self._interface.on_press:
            # process_callback(self._interface.on_press(self._interface))
            self._interface.on_press(self._interface)


class Button(ButtonInterface, WidgetMixin):
    def __init__(self, label, id=None, on_press=None, style=None, enabled=True):
        super().__init__(label, id=id, style=style, on_press=on_press, enabled=enabled)
        self._create()

    def create(self):
        self._impl = TogaButton.alloc().init()
        self._impl._interface = self

        self._impl.setTitleColor_forState_(self._impl.tintColor, UIControlStateNormal)
        self._impl.setTitleColor_forState_(UIColor.grayColor, UIControlStateDisabled)
        self._impl.addTarget_action_forControlEvents_(self._impl, SEL('onPress:'), UIControlEventTouchDown)

        # Add the layout constraints
        self._add_constraints()

    def _set_label(self, value):
        self._impl.setTitle_forState_(value, UIControlStateNormal)

    def _set_enabled(self, value):
        self._impl.enabled = value

    def _set_background_color(self, background_color):
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

            self._impl.setBordered_(False)
            self._impl.setWantsLayer_(True)
            self._impl.setBackgroundColor_(background_color)

    def rehint(self):
        fitting_size = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
