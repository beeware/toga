import toga

from .base import Widget


class MapView(Widget):
    def create(self):
        self._action("create MapView")

    def get_location(self):
        return self._get_value("location", toga.LatLng(0, 0))

    def set_location(self, position):
        self._set_value("location", position)

    def get_zoom(self):
        return self._get_value("zoom")

    def set_zoom(self, zoom):
        self._set_value("zoom", zoom)

    def add_pin(self, pin):
        self._action("add pin", pin=pin)

    def update_pin(self, pin):
        self._action("update pin", pin=pin)

    def remove_pin(self, pin):
        self._action("remove pin", pin=pin)

    def simulate_pin_selected(self, pin):
        self.interface.on_select(pin=pin)
