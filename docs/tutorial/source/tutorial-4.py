import toga
from colosseum import CSS

"""Based on cairo-demo/X11/cairo-demo.c"""


def build(app):
    SIZE = 30

    def triangle(context):
        with context.begin_close_path(SIZE, 0):
            context.line_to(SIZE, 2 * SIZE)
            context.line_to(-2 * SIZE, 0)

    def square(context):
        with context.begin_close_path(0, 0):
            context.line_to(2 * SIZE, 0)
            context.line_to(0, 2 * SIZE)
            context.line_to(-2 * SIZE, 0)

    def bowtie(context):
        with context.begin_close_path(0, 0):
            context.line_to(2 * SIZE, 2 * SIZE)
            context.line_to(-2 * SIZE, 0)
            context.line_to(2 * SIZE, -2 * SIZE)

    def inf(context):
        with context.begin_close_path(0, SIZE):
            context.bezier_curve_to(0, SIZE, SIZE, SIZE, 2 * SIZE, 0)
            context.bezier_curve_to(SIZE, -SIZE, 2 * SIZE, -SIZE, 2 * SIZE, 0)
            context.bezier_curve_to(0, SIZE, -SIZE, SIZE, -2 * SIZE, 0)
            context.bezier_curve_to(-SIZE, -SIZE, -2 * SIZE, -SIZE, -2 * SIZE, 0)

    def fill_shapes(context, x, y):
        with context.save_restore():
            for shape in range(4):
                with context.fill():
                    if shape == 0:
                        context.translate(x + SIZE, y + SIZE)
                        bowtie(context)
                    elif shape == 1:
                        context.translate(3 * SIZE, 0)
                        square(context)
                    elif shape == 2:
                        context.translate(3 * SIZE, 0)
                        triangle(context)
                    else:
                        context.translate(3 * SIZE, 0)
                        inf(context)

    def stroke_shapes(context, x, y):
        with context.save_restore():
            for shape in range(4):
                with context.stroke():
                    if shape == 0:
                        context.translate(x + SIZE, y + SIZE)
                        bowtie(context)
                    elif shape == 1:
                        context.translate(3 * SIZE, 0)
                        square(context)
                    elif shape == 2:
                        context.translate(3 * SIZE, 0)
                        triangle(context)
                    else:
                        context.translate(3 * SIZE, 0)
                        inf(context)

    def draw(canvas, context):
        context.line_style('rbga(0, 0, 0, 1)')

        context.line_width(SIZE / 4)
        context.set_tolerance(0.1)

        context.set_line_join('ROUND')
        context.set_dash([SIZE / 4.0, SIZE / 4.0], 0)
        stroke_shapes(context, 0, 0)

        context.set_dash([], 0)
        stroke_shapes(context, 0, 3 * SIZE)

        context.set_line_join('BEVEL')
        stroke_shapes(context, 0, 6 * SIZE)

        context.set_line_join('MITER')
        stroke_shapes(context, 0, 9 * SIZE)

        fill_shapes(context, 0, 12 * SIZE)

        context.set_line_join('BEVEL')
        fill_shapes(context, 0, 15 * SIZE)
        context.line_style('rgba(1, 0, 0, 1)')
        stroke_shapes(context, 0, 15 * SIZE)

    canvas = toga.Canvas()
    # window = toga.Window()
    # window.app(app)
    # window.content(canvas)
    canvas.draw(draw)


def main():
    return toga.App('First App', 'org.pybee.canvas_draw', startup=build)


if __name__ == '__main__':
    main().main_loop()
