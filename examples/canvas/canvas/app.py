import toga
from toga.style import Pack

class ExampleCanvasApp(toga.App):
    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name, size=(148, 200))

        canvas = toga.Canvas(style=Pack(flex=1))
        box = toga.Box(children=[canvas])

        # Add the content on the main window
        self.main_window.content = box

        # Show the main window
        self.main_window.show()

        with canvas.stroke() as stroker:
            with stroker.closed_path(50, 50) as closer:
                closer.line_to(100, 100)
                closer.line_to(100, 50)


def main():
    return ExampleCanvasApp('Canvas', 'org.beeware.widgets.canvas')


if __name__ == '__main__':
    main().main_loop()
