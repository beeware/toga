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

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow()

        self.map_view = toga.MapView(
            style=Pack(flex=1),
            pins=[
                ((-41.2784, 174.7767), "The Bee Hive", "NZ Parliament building"),
                ((36.47032, -86.65138), "The White House", "The have beehives!"),
            ],
        )

        # Add a pin at runtime.
        self.map_view.pins.add(
            (
                random.uniform(-70, 70),
                random.uniform(-180, 180),
            ),
            title="Carmen Sandiego",
        )

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

        # Label to show responses.
        self.label = toga.Label("Ready.", style=Pack(padding=5))

        # Add the content on the main window
        self.main_window.content = toga.Box(
            children=[self.map_view, location_box, zoom_box, self.label],
            style=Pack(flex=1, direction=COLUMN),
        )

        # Show the main window
        self.main_window.show()


def main():
    return ExampleMapViewApp("Map View", "org.beeware.toga.examples.mapview")


if __name__ == "__main__":
    app = main()
    app.main_loop()
