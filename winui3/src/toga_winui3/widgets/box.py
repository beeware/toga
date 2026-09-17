from win32more.Microsoft.UI.Xaml.Controls import Canvas

from .base import Widget


class Box(Widget):
    def create(self):
        # Setting native_cls defines self.native and means that events are managed by
        # the nativeevents module.
        self.native_cls = Canvas

        # Box cannot receive input focus, so remove it from the tab sequence.
        self.native.IsTabStop = False

    ####################################################################################
    # Overrides of methods called by the Toga style applicator.
    ####################################################################################

    def set_color(self, font):
        # Canvas has no Foreground attributes to set.
        pass

    def set_font(self, font):
        # Canvas has no font attributes to set.
        pass
