from ...libs.android.view import OnClickListener, View__MeasureSpec
from ...libs.android.widget import EditText
from ..base import Widget
from abc import ABC, abstractclassmethod, abstractmethod


class TogaPickerClickListener(OnClickListener):
    def __init__(self, picker_impl):
        super().__init__()
        self.picker_impl = picker_impl

    def onClick(self, _):
        self.picker_impl._create_dialog()


class TogaPickerSetListener:
    def __init__(self, picker_impl):
        super().__init__()
        self.picker_impl = picker_impl

    def listen(self, _, *args):
        new_value = self.picker_impl.args_to_obj(*args)

        self.picker_impl._showing = False
        self.picker_impl._dialog = None
        self.picker_impl.interface.value = new_value
        if self.picker_impl.interface.on_change:
            self.picker_impl.interface.on_change(self.picker_impl)

    onDateSet = listen
    onTimeSet = listen


class PickerBase(Widget, ABC):
    @abstractclassmethod
    def _get_icon(cls):
        raise NotImplementedError

    @abstractclassmethod
    def _get_hint(cls):
        raise NotImplementedError

    @abstractclassmethod
    def obj_to_args(cls, value):
        raise NotImplementedError

    @abstractclassmethod
    def args_to_obj(cls, *args):
        raise NotImplementedError

    @abstractclassmethod
    def obj_to_str(cls, value):
        raise NotImplementedError

    @abstractclassmethod
    def str_to_obj(cls, value):
        raise NotImplementedError

    @abstractmethod
    def _get_update_fn(self):
        raise NotImplementedError

    def create(self):
        self._value = None
        self._dialog = None
        self._showing = False
        self.native = EditText(self._native_activity)
        self.native.setFocusable(False)
        self.native.setClickable(False)
        self.native.setCursorVisible(False)
        self.native.setFocusableInTouchMode(False)
        self.native.setLongClickable(False)
        self.native.setOnClickListener(TogaPickerClickListener(self))
        self.native.setCompoundDrawablesWithIntrinsicBounds(self._get_icon(), 0, 0, 0)
        self.native.setHint(self._get_hint())

    def set_value(self, value):
        if isinstance(value, str):
            value = self.str_to_obj(value)
        self._value = value
        if value is not None:
            self.native.setText(self.obj_to_str(value))
            if self._dialog is not None and self._showing:
                fn = self._get_update_fn()
                fn(*self.obj_to_args(value))

    def get_value(self):
        return self._value

    def set_on_change(self, handler):
        # nothing to do here, but it just has to exist
        pass

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
