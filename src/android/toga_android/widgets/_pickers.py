from ..libs.android.view import OnClickListener, View__MeasureSpec
from ..libs.android.widget import EditText
from .base import Widget


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
        new_value = self.picker_impl._to_obj_converter_class(*self.picker_impl._value_pack_fn(*args))

        self.picker_impl._showing = False
        self.picker_impl._dialog = None
        self.picker_impl.interface.value = new_value
        if self.picker_impl.interface.on_change:
            self.picker_impl.interface.on_change(self.picker_impl)

    onDateSet = listen
    onTimeSet = listen


class PickerBase(Widget):
    _icon = None
    _hint = None
    _to_obj_converter_class = None
    _to_str_converter_kwargs = None
    _dialog_class = None
    _update_dialog_name = None
    _value_unpack_fn = None
    _value_pack_fn = None
    _extra_dialog_setters = None
    _extra_dialog_args = None
    _dialog_listener_class = None

    def __init__(self, interface):
        super().__init__(interface)
        if None in (
            self._icon,
            self._hint,
            self._to_obj_converter_class,
            self._to_str_converter_kwargs,
            self._dialog_class,
            self._update_dialog_name,
            self._value_unpack_fn,
            self._value_pack_fn,
            self._extra_dialog_setters,
            self._extra_dialog_args,
            self._dialog_listener_class
        ):
            raise ValueError("You have to subclass the picker class and define some fields!")

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
        self.native.setCompoundDrawablesWithIntrinsicBounds(self._icon, 0, 0, 0)
        self.native.setHint(self._hint)

    def set_value(self, value):
        if isinstance(value, str):
            value = self._to_obj_converter_class.fromisoformat(value)
        self._value = value
        if value is not None:
            self.native.setText(value.isoformat(**self._to_str_converter_kwargs))
            if self._dialog is not None and self._showing:
                fn = getattr(self._dialog, self._update_dialog_name)
                fn(*self._value_unpack_fn(value))

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

    def _create_dialog(self):
        listener = type("Listener", (TogaPickerSetListener, self._dialog_listener_class), {})
        self._dialog = self._dialog_class(self._native_activity, listener(self), *self._value_unpack_fn(self._value), *self._extra_dialog_args)
        self._showing = True
        for setter_name in self._extra_dialog_setters:
            setter = getattr(self, f"set_{setter_name}")
            setter(getattr(self.interface, f"_{setter_name}"))
        self._dialog.show()
