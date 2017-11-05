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
        with context.closed_path(0, 0):
            context.line_to(2 * self.SIZE, 0)
            context.line_to(0, 2 * self.SIZE)
            context.line_to(-2 * self.SIZE, 0)

    def bowtie(self, context):
        with context.closed_path(0, 0):
            context.line_to(2 * self.SIZE, 2 * self.SIZE)
            context.line_to(-2 * self.SIZE, 0)
            context.line_to(2 * self.SIZE, -2 * self.SIZE)

    def inf(self, context):
        with context.closed_path(0, self.SIZE):
            context.bezier_curve_to(0, self.SIZE, self.SIZE, self.SIZE, 2 * self.SIZE, 0)
            context.bezier_curve_to(self.SIZE, -self.SIZE, 2 * self.SIZE, -self.SIZE, 2 * self.SIZE, 0)
            context.bezier_curve_to(0, self.SIZE, -self.SIZE, self.SIZE, -2 * self.SIZE, 0)
            context.bezier_curve_to(-self.SIZE, -self.SIZE, -2 * self.SIZE, -self.SIZE, -2 * self.SIZE, 0)

    def fill_shapes(self, canvas, context, x, y):
        for shape in range(4):
            with context.fill():
                if shape == 0:
                    context.translate(x + self.SIZE, y + self.SIZE)
                    self.bowtie(context)
                elif shape == 1:
                    context.translate(3 * self.SIZE, 0)
                    self.square(context)
                elif shape == 2:
                    context.translate(3 * self.SIZE, 0)
                    self.triangle(context)
                else:
                    context.translate(3 * self.SIZE, 0)
                    self.inf(context)

    def stroke_shapes(self, canvas, context, x, y):
        for shape in range(4):
            with context.stroke():
                if shape == 0:
                    context.translate(x + self.SIZE, y + self.SIZE)
                    self.bowtie(context)
                elif shape == 1:
                    context.translate(3 * self.SIZE, 0)
                    self.square(context)
                elif shape == 2:
                    context.translate(3 * self.SIZE, 0)
                    self.triangle(context)
                else:
                    context.translate(3 * self.SIZE, 0)
                    self.inf(context)

    def draw_steps(self, canvas, context):
        context.line_style('rbga(0, 0, 0, 1)')
        canvas.line_width(context, self.SIZE / 4)
        canvas.draw(self.stroke_shapes(x=0, y=0))
        canvas.draw(self.stroke_shapes(x=0, y=3 * self.SIZE))
        canvas.draw(self.stroke_shapes(x=0, y=6 * self.SIZE))
        canvas.draw(self.stroke_shapes(x=0, y=9 * self.SIZE))
        canvas.draw(self.fill_shapes(x=0, y=12 * self.SIZE))
        canvas.draw(self.fill_shapes(x=0, y=15 * self.SIZE))
        context.line_style('rgba(1, 0, 0, 1)')
        canvas.draw(self.stroke_shapes(x=0, y=15 * self.SIZE))


if __name__ == '__main__':
    # Application class
    #   App name and namespace
    app = StartApp('Tutorial 4', 'org.pybee.helloworld')

    app.main_loop()
