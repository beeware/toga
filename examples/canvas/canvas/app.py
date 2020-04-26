import toga
from toga.style import Pack
from toga.style.pack import ROW, COLUMN

STROKE = "Stroke"
FILL = "Fill"

TRIANGLE = "triangle"
ELLIPSE = "ellipse"


class ExampleCanvasApp(toga.App):
    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name, size=(148, 200))

        self.canvas = toga.Canvas(style=Pack(flex=1), on_resize=self.refresh_canvas)
        self.context_selection = toga.Selection(items=[STROKE, FILL], on_select=self.refresh_canvas)
        self.shape_selection = toga.Selection(items=[TRIANGLE, ELLIPSE], on_select=self.refresh_canvas)
        box = toga.Box(
            style=Pack(direction=COLUMN),
            children=[
                toga.Box(
                    style=Pack(direction=ROW),
                    children=[self.context_selection, self.shape_selection]
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
        if self.shape_selection.value == TRIANGLE:
            self.draw_triangle(context, h, w)
        else:
            self.draw_ellipse(context, h, w)

    def draw_triangle(self, context, h, w):
        # Scale to the smallest axis to maintain aspect ratio
        factor = min(w, h)
        # calculate offsets to centralize drawing in the bigger axis
        dx = (w - factor) / 2
        dy = (h - factor) / 2
        with context.closed_path(dx + factor / 3, dy + factor / 3) as closer:
            closer.line_to(dx + 2 * factor / 3, dy + 2 * factor / 3)
            closer.line_to(dx + 2 * factor / 3, dy + factor / 3)

    def draw_ellipse(self, context, h, w):
        # Scale to the smallest axis to maintain aspect ratio
        factor = min(w, h)

        rx = factor / 3
        ry = factor / 4

        context.ellipse(w / 2, h / 2, rx, ry)

    def get_context(self, canvas):
        if self.context_selection.value == STROKE:
            return canvas.stroke()
        return canvas.fill()

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
