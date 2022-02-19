from ...libs.android.view import OnClickListener, View__MeasureSpec
from ...libs.android.widget import EditText
from ..base import Widget
from abc import ABC, abstractclassmethod


class TogaPickerClickListener(OnClickListener):
    def __init__(self, picker_impl):
        super().__init__()
        self.picker_impl = picker_impl

    def onClick(self, _):
        self.picker_impl._create_dialog()


class PickerBase(Widget, ABC):
    @abstractclassmethod
    def _get_icon(cls):
        raise NotImplementedError

    @abstractclassmethod
    def _get_hint(cls):
        raise NotImplementedError

    def create(self):
        self._value = None
        self._dialog = None
        self.native = EditText(self._native_activity)
        self.native.setFocusable(False)
        self.native.setClickable(False)
        self.native.setCursorVisible(False)
        self.native.setFocusableInTouchMode(False)
        self.native.setLongClickable(False)
        self.native.setOnClickListener(TogaPickerClickListener(self))
        self.native.setCompoundDrawablesWithIntrinsicBounds(self._get_icon(), 0, 0, 0)
        self.native.setHint(self._get_hint())

    def rehint(self):
        self.interface.intrinsic.width = self.native.getMeasuredWidth()
        # Refuse to call measure() if widget has no container, i.e., has no LayoutParams.
        # On Android, EditText's measure() throws NullPointerException if the widget has no
        # LayoutParams.
        if not self.native.getLayoutParams():
            return
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
