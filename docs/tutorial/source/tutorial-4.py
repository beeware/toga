import toga


class StartApp(toga.App):

    SIZE = 30

    def startup(self):
        # Window class
        #   Main window of the application with title and size
        self.main_window = toga.MainWindow(self.name, size=(500, 500))
        self.main_window.app = self

        self.canvas = toga.Canvas(on_draw=self.draw_steps)
        box = toga.Box(children=[self.canvas])

        # Add the content on the main window
        self.main_window.content = box

        # Show the main window
        self.main_window.show()

    def triangle(self):
        with self.canvas.closed_path(self.SIZE, 0):
            self.canvas.line_to(self.SIZE, 2 * self.SIZE)
            self.canvas.line_to(-2 * self.SIZE, 0)

    def square(self):
        with self.canvas.closed_path(0, 0):
            self.canvas.line_to(2 * self.SIZE, 0)
            self.canvas.line_to(0, 2 * self.SIZE)
            self.canvas.line_to(-2 * self.SIZE, 0)

    def bowtie(self):
        with self.canvas.closed_path(0, 0):
            self.canvas.line_to(2 * self.SIZE, 2 * self.SIZE)
            self.canvas.line_to(-2 * self.SIZE, 0)
            self.canvas.line_to(2 * self.SIZE, -2 * self.SIZE)

    def inf(self):
        with self.canvas.closed_path(0, self.SIZE):
            self.canvas.bezier_curve_to(0, self.SIZE, self.SIZE, self.SIZE, 2 * self.SIZE, 0)
            self.canvas.bezier_curve_to(self.SIZE, -self.SIZE, 2 * self.SIZE, -self.SIZE, 2 * self.SIZE, 0)
            self.canvas.bezier_curve_to(0, self.SIZE, -self.SIZE, self.SIZE, -2 * self.SIZE, 0)
            self.canvas.bezier_curve_to(-self.SIZE, -self.SIZE, -2 * self.SIZE, -self.SIZE, -2 * self.SIZE, 0)

    def fill_shapes(self, x, y):
        for shape in range(4):
            with self.canvas.fill():
                if shape == 0:
                    self.canvas.translate(x + self.SIZE, y + self.SIZE)
                    self.bowtie()
                elif shape == 1:
                    self.canvas.translate(3 * self.SIZE, 0)
                    self.square()
                elif shape == 2:
                    self.canvas.translate(3 * self.SIZE, 0)
                    self.triangle()
                else:
                    self.canvas.translate(3 * self.SIZE, 0)
                    self.inf()

    def stroke_shapes(self, x, y):
        for shape in range(4):
            with self.canvas.stroke():
                if shape == 0:
                    self.canvas.translate(x + self.SIZE, y + self.SIZE)
                    self.bowtie()
                elif shape == 1:
                    self.canvas.translate(3 * self.SIZE, 0)
                    self.square()
                elif shape == 2:
                    self.canvas.translate(3 * self.SIZE, 0)
                    self.triangle()
                else:
                    self.canvas.translate(3 * self.SIZE, 0)
                    self.inf()

    def draw_steps(self, canvas, context):
        print('start draw_steps')
        self.canvas.stroke_style('rbga(0, 0, 0, 1)')
        self.canvas.line_width(self.SIZE / 4)
        self.stroke_shapes(0, 0)
        self.stroke_shapes(0, 3 * self.SIZE)
        self.stroke_shapes(0, 6 * self.SIZE)
        self.stroke_shapes(0, 9 * self.SIZE)
        self.fill_shapes(0, 12 * self.SIZE)
        self.fill_shapes(0, 15 * self.SIZE)
        self.canvas.stroke_style('rgba(1, 0, 0, 1)')
        self.stroke_shapes(0, 15 * self.SIZE)


if __name__ == '__main__':
    # Application class
    #   App name and namespace
    app = StartApp('Tutorial 4', 'org.pybee.helloworld')

    app.main_loop()
