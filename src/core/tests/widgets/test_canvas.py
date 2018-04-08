import math

import toga
from toga.font import SANS_SERIF

import toga_dummy
from toga_dummy.utils import TestCase


class CanvasTests(TestCase):
    def setUp(self):
        super().setUp()

        # Create a canvas with the dummy factory
        self.testing_canvas = toga.Canvas(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.testing_canvas._impl.interface, self.testing_canvas)
        self.assertActionPerformed(self.testing_canvas, 'create Canvas')

    def test_basic_drawing(self):
        basic_context = self.testing_canvas.create_context()
        with self.testing_canvas.context(basic_context):
            fill = self.testing_canvas.fill(color='rgba(0, 0, 0, 0.4)', preserve=True)
            with fill:
                self.assertActionPerformedWith(self.testing_canvas, 'new path')
                stroke = self.testing_canvas.stroke(color='rgba(0, 0, 0, 0.6)', line_width=1)
                with stroke:
                    rect = self.testing_canvas.rect(-3, -3, 6, 6)
                    self.assertIn(rect, self.testing_canvas.drawing_objects)
                    self.assertActionPerformedWith(self.testing_canvas, 'rect', x=-3, y=-3, width=6, height=6)
                self.assertActionPerformedWith(self.testing_canvas, 'stroke')
            self.assertActionPerformedWith(self.testing_canvas, 'fill preserve')
        self.assertIn(basic_context.drawing_objects, self.testing_canvas.drawing_objects)

    def test_self_oval_path(self):
        xc = 50
        yc = 60
        xr = 25
        yr = 30
        translate = self.testing_canvas.translate(xc, yc)
        self.assertIn(translate, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'translate', tx=xc, ty=yc)
        scale = self.testing_canvas.scale(1.0, yr / xr)
        self.assertIn(scale, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'scale', sx=1.0, sy=yr/xr)
        closed_path = self.testing_canvas.closed_path(xr, 0.0)
        with closed_path:
            self.assertActionPerformedWith(self.testing_canvas, 'move to', x=xr, y=0.0)
            arc = self.testing_canvas.arc(0, 0, xr, 0, 2 * math.pi)
            self.assertIn(arc, self.testing_canvas.drawing_objects)
            self.assertActionPerformedWith(self.testing_canvas, 'arc', x=0, y=0, radius=xr, startangle=0,
                                           endangle=2*math.pi, anticlockwise=False)
        self.assertActionPerformedWith(self.testing_canvas, 'closed path')

    def test_fill_checks(self):
        check_size = 32
        x = 10
        y = -10
        width = 200
        height = 200
        fill1 = self.testing_canvas.fill(color='rgba(1, 1, 1, 1)')
        with fill1:
            rect = self.testing_canvas.rect(x, y, width, height)
            self.assertIn(rect, self.testing_canvas.drawing_objects)
            self.assertActionPerformedWith(self.testing_canvas, 'rect', x=10, y=-10, width=200, height=200)
        self.assertActionPerformedWith(self.testing_canvas, 'fill')

        fill2 = self.testing_canvas.fill(color='rgba(1, 1, 1, 1)')
        with fill2:
            # Only works for check_size a power of 2
            for j in range(x & -check_size, height, check_size):
                for i in range(y & -check_size, width, check_size):
                    if (i / check_size + j / check_size) % 2 == 0:
                        rect = self.testing_canvas.rect(i, j, check_size, check_size)
                        self.assertIn(rect, self.testing_canvas.drawing_objects)
                        self.assertActionPerformedWith(self.testing_canvas, 'rect', x=i, y=j, width=check_size,
                                                       height=check_size)
        self.assertActionPerformedWith(self.testing_canvas, 'fill')

    def test_draw_3circles(self):
        xc = 100
        yc = 150
        radius = 0.5 * 50 - 10
        alpha = 0.8
        subradius = radius * (2 / 3. - 0.1)

        fill1 = self.testing_canvas.fill(color='rgba(1, 0, 0, ' + str(alpha) + ')')
        with fill1:
            ellipse1 = self.testing_canvas.ellipse(xc + radius / 3. * math.cos(math.pi * 0.5),
                                                   yc - radius / 3. * math.sin(math.pi * 0.5),
                                                   subradius, subradius, 2.0 * math.pi)
            self.assertIn(ellipse1, self.testing_canvas.drawing_objects)
            self.assertActionPerformedWith(self.testing_canvas, 'ellipse',
                                           x=xc + radius / 3. * math.cos(math.pi * 0.5),
                                           y=yc - radius / 3. * math.sin(math.pi * 0.5),
                                           radiusx=subradius, radiusy=subradius, rotation=2.0*math.pi)
        self.assertActionPerformedWith(self.testing_canvas, 'fill')

        fill2 = self.testing_canvas.fill(color='rgba(0, 1, 0, ' + str(alpha) + ')')
        with fill2:
            ellipse2 = self.testing_canvas.ellipse(xc + radius / 3. * math.cos(math.pi * (0.5 + 2 / .3)),
                                                   yc - radius / 3. * math.sin(math.pi * (0.5 + 2 / .3)),
                                                   subradius, subradius)
            self.assertIn(ellipse2, self.testing_canvas.drawing_objects)
            self.assertActionPerformedWith(self.testing_canvas, 'ellipse',
                                           x=xc + radius / 3. * math.cos(math.pi * (0.5 + 2 / .3)),
                                           y=yc - radius / 3. * math.sin(math.pi * (0.5 + 2 / .3)),
                                           radiusx=subradius, radiusy=subradius)
        self.assertActionPerformedWith(self.testing_canvas, 'fill')

        fill3 = self.testing_canvas.fill(color='rgba(0, 0, 1, ' + str(alpha) + ')')
        with fill3:
            ellipse3 = self.testing_canvas.ellipse(xc + radius / 3. * math.cos(math.pi * (0.5 + 4 / .3)),
                                                   yc - radius / 3. * math.sin(math.pi * (0.5 + 4 / .3)),
                                                   subradius, subradius)
            self.assertIn(ellipse3, self.testing_canvas.drawing_objects)
            self.assertActionPerformedWith(self.testing_canvas, 'ellipse',
                                           x=xc + radius / 3. * math.cos(math.pi * (0.5 + 4 / .3)),
                                           y=yc - radius / 3. * math.sin(math.pi * (0.5 + 4 / .3)),
                                           radiusx=subradius, radiusy=subradius)
        self.assertActionPerformedWith(self.testing_canvas, 'fill')

    def test_draw_triangle(self):
        closed_path = self.testing_canvas.closed_path(32, 0)
        with closed_path:
            self.assertActionPerformedWith(self.testing_canvas, 'move to', x=32, y=0)
            line_to1 = self.testing_canvas.line_to(32, 64)
            self.assertIn(line_to1, self.testing_canvas.drawing_objects)
            self.assertActionPerformedWith(self.testing_canvas, 'line to', x=32, y=64)
            line_to2 = self.testing_canvas.line_to(-64, 0)
            self.assertIn(line_to2, self.testing_canvas.drawing_objects)
            self.assertActionPerformedWith(self.testing_canvas, 'line to', x=-64, y=0)
        self.assertActionPerformedWith(self.testing_canvas, 'closed path')

    def test_move_to(self):
        move_to1 = self.testing_canvas.move_to(5, 7)
        self.assertIn(move_to1, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'move to', x=5, y=7)
        move_to2 = self.testing_canvas.move_to(-5, 20.0)
        self.assertIn(move_to2, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'move to', x=-5, y=20.0)

    def test_line_to(self):
        line_to = self.testing_canvas.line_to(2, 3)
        self.assertIn(line_to, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'line to', x=2, y=3)

    def test_bezier_curve_to(self):
        bezier = self.testing_canvas.bezier_curve_to(1, 1, 2, 2, 5, 5)
        self.assertIn(bezier, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'bezier curve to', cp1x=1, cp1y=1, cp2x=2, cp2y=2, x=5, y=5)

    def test_quadratic_curve_to(self):
        quad = self.testing_canvas.quadratic_curve_to(1, 1, 5, 5)
        self.assertIn(quad, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'quadratic curve to', cpx=1, cpy=1, x=5, y=5)

    def test_arc(self):
        arc = self.testing_canvas.arc(-10, -10, 10, math.pi / 2, 0, True)
        self.assertIn(arc, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'arc', x=-10, y=-10, radius=10, startangle=math.pi / 2,
                                       endangle=0, anticlockwise=True)

    def test_remove_arc(self):
        arc = self.testing_canvas.arc(-10, -10, 10, math.pi / 2, 0, True)
        self.assertIn(arc, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'arc', x=-10, y=-10, radius=10, startangle=math.pi / 2,
                                       endangle=0, anticlockwise=True)
        self.testing_canvas.remove(arc)
        self.assertNotIn(arc, self.testing_canvas.drawing_objects)

    def test_ellipse(self):
        ellipse = self.testing_canvas.ellipse(1, 1, 50, 20, 0, math.pi, 2 * math.pi, False)
        self.assertIn(ellipse, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'ellipse', x=1, y=1, radiusx=50, radiusy=20, rotation=0,
                                       startangle=math.pi, endangle=2 * math.pi, anticlockwise=False)

    def test_rotate(self):
        rotate = self.testing_canvas.rotate(math.pi)
        self.assertIn(rotate, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'rotate', radians=math.pi)

    def test_scale(self):
        scale = self.testing_canvas.scale(2, 1.5)
        self.assertIn(scale, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'scale', sx=2, sy=1.5)

    def test_translate(self):
        translate = self.testing_canvas.translate(5, 3.5)
        self.assertIn(translate, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'translate', tx=5, ty=3.5)

    def test_reset_transform(self):
        reset_transform = self.testing_canvas.reset_transform()
        self.assertIn(reset_transform, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'reset transform')

    def test_write_text(self):
        test_font = toga.Font(family=SANS_SERIF, size=15)
        write_text = self.testing_canvas.write_text('test text', 0, 0, test_font)
        self.assertIn(write_text, self.testing_canvas.drawing_objects)
        self.assertActionPerformedWith(self.testing_canvas, 'write text', text='test text', x=0, y=0, font=test_font)
