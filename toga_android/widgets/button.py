from android.widget import Button as AndroidButton

from ..app import MobileApp
from .base import Widget


class TogaOnClickListener(implements=android.view.View[OnClickListener]):
    def __init__(self, text_view):
        self.text_view = text_view

    def onClick(self, v: android.view.View) -> void:
        Log.i("TESTAPP", "Push the button")
        if self.interface.on_press:
            self.interface.on_press(self.interface)
        self.text_view.setText(self.text_view.getText().toString() + "\nPlease Stop touching me!\n")


class Button(Widget):
    def __init__(self, label, on_press=None):
        super(Button, self).__init__()

        self.on_press = on_press
        self.label = label

        self.startup()

    def startup(self):
        self._impl = AndroidButton(App._impl)
        self._impl.setHint(self.label)

        self._listener = TogaOnClickListener(self)
        self._impl.setOnClickListener(self._listener)

        # # Height of a button is known.
        # if self.height is None:
        #     self.height = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0)).height
        # # Set the minimum width of a button to be a square
        # if self.min_width is None:
        #     self.min_width = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0)).width
