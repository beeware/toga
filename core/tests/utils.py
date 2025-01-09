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


def assert_window_event_triggered(window, expected_event=None):
    window_events = {
        window.on_gain_focus,
        window.on_lose_focus,
        window.on_show,
        window.on_hide,
    }
    unexpected_events = window_events - {expected_event}

    if expected_event:
        expected_event._raw.assert_called_once_with(window)

    for unexpected_event in unexpected_events:
        if unexpected_event._raw is not None:
            unexpected_event._raw.assert_not_called()

    for event in window_events:
        if event._raw is not None:
            event._raw.reset_mock()
