import random

import toga
from toga.constants import COLUMN, ROW


class MapViewApp(toga.App):
    def zoom(self, factor):
        def _zoom(widget, **kwargs):
            self.map_view.zoom = factor

        return _zoom

    def goto_perth(self, widget, **kwargs):
        self.map_view.location = (-31.9559, 115.8606)

    def goto_london(self, widget, **kwargs):
        self.map_view.location = (51.507222, -0.1275)

    def goto_austin(self, widget, **kwargs):
        self.map_view.location = (30.267222, -97.743056)

    def goto_rio(self, widget, **kwargs):
        self.map_view.location = (-22.911111, -43.205556)

    def where_am_i(self, widget, **kwargs):
        self.label.text = f"{self.map_view.location}, zoom={self.map_view.zoom}"

    def goto_pin_1(self, widget, **kwargs):
        self.map_view.location = self.pin_1.location

    def goto_pin_2(self, widget, **kwargs):
        self.map_view.location = self.pin_2.location

    def goto_pin_3(self, widget, **kwargs):
        self.map_view.location = self.pin_3.location

    def move_carmen(self, widget, **kwargs):
        self.pin_3.location = (random.uniform(-70, 70), random.uniform(-180, 180))

    def pin_selected(self, widget, pin, **kwargs):
        self.label.text = f"Pin selected: {pin}"

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow()

        self.pin_1 = toga.MapPin(
            (-41.2784, 174.7767),
            title="The Bee Hive",
            subtitle="NZ Parliament building",
        )
        self.pin_2 = toga.MapPin(
            (38.897778, -77.036389),
            title="The White House",
            subtitle="They have beehives!",
        )

        self.map_view = toga.MapView(
            flex=1,
            pins=[self.pin_1, self.pin_2],
            on_select=self.pin_selected,
        )

        # Add a pin at runtime.
        self.pin_3 = toga.MapPin(
            (32.726, -117.07714),
            title="Carmen Sandiego",
        )
        self.map_view.pins.add(self.pin_3)

        # Location buttons
        btn_perth = toga.Button("PER", on_press=self.goto_perth, flex=1)
        btn_london = toga.Button("LON", on_press=self.goto_london, flex=1)
        btn_austin = toga.Button("AUS", on_press=self.goto_austin, flex=1)
        btn_rio = toga.Button("RIO", on_press=self.goto_rio, flex=1)
        btn_where = toga.Button("???", on_press=self.where_am_i, flex=1)
        location_box = toga.Box(
            children=[btn_perth, btn_london, btn_austin, btn_rio, btn_where],
            direction=ROW,
            margin=5,
        )

        # Zoom buttons
        zoom_box = toga.Box(
            children=[
                toga.Button(i, on_press=self.zoom(i), flex=1) for i in range(0, 20, 3)
            ],
            direction=ROW,
            margin=5,
        )

        # Point Of Interest buttons
        btn_pin_1 = toga.Button("Pin 1", on_press=self.goto_pin_1, flex=1)
        btn_pin_2 = toga.Button("Pin 2", on_press=self.goto_pin_2, flex=1)
        btn_pin_3 = toga.Button("Pin 3", on_press=self.goto_pin_3, flex=1)
        btn_move = toga.Button("Move", on_press=self.move_carmen, flex=1)
        pin_box = toga.Box(
            children=[btn_pin_1, btn_pin_2, btn_pin_3, btn_move],
            direction=ROW,
            margin=5,
        )

        # Label to show responses.
        self.label = toga.Label("Ready.", margin=5)

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[self.map_view, location_box, zoom_box, pin_box, self.label],
            flex=1,
            direction=COLUMN,
        )

        # Show the main window
        self.main_window.show()


def main():
    return MapViewApp("Map View", "org.beeware.toga.examples.mapview")


if __name__ == "__main__":
    main().main_loop()
