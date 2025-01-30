import toga


# Create the simplest possible widget with a concrete implementation that will
# allow children
class ExampleWidget(toga.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._children = []

    def _create(self):
        return self.factory.Widget(interface=self)

    def __repr__(self):
        return f"Widget(id={self.id!r})"


# Create the simplest possible widget with a concrete implementation that cannot
# have children.
class ExampleLeafWidget(toga.Widget):
    def _create(self):
        return self.factory.Widget(interface=self)

    def __repr__(self):
        return f"Widget(id={self.id!r})"


def assert_window_gain_focus(window, trigger_expected=True):
    on_gain_focus_handler = window.on_gain_focus._raw
    on_lose_focus_handler = window.on_lose_focus._raw
    if trigger_expected:
        on_gain_focus_handler.assert_called_once_with(window)
    else:
        on_gain_focus_handler.assert_not_called()
    on_lose_focus_handler.assert_not_called()

    on_gain_focus_handler.reset_mock()
    on_lose_focus_handler.reset_mock()


def assert_window_lose_focus(window, trigger_expected=True):
    on_gain_focus_handler = window.on_gain_focus._raw
    on_lose_focus_handler = window.on_lose_focus._raw
    if trigger_expected:
        on_lose_focus_handler.assert_called_once_with(window)
    else:
        on_lose_focus_handler.assert_not_called()
    on_gain_focus_handler.assert_not_called()

    on_gain_focus_handler.reset_mock()
    on_lose_focus_handler.reset_mock()


def assert_window_on_show(window, trigger_expected=True):
    on_show_handler = window.on_show._raw
    on_hide_handler = window.on_hide._raw
    if trigger_expected:
        on_show_handler.assert_called_once_with(window)
    else:
        on_show_handler.assert_not_called()
    on_hide_handler.assert_not_called()

    on_show_handler.reset_mock()
    on_hide_handler.reset_mock()


def assert_window_on_hide(window, trigger_expected=True):
    on_show_handler = window.on_show._raw
    on_hide_handler = window.on_hide._raw
    if trigger_expected:
        on_hide_handler.assert_called_once_with(window)
    else:
        on_hide_handler.assert_not_called()
    on_show_handler.assert_not_called()

    on_show_handler.reset_mock()
    on_hide_handler.reset_mock()
