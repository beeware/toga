import toga
import math


class StartApp(toga.App):
    def startup(self):
        # Window class
        #   Main window of the application with title and size
        self.main_window = toga.MainWindow(self.name, size=(148, 200))
        self.main_window.app = self

        self.canvas = toga.Canvas(on_draw=self.draw_tiberius)
        box = toga.Box(children=[self.canvas])

        # Add the content on the main window
        self.main_window.content = box

        # Show the main window
        self.main_window.show()

    def fill_head(self):
        with self.canvas.fill():
            self.canvas.fill_style('rgba(149.0, 119, 73, 1)')
            self.canvas.move_to(112, 103)
            self.canvas.line_to(112, 113)
            self.canvas.ellipse(73, 114, 39, 47, 0, 0, math.pi)
            self.canvas.line_to(35, 84)
            self.canvas.arc(65, 84, 30, math.pi, 3 * math.pi / 2)
            self.canvas.arc(82, 84, 30, 3 * math.pi / 2, 2 * math.pi)

    def stroke_head(self):
        with self.canvas.stroke():
            with self.canvas.closed_path(112, 103):
                self.canvas.line_width(4.0)
                self.canvas.stroke_style()
                self.canvas.line_to(112, 113)
                self.canvas.ellipse(73, 114, 39, 47, 0, 0, math.pi)
                self.canvas.line_to(35, 84)
                self.canvas.arc(65, 84, 30, math.pi, 3 * math.pi / 2)
                self.canvas.arc(82, 84, 30, 3 * math.pi / 2, 2 * math.pi)

    def draw_eyes(self):
        self.canvas.line_width(4.0)
        with self.canvas.fill():
            self.canvas.fill_style('rgba(255, 255, 255, 1)')
            self.canvas.arc(58, 92, 15)
            self.canvas.arc(88, 92, 15, math.pi, 3 * math.pi)
        with self.canvas.stroke():
            self.canvas.stroke_style('rgba(0, 0, 0, 1)')
            self.canvas.arc(58, 92, 15)
            self.canvas.arc(88, 92, 15, math.pi, 3 * math.pi)
        with self.canvas.fill():
            self.canvas.arc(58, 97, 3)
            self.canvas.arc(88, 97, 3)

    def draw_horns(self):
        # Right horn
        with self.canvas.fill():
            self.canvas.fill_style('rgba(212, 212, 212, 1)')
            self.canvas.move_to(112, 99)
            self.canvas.bezier_curve_to(145, 65, 145, 60, 139, 36)
            self.canvas.bezier_curve_to(130, 60, 130, 60, 109, 75)
        with self.canvas.stroke():
            self.canvas.stroke_style()
            self.canvas.move_to(112, 99)
            self.canvas.bezier_curve_to(145, 65, 145, 60, 139, 36)
            self.canvas.bezier_curve_to(130, 60, 130, 60, 109, 75)
        # Left horn
        with self.canvas.fill():
            self.canvas.fill_style('rgba(212, 212, 212, 1)')
            self.canvas.move_to(35, 99)
            self.canvas.bezier_curve_to(2, 65, 2, 60, 6, 36)
            self.canvas.bezier_curve_to(17, 60, 17, 60, 37, 75)
        with self.canvas.stroke():
            self.canvas.stroke_style()
            self.canvas.move_to(35, 99)
            self.canvas.bezier_curve_to(2, 65, 2, 60, 6, 36)
            self.canvas.bezier_curve_to(17, 60, 17, 60, 37, 75)

    def draw_nostrils(self):
        with self.canvas.fill():
            self.canvas.fill_style('rgba(212, 212, 212, 1)')
            self.canvas.move_to(45, 145)
            self.canvas.bezier_curve_to(51, 123, 96, 123, 102, 145)
            self.canvas.ellipse(73, 114, 39, 47, 0, math.pi / 4, 3 * math.pi / 4)
        with self.canvas.fill():
            self.canvas.fill_style()
            self.canvas.arc(63, 140, 3)
            self.canvas.arc(83, 140, 3)
        with self.canvas.stroke():
            self.canvas.move_to(45, 145)
            self.canvas.bezier_curve_to(51, 123, 96, 123, 102, 145)

    def draw_tiberius(self, canvas, context):
        self.canvas.set_context(context)
        self.fill_head()
        self.draw_eyes()
        self.draw_horns()
        self.draw_nostrils()
        self.stroke_head()


if __name__ == '__main__':
    # Application class
    #   App name and namespace
    app = StartApp('Tutorial 4', 'org.pybee.helloworld')

    app.main_loop()

