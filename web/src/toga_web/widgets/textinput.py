from pyodide.ffi.wrappers import add_event_listener, remove_event_listener

from .base import Widget


class ReturnHandler:
    def __init__(self, impl):
        self.impl = impl

    def onReturn(self, handler):
        def runHandler(keyPressed):
            self.impl.interface.on_confirm(handler)

        # print(args[0].key)
        # print(args)
        return runHandler
        # print(self.impl.interface.on_confirm(None))


class TextInput(Widget):
    def create(self):
        self._return_listener = None
        self.native = self._create_native_widget("sl-input")

    def set_readonly(self, value):
        self.native.readOnly = value

    def set_placeholder(self, value):
        if value:
            self.native.placeholder = value

    def get_value(self):
        return self.native.value

    def set_value(self, value):
        self.native.value = value

    def set_font(self, font):
        pass

    def set_alignment(self, value):
        pass

    def rehint(self):
        pass

    def set_on_change(self, handler):
        pass

    def set_on_gain_focus(self, handler):
        pass

    def set_on_lose_focus(self, handler):
        pass

    def set_error(self, error_message):
        pass

    def clear_error(self):
        pass

    def is_valid(self):
        self.interface.factory.not_implemented("TextInput.is_valid()")
        return True

    def set_on_confirm(self, handler):
        # self.native.addEventListener("sl-change", handler)
        # print("Hello")
        print(self.native.id)
        if self._return_listener:
            remove_event_listener(self.native, "keyup", listener=self._return_listener)
        self._return_listener = ReturnHandler(self)
        add_event_listener(
            self.native, "keyup", self._return_listener.onReturn(handler)
        )
        # self.interface.factory.not_implemented("TextInput.on_confirm()")
