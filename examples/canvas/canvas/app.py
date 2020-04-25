import toga
from toga.style import Pack

class ExampleCanvasApp(toga.App):
    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name, size=(148, 200))

        canvas = toga.Canvas(style=Pack(flex=1), on_resize=self.resize_contents)
        box = toga.Box(children=[canvas])

        # Add the content on the main window
        self.main_window.content = box

        # Show the main window
        self.main_window.show()

        self.render_drawing(canvas, *self.main_window.size)

    def render_drawing(self, canvas, w, h):
        # Scale to the smallest axis to maintain aspect ratio
        factor = min(w, h)

        # calculate offsets to centralize drawing in the bigger axis
        dx = (w - factor) / 2
        dy = (h - factor) / 2

        canvas.clear()
        with canvas.stroke() as stroker:
            with stroker.closed_path(dx+factor/3, dy+factor/3) as closer:
                closer.line_to(dx+2*factor/3, dy+2*factor/3)
                closer.line_to(dx+2*factor/3, dy+factor/3)

    def resize_contents(self, canvas):
        self.render_drawing(
            canvas,
            canvas.layout.content_width,
            canvas.layout.content_height
        )


def main():
    return ExampleCanvasApp('Canvas', 'org.beeware.widgets.canvas')


if __name__ == '__main__':
    main().main_loop()
