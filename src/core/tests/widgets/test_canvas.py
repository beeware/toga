import unittest
from unittest.mock import MagicMock
import math

import toga
import toga_dummy


class TestCanvas(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.Canvas = MagicMock(return_value=MagicMock(spec=toga_dummy.widgets.canvas.Canvas))

        self.canvas = toga.Canvas(factory=self.factory)

    def test_factory_called(self):
        self.factory.Canvas.assert_called_once_with(interface=self.canvas)

    def test_basic_drawing(self):
        with self.canvas.save_restore():
            self.canvas.rect(-3, -3, 6, 6)
            self.canvas.fill_style('rgba(0, 0.5, 0, 0.4)')
            self.canvas.fill(preserve=True)
            self.canvas.stroke_style('rgba(0.25, 0.25, 0.25, 0.6)')
            self.canvas.line_width(1)
            self.canvas.stroke()

    def test_self_oval_path(self):
        xc = 50
        yc = 60
        xr = 25
        yr = 30
        with self.canvas.save_restore():
            self.canvas.translate(xc, yc)
            self.canvas.scale(1.0, yr / xr)
            with self.canvas.begin_close_path(xr, 0.0):
                self.canvas.arc(0, 0, xr, 0, 2 * math.pi)

    def test_fill_checks(self):
        CHECK_SIZE = 32
        x = 10
        y = -10
        width = 200
        height = 200
        self.canvas.rect(x, y, width, height)
        self.canvas.fill_style('rgba(0.4, 0.4, 0.4, 1)')
        self.canvas.fill()

        # Only works for CHECK_SIZE a power of 2
        for j in range(x & -CHECK_SIZE, height, CHECK_SIZE):
            for i in range(y & -CHECK_SIZE, width, CHECK_SIZE):
                if((i / CHECK_SIZE + j / CHECK_SIZE) % 2 == 0):
                    self.canvas.rect(i, j, CHECK_SIZE, CHECK_SIZE)

        self.canvas.fill_style('rgba(0.7, 0.7, 0.7, 1)')
        self.canvas.fill()

    def test_draw_3circles(self):
        xc = 100
        yc = 150
        radius = 0.5 * 50 - 10
        alpha = 0.8
        subradius = radius * (2 / 3. - 0.1)

        self.canvas.fill_style('rgba(1, 0, 0, ' + str(alpha) +')')
        self.canvas.ellipse(self.canvas,
                             xc + radius / 3. * math.cos(math.pi * 0.5),
                             yc - radius / 3. * math.sin(math.pi * 0.5),
                             subradius, subradius)
        self.canvas.fill()

        self.canvas.fill_style('rgba(0, 1, 0, ' + str(alpha) + ')')
        self.canvas.ellipse(self.canvas,
                             xc + radius / 3. * math.cos(math.pi * (0.5 + 2 / .3)),
                             yc - radius / 3. * math.sin(math.pi * (0.5 + 2 / .3)),
                             subradius, subradius)
        self.canvas.fill()

        self.canvas.fill_style('rgba(0, 0, 1, ' + str(alpha) + ')')
        self.canvas.ellipse(self.canvas,
                             xc + radius / 3. * math.cos(math.pi * (0.5 + 4 / .3)),
                             yc - radius / 3. * math.sin(math.pi * (0.5 + 4 / .3)),
                             subradius, subradius)
        self.canvas.fill()

    def test_draw_triangle(self):
        with self.canvas.begin_close_path(32, 0):
            self.canvas.line_to(32, 64)
            self.canvas.line_to(-64, 0)

    def test_move_to(self):
        self.canvas.move_to(5, 7)

    def test_line_to(self):
        self.canvas.line_to(2, 3)

    def test_bezier_curve_to(self):
        self.canvas.bezier_curve_to(1, 1, 2, 2, 5, 5)

    def test_quadratic_curve_to(self):
        self.canvas.quadratic_curve_to(1, 1, 5, 5)

    def test_arc(self):
        self.canvas.arc(-10, -10, 10, math.pi/2, 0, True)

    def test_ellipse(self):
        self.canvas.ellipse(1, 1, 50, 20, 0, math.pi, 2*math.pi, False)

    def test_rotate(self):
        self.canvas.rotate(math.pi)

    def test_scale(self):
        self.canvas.scale(2, 1.5)

    def test_translate(self):
        self.canvas.translate(5, 3.5)

    def test_reset_transform(self):
        self.canvas.reset_transform()
