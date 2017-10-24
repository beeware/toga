import unittest
from unittest.mock import MagicMock
import math

import toga
import toga_dummy


class TestContext2D(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.Context2D = MagicMock(return_value=MagicMock(spec=toga_dummy.widgets.context2d.Context2D))

        self.context = toga.Context2D(factory=self.factory)

    def test_factory_called(self):
        self.factory.Context2D.assert_called_once_with(interface=self.context)

    def test_basic_drawing(self):
        self.context.save()
        self.context.rect(-3, -3, 6, 6)
        self.context.fill_style('rgba(0, 0.5, 0, 0.4)')
        self.context.fill(preserve=True)
        self.context.stroke_style('rgba(0.25, 0.25, 0.25, 0.6)')
        self.context.line_width(1)
        self.context.stroke()
        self.context.restore()

    def test_self_oval_path(self):
        xc = 50
        yc = 60
        xr = 25
        yr = 30
        self.context.save()
        self.context.translate(xc, yc)
        self.context.scale(1.0, yr / xr)
        self.context.move_to(xr, 0.0)
        self.context.arc(0, 0, xr, 0, 2 * math.pi)
        self.context.close_path()
        self.context.restore()

    def test_fill_checks(self):
        CHECK_SIZE = 32
        x = 10
        y = -10
        width = 200
        height = 200
        self.context.rect(x, y, width, height)
        self.context.fill_style('rgba(0.4, 0.4, 0.4, 1)')
        self.context.fill()

        # Only works for CHECK_SIZE a power of 2
        for j in range(x & -CHECK_SIZE, height, CHECK_SIZE):
            for i in range(y & -CHECK_SIZE, width, CHECK_SIZE):
                if((i / CHECK_SIZE + j / CHECK_SIZE) % 2 == 0):
                    self.context.rect(i, j, CHECK_SIZE, CHECK_SIZE)

        self.context.fill_style('rgba(0.7, 0.7, 0.7, 1)')
        self.context.fill()

    def test_draw_3circles(self):
        xc = 100
        yc = 150
        radius = 0.5 * 50 - 10
        alpha = 0.8
        subradius = radius * (2 / 3. - 0.1)

        self.context.fill_style('rgba(1, 0, 0, ' + str(alpha) +')')
        self.context.ellipse(self.context,
              xc + radius / 3. * math.cos(math.pi * 0.5),
              yc - radius / 3. * math.sin(math.pi * 0.5),
              subradius, subradius)
        self.context.fill()

        self.context.fill_style('rgba(0, 1, 0, ' + str(alpha) + ')')
        self.context.ellipse(self.context,
              xc + radius / 3. * math.cos(math.pi * (0.5 + 2 / .3)),
              yc - radius / 3. * math.sin(math.pi * (0.5 + 2 / .3)),
              subradius, subradius)
        self.context.fill()

        self.context.fill_style('rgba(0, 0, 1, ' + str(alpha) + ')')
        self.context.ellipse(self.context,
              xc + radius / 3. * math.cos(math.pi * (0.5 + 4 / .3)),
              yc - radius / 3. * math.sin(math.pi * (0.5 + 4 / .3)),
              subradius, subradius)
        self.context.fill()

    def test_release(self):
        self.context.release()

    def test_begin_path(self):
        self.context.begin_path()

    def test_close_path(self):
        self.context.close_path()

    def test_move_to(self):
        self.context.move_to(5, 7)

    def test_line_to(self):
        self.context.line_to(2, 3)

    def test_bezier_curve_to(self):
        self.context.bezier_curve_to(1, 1, 2, 2, 5, 5)

    def test_quadratic_curve_to(self):
        self.context.quadratic_curve_to(1, 1, 5, 5)

    def test_arc(self):
        self.context.arc(-10, -10, 10, math.pi/2, 0, True)

    def test_ellipse(self):
        self.context.ellipse(1, 1, 50, 20, 0, math.pi, 2*math.pi, False)

    def test_rotate(self):
        self.context.rotate(math.pi)

    def test_scale(self):
        self.context.scale(2, 1.5)

    def test_translate(self):
        self.context.translate(5, 3.5)

    def test_reset_transform(self):
        self.context.reset_transform()
