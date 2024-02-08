import random

import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class ExampleMapViewApp(toga.App):
    def zoom(self, factor):
        def _zoom(widget, **kwargs):
            self.map_view.zoom = factor

        return _zoom

    def goto_perth(self, widget, **kwargs):
        self.map_view.location = (-31.9513, 115.8553)

    def goto_london(self, widget, **kwargs):
        self.map_view.location = (51.5098, -0.1181)

    def goto_austin(self, widget, **kwargs):
        self.map_view.location = (30.2666, -97.7333)

    def goto_rio(self, widget, **kwargs):
        self.map_view.location = (-22.9028, -43.2075)

    def where_am_i(self, widget, **kwargs):
        self.label.text = self.map_view.location

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
            (36.47032, -86.65138),
            title="The White House",
            subtitle="They have beehives!",
        )

        self.map_view = toga.MapView(
            style=Pack(flex=1),
            pins=[self.pin_1, self.pin_2],
            on_select=self.pin_selected,
        )

        # Add a pin at runtime.
        self.pin_3 = toga.MapPin(
            (random.uniform(-70, 70), random.uniform(-180, 180)),
            title="Carmen Sandiego",
        )
        self.map_view.pins.add(self.pin_3)

        btn_style = Pack(flex=1)
        # Location buttons
        btn_perth = toga.Button("PER", on_press=self.goto_perth, style=btn_style)
        btn_london = toga.Button("LON", on_press=self.goto_london, style=btn_style)
        btn_austin = toga.Button("AUS", on_press=self.goto_austin, style=btn_style)
        btn_rio = toga.Button("RIO", on_press=self.goto_rio, style=btn_style)
        btn_where = toga.Button("???", on_press=self.where_am_i, style=btn_style)
        location_box = toga.Box(
            children=[btn_perth, btn_london, btn_austin, btn_rio, btn_where],
            style=Pack(direction=ROW, padding=5),
        )

        # Zoom buttons
        zoom_box = toga.Box(
            children=[
                toga.Button(i, on_press=self.zoom(i), style=btn_style)
                for i in range(0, 6)
            ],
            style=Pack(direction=ROW, padding=5),
        )

        # Point Of Interest buttons
        btn_pin_1 = toga.Button("Pin 1", on_press=self.goto_pin_1, style=btn_style)
        btn_pin_2 = toga.Button("Pin 2", on_press=self.goto_pin_2, style=btn_style)
        btn_pin_3 = toga.Button("Pin 3", on_press=self.goto_pin_3, style=btn_style)
        btn_move = toga.Button("Move", on_press=self.move_carmen, style=btn_style)
        pin_box = toga.Box(
            children=[btn_pin_1, btn_pin_2, btn_pin_3, btn_move],
            style=Pack(direction=ROW, padding=5),
        )

        # Label to show responses.
        self.label = toga.Label("Ready.", style=Pack(padding=5))

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[self.map_view, location_box, zoom_box, pin_box, self.label],
            style=Pack(flex=1, direction=COLUMN),
        )

        # Show the main window
        self.main_window.show()


def main():
    return ExampleMapViewApp("Map View", "org.beeware.toga.examples.mapview")


if __name__ == "__main__":
    app = main()
    app.main_loop()
