from travertino.size import at_least

from toga_iOS.libs import CGSize, UIProgressView, UIProgressViewStyle
from toga_iOS.widgets.base import Widget


class ProgressBar(Widget):

    def create(self):
        self.native = UIProgressView.alloc().initWithProgressViewStyle_(UIProgressViewStyle.Default)
        self.add_constraints()

    def start(self):
        # Indeterminate progress is not supported for UIProgressView in iOS
        pass

    def stop(self):
        pass

    def set_value(self, value):
        if self.interface.max is not None:
            self.native.setProgress_animated_(
                self.interface.value / self.interface.max,
                True
            )

    def set_max(self, value):
        pass

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = fitting_size.height
