from travertino.size import at_least
from ..libs.android import R__attr
from ..libs.android.util import AttributeSet
from ..libs.android.view import View__MeasureSpec
from ..libs.android.widget import ProgressBar as A_ProgressBar
from .base import Widget


class ProgressBar(Widget):
    def create(self):
        progressbar = A_ProgressBar(
            self._native_activity,
            AttributeSet.__null__,
            R__attr.progressBarStyleHorizontal,
        )
        self.native = progressbar

    def start(self):
        self.set_running_style()

    def stop(self):
        self.set_stopping_style()

    @property
    def max(self):
        return self.interface.max

    def set_max(self, value):
        if value is not None:
            self.native.setMax(int(value))
        if self.interface.is_running:
            self.set_running_style()
        else:
            self.set_stopping_style()

    def set_running_style(self):
        if self.max is None:
            self.native.setIndeterminate(True)
        else:
            self.native.setIndeterminate(False)

    def set_stopping_style(self):
        self.native.setIndeterminate(False)

    def set_value(self, value):
        if value is not None:
            self.native.setProgress(int(value))

    def rehint(self):
        # Android can crash when rendering some widgets until
        # they have their layout params set. Guard for that case.
        if not self.native.getLayoutParams():
            return
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED,
            View__MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = at_least(self.native.getMeasuredHeight())
