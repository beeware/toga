import toga


class StartApp(toga.App):

    SIZE = 30

    def startup(self):
        # Window class
        #   Main window of the application with title and size
        self.main_window = toga.MainWindow(self.name, size=(500, 500))
        self.main_window.app = self

        canvas = toga.Canvas()
        canvas.draw(self.draw_steps)
        box = toga.Box(children=[canvas])

        # Add the content on the main window
        self.main_window.content = box

        # Show the main window
        self.main_window.show()

    def triangle(self, context):
        with context.closed_path(self.SIZE, 0):
            context.line_to(self.SIZE, 2 * self.SIZE)
            context.line_to(-2 * self.SIZE, 0)

    def square(self, context):
        self.context = context
        with self.context.closed_path(0, 0):
            self.context.line_to(2 * self.SIZE, 0)
            self.context.line_to(0, 2 * self.SIZE)
            self.context.line_to(-2 * self.SIZE, 0)

    def bowtie(self, context):
        self.context = context
        with self.context.closed_path(0, 0):
            self.context.line_to(2 * self.SIZE, 2 * self.SIZE)
            self.context.line_to(-2 * self.SIZE, 0)
            self.context.line_to(2 * self.SIZE, -2 * self.SIZE)

    def inf(self, context):
        self.context = context
        with self.context.closed_path(0, self.SIZE):
            self.context.bezier_curve_to(0, self.SIZE, self.SIZE, self.SIZE, 2 * self.SIZE, 0)
            self.context.bezier_curve_to(self.SIZE, -self.SIZE, 2 * self.SIZE, -self.SIZE, 2 * self.SIZE, 0)
            self.context.bezier_curve_to(0, self.SIZE, -self.SIZE, self.SIZE, -2 * self.SIZE, 0)
            self.context.bezier_curve_to(-self.SIZE, -self.SIZE, -2 * self.SIZE, -self.SIZE, -2 * self.SIZE, 0)

    def fill_shapes(self, context, x, y):
        self.context = context
        with self.context.save_restore():
            for shape in range(4):
                with self.context.fill():
                    if shape == 0:
                        self.context.translate(x + self.SIZE, y + self.SIZE)
                        self.bowtie(context)
                    elif shape == 1:
                        self.context.translate(3 * self.SIZE, 0)
                        self.square(context)
                    elif shape == 2:
                        self.context.translate(3 * self.SIZE, 0)
                        self.triangle(context)
                    else:
                        self.context.translate(3 * self.SIZE, 0)
                        self.inf(context)

    def stroke_shapes(self, context, x, y):
        self.context = context
        with self.context.save_restore():
            for self.shape in range(4):
                with self.context.stroke():
                    if self.shape == 0:
                        self.context.translate(x + self.SIZE, y + self.SIZE)
                        self.bowtie(context)
                    elif self.shape == 1:
                        self.context.translate(3 * self.SIZE, 0)
                        self.square(context)
                    elif self.shape == 2:
                        self.context.translate(3 * self.SIZE, 0)
                        self.triangle(context)
                    else:
                        self.context.translate(3 * self.SIZE, 0)
                        self.inf(context)

    def draw_steps(self, canvas, context):
        self.context = context
        self.context.line_style('rbga(0, 0, 0, 1)')
        self.context.line_width(self.SIZE / 4)
        self.stroke_shapes(context, 0, 0)
        self.stroke_shapes(context, 0, 3 * self.SIZE)
        self.stroke_shapes(context, 0, 6 * self.SIZE)
        self.stroke_shapes(context, 0, 9 * self.SIZE)
        self.fill_shapes(context, 0, 12 * self.SIZE)
        self.fill_shapes(context, 0, 15 * self.SIZE)
        self.context.line_style('rgba(1, 0, 0, 1)')
        self.stroke_shapes(context, 0, 15 * self.SIZE)


if __name__ == '__main__':
    # Application class
    #   App name and namespace
    app = StartApp('Tutorial 4', 'org.pybee.helloworld')

    app.main_loop()
