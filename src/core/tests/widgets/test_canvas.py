import toga
import toga_dummy
from toga_dummy.utils import EventLog, TestCase
import math


class CanvasTests(TestCase):
    def setUp(self):
        super().setUp()

        # Create a canvas with the dummy factory
        self.testing_canvas = toga.Canvas(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.testing_canvas._impl.interface, self.testing_canvas)
        self.assertActionPerformed(self.testing_canvas, 'create Canvas')

    def test_canvas_on_draw(self):
        self.assertIsNone(self.testing_canvas._on_draw)

        # set a new callback
        def callback(widget, **extra):
            return 'called {} with {}'.format(type(widget), extra)

        self.testing_canvas.on_draw = callback
        self.assertValueSet(self.testing_canvas, 'on_draw', self.testing_canvas.on_draw)

    def test_basic_drawing(self):
        def drawing(widget):
            self.testing_canvas.rect(-3, -3, 6, 6)
            self.assertActionPerformedWith(self.testing_canvas, 'rect', x=-3, y=-3, width=6, height=6)
            self.testing_canvas.fill_style('rgba(0, 0.5, 0, 0.4)')
            self.assertActionPerformedWith(self.testing_canvas, 'fill style', color='rgba(0, 0.5, 0, 0.4)')
            self.testing_canvas.fill(preserve=True)
            self.assertActionPerformedWith(self.testing_canvas, 'fill', preserve=True)
            self.testing_canvas.stroke_style('rgba(0.25, 0.25, 0.25, 0.6)')
            self.assertActionPerformedWith(self.testing_canvas, 'stroke style', color='rgba(0.25, 0.25, 0.25, 0.6)')
            self.testing_canvas.line_width(1)
            self.assertActionPerformedWith(self.testing_canvas, 'line width', width=1)
            self.testing_canvas.stroke()
            self.assertActionPerformedWith(self.testing_canvas, 'stroke')

        self.testing_canvas.on_draw = drawing

    def test_self_oval_path(self):
        xc = 50
        yc = 60
        xr = 25
        yr = 30
        self.testing_canvas.translate(xc, yc)
        self.assertActionPerformedWith(self.testing_canvas, 'translate', tx=xc, ty=yc)
        self.testing_canvas.scale(1.0, yr / xr)
        self.assertActionPerformedWith(self.testing_canvas, 'scale', sx=1.0, sy=yr/xr)
        with self.testing_canvas.closed_path(xr, 0.0):
            self.testing_canvas.arc(0, 0, xr, 0, 2 * math.pi)

    def test_fill_checks(self):
        def drawing(widget):
            CHECK_SIZE = 32
            x = 10
            y = -10
            width = 200
            height = 200
            self.testing_canvas.rect(x, y, width, height)
            self.assertActionPerformedWith(self.testing_canvas, 'rect', x=10, y=-10, width=200, height=200)
            self.testing_canvas.fill_style('rgba(0.4, 0.4, 0.4, 1)')
            self.assertActionPerformedWith(self.testing_canvas, 'fill style', color='rgba(0.4, 0.4, 0.4, 1)')
            self.testing_canvas.fill()
            self.assertActionPerformedWith(self.testing_canvas, 'fill')

            # Only works for CHECK_SIZE a power of 2
            for j in range(x & -CHECK_SIZE, height, CHECK_SIZE):
                for i in range(y & -CHECK_SIZE, width, CHECK_SIZE):
                    if (i / CHECK_SIZE + j / CHECK_SIZE) % 2 == 0:
                        self.testing_canvas.rect(i, j, CHECK_SIZE, CHECK_SIZE)
                        self.assertActionPerformedWith(self.testing_canvas, 'rect', x=i, y=j, width=CHECK_SIZE, height=CHECK_SIZE)

            self.testing_canvas.fill_style('rgba(0.7, 0.7, 0.7, 1)')
            self.assertActionPerformedWith(self.testing_canvas, 'fill style', color='rgba(0.7, 0.7, 0.7, 1)')
            self.testing_canvas.fill()
            self.assertActionPerformedWith(self.testing_canvas, 'fill')

        self.testing_canvas.on_draw = drawing

    def test_draw_3circles(self):
        def drawing(widget):
            xc = 100
            yc = 150
            radius = 0.5 * 50 - 10
            alpha = 0.8
            subradius = radius * (2 / 3. - 0.1)

            self.testing_canvas.fill_style('rgba(1, 0, 0, ' + str(alpha) + ')')
            self.assertActionPerformedWith(self.testing_canvas, 'fill style', color='rgba(1, 0, 0, ' + str(alpha) + ')')
            self.testing_canvas.ellipse(self.testing_canvas,
                                        xc + radius / 3. * math.cos(math.pi * 0.5),
                                        yc - radius / 3. * math.sin(math.pi * 0.5),
                                        subradius, subradius, 2.0 * math.pi)
            self.assertActionPerformedWith(self.testing_canvas, 'ellipse',
                                           x=xc + radius / 3. * math.cos(math.pi * 0.5),
                                           y=yc - radius / 3. * math.sin(math.pi * 0.5),
                                           radiusx=subradius, radiusy=subradius, rotation=2.0*math.pi)

            self.testing_canvas.fill()
            self.assertActionPerformedWith(self.testing_canvas, 'fill')

            self.testing_canvas.fill_style('rgba(0, 1, 0, ' + str(alpha) + ')')
            self.assertActionPerformedWith(self.testing_canvas, 'fill style', color='rgba(0, 1, 0, ' + str(alpha) + ')')
            self.testing_canvas.ellipse(self.testing_canvas,
                                        xc + radius / 3. * math.cos(math.pi * (0.5 + 2 / .3)),
                                        yc - radius / 3. * math.sin(math.pi * (0.5 + 2 / .3)),
                                        subradius, subradius)
            self.assertActionPerformedWith(self.testing_canvas, 'ellipse',
                                           x=xc + radius / 3. * math.cos(math.pi * (0.5 + 2 / .3)),
                                           y=yc - radius / 3. * math.sin(math.pi * (0.5 + 2 / .3)),
                                           radiusx=subradius, radiusy=subradius)
            self.testing_canvas.fill()
            self.assertActionPerformedWith(self.testing_canvas, 'fill')

            self.testing_canvas.fill_style('rgba(0, 0, 1, ' + str(alpha) + ')')
            self.assertActionPerformedWith(self.testing_canvas, 'fill style', color='rgba(0, 0, 1, ' + str(alpha) + ')')
            self.testing_canvas.ellipse(self.testing_canvas,
                                        xc + radius / 3. * math.cos(math.pi * (0.5 + 4 / .3)),
                                        yc - radius / 3. * math.sin(math.pi * (0.5 + 4 / .3)),
                                        subradius, subradius)
            self.assertActionPerformedWith(self.testing_canvas, 'ellipse',
                                           x=xc + radius / 3. * math.cos(math.pi * (0.5 + 4 / .3)),
                                           y=yc - radius / 3. * math.sin(math.pi * (0.5 + 4 / .3)),
                                           radiusx=subradius, radiusy=subradius)
            self.testing_canvas.fill()
            self.assertActionPerformedWith(self.testing_canvas, 'fill')

        self.testing_canvas.on_draw = drawing

    def test_draw_triangle(self):
        def drawing(widget):
            with self.testing_canvas.closed_path(32, 0):
                self.assertActionPerformedWith(self.testing_canvas, 'move to', x=32, y=0)
                self.testing_canvas.line_to(32, 64)
                self.assertActionPerformedWith(self.testing_canvas, 'line to', x=32, y=64)
                self.testing_canvas.line_to(-64, 0)
                self.assertActionPerformedWith(self.testing_canvas, 'line to', x=-64, y=0)
                self.assertActionPerformedWith(self.testing_canvas, 'close path')

        self.testing_canvas.on_draw = drawing

    def test_move_to(self):
        self.testing_canvas.move_to(5, 7)
        self.assertActionPerformedWith(self.testing_canvas, 'move to', x=5, y=7)
        self.testing_canvas.move_to(-5, 20.0)
        self.assertActionPerformedWith(self.testing_canvas, 'move to', x=-5, y=20.0)

    def test_line_to(self):
        self.testing_canvas.line_to(2, 3)
        self.assertActionPerformedWith(self.testing_canvas, 'line to', x=2, y=3)

    def test_bezier_curve_to(self):
        self.testing_canvas.bezier_curve_to(1, 1, 2, 2, 5, 5)
        self.assertActionPerformedWith(self.testing_canvas, 'bezier curve to', cp1x=1, cp1y=1, cp2x=2, cp2y=2, x=5, y=5)

    def test_quadratic_curve_to(self):
        self.testing_canvas.quadratic_curve_to(1, 1, 5, 5)
        self.assertActionPerformedWith(self.testing_canvas, 'quadratic curve to', cpx=1, cpy=1, x=5, y=5)

    def test_arc(self):
        self.testing_canvas.arc(-10, -10, 10, math.pi / 2, 0, True)
        self.assertActionPerformedWith(self.testing_canvas, 'arc', x=-10, y=-10, radius=10, startangle=math.pi / 2,
                                       endangle=0, anticlockwise=True)

    def test_ellipse(self):
        self.testing_canvas.ellipse(1, 1, 50, 20, 0, math.pi, 2 * math.pi, False)
        self.assertActionPerformedWith(self.testing_canvas, 'ellipse', x=1, y=1, radiusx=50, radiusy=20, rotation=0,
                                       startangle=math.pi, endangle=2 * math.pi, anticlockwise=False)

    def test_rotate(self):
        self.testing_canvas.rotate(math.pi)
        self.assertActionPerformedWith(self.testing_canvas, 'rotate', radians=math.pi)

    def test_scale(self):
        self.testing_canvas.scale(2, 1.5)
        self.assertActionPerformedWith(self.testing_canvas, 'scale', sx=2, sy=1.5)

    def test_translate(self):
        self.testing_canvas.translate(5, 3.5)
        self.assertActionPerformedWith(self.testing_canvas, 'translate', tx=5, ty=3.5)

    def test_reset_transform(self):
        self.testing_canvas.reset_transform()
        self.assertActionPerformedWith(self.testing_canvas, 'reset transform')
