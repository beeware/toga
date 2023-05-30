from ..libs import (
    SEL,
    NSSecureTextField,
    objc_method,
    objc_property,
)
from .textinput import TextInput, TogaTextFieldProxy


class TogaSecureTextField(NSSecureTextField):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def textDidChange_(self, notification) -> None:
        TogaTextFieldProxy.textDidChange_(__class__, self, notification)

    @objc_method
    def becomeFirstResponder(self) -> bool:
        return TogaTextFieldProxy.becomeFirstResponder(__class__, self)

    @objc_method
    def textDidEndEditing_(self, textObject) -> None:
        TogaTextFieldProxy.textDidEndEditing_(__class__, self, textObject)

    @objc_method
    def control_textView_doCommandBySelector_(
        self,
        control,
        textView,
        selector: SEL,
    ) -> bool:
        TogaTextFieldProxy.control_textView_doCommandBySelector_(
            __class__, self, control, textView, selector
        )


class PasswordInput(TextInput):
    def _make_instance(self):
        return TogaSecureTextField.new()
