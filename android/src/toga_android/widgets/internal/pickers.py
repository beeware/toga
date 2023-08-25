from abc import ABC, abstractmethod

from travertino.size import at_least

from ...libs.android.view import OnClickListener, View__MeasureSpec
from ...libs.android.widget import EditText
from ..label import TextViewWidget


class TogaPickerClickListener(OnClickListener):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onClick(self, _):
        self.impl._dialog.show()


class PickerBase(TextViewWidget, ABC):
    @classmethod
    @abstractmethod
    def _get_icon(cls):
        raise NotImplementedError

    @abstractmethod
    def _create_dialog(self):
        raise NotImplementedError

    def create(self):
        self._dialog = self._create_dialog()
        self.native = EditText(self._native_activity)
        self.native.setFocusable(False)
        self.native.setClickable(False)
        self.native.setCursorVisible(False)
        self.native.setFocusableInTouchMode(False)
        self.native.setLongClickable(False)
        self.native.setOnClickListener(TogaPickerClickListener(self))
        self.native.setCompoundDrawablesWithIntrinsicBounds(self._get_icon(), 0, 0, 0)
        self.cache_textview_defaults()

    def rehint(self):
        self.interface.intrinsic.width = at_least(300)
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
