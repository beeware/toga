import math

from travertino.constants import BLACK, BLUE, GREEN, RED, YELLOW

import toga
from toga.style import Pack
from toga.style.pack import ROW, COLUMN

STROKE = "Stroke"
FILL = "Fill"

TRIANGLE = "triangle"
RECTANGLE = "rectangle"
ELLIPSE = "ellipse"
ICE_CREAM = "ice cream"
SMILE = "smile"
SEA = "sea"


class ExampleCanvasApp(toga.App):

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name, size=(250, 250))

        self.canvas = toga.Canvas(style=Pack(flex=1), on_resize=self.refresh_canvas)
        self.context_selection = toga.Selection(items=[STROKE, FILL], on_select=self.refresh_canvas)
        self.drawing_shape_instructions = {
            TRIANGLE: self.draw_triangle,
            RECTANGLE: self.draw_rectangle,
            ELLIPSE: self.draw_ellipse,
            ICE_CREAM: self.draw_ice_cream,
            SMILE: self.draw_smile,
            SEA: self.draw_sea
        }
        self.shape_selection = toga.Selection(
            items=list(self.drawing_shape_instructions.keys()),
            on_select=self.refresh_canvas
        )
        self.color_selection = toga.Selection(
            items=[BLACK, BLUE, GREEN, RED, YELLOW],
            on_select=self.refresh_canvas
        )
        box = toga.Box(
            style=Pack(direction=COLUMN),
            children=[
                toga.Box(
                    style=Pack(direction=ROW),
                    children=[
                        self.context_selection,
                        self.shape_selection,
                        self.color_selection
                    ]
                ),
                self.canvas
            ]
        )

        # Add the content on the main window
        self.main_window.content = box

        self.render_drawing(self.canvas, *self.main_window.size)

        # Show the main window
        self.main_window.show()

    def render_drawing(self, canvas, w, h):
        canvas.clear()
        with self.get_context(canvas) as context:
            self.draw_shape(context, h, w)

    def draw_shape(self, context, h, w):
        # Scale to the smallest axis to maintain aspect ratio
        factor = min(w, h)
        drawing_instructions = self.drawing_shape_instructions.get(
            str(self.shape_selection.value), None
        )
        if drawing_instructions is not None:
            drawing_instructions(context, h, w, factor)

    def draw_triangle(self, context, h, w, factor):
        # calculate offsets to centralize drawing in the bigger axis
        dx = (w - factor) / 2
        dy = (h - factor) / 2
        with context.closed_path(dx + factor / 3, dy + factor / 3) as closer:
            closer.line_to(dx + 2 * factor / 3, dy + 2 * factor / 3)
            closer.line_to(dx + 2 * factor / 3, dy + factor / 3)

    def draw_rectangle(self, context, h, w, factor):
        dx = w / 2
        dy = h / 2
        context.rect(dx - factor / 3, dy - factor / 6, 2 * factor / 3, factor / 3)

    def draw_ellipse(self, context, h, w, factor):
        rx = factor / 3
        ry = factor / 4

        context.ellipse(w / 2, h / 2, rx, ry)

    def draw_ice_cream(self, context, h, w, factor):
        dx = w / 2
        dy = h / 2 - factor / 6
        with context.closed_path(dx - factor / 5, dy) as closer:
            closer.arc(dx, dy, factor / 5, math.pi, 2 * math.pi)
            closer.line_to(dx, dy + 2 * factor / 5)

    def draw_smile(self, context, h, w, factor):
        dx = w / 2
        dy = h / 2 - factor / 5
        with context.closed_path(dx - factor / 5, dy) as closer:
            closer.quadratic_curve_to(dx, dy + 3 * factor / 5, dx + factor / 5, dy)
            closer.quadratic_curve_to(dx, dy + factor / 5, dx - factor / 5, dy)

    def draw_sea(self, context, h, w, factor):
        dx = w / 2
        dy = h / 2
        with context.closed_path(dx - 1 * factor / 5, dy - 1 * factor / 5) as closer:
            closer.bezier_curve_to(
                dx - 1 * factor / 10,
                dy,
                dx + 1 * factor / 10,
                dy - 2 * factor / 5,
                dx + 1 * factor / 5,
                dy - 1 * factor / 5)
            closer.line_to(dx + 1 * factor / 5, dy + 1 * factor / 5)
            closer.line_to(dx - 1 * factor / 5, dy + 1 * factor / 5)

    def get_context(self, canvas):
        if self.context_selection.value == STROKE:
            return canvas.stroke(color=str(self.color_selection.value))
        return canvas.fill(color=str(self.color_selection.value))

    def refresh_canvas(self, widget):
        self.render_drawing(
            self.canvas,
            self.canvas.layout.content_width,
            self.canvas.layout.content_height
        )


def main():
    return ExampleCanvasApp('Canvas', 'org.beeware.widgets.canvas')


if __name__ == '__main__':
    main().main_loop()
